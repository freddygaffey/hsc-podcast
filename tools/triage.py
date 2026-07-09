#!/usr/bin/env python3
"""Auto-triage every segmented paper into PASS / FAIL at the PAGE level, so manual review can
sort clean pages from ones that need attention. Runs the geometric invariants per paper and maps
each reported error back to its page. Writes papers/_work/_triage.json:

  { "<paperId>": {
      "mc": 10, "s2": 15, "solStart": 14,
      "paperIssues": ["count-min: section I: 0 questions ..."],   # not tied to one page
      "pages": { "2": {"units": ["q1","q2"], "issues": [], "status": "pass"},
                 "6": {"units": ["q6"], "issues": ["line-cross: q6 crosses text"], "status": "fail"} } } }

    python3 tools/triage.py            # all segmented papers
    python3 tools/triage.py <paperId>  # one
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = ROOT / "papers" / "_work"
sys.path.insert(0, str(HERE))
import vision_seg as vs  # noqa: E402

ERR_PAGE = re.compile(r"\[ERROR\]\s*([\w-]+):\s*(.*?)\s+on\s+p(\d+)", re.I)
ERR_ANY = re.compile(r"\[ERROR\]\s*([\w-]+):\s*(.+)")


def triage_paper(pid):
    wd = WORK / pid
    split = json.loads((wd / "split.json").read_text())
    units = split.get("units", [])
    page_units = {}
    for u in units:
        for r in u.get("regions", []):
            page_units.setdefault(r["page"], []).append(u["id"])

    out = subprocess.run(["python3", str(HERE / "invariants.py"), pid],
                         capture_output=True, text=True).stdout
    page_issues, paper_issues = {}, []
    for line in out.splitlines():
        m = ERR_PAGE.search(line)
        if m:
            page_issues.setdefault(int(m.group(3)), []).append(f"{m.group(1)}: {m.group(2)}")
        elif "[ERROR]" in line:
            m2 = ERR_ANY.search(line)
            if m2:
                paper_issues.append(f"{m2.group(1)}: {m2.group(2).strip()}")

    pages = {}
    for p in sorted(page_units):
        iss = page_issues.get(p, [])
        pages[str(p)] = {"units": page_units[p], "issues": iss,
                         "status": "fail" if iss else "pass"}
    return {"mc": sum(1 for u in units if not vs._is_ii(u.get("section"))),
            "s2": sum(1 for u in units if vs._is_ii(u.get("section"))),
            "solStart": split.get("solutionsStartPage"),
            "paperIssues": paper_issues, "pages": pages}


def main():
    if len(sys.argv) > 1:
        papers = [sys.argv[1]]
        tri = json.loads((WORK / "_triage.json").read_text()) if (WORK / "_triage.json").exists() else {}
    else:
        papers = sorted(x.name for x in WORK.iterdir()
                        if (x / "split.json").exists() and any(x.glob("p*.png")))
        tri = {}
    for pid in papers:
        try:
            tri[pid] = triage_paper(pid)
            t = tri[pid]
            nfail = sum(1 for p in t["pages"].values() if p["status"] == "fail") + len(t["paperIssues"])
            print(f"  {'FAIL' if nfail else 'pass'}  {pid[18:]:52.52}  mc={t['mc']} s2={t['s2']} issues={nfail}")
        except Exception as e:
            tri[pid] = {"error": str(e)}
            print(f"  ERR   {pid[18:]:52.52}  {e}")
    (WORK / "_triage.json").write_text(json.dumps(tri, indent=2))
    print(f"-> {WORK / '_triage.json'}  ({len(papers)} paper(s))")


if __name__ == "__main__":
    main()
