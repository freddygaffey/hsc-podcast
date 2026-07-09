#!/usr/bin/env python3
"""Render a structured solution -> a single A4 PDF page in the house style.

The unified-solution path (see docs/solution-style-guide.md + memory solution-coverage):
an AI-generated solution is rendered to PDF page(s), APPENDED to the paper's PDF
(tools/append_solutions.py), and then the ordinary solution-crop pipeline treats it like
any real solution. Real solutions are cropped as-is and never come through here.

Math is set with matplotlib's mathtext (a LaTeX subset — the generator is constrained to
it); graphs are drawn by matplotlib from an explicit DATA spec (never generated code).
AI solutions carry a diagonal "AI-GENERATED SOLUTION" watermark; MC whose answer is real
but working is synthesised carry the "answer from marking guide" note.

Structured solution JSON:
{
  "number":"11", "section":"II",
  "aiGenerated": true,
  "answerNote": "answer from marking guide · working AI-generated",   # optional
  "parts": [
    { "label":"(a)",                      # or null
      "steps": ["$2x+3=7$", "$x=2$"],     # each a mathtext line
      "answer": "$x=2$",                   # boxed; optional
      "graph": {                           # optional, drawn from data
        "title":"$y=x^2$", "xlabel":"$x$", "ylabel":"$y$",
        "curves":[{"x":[...],"y":[...]}],
        "points":[{"x":1,"y":1,"label":"$(1,1)$"}],
        "hlines":[{"y":3,"label":"$y=3$"}]
      }
    }
  ]
}

    python3 tools/render_solution.py <solution.json> -o out.pdf
"""
import argparse
import json
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

PAPER = "#ffffff"
INK = "#1c1e24"
ACC = "#3b4cc0"
MUT = "#5b6472"
AI = "#b45309"
plt.rcParams.update({"mathtext.fontset": "stix", "font.family": "STIXGeneral",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.22, "font.size": 11,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK})

# A solution is rendered as a TIGHT, content-sized crop (variable height, fixed column
# width) — NOT a fixed page — so the existing compact-flow export engine packs several per
# printed page, exactly like question crops. Heights below are in inches.
COL_W = 6.6                # column width
MARGIN = 0.3               # top/bottom margin
H_HEAD = 0.34              # header block
H_NOTE = 0.22              # optional answer note
H_LABEL = 0.30             # part label
H_STEP = 0.32              # one working line
H_ANSWER = 0.46            # boxed answer
H_GRAPH = 2.3              # graph
GAP = 0.14                 # gap after a part


_PLAIN = False


def _plainify(s):
    """Last-resort: turn LaTeX into readable literal text (never crashes) while KEEPING
    the meaning — fractions keep their slash, roots their √, vectors their letters."""
    if not s:
        return s
    s = s.replace("$", "")
    for _ in range(3):                                   # resolve simple nesting in a few passes
        s = re.sub(r"\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", s)
        s = re.sub(r"\\sqrt\s*\{([^{}]*)\}", r"√(\1)", s)
        s = re.sub(r"\\overrightarrow\s*\{([^{}]*)\}", r"\1", s)
        s = re.sub(r"\\(?:vec|hat|bar|underline|mathbf|mathrm|text)\s*\{([^{}]*)\}", r"\1", s)
    for a, b in [(r"\times", "×"), (r"\cdot", "·"), (r"\pi", "π"), (r"\theta", "θ"),
                 (r"\alpha", "α"), (r"\beta", "β"), (r"\geq", "≥"), (r"\leq", "≤"),
                 (r"\approx", "≈"), (r"\Rightarrow", "⇒"), (r"\rightarrow", "→"),
                 (r"\infty", "∞"), (r"\circ", "°"), (r"\degree", "°"), (r"\pm", "±"),
                 (r"\int", "∫"), (r"\sqrt", "√"), (r"\ne", "≠"), (r"\in", "∈")]:
        s = s.replace(a, b)
    s = re.sub(r"\\begin\{[a-z]*matrix\}|\\end\{[a-z]*matrix\}", " ", s)
    s = s.replace("\\\\", "  ").replace("&", " ")
    s = re.sub(r"\\[a-zA-Z]+", " ", s)                   # any remaining commands
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()


def _mt(s):
    """Coerce common LLM-LaTeX into matplotlib's mathtext subset so a stray \\text or
    \\boxed doesn't blow up the whole render. In _PLAIN fallback mode, strip math entirely."""
    if _PLAIN:
        return _plainify(s)
    if not s:
        return s
    s = re.sub(r"\\(?:text|operatorname)\s*\{", r"\\mathrm{", s)
    s = re.sub(r"\\boxed\s*\{([^{}]*)\}", r"\1", s)
    s = s.replace(r"\left", "").replace(r"\right", "")
    s = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", "", s)
    return s


