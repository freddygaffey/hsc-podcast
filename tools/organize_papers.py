#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Generate an organized, distributable view of the raw papers/ tree.

The raw `papers/` tree (written by the scrapers + the server sync) is the SOURCE
OF TRUTH and is never reorganized. This script DERIVES `papers_organized/` from
it and is safe to re-run any time — new papers that land in `papers/` are picked
up on the next run.

Per-subject layout produced:

    papers_organized/<Subject>/
        Papers/
            HSC/            official HSC finals (NESA + THSC + ACE) + marking guides
            Trial/          Year 12 trial papers (+ solutions)
            Yearly-Y11/     Year 11 yearly / prelim papers
        Other/              half-yearlies, assessments, HSC-question sets, misc
        Resources/          notes, essays, case studies, quizzes, videos, syllabus
        Archive-pre-<cutoff>/
            HSC/ Trial/ Yearly-Y11/     old-syllabus exam papers (year < cutoff)

Cutoffs (first HSC-exam year of the current syllabus) come from
`tools/syllabus_cutoffs.json`. Subjects with no cutoff entry are all-current.

By default files are real COPIES (independent, portable — pushes cleanly to object
storage like R2 with no link semantics). Use --hardlink for a fast, zero-extra-disk
LOCAL view (same filesystem only; NOT for uploading).

    python3 tools/organize_papers.py                 # all subjects, real copies
    python3 tools/organize_papers.py Physics          # one subject (sample)
    python3 tools/organize_papers.py --hardlink       # fast local view (no upload)
"""
import os, re, sys, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW  = ROOT / "papers"
OUT  = ROOT / "papers_organized"
CUTOFFS = {k: v for k, v in json.load(open(ROOT / "tools" / "syllabus_cutoffs.json")).items()
           if not k.startswith("_")}

YEAR_RE = re.compile(r"(19[6-9]\d|20[0-4]\d)")

# raw category dir -> Papers sub-bucket (HSC / Trial / Yearly-Y11)
PAPER_CATS = {
    "Y12-HSC": "HSC", "HSC-NESA": "HSC", "ACE-HSC": "HSC",
    "Y12-Trial": "Trial", "Y12-Trial-P1": "Trial",
    "Y12-Trial-P2-Adv": "Trial", "Y12-Trial-P2-Std": "Trial", "ACE-Trial": "Trial",
    "Y11-Yearly": "Yearly-Y11",
}
RESOURCE_CATS = {"ACE-Notes", "ACE-Essay", "ACE-CaseStudy", "ACE-Quiz",
                 "ACE-Video", "ACE-Syllabus"}
# any other category (ACE-Assessment/HalfYearly/HSC-Questions/Yearly/Misc/Other, root, unknown) -> Other


def classify(category):
    """Return (bucket, sub) where sub is the Papers/Archive sub-bucket or None."""
    if category in PAPER_CATS:
        return "Papers", PAPER_CATS[category]
    if category in RESOURCE_CATS:
        return "Resources", None
    return "Other", None


def link(src: Path, dst: Path, do_copy: bool):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    if do_copy:
        shutil.copy2(src, dst)
    else:
        os.link(src, dst)


def organize(subjects, do_copy):
    stats = {}   # subject -> Counter-ish dict
    undated = []
    for subj_dir in sorted(RAW.iterdir()):
        if not subj_dir.is_dir() or subj_dir.name.startswith("_"):
            continue
        subject = subj_dir.name
        if subjects and subject not in subjects:
            continue
        cutoff = CUTOFFS.get(subject)
        dest_root = OUT / subject
        if dest_root.exists():
            shutil.rmtree(dest_root)
        s = {"Papers": 0, "Archive": 0, "Other": 0, "Resources": 0}
        for pdf in subj_dir.rglob("*.pdf"):
            rel = pdf.relative_to(subj_dir).parts
            category = rel[0] if len(rel) > 1 else "(root)"
            bucket, sub = classify(category)
            if bucket == "Papers":
                yr = YEAR_RE.search(pdf.name)
                yr = int(yr.group(1)) if yr else None
                if cutoff and yr and yr < cutoff:
                    dst = dest_root / f"Archive-pre-{cutoff}" / sub / pdf.name
                    s["Archive"] += 1
                else:
                    dst = dest_root / "Papers" / sub / pdf.name
                    s["Papers"] += 1
                    if cutoff and not yr:
                        undated.append(str(pdf.relative_to(RAW)))
            elif bucket == "Resources":
                dst = dest_root / "Resources" / pdf.name
                s["Resources"] += 1
            else:
                dst = dest_root / "Other" / pdf.name
                s["Other"] += 1
            link(pdf, dst, do_copy)
        stats[subject] = s
    return stats, undated


def main():
    args = sys.argv[1:]
    do_copy = "--hardlink" not in args   # copies by default; --hardlink for a fast local view
    subjects = [a for a in args if not a.startswith("-")]
    OUT.mkdir(exist_ok=True)

    stats, undated = organize(subjects, do_copy)

    # manifest for humans
    manifest = {
        "generated_from": "papers/ (raw ingest)",
        "mode": "copy" if do_copy else "hardlink",
        "cutoffs": CUTOFFS,
        "subjects": stats,
    }
    (OUT / "_MANIFEST.json").write_text(json.dumps(manifest, indent=2))

    tot = {"Papers": 0, "Archive": 0, "Other": 0, "Resources": 0}
    print(f"{'Subject':32s} {'Papers':>6s} {'Archive':>7s} {'Other':>6s} {'Resource':>8s}  cutoff")
    print("-" * 74)
    for subj in sorted(stats):
        s = stats[subj]
        for k in tot: tot[k] += s[k]
        print(f"{subj:32s} {s['Papers']:>6d} {s['Archive']:>7d} {s['Other']:>6d} {s['Resources']:>8d}"
              f"  {CUTOFFS.get(subj, '-')}")
    print("-" * 74)
    print(f"{'TOTAL':32s} {tot['Papers']:>6d} {tot['Archive']:>7d} {tot['Other']:>6d} {tot['Resources']:>8d}")
    print(f"\nwrote {OUT.relative_to(ROOT)}/ ({'copies' if do_copy else 'hardlinks'})")
    if undated:
        print(f"note: {len(undated)} exam papers in cutoff subjects had no parseable year -> "
              f"kept in Papers/ (current). e.g. {undated[0]}")


if __name__ == "__main__":
    main()
