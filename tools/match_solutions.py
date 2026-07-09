#!/usr/bin/env python3
"""Match located solutions to questions and record coverage — deterministic, ZERO tokens.

Input: the locate-solutions workflow output (JSON list of
  {paperId, solutionsStartPage, solutionUnits:[{section,number,page,bbox,mcAnswer,hasWorking}]}).
For each paper it:
  - attaches a crop-as-is `answer` to every matched question unit in split.json
    ({regions:[{page,bbox}], mcAnswer, hasWorking, source:"crop"});
  - classifies the paper's solution coverage and writes split["solutions"]:
      complete  — every question matched to a real solution
      gaps      — the paper HAS solutions but some questions are unmatched → HUMAN REVIEW
                  (Fred's rule: do NOT auto-fill; a gap usually means a matching bug)
      none      — no solutions located and none expected → whole paper queued for AI-fill
      missing   — solutions were expected (w-sol / solutionsStartPage set) but none located → REVIEW
    plus mcLetterOnly: MC questions whose solution shows only the letter (no working) →
    these need AI-generated working (answer stays authoritative from the marking guide).

    python3 tools/match_solutions.py <locate-output.json>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/fred/hsc-podcast")
WORK = ROOT / "papers" / "_work"


def _is_ii(section):
    return "II" in str(section or "").replace(" ", "").upper()


def key(section, number):
    return ("II" if _is_ii(section) else "I", str(number))


def match_paper(paper):
    pid = paper["paperId"]
    sp = WORK / pid / "split.json"
    if not sp.exists():
        print(f"  SKIP {pid[-40:]}: no split.json")
        return
    split = json.loads(sp.read_text())
    # index located solutions by (section, number) -> regions + mc info
    sols = {}
    for u in paper.get("solutionUnits", []):
        k = key(u.get("section"), u.get("number"))
        s = sols.setdefault(k, {"regions": [], "mcAnswer": None, "hasWorking": False})
        s["regions"].append({"page": u["page"], "bbox": [round(v, 4) for v in u["bbox"]]})
        if u.get("mcAnswer"):
            s["mcAnswer"] = u["mcAnswer"]
        s["hasWorking"] = s["hasWorking"] or bool(u.get("hasWorking"))

    total = matched = 0
    gaps, mc_letter_only = [], []
    for q in split.get("units", []):
        total += 1
        k = key(q.get("section"), q.get("number"))
        s = sols.get(k)
        if not s:
            gaps.append(q.get("number"))
            continue
        matched += 1
        q["answer"] = {"regions": s["regions"], "mcAnswer": s["mcAnswer"],
                       "hasWorking": s["hasWorking"], "source": "crop"}
        if not _is_ii(q.get("section")) and not s["hasWorking"]:
            mc_letter_only.append(q.get("number"))

    # classify the paper
    wsol = bool(re.search(r"\bw[-_ ]?sol|with[-_ ]?solutions?\b", pid, re.I))
    expects = wsol or split.get("solutionsStartPage") or paper.get("solutionsStartPage")
    located = bool(paper.get("solutionUnits"))
    if not located:
        status = "missing" if expects else "none"      # expected→review ; not expected→AI-fill
    elif gaps:
        status = "gaps"                                  # has solutions but unmatched → review
    else:
        status = "complete"

    split["solutions"] = {"status": status, "matched": matched, "total": total,
                          "gaps": [g for g in gaps if g is not None],
                          "mcLetterOnly": [m for m in mc_letter_only if m is not None]}
    sp.write_text(json.dumps(split, indent=2))
    tag = {"complete": "✓", "gaps": "⚑ REVIEW", "none": "→ AI-fill", "missing": "⚑ REVIEW"}[status]
    extra = (f" · MC-need-working: {mc_letter_only}" if mc_letter_only else "")
    print(f"  {pid[-40:]}: {status} {tag}  {matched}/{total} matched"
          + (f" · gaps {gaps}" if gaps else "") + extra)


def main():
    data = json.loads(Path(sys.argv[1]).read_text())
    for paper in data:
        match_paper(paper)


if __name__ == "__main__":
    main()
