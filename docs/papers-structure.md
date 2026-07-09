> ⛔ STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# Papers Directory Structure — Contract

_The canonical, machine-readable layout for HSC past papers. Anything that **pulls**
papers (the past-paper generator, the parser, a Cloudflare/R2 sync, a distribution zip)
reads the **organized** tree defined here and can rely on it. Last updated 2026-07-08._

There are **two layers**. Keep them separate.

---

## 1. Raw ingest — `papers/` (source of truth, do not reorganize)

Written by the scrapers (`papers/_downloader.py` THSC, `papers/_nesa.py` NESA,
`papers/_acehsc.py` acehsc) and mirrored to local by the server sync loop. Shape:

```
papers/<Subject>/<Category>/<file>.pdf
```

- `<Subject>` — human subject folder, e.g. `Physics`, `Maths Advanced`, `English Standard`.
- `<Category>` — the raw source bucket, e.g. `Y12-HSC`, `HSC-NESA`, `Y12-Trial`,
  `Y11-Yearly`, `ACE-Trial`, `ACE-Notes`, … (full mapping in §3).
- `papers/_*` — tooling, logs, indexes, and the parser working dir (`_work/`). **Never**
  part of the papers contract; consumers ignore anything starting with `_`.

Producers write here. **Consumers must not read the raw layout directly** — it changes
shape per source and mixes syllabus eras. Consume the organized layer instead.

`papers/_index.json` (built by `tools/index_papers.py`) is the metadata catalogue over
the raw tree: `{paperId, subject, kind, board, year, role, hasSolutions, path, …}`.

---

## 2. Organized view — `papers_organized/` (derived, what consumers pull)

Generated from the raw tree by `tools/organize_papers.py` (safe to re-run any time;
new raw papers are picked up on the next run). Real **copies** by default so it pushes
cleanly to object storage (no sym/hardlink semantics). Shape:

```
papers_organized/
  _MANIFEST.json                         generation metadata + per-subject counts + cutoffs
  <Subject>/
    Papers/                              CURRENT-syllabus exam papers (+ marking guides alongside)
      HSC/                               official HSC finals (NESA + THSC + ACE)
      Trial/                             Year 12 trial papers (+ solutions)
      Yearly-Y11/                        Year 11 yearly / prelim papers
    Other/                               paper-shaped but not a standard exam: half-yearlies,
                                         assessment tasks, topic HSC-question sets, misc
    Resources/                           supplementary: notes, essays, case studies, quizzes,
                                         videos, syllabus extracts
    Archive-pre-<cutoff>/                OLD-syllabus exam papers only (year < cutoff)
      HSC/  Trial/  Yearly-Y11/
```

### Guarantees consumers can rely on
- **`Papers/**` is the clean current-syllabus exam set** — the default input for paper
  generation. It never contains notes, and never contains superseded-syllabus papers.
- **`Archive-pre-<cutoff>/`** holds only exam papers older than the subject's current
  syllabus. The `<cutoff>` is that subject's first HSC-exam year under the current
  syllabus (see §4). Subjects with no cutoff have no Archive folder.
- **`Resources/` and `Other/` are era-agnostic** (not year-archived) — they are not
  syllabus-bound exams.
- A marking guide always sits in the **same folder as its exam** (never split out), so
  exam↔guide stay paired by shared folder + year.

---

## 3. Category → bucket mapping (authoritative; lives in `tools/organize_papers.py`)

| Raw category | Organized bucket |
|---|---|
| `Y12-HSC`, `HSC-NESA`, `ACE-HSC` | `Papers/HSC` |
| `Y12-Trial`, `Y12-Trial-P1`, `Y12-Trial-P2-Adv`, `Y12-Trial-P2-Std`, `ACE-Trial` | `Papers/Trial` |
| `Y11-Yearly` | `Papers/Yearly-Y11` |
| `ACE-Notes`, `ACE-Essay`, `ACE-CaseStudy`, `ACE-Quiz`, `ACE-Video`, `ACE-Syllabus` | `Resources` |
| anything else (`ACE-Assessment`, `ACE-HalfYearly`, `ACE-HSC-Questions`, `ACE-Yearly`, `ACE-Misc`, `ACE-Other`, unknown) | `Other` |

A `Papers/*` file whose parsed year `< cutoff` is redirected to
`Archive-pre-<cutoff>/<same sub-bucket>`.

---

## 4. Syllabus cutoffs — `tools/syllabus_cutoffs.json`

`{ "<Subject>": <first HSC-exam year of the current syllabus> }`. Only subjects that
have actually changed syllabus need an entry; the rest are treated as all-current.
Currently populated for the 16 high-confidence, high-volume subjects (Maths, Sciences,
English, History). Language/VET cutoffs still need authoritative implementation years
before they are added (until then those subjects are all-current — nothing archived).

**The only recurring human task:** when NSW introduces a new syllabus, add/update one
line here and re-run `tools/organize_papers.py`. Everything else is automatic:
- new papers → land in raw → reclassified on next run;
- a new year (e.g. 2026 HSC) → `year ≥ cutoff` → drops into `Papers/` with no change;
- a new subject → auto-detected (add a line only if its category mapping is unusual).

---

## 5. How to regenerate

```bash
python3 tools/organize_papers.py            # all subjects, real copies -> papers_organized/
python3 tools/organize_papers.py Physics    # one subject (sample)
python3 tools/organize_papers.py --hardlink # local-only fast view (NOT for R2 upload)
```

`papers_organized/` and `papers_organized_*.tar.gz` snapshots are git-ignored (large,
copyright). Distribution/backup = tar the tree (or rsync the copies to R2).
