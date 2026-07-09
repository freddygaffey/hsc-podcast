#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Persist ONE paper's verified segmentation to split.json — called incrementally by the
segmentation workflow's persist stage, so progress is durable per-paper (a stopped run loses
nothing; a re-run skips papers whose split.json already has source:"agent").

Reads papers/_work/<paperId>/_verified.json (the workflow's validated result for this paper:
{paperId, units:[...], sectionIIStartPage, solutionsStartPage, mcExpected}) and writes
papers/_work/<paperId>/split.json in the merged, canonical shape (same as persist_agent_splits).

    python3 tools/persist_one.py "<paperId>"
"""
import json
import sys
from pathlib import Path

ROOT = Path("/Users/fred/hsc-podcast")
WORK = ROOT / "papers" / "_work"


def _is_ii(section):
    return "II" in str(section or "").replace(" ", "").upper()


def main():
    pid = sys.argv[1]
    wd = WORK / pid
    data = json.loads((wd / "_verified.json").read_text())
    subject = None
    if (wd / "info.json").exists():
        try:
            subject = json.loads((wd / "info.json").read_text()).get("subject")
        except Exception:
            pass

    groups = {}
    for u in data.get("units", []):
        key = (u.get("section"), str(u.get("number")), u.get("part"))
        region = {"page": u["page"], "bbox": [round(v, 4) for v in u["bbox"]]}
        g = groups.get(key)
        if not g:
            groups[key] = {
                "id": "q" + str(u.get("number")) + (u.get("part") or ""),
                "number": str(u.get("number")), "part": u.get("part"),
                "marks": u.get("marks"), "marksPrinted": u.get("marks") is not None,
                "type": "mc" if u.get("section") == "I" else None,
                "section": u.get("section"), "ruleId": "agent-verify",
                "confidence": u.get("confidence"), "optionsComplete": u.get("optionsComplete"),
                "note": u.get("note", ""), "writingSpace": list(u.get("writingSpace") or []),
                "ruleException": u.get("ruleException"), "regions": [region],
            }
        else:
            g["regions"].append(region)
            g["writingSpace"].extend(u.get("writingSpace") or [])
            g["confidence"] = min(g["confidence"] or 1, u.get("confidence") or 1)
            if g["marks"] is None and u.get("marks") is not None:
                g["marks"] = u["marks"]
                g["marksPrinted"] = True

    def sortkey(x):
        try:
            return (0 if x["section"] == "I" else 1, int(x["number"]))
        except (TypeError, ValueError):
            return (2, 0)

    units = sorted(groups.values(), key=sortkey)
    out = {"paperId": pid, "subject": subject, "source": "agent",
           "sectionIIStartPage": data.get("sectionIIStartPage"),
           "solutionsStartPage": data.get("solutionsStartPage"), "units": units}
    (wd / "split.json").write_text(json.dumps(out, indent=2))
    print(f"persisted {pid}: {len(units)} units")


if __name__ == "__main__":
    main()
