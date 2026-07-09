#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""ONE command → the whole Maths Extension-1 pipeline, for the new syllabus (2020+).

Per paper, in order:
  1. render_paper.py   pages -> papers/_work/<pid>/pNN.png          (local, free)
  2. locate_ocr.py     -> ocr.json                                   (local, free)
  3. ext1_split.py     deterministic Section II ranges + marks       (local, free)
  4. vision_seg.py     Qwen3-VL: MC boxes + Section II PART boxes     (~$0.004/paper)
  5. gen_solutions.py  Qwen3-VL read + DeepSeek solve -> KaTeX PNGs   (~$0.02/paper)

Papers run CONCURRENTLY (a thread pool) — running more at once costs the SAME dollars, it's
just faster. A global --budget hard-stops before overspending; already-finished papers are
skipped so it's resumable. Key: ~/.config/hsc/openrouter.key.

    python3 tools/run_ext1.py --all                 # every 2020+ Ext-1 question paper
    python3 tools/run_ext1.py --all --limit 5       # first 5 (good for a trial)
    python3 tools/run_ext1.py --papers <pid> <pid>  # specific papers
    python3 tools/run_ext1.py --all --budget 6 --workers 10
"""
import argparse
import json
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
TOOLS = ROOT / "tools"
PY = sys.executable

_lock = threading.Lock()
_spent = [0.0]
_stop = threading.Event()


def discover():
    """New-syllabus (2020+) Ext-1 papers with the Year-12 Q11-14 structure — i.e. Trial and
    HSC papers. Excludes Year-11 / yearly / preliminary / assessment-task fragments and
    marking guides, which don't have the Section II structure."""
    idx = json.loads((ROOT / "papers" / "_index.json").read_text())
    items = idx if isinstance(idx, list) else idx.get("papers", list(idx.values()))
    GOOD = ("y12", "trial", "hsc", "nesa")            # Year-12 exam-structure signal
    BAD = ("year-11", "year 11", "yearly", "y11", "task", "part-a", "part-b",
           "prelim", "preliminary", "half-yearly", "half yearly", "-mg", "marking",
           "-notes", "guide")
    out = []
    for p in items:
        pid = (p.get("paperId") or p.get("id") or "") if isinstance(p, dict) else str(p)
        if not pid.startswith("maths-extension-1"):
            continue
        m = re.search(r"(20\d\d)", pid)
        if not (m and int(m.group(1)) >= 2020):
            continue
        low = pid.lower()
        if any(b in low for b in BAD):
            continue
        if not any(g in low for g in GOOD):
            continue
        out.append(pid)
    return sorted(set(out))


def is_done(pid):
    """A paper is done when every unit in its split.json has a rendered solution PNG."""
    sp = WORK / pid / "split.json"
    sd = WORK / pid / "solutions"
    if not sp.exists() or not sd.is_dir():
        return False
    try:
        units = json.loads(sp.read_text()).get("units", [])
    except Exception:
        return False
    return bool(units) and all((sd / f'{u["id"]}.png').exists() for u in units)


def _run(cmd, timeout):
    r = subprocess.run([PY, *cmd], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def _cost_from(stdout):
    costs = re.findall(r"\$([0-9]+\.[0-9]+)", stdout)
    return float(costs[-1]) if costs else 0.0


def process(pid, per_paper_budget):
    if _stop.is_set():
        return pid, "skipped (budget)", 0.0
    if is_done(pid):
        return pid, "already done", 0.0
    paper_cost = 0.0
    try:
        # 1-3: local, free (skip if already rendered/split)
        if not (WORK / pid / "info.json").exists():
            _run(["tools/render_paper.py", pid], 300)
        if not (WORK / pid / "ocr.json").exists():
            _run(["tools/locate_ocr.py", pid], 600)
        rc, out, err = _run(["tools/ext1_split.py", pid], 120)
        if rc != 0:
            return pid, f"split failed: {err.strip()[:120]}", 0.0
        # 4: vision boxes
        rc, out, err = _run(["tools/vision_seg.py", pid], 600)
        paper_cost += _cost_from(out)
        # 4b: geometric invariants (rules gate — logged; failures flagged in run output)
        rc_inv, out_inv, _ = _run(["tools/invariants.py", pid], 120)
        # 4c: whole-paper semantic check (DeepSeek, flag-first)
        rc_sem, out_sem, _ = _run(["tools/semantic_check.py", pid, "--write"], 180)
        paper_cost += _cost_from(out_sem)
        rules_ok = rc_inv == 0 and rc_sem == 0
        # 5: solutions (per-paper spend cap as a backstop)
        rc, out, err = _run(["tools/gen_solutions.py", pid, "--budget", str(per_paper_budget)], 3600)
        paper_cost += _cost_from(out)
        with _lock:
            _spent[0] += paper_cost
        status = ("ok" if is_done(pid) else "partial") + ("" if rules_ok else " ⚠rules")
        return pid, status, paper_cost
    except subprocess.TimeoutExpired:
        return pid, "timeout", paper_cost
    except Exception as e:
        return pid, f"error: {e}", paper_cost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="all 2020+ Ext-1 question papers")
    ap.add_argument("--papers", nargs="+", help="explicit paperIds")
    ap.add_argument("--limit", type=int, help="cap number of papers (trial)")
    ap.add_argument("--workers", type=int, default=8, help="papers processed concurrently")
    ap.add_argument("--budget", type=float, default=12.0, help="GLOBAL hard spend cap (USD)")
    ap.add_argument("--per-paper-budget", type=float, default=0.10)
    a = ap.parse_args()

    papers = a.papers or (discover() if a.all else [])
    if not papers:
        sys.exit("nothing to do — pass --all or --papers")
    if a.limit:
        papers = papers[:a.limit]
    todo = [p for p in papers if not is_done(p)]
    print(f"{len(papers)} papers ({len(papers) - len(todo)} already done) · "
          f"{len(todo)} to run · {a.workers} workers · budget ${a.budget:.2f}")

    done = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(process, p, a.per_paper_budget): p for p in todo}
        for f in as_completed(futs):
            pid, status, cost = f.result()
            done += 1
            print(f"[{done}/{len(todo)}] {pid[24:]:<46} {status:<14} "
                  f"+${cost:.4f}  total ${_spent[0]:.3f}")
            if _spent[0] >= a.budget and not _stop.is_set():
                _stop.set()
                print(f"⛔ global budget ${a.budget:.2f} reached — no new papers will start")
    print(f"\nDONE. spent ${_spent[0]:.3f} across {done} papers.")


if __name__ == "__main__":
    main()
