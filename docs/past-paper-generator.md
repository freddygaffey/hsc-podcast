> ⛔ STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# Feature Spec — Past-Paper Generator & Diagnostic Marking

> Status: **Draft for review.** This is a design document, not implementation. It
> captures how the feature must work so we build the right thing once.
> Owner: Fred. Last updated: 2026-07-02.

---

## 1. The goal in one paragraph

Students build their **own** practice papers by pulling real questions from a large,
tagged bank of scraped past papers (school trials + NESA HSC). They choose *whose*
papers they want (some schools are higher quality than others), filter by module /
question style / marks / paper type, and generate a **downloadable, print-ready PDF**.
Every question on that PDF is a **stitched screenshot of the original**, carrying a
**provenance label** so it is fully traceable. After sitting the paper they **mark it on
the laptop**, tagging *why* each mark was lost. The app maps those losses to **syllabus
weaknesses and error types**, then **recommends targeted remediation** — more projectile-
motion questions, or the case-study podcast that fills the gap. Assess → diagnose →
remediate → reassess.

**Non-negotiables (Fred's explicit requirements):**

1. **Traceability is mandatory.** Every question, on-screen and on the printout, shows
   where it came from (school, paper, year, question number, marks).
2. **Screenshots, not parsed text.** Questions are rendered from **cropped images of the
   source PDF**, stitched together — *not* re-typeset from OCR/LLM text. This preserves
   diagrams/graphs/stimulus and avoids hallucinated content.
3. **Flexible & dynamic selection.** Students filter by school, paper type (trial vs HSC),
   module, question style, marks, quality — or ignore schools and just pick questions.
4. **Diagnostic marking.** Marking classifies the *type* of error and maps to syllabus,
   producing recommendations, not just a score.

---

## 2. How it fits the existing app

Current stack (do not fight it):

- **Static PWA** deployed to Cloudflare (`hsc.pebnum.com`), no server rendering.
- **R2 bucket** (`hsc-podcast-audio`) already serves per-episode assets via a base URL in
  the manifest. Baked per-question PDFs live the same way (new bucket or prefix).
- **Content pipeline is build-time Python** under `tools/` (`generate_manifest.py`,
  `upload_audio.py`, `validate_quiz.py`, …), and the **THSC scraper already exists**
  (`papers/_downloader.py`, ~203 PDFs). Ingestion follows the same pattern: offline tooling
  produces assets + a manifest; the app just consumes JSON + PDFs.
- **Runtime state is client-side** (localStorage FSRS store, paper-attempt store) with an
  auth-worker sync layer whose `events` table is **E2E-encrypted (zero-knowledge)** — see §5b.
- **Existing quiz schema** (`content/<subject>/<ep>/quiz.json`) informed the question model,
  but the `source` shape diverges — treat this as a *new* schema, not an extension.

So the feature splits cleanly into **two halves**:

| Half | Where it runs | Output |
|------|---------------|--------|
| **A. Ingestion** (scrape ✓ → segment → **bake per-question PDFs** → tag) | Offline Python tooling | Sharded manifest + anonymised per-question PDFs in R2 |
| **B. App** (browse → generate → export → mark → recommend) | Client PWA | PDF export + diagnostic stats, synced |

The hard, risky, one-time work is Half A. Half B reuses infrastructure we already have.

---

## 3. Data model

The atomic unit is a **Question**. A past paper is just an ordered list of questions that
share a `source`. A generated paper is a user-built list of question references.

### 3.1 Question (bank entry)

The record below is what **ships** to the client. The stored asset is an **anonymised,
baked per-question PDF** keyed by an arbitrary id — the full source paper never ships (see
§4.4 for the serving decision). The ingest-time coordinates that produced the crop live in
a **local sidecar**, not in this record (§4.1).

```jsonc
{
  "id": "q_a8f3d2",                    // ARBITRARY key — also the R2 object name (q_a8f3d2.pdf)
  "subject": "maths-advanced",

  "assetKey": "q_a8f3d2.pdf",          // baked per-question PDF in R2 (anonymised bucket)
  "markingKey": "m_a8f3d2.pdf",        // baked marking-guideline crop, if any (nullable; §4.4)

  "source": {
    "kind": "trial",                   // "trial" | "hsc" | "textbook"
    // exam sources (trial / hsc):
    "school": "Sydney Grammar School", // null for NESA HSC
    "board": "NESA",
    "paperName": "2019 Maths Advanced Trial",
    // textbook sources (kind === "textbook") — reuses the ingest_textbook.py copyright model:
    "book": null, "edition": null, "chapter": null, "page": null,
    // common:
    "year": 2019,
    "questionNumber": "21",            // parent question (metadata group)
    "partLabel": "b",                  // atomic unit = LETTER PART; null if none (D4). Romans stay bundled.
    "questionMarks": 7,                // parent total; `marks` above is THIS part's marks
    "syllabusEra": "2019-",            // syllabus version this Q belongs to (see §6; NEW)
    "onSyllabus": true                 // false = off current syllabus, hidden by default
  },

  "syllabus": {
    "module": "Calculus",
    "topic": "Integration",
    "points": ["MA-C-01"]              // OUR minted refs (NESA dot points have no stable ids; §6)
  },

  "type": "mc" | "short" | "extended" | "calculation" | "worked",
  "style": ["calculation", "diagram-interpretation"], // free tags for finer filtering
  "marks": 3,

  // For auto-markable MCQs only — lets the app grade without human input:
  "answer": 1,                          // index, mc only (extracted from the solutions; §4)
  "options": ["A", "B", "C", "D"],      // mc only (text or image refs)

  "quality": {
    "rating": 3,                        // 1–5; DEFAULT 3, refine from usage (not hand-curated pre-launch)
    "flags": []                         // e.g. "scanned", "multipart", "needs-review"
  },

  "provenanceLabel": "2019 Trial · Q21 · 3 marks"  // shown to the student (traceable); soft on school
}
```

Notes:
- **Serving model (decided — §4.4, D1):** each question is a **baked per-question PDF** with
  an **arbitrary key**; the bucket has no paper/school structure, so it can't be bulk-scraped
  by paper, and a lone question is ambiguous as to origin. The full source paper stays
  **local**. Front end pulls `assetKey` and merges — **no client-side cropping** needed.
- **Traceability is at the DB layer, anonymisation at the storage layer** — the manifest
  still holds full provenance, so the student sees where a question came from; only the
  stored files are anonymised. This satisfies both the traceability rule and copyright.
- **MCQs carry `answer`** (extracted from the paper's solutions) → auto-marked. Written
  questions reference `markingKey` and are **self-marked** (v1) — see §7.
- **`quality.rating`** defaults to 3; refine from real usage — no hand-rating hundreds of
  papers before launch.
- **`provenanceLabel`** is precomputed; one source of truth for the label on the PDF, in the
  browser, and in stats.

### 3.2 Question bank manifest

Per subject, `{ "questions": [ ...Question ], "assetBaseUrl": "<R2>" }` like the current
`audioBaseUrl`. The manifest holds records + arbitrary keys; the baked per-question PDFs
live in R2 under those keys.

**Scale — thousands of papers is the design point.** Thousands of papers × ~30 questions =
tens of thousands of records; a single `questions.json` at ~500 B/record would be 10–30 MB.
So **shard the manifest** — a small top-level index (subjects → modules → shard URLs) plus
per-module (or per-paper) shards the app lazy-loads only for the filters in play. Don't ship
one giant file. (Baked per-question PDFs in R2 scale fine as a flat arbitrary-key namespace.)

### 3.3 Generated paper (client-side, synced)

```jsonc
{
  "id": "paper-local-uuid",
  "title": "My Projectile Motion Set",
  "createdAt": 1751400000000,
  "filters": { /* the selection used, for "regenerate similar" */ },
  "questionIds": ["phy-2019-sgs-trial-q21", "phy-2018-nesa-hsc-q31", ...],
  "totalMarks": 42
}
```

### 3.4 Attempt & marking (client-side, synced)

```jsonc
{
  "paperId": "paper-local-uuid",
  "startedAt": 1751400000000,
  "status": "in-progress" | "submitted" | "marked",
  "perQuestion": [
    {
      "questionId": "phy-2019-sgs-trial-q21",
      "marksAwarded": 1,
      "marksPossible": 3,
      "errorTags": ["skill-gap:projectile-motion"],  // see §7.2
      "note": "forgot to resolve into components"
    }
  ]
}
```

Resumability ("come back to it") = persist `status: in-progress` and re-open where left off,
exactly like the existing paper-attempt store.

---

## 4. Half A — Ingestion pipeline (the hard part)

Source: **THSC** (thsconline) — thousands of school trials + HSC papers as PDFs, and the
**scraper already exists** (`papers/_downloader.py`, ~203 downloaded, maths prioritised). The
pipeline segments each PDF and **bakes each question into its own anonymised PDF** (§4.4); the
full source paper stays local. **This is the highest-risk component; budget the most care here.**

### 4.1 Pipeline stages

```
PDF → render pages to images → detect question regions → record region coords → OCR (metadata only)
    → classify (module/topic/type/marks) → human review → publish (PDF to R2 + coords to manifest)
```

0. **Detect born-digital vs scanned** (`pymupdf` text layer present?). Born-digital → crop as
   **vector** (tiny, print-perfect); scanned (~23% of the corpus) → crop as **raster**. Handle
   page rotation (`/Rotate`) here, once, so the render path never has to.

1. **Render** each page to a raster only where needed (scans, or to help detection). The
   shipped crop for born-digital pages is a **vector clip**, not a raster (§4.4).

2. **Detect question regions.** Find the vertical span of each question on each page
   (a question = from its "Question N" heading to the next). This is the classifier Fred
   described — "select where in the PDF each question is." Approach, cheapest-first:
   - **Heuristic pass:** OCR text + regex for question markers ("Question 21", "(a)", mark
     annotations like "(3 marks)") → candidate y-cut lines per page.
   - **Vision pass (fallback / low-confidence):** a vision model (Claude) given the page
     image returns bounding boxes for each question + its marking region. Used only where
     heuristics are unsure, to keep cost down.
   - Output per question: an ordered list of `(page, x0,y0,x1,y1)` rectangles.

3. **Record regions in a LOCAL sidecar, then bake.** Store each question's rectangles
   (normalised, per page) in a **local** `regions.jsonl` next to the source PDF — this is the
   editable master (fix a crop = edit numbers), and it **never ships**. Then **bake** each
   question into its own anonymised per-question PDF (`q_<key>.pdf`): vector clip for
   born-digital, raster for scans; shared stimulus (a graph feeding Q3–Q5) is composited into
   each question that needs it. **No re-typesetting — the baked pixels/vectors are the
   original.** (Serving rationale: §4.4.)

4. **OCR for metadata only.** OCR extracts text used *only* for tagging and search
   (module, marks, keywords) — **never** shown to the student as the question. This is the
   key hallucination guard: text can be wrong without corrupting what the student sees.

5. **Classify** each question into `type`, `style`, `marks`, `module`, `topic`, `points`,
   `syllabusEra`/`onSyllabus` (LLM + syllabus map from §6). Low-confidence → flagged. Also
   **extract MCQ answers** from the paper's solutions pages (own sub-task — it's what makes
   auto-marking work; many corpus papers are "w. sol." so the answers are present).

6. **Confidence-triaged review gate.** Attach a confidence score (born-digital + clean
   single-column + matched "(N marks)" = high). **Auto-accept high-confidence; route only the
   ambiguous to a human.** At thousands of papers, review throughput — not segmentation — is
   the real bottleneck, so the **visual box-adjust review tool is first-class** (it doubles as
   the manual-annotation tool you bootstrap with). A CSV checklist will not survive paper #3.

7. **Publish.** Upload the **baked per-question PDFs** to R2 under their arbitrary keys
   (`q_<key>.pdf`, flat namespace; fork of `upload_audio.py`), append the question **records**
   to the sharded manifest (§3.2). The **full source PDF stays local** — never uploaded.

### 4.2 Why screenshots (design rationale, keep this decision recorded)

- Preserves diagrams, graphs, tables, and exact stimulus wording.
- Eliminates LLM transcription errors in the thing students actually study.
- Matches how students see real exams (builds familiarity — the good-UI principle again).
- Cost: no reflow on mobile (a fixed crop, not flowing text). Accepted trade-off. (Serving
  handled by baked per-question PDFs, §4.4.)

### 4.3 Tooling

New scripts under `tools/`, following existing conventions. Note: the THSC **scraper already
exists** (`papers/_downloader.py`, ~203 PDFs downloaded, maths prioritised) — reuse it.
- `tools/ingest_papers.py` — orchestrates detect → segment → bake per-question PDFs → OCR → classify.
- `tools/review_papers.py` — the **visual box-adjust** review + annotation tool (first-class).
- `tools/upload_papers.py` — upload **baked per-question PDFs** to R2 (fork of `upload_audio.py`).
- Extend `tools/generate_manifest.py` to emit the **sharded** questions manifest + `assetBaseUrl`.

### 4.4 Serving model — baked per-question PDFs, readable per-paper folders (REVISED 2026-07-03)

Each question is **baked at ingest into its own PDF** and served from a **readable per-paper
folder** in the shared public bucket:

    <subject>/papers/<paperSlug>/q01a.pdf     question crop
    <subject>/papers/<paperSlug>/a01a.pdf     its answer crop
    <subject>/papers/<paperSlug>/paper.pdf    full original exam (kept deliberately)

This **revises the original D1 decision** (anonymised arbitrary keys, full paper never
published). Rationale for the revision (Fred, 2026-07-03): readable keys are simpler for an
MVP and debuggable by eye; the full `paper.pdf` doubles as an optional source of truth and
enables a "download the full original trial" feature; THSC already redistributes these
papers publicly, so incremental copyright exposure is low. The trade-off accepted: the
bucket is walkable by school/paper. **Textbook crops are the exception — they are
commercial-publisher content and must be login-gated (served via the auth-worker), never
public** (see textbook ingestion notes).

- **Born-digital → vector clip** (`pymupdf`/`pdf-lib` bounding-box embed): tiny, print-perfect,
  literally the original vectors. **Scanned (~23%) → raster crop.** Fidelity preserved either way.
- **Front end is simple:** fetch `assetKey` (a ~tens-of-KB PDF), display/embed it, merge the
  selected ones for export. **No pdf.js cropping, no range requests, no rotation handling** at
  runtime — all resolved once at bake time.
- **Offline:** "download this paper" caches the handful of small per-question PDFs — trivial,
  no synthesised-206 machinery.
- **Traceability:** full provenance ships in the manifest records (paperSlug, question number,
  marks) and is visible in the bucket path itself.

---

## 5. Half B — The app

### 5.1 Paper generator (selection)

A **filter builder**, dynamic and additive. Filters (all optional, combine freely):

- **Schools** — multi-select; or "any school." Show quality rating per school/paper.
- **Source kind** — School Trial / NESA HSC / **Textbook** (§3.1 `source.kind`). Textbook
  questions are scaffolded/worked — best for rebuilding foundations; exam papers for
  pressure. See severity→source routing in §7.2.
- **Year range.**
- **Module / topic** — from the syllabus map.
- **Question style / type** — MC, short, extended, calculation, case-study, etc.
- **Marks target** — "build me a ~50-mark paper" (auto-fill to hit the target).
- **Quality** — minimum rating (default: hide low; default rating 3).
- **On-syllabus** — default **on** (`source.onSyllabus`); hides off-current-syllabus questions
  (the corpus reaches back to 2001/1969 and maths changed in 2020 — a year filter is *not*
  enough, students don't know the cutover). Advanced users can include older material.

**One filter builder, one mode** — "pick schools" is just the Schools filter set; there's no
separate "start from schools" flow. Live results list; hand-pick or auto-fill to N marks;
Save as paper (§3.3).

### 5.2 PDF export & traceability

- Client-side assembly: **merge the selected questions' baked PDFs** (`assetKey`) with
  `pdf-lib` into a print-ready A4 PDF. No cropping/rendering — the crops are already baked.
- **Every question is labelled** with `provenanceLabel` in a consistent header/footer.
- **Writing space** proportional to marks after each question (ruled lines) — a real paper is
  answerable. *This is a Part-1 requirement, not a nicety.*
- Append the **NESA reference/formula sheet** (maths papers assume it's provided).
- Cover page (title, total marks, suggested time) + a separate marking booklet from each
  question's `markingKey` (exported separately so students can't peek).
- Also viewable **on-screen** for laptop marking without printing.
- **Download for offline is an explicit, wanted feature** — the generated paper is a plain
  downloadable PDF, and its per-question assets cache in the service worker for offline study.
  (This is *not* in tension with §4.4's anonymised storage: the anonymisation only blocks
  bulk-scraping the whole raw corpus — it never restricts a student saving the paper *they*
  built. Downloading is allowed.)

### 5.3 Marking on the laptop

- Question-by-question marking view: shows the baked question PDF (+ `markingKey` on reveal),
  a **marks-awarded input**, and **one dominant error tag** per question (§7.2), plus a note.
- MCQs auto-mark (we have `answer`); written questions are self-marked against the guideline.
- Persist as an **Attempt** (§3.4); resumable; synced. *(All of §5.3–5.4 is Part 2.)*

### 5.4 Diagnostics & recommendations (the payoff)

From marking data, roll up:
- **Weak syllabus areas** — marks lost per module/topic/dot-point.
- **Error-type profile** — skill gaps vs knowledge gaps vs exam-technique (§7.2).
- **Recommendations engine** turns that into actions:
  - Lost marks on projectile motion *skills* → "Practise these 6 projectile-motion
    questions" (bank query by topic + type).
  - Lost marks because a *case study* was missing → "Listen to *[case-study podcast]*" +
    the related flashcards (links into existing content).
- Feeds the headline **Daily Review** surface (see the broader redesign): due flashcards +
  weak-area questions + unfinished papers in one place.

---

## 5b. Data capture philosophy — capture raw, derive later

> **Scope: PART 2.** Part 1 needs only two persisted objects — saved papers (§3.3) and later
> attempts (§3.4) — via the existing localStorage + sync. Don't build the event log for the
> generator; just don't *design it out*. **Encryption constraint:** the auth-worker's `events`
> table already exists and stores **opaque AES-GCM ciphertext the server can't read**
> (zero-knowledge — and a genuine privacy asset for minors, §5b.4). "Analyse server-side
> later" would break that boundary, so either keep analytics **client-side** or make an
> explicit, deliberate decision to relax the encryption. Resolve in the Part 2 design.

**Principle (Fred's directive):** collect as much data as we possibly can *now*, lose
nothing, and design better algorithms + UI on top of it *later*. The correct
implementation of this is an **append-only, immutable event log** — event sourcing — not a
schema-less dump. All metrics, mastery models, stats, and recommendations are *derived
views* over this log and are always recomputable; the raw log is the source of truth.

### 5b.1 What we log

Every meaningful interaction becomes an event. Capture **process, not just outcomes** —
the behavioural signal is where the value is:

- **Outcomes:** `marks_awarded`, `option_selected`, `error_tagged`, `flashcard_rated`.
- **Process (the gold):** `question_viewed` (+ dwell time), time-to-first-interaction,
  answer revisions, order questions were attempted, `guideline_revealed`,
  blank-vs-attempted, hesitation.
- **Intent & funnel:** `filter_changed`, `paper_generated` (+ the filter used),
  `recommendation_shown` vs `recommendation_followed`, `audio_played`, `paper_resumed`.

### 5b.2 Event shape

```jsonc
{
  "eventId": "uuid",            // idempotency key for sync dedupe
  "userId": "pseudonymous-id",  // NOT tied to real identity (see §5b.4)
  "ts": 1751400000000,
  "type": "marks_awarded",
  "schemaVersion": 1,           // additive; new types/fields never break old ones
  "payload": { /* type-specific */ },
  "ctx": { "app": "build-hash", "device": "…", "online": false }
}
```

### 5b.3 Rules that make "no data lost" real

- **Immutable + additive.** Corrections are *new* events, never edits/deletes → history is
  complete. New event types must never break old consumers; version every payload.
- **Raw kept forever; aggregates derived.** Mastery/stats/recommendations are recomputable
  views — invent a better algorithm later and re-derive from the full history.
- **Offline durability (engineering requirement, not a hope).** PWA is offline-first, so:
  a **local append-only outbox** survives being offline and app reinstalls; **idempotent
  sync** (dedupe by `eventId`) pushes to the existing auth-worker + D1 — add an `events`
  table (or Cloudflare Analytics Engine / R2 for volume). Nothing is lost on a flaky train.

### 5b.4 Privacy — these are students, often minors (non-negotiable)

HSC students are 16–18, some under 16. "Collect everything, never delete" about minors is a
real legal + trust obligation and must be designed in from event #1:

- **Pseudonymous IDs; minimal PII.** Keep identity separate from behaviour — you don't need
  a real name to model learning.
- **Explicit consent + privacy policy**; Australian Privacy Act / APPs; parental-consent
  considerations for under-16. Be especially careful with **free-text** (marking notes).
- Done right this is a **selling point** for schools/parents, not just compliance.

---

## 6. Syllabus map (dependency for tagging + recommendations)

Recommendations only work if questions map to syllabus. Build a structured NESA syllabus
per subject: `content/<subject>/syllabus.json` → modules → topics → dot-points with stable
ids (`PH12-5`, etc.). Used to: tag questions during ingestion, drive the module/topic
filters, and target recommendations. Podcast episodes and flashcards should reference the
same ids so the loop can recommend *content*, not just more questions.

---

## 7. Marking model detail

### 7.1 v1 vs v2 marking

- **v1 — self-mark.** Student compares to the marking-guideline image and assigns marks.
  Simple, ships fast, no accuracy risk. **Recommended first.**
- **v2 — assisted mark.** For written answers, optionally let Claude mark against the
  guidelines and suggest a band/marks + feedback. Clean upgrade; do not block v1 on it.

### 7.2 Error taxonomy — maths first (two levels + modifiers)

Six **top-level** categories, **ordered by severity** (severity drives remediation
intensity *and* which source we route the student back to). Each has **subclasses** —
optional refinement, so the student taps one category and *may* add detail. Two
**orthogonal modifiers** apply across all. Aligns with Newman's Error Analysis.

| Severity | Tag | Means | Subclasses | Route back to |
|----------|-----|-------|-----------|---------------|
| 🔴 highest | `no-entry` | **Couldn't even begin** — didn't recognise the concept or understand the question. The red flag. | `concept-unknown`, `question-unclear`, `cant-connect` (knows pieces, can't combine), `prerequisite-frozen` | **Teaching + textbook worked examples** — *not* more exam questions |
| 🟠 high | `method` | Engaged, wrong/absent approach | `wrong-technique`, `formula-recall`, `setup-translation`, `domain-restriction`, `proof-logic` | Targeted method practice |
| 🟡 med | `slip` | Right method, mechanical error | `sign`, `arithmetic`, `algebra-manipulation`, `transcription` | Drills + checking habit |
| 🟢 low | `misread` | Interpretation error | `wrong-value`, `missed-condition`, `answered-different-question`, `diagram-misread` | Question-decoding technique |
| 🟢 low | `communication` | Right idea, lost presentation marks | `no-working`, `units`, `rounding`, `sig-figs`, `notation`, `justification` | Model-answer discipline |
| ⚪ n/a | `incomplete` | Blank/partial due to **time, not knowledge** | `partial`, `ran-out-of-time` | Timed practice, exam strategy |

**Modifiers (orthogonal — apply to any tag):**
- `carried` — this mark was lost as a *consequence* of an earlier error (HSC follow-through).
  Stops the mastery model counting one root mistake as several gaps.
- `prerequisite-gap` — root cause is an *earlier-year* skill; points the student upstream.

**Capture rules:**
- **One dominant tag per *question*, not per lost mark.** Tagging each of 3 lost marks on a
  4-marker across a 50-mark paper is a compliance fantasy — students drop off after paper one
  and starve Part 2 of data. One tag per question (optional marks-lost split, optional
  subclass/modifiers) is realistic and still diagnostic. This is the single biggest practical
  risk to Part 2; keep the marking UI one-tap.
- The picker shows a **one-line example per tag** (the boundary cases — `slip:transcription`
  vs `misread:wrong-value`, `rounding` vs `slip` — are where students get confused). When
  torn between two, pick the **more severe**.
- `no-entry` can be logged **pre-attempt** — a one-tap "froze on sight" event. This is the
  purest foundational-gap signal, and it's what turns "I have no clue where to start" from a
  dead end into a diagnosis.
- **Blank ≠ blank:** `no-entry` blank (didn't understand 🔴) vs `incomplete:ran-out-of-time`
  blank (time 🟢) are opposite diagnoses of the same empty page — never collapse them.
- **`slip` vs `method`** is the load-bearing distinction: `slip` = "can do it, be careful"
  (don't drill the topic); `method` = real gap (drill + teach).
- Extensible + versioned — add subclasses as data reveals them; never renumber.

**Severity drives remediation *type*, but rollups weight by *marks lost*.** Severity ≠ marks
impact: `misread:answered-different-question` is 🟢 but can zero a 4-marker — a chronic
misreader is not a low-severity student. So the routing (below) is chosen by tag, but "how big
is this gap" is measured in marks lost.

**Severity → source routing** (ties the taxonomy to §5.1 and the textbook source): the worse
the error *type*, the more foundational the material — `no-entry` → textbook / worked
examples; mid → topic questions; exam-readiness → full past papers.

---

## 8. Suggested phasing (milestones)

**Two-part delivery (Fred's directive).** Build in two parts, and treat Part 1 as a
complete product, not a stepping stone:

- **PART 1 — The Generator (primary feature).** Target the areas + question types you want,
  assemble a custom paper, export a traceable PDF. Ships standalone — valuable with *no*
  marking, accounts, or AI. Here "weak areas" = **you pick them manually**. (= M0–M2.)
- **PART 2 — Marking + recommendation (intelligence layer).** Archive attempts, diagnostic
  marking, mastery model, and **auto-detected** weak areas built *on top of* Part 1. Here
  "weak areas" = **the app detects them** from your error data. (= M3–M5.)

Same feature ("generate questions in your weak areas") — Part 1 delivers it by *you telling
it*, Part 2 upgrades it to *it telling you*.

### Milestones

1. **M1 — Ingestion spike (comes FIRST; it *produces* the schema).** Take 2–3 born-digital
   Maths Advanced papers already in `papers/`, hand-record `regions`, bake per-question PDFs,
   and prototype **merge → provenance-labelled export with writing space** — include one
   scanned paper to test the raster path. You cannot finalise `regions`/multipart/marking
   shape before segmenting real papers, so the spike defines them. The box-adjust tool you
   build here *is* the M-scale review tool.
2. **M0 — Schema lock (right after M1).** Freeze Question / manifest / attempt schemas (§3)
   + the minted syllabus refs (§6) from what M1 taught you. *No scraping at scale until locked.*
3. **M2 — Browse & generate (ships Part 1).** Sharded manifest load + filter builder + save
   paper + **export with provenance, writing space, reference sheet** (§5.1–5.2). **Confirm
   D1/serving (§4.4) here** — it sets the storage architecture. Usable before marking exists.
4. **M3 — Marking + attempts (Part 2).** On-laptop marking, one-tag-per-question, resumable
   attempts (§5.3). Resolve the §5b encryption boundary before any event log.
5. **M4 — Diagnostics + recommendations.** Weakness rollups (marks-weighted) + engine (§5.4),
   wired into Daily Review. (Note: no maths teaching content exists yet — routing falls back
   to textbook/worked questions until it does.)
6. **M5 — Scale ingestion** across all subjects/schools (confidence-triaged review); v2 marking.

Ship M1's learnings before committing to M2's UI — crop quality determines everything.

---

## 9. Risks & open decisions

**Decisions needed (flagging, not deciding here):**

- **D1 — Copyright / serving. REVISED (Fred, 2026-07-03).** Bake **per-question PDFs**,
  serve them from **readable per-paper folders** (`<subject>/papers/<paperSlug>/`), with the
  **full `paper.pdf` included** as an optional source of truth / full-trial download.
  Supersedes the original anonymised-key decision — simpler for MVP; copyright exposure
  accepted on THSC precedent. Exception: **textbook crops are login-gated, never public.**
  See §4.4.
- **D2 — Segmentation accuracy target.** How much human review per question is acceptable?
  Confidence-triage: auto-accept high-confidence, review the rest. M1 sets the realistic ratio.
- **D3 — Marking depth for v1.** Self-mark only, or ship assisted (Claude) marking sooner?
- **D4 — Multi-part questions. REVISED (Fred, 2026-07-03).** The **display/selection unit
  is the WHOLE question** — bake_questions.py bakes `q<N>.pdf` = stem + stimulus + all
  parts (continuation "(continued)" entries merged), and the generator lists/exports only
  `unit: "question"` records. Rationale: review-sheet output (the SmarterMaths exemplar) —
  an orphaned "(a)" fragment on a worksheet makes no sense. **Letter parts are still baked
  and recorded (`unit: "part"`, stimulus riding along) but serve as metadata only** —
  per-part marks, future finer filtering/diagnostics. Roman sub-parts stay bundled as
  before. This also neutralises the roman-numeral mis-split bug for display (the "i"
  mislabel corpus-wide: 236 papers / 967 questions — parts data still needs the repair
  pass, but whole-question crops are unaffected).
- **D5 — Consent & privacy model for minors.** Required before any event log ships (§5b.4):
  consent flow, pseudonymisation boundary, retention policy, parental consent for under-16.

**Risks:**

- **Review throughput is the real schedule risk** (not segmentation alone). At thousands of
  papers, "human glances at everything" is the bottleneck — hence confidence-triage + a
  first-class visual box-adjust tool (§4.1, §4.3). M1 surfaces the realistic ratio.
- **Manifest scale** — tens of thousands of records → **shard the manifest** and lazy-load
  (§3.2), never one giant JSON.
- **OCR mis-tagging** — mitigated by never showing OCR text as the question (tags only) and
  by the review gate.
- **Near-duplicate questions** — schools recycle HSC/each other; dedupe (perceptual-hash /
  OCR-text similarity) at ingest so generated papers and diagnostics aren't polluted.
- **Scanned papers (~23%)** — no vector to clip; baked as raster crops (larger, still fine).
- **PWA offline** — a downloaded paper caches its handful of small per-question PDFs; the full
  bank can't preload. Simple per-paper download story (no range machinery).
- **`app.js` is a 3,300-line single file mid-restructure** (the unify redesign) — sequence the
  generator UI against that or the filter UI gets built twice.

---

## 10. Summary

Two clean halves. **Half A (ingestion)** is an offline Python pipeline that segments THSC
PDFs and **bakes each question into its own anonymised, arbitrary-keyed PDF** (real
pixels/vectors, not text — no hallucination); the full source paper never ships. **Half B
(app)** reuses the static-PWA + R2 + sync stack: **PART 1** lets students filter by the areas
and question types they want and **export a custom, traceable paper** (writing space +
reference sheet) — a complete product on its own; **PART 2** adds one-tap marking, a
marks-weighted mastery model, and auto-detected weak areas on top. Spike ingestion first (M1
defines the schema), lock it (M0), ship Part 1 (M2), then build the intelligence. Traceability
(in the DB) + real-screenshot fidelity + anonymised storage are the spine.
