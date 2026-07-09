#!/usr/bin/env python3
"""Generate worked solutions for a paper via OpenRouter, cheaply:

  1. VISION  (Qwen3-VL) reads each question's crop(s) -> clean LaTeX text incl. any
     diagram description + the printed per-part marks.
  2. REASONING (DeepSeek V4) solves from that text -> structured solution JSON in the
     render_solution.py schema (matplotlib-mathtext-safe LaTeX).
  3. render_solution.py renders each -> papers/_work/<pid>/solutions/<uid>.png, which the
     eval UI auto-discovers. Watermarked AI-GENERATED (DeepSeek generated it).

    python3 tools/gen_solutions.py <paperId> [--only q11] [--section II]

Costs ~$0.002-0.004/question (printed at the end). Key: ~/.config/hsc/openrouter.key.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import or_client as orc  # noqa: E402
import render_solution_html as render_html  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

TRANSCRIBE_PROMPT = (
    "Transcribe this HSC Mathematics Extension 1 exam question EXACTLY. Use LaTeX for all "
    "math (inline $...$). Preserve every part label (a),(b),(c) and sub-part (i),(ii),(iii). "
    "For each part, note the marks printed in the right margin as '[N marks]'. If a diagram, "
    "graph or number-plane is present, write [DIAGRAM: <concise description of exactly what is "
    "shown — axes, curves, key points, labels>] so it can be solved without the image. "
    "Output ONLY the transcription, no commentary.")

SOLVE_SYSTEM = (
    "You are an expert HSC Mathematics Extension 1 marker writing the official worked "
    "solution. Solve correctly and show the working a marker expects. Output STRICT JSON only "
    "(no markdown fence), matching this schema exactly:\n"
    '{"number":"11","section":"II","aiGenerated":true,'
    '"parts":[{"label":"(a)","marks":2,"steps":["$...$","$...$"],"answer":"$...$",'
    '"graph":{"title":"$...$","xlabel":"$x$","ylabel":"$y$","curves":[{"x":[..],"y":[..]}],'
    '"points":[{"x":1,"y":1,"label":"$(1,1)$"}]}}]}\n'
    "RULES:\n"
    "- One JSON object, parts in order, labels matching the question exactly.\n"
    "- Every step and answer is a single inline $...$ math line — ALWAYS wrap math in $...$.\n"
    "- Use normal LaTeX (rendered by KaTeX): \\frac, \\dfrac, \\sqrt, \\begin{pmatrix}...\\end{pmatrix} "
    "for vectors/matrices, \\overrightarrow, \\vec, \\hat, \\binom, \\int, \\sum, ^ and _, greek, "
    "\\times \\cdot \\approx \\Rightarrow \\leq \\geq. Do NOT use \\hfill or alignment environments.\n"
    "- Keep each step to ONE short line — a single equation or a brief phrase (aim < 55 "
    "characters). Break long working across multiple steps; do NOT write full sentences.\n"
    "- 'marks' per part = ONLY the total marks printed for that part in the question (or null "
    "if none shown). Do NOT indicate which step earns which mark and do NOT add any "
    "mark-allocation / mark-drop notes — you do not have the official marking guide, so never "
    "invent where marks are awarded. 'answer' = the final boxed result.\n"
    "- Include 'graph' ONLY when the answer requires a sketch AND you can give real numeric "
    "data points; otherwise omit it. Keep working concise but complete.")


def _crop_regions(pid, regions):
    """Save each region of a unit as a PNG; return the list of file paths."""
    wd = WORK / pid
    paths = []
    for i, r in enumerate(regions):
        pg = r["page"]
        img = Image.open(wd / f"p{pg:02d}.png")
        W, H = img.size
        x0, y0, x1, y1 = r["bbox"]
        crop = img.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
        p = wd / "solutions" / f"_src_{r.get('page')}_{i}.png"
        p.parent.mkdir(exist_ok=True)
        crop.save(p)
        paths.append(str(p))
    return paths


def transcribe(pid, regions):
    """Read the given crop region(s) with Qwen3-VL -> clean LaTeX question text."""
    imgs = _crop_regions(pid, regions)
    content = [{"type": "text", "text": TRANSCRIBE_PROMPT}]
    for p in imgs:
        content.append({"type": "image_url", "image_url": {"url": orc._data_uri(p)}})
    txt, u = orc.chat(orc.VISION_MODEL, [{"role": "user", "content": content}], max_tokens=1800)
    for p in imgs:
        Path(p).unlink(missing_ok=True)
    return txt, u.get("cost", 0)


def _solve(prompt, number, section):
    for attempt in range(2):
        txt, u = orc.chat(orc.REASON_MODEL,
                          [{"role": "system", "content": SOLVE_SYSTEM},
                           {"role": "user", "content": prompt}], max_tokens=5000,
                          reasoning={"max_tokens": 1500},
                          response_format={"type": "json_object"})
        raw = (txt or "").strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1].lstrip("json").strip() if "```" in raw[3:] else raw.strip("`")
        try:
            obj = json.loads(raw)
            obj["number"] = str(number)
            obj["section"] = section
            obj["aiGenerated"] = True
            obj.setdefault("answerNote", "AI-generated worked solution (DeepSeek V4) — verify")
            return obj, u.get("cost", 0)
        except json.JSONDecodeError:
            if attempt:
                return {"_error": "invalid JSON", "_raw": raw[:400]}, u.get("cost", 0)
    return {"_error": "no solution"}, 0


def solve_mc(qtext, number, marks):
    return _solve(f"Multiple-choice Question {number}:\n\n{qtext}\n\n"
                  "Give the worked solution and the correct option as the JSON object "
                  "(one part, its 'answer' the correct letter).", number, "I")


def solve_part(context, number, label, marks):
    """Solve ONE lettered part, given the whole question for 'hence'-linkage context."""
    return _solve(
        f"Here is the FULL Question {number} (all parts, for context):\n\n{context}\n\n"
        f"Write the worked solution for PART ({label}) ONLY"
        + (f" [{marks} marks]" if marks else "") +
        ". Output the JSON object with a SINGLE part in 'parts' whose label is "
        f'"({label})". Use earlier parts\' results if this part says "hence".', number, "II")


def render(pid, uid, sol):
    wd = WORK / pid / "solutions"
    (wd / f"{uid}.json").write_text(json.dumps(sol, indent=2))
    render_html.render_png(sol, str(wd / f"{uid}.png"))     # KaTeX + headless Chrome


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId")
    ap.add_argument("--only", help="single unit id, e.g. q11")
    ap.add_argument("--section", help="only this section (I/II)")
    ap.add_argument("--budget", type=float, default=1.00,
                    help="hard spend cap in USD — abort before exceeding it (safety)")
    a = ap.parse_args()
    split = json.loads((WORK / a.paperId / "split.json").read_text())
    (WORK / a.paperId / "solutions").mkdir(exist_ok=True)
    units = split["units"]

    def is_ii(u):
        return "II" in str(u.get("section", "")).replace(" ", "").upper()

    # transcribe each Section II question's parts ONCE (shared context for all its parts);
    # charge that transcription cost only the first time the question is seen.
    qcache = {}
    spent = [0.0]

    def qcontext(number):
        if number not in qcache:
            regs = [r for u in units if is_ii(u) and u["number"] == number for r in u["regions"]]
            txt, c = transcribe(a.paperId, regs) if regs else ("", 0)
            qcache[number] = txt
            spent[0] += c
        return qcache[number]

    for u in units:
        uid = u.get("id") or ("q" + str(u["number"]) + (u.get("part") or ""))
        if a.only and uid != a.only:
            continue
        if a.section and str(u.get("section")) != a.section:
            continue
        if spent[0] >= a.budget:
            print(f"  ⛔ budget ${a.budget:.2f} reached (spent ${spent[0]:.4f}) — stopping")
            break
        if is_ii(u):
            ctx = qcontext(u["number"])
            sol, c2 = solve_part(ctx, u["number"], u.get("part") or "", u.get("marks"))
        else:
            qtext, c1 = transcribe(a.paperId, u["regions"])
            spent[0] += c1
            sol, c2 = solve_mc(qtext, u["number"], u.get("marks"))
        spent[0] += c2
        if sol.get("_error"):
            print(f"  {uid}: ⚠ {sol['_error']}")
            continue
        # carry the part's printed marks + label through to the render
        for pt in sol.get("parts", []):
            if u.get("part") and not pt.get("label"):
                pt["label"] = f"({u['part']})"
            if u.get("marks") is not None:
                pt.setdefault("marks", u["marks"])
        render(a.paperId, uid, sol)
        print(f"  {uid}: ok  (running ${spent[0]:.4f})")
    print(f"total: ${spent[0]:.4f}")


if __name__ == "__main__":
    main()