def _wrap(s, budget=60):
    """Break a step into lines that fit the column, keeping each $...$ span atomic so a
    formula is never split. `budget` ~ visible chars per line at COL_W."""
    toks = re.findall(r"\$[^$]*\$|\S+", s or "")
    lines, cur, ln = [], [], 0
    for t in toks:
        w = len(re.sub(r"[\\${}^_]", "", t)) + 1
        if ln + w > budget and cur:
            lines.append(" ".join(cur))
            cur, ln = [], 0
        cur.append(t)
        ln += w
    if cur:
        lines.append(" ".join(cur))
    return lines or [s or ""]


def _content_height(sol):
    h = MARGIN * 2 + H_HEAD + (H_NOTE if sol.get("answerNote") else 0)
    for p in sol.get("parts", []):
        if p.get("label"):
            h += H_LABEL
        for s in p.get("steps", []):
            h += H_STEP * len(_wrap(s))
        if p.get("graph"):
            h += H_GRAPH + 0.1
        if p.get("answer"):
            h += H_ANSWER
        h += GAP
    return max(h, 1.2)


def _graph(fig, spec, y_top_frac, h_frac):
    ax = fig.add_axes([0.05, y_top_frac - h_frac, 0.86, h_frac])
    ax.set_facecolor(PAPER)
    for c in spec.get("curves", []):
        ax.plot(c["x"], c["y"], color=ACC, lw=2)
    for h in spec.get("hlines", []):
        ax.axhline(h["y"], ls="--", color="#9aa1ad", lw=1)
        if h.get("label"):
            ax.text(0.99, h["y"], h["label"], transform=ax.get_yaxis_transform(),
                    ha="right", va="bottom", color=MUT, fontsize=8)
    for p in spec.get("points", []):
        ax.plot(p["x"], p["y"], "o", color=ACC, ms=5)
        if p.get("label"):
            ax.annotate(p["label"], (p["x"], p["y"]), textcoords="offset points",
                        xytext=(6, 4), color=INK, fontsize=9)
    if spec.get("xlabel"):
        ax.set_xlabel(_mt(spec["xlabel"]))
    if spec.get("ylabel"):
        ax.set_ylabel(_mt(spec["ylabel"]))
    if spec.get("title"):
        ax.set_title(_mt(spec["title"]), fontsize=11, color=INK)


def render(sol, out_pdf):
    """Crash-proof: try the mathtext render; if a bad LaTeX string throws at savefig,
    retry once in plain-text mode so one bad formula never kills a paper's run."""
    global _PLAIN
    try:
        _PLAIN = False
        _render_once(sol, out_pdf)
    except Exception:
        plt.close("all")
        _PLAIN = True
        try:
            _render_once(sol, out_pdf)
        finally:
            _PLAIN = False


def _render_once(sol, out_pdf):
    H = _content_height(sol)
    fig = plt.figure(figsize=(COL_W, H), facecolor=PAPER)
    LEFT = 0.055

    def fy(inch_from_top):            # inches-from-top -> figure fraction
        return 1 - inch_from_top / H

    cur = MARGIN
    num, sec = sol.get("number", "?"), sol.get("section", "")
    fig.text(LEFT, fy(cur), f"Question {num}", fontsize=14, fontweight="bold",
             color=INK, va="top")
    fig.text(0.985, fy(cur), "Multiple choice" if sec == "I" else "Worked solution",
             fontsize=9.5, color=MUT, ha="right", va="top")
    cur += H_HEAD
    if sol.get("answerNote"):
        fig.text(LEFT, fy(cur), sol["answerNote"], fontsize=9.5, color=AI,
                 style="italic", va="top")
        cur += H_NOTE

    for part in sol.get("parts", []):
        if part.get("label"):
            fig.text(LEFT, fy(cur), part["label"], fontsize=12, fontweight="bold",
                     color=INK, va="top")
            if part.get("marks") is not None:      # printed per-part total (factual, not a guess)
                mk = part["marks"]
                fig.text(0.985, fy(cur), f"{mk} mark" + ("" if mk == 1 else "s"),
                         fontsize=10, color=MUT, ha="right", va="top")
            cur += H_LABEL
        for step in part.get("steps", []):
            for line in _wrap(step):
                fig.text(LEFT + 0.02, fy(cur), _mt(line), fontsize=12, color=INK, va="top")
                cur += H_STEP
        if part.get("graph"):
            _graph(fig, part["graph"], fy(cur), H_GRAPH / H)
            cur += H_GRAPH + 0.1
        if part.get("answer"):
            fig.text(LEFT + 0.02, fy(cur), _mt(part["answer"]), fontsize=13, color=ACC,
                     va="top", bbox=dict(boxstyle="round,pad=0.4", facecolor="#eef0fb",
                                         edgecolor=ACC, lw=1.3))
            cur += H_ANSWER
        cur += GAP

    if sol.get("aiGenerated"):
        fig.text(0.5, 0.5, "AI-GENERATED SOLUTION", fontsize=min(30, H * 5.0),
                 color=AI, alpha=0.11, rotation=18, ha="center", va="center",
                 fontweight="bold")

    fig.savefig(out_pdf, format="pdf", facecolor=PAPER)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("solution")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    render(json.loads(open(a.solution).read()), a.out)
    print(f"rendered -> {a.out}")


if __name__ == "__main__":
    main()
