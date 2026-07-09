# English (Standard) question categorisation — findings & handoff

Status: **investigated, not executed.** The actual categorisation needs an LLM
(Haiku) parsing pass over the source PDFs — see "How to run it" below. This doc
captures the model, the authoritative exam structure, the data problems, and the
exact file paths so the next session can start immediately.

Scope so far: **English Standard, current syllabus only (2019–2025).** Older
syllabus (2014–2018, "Area of Study: Discovery") is deliberately out of scope.
Other English courses (Advanced, EAL/D, Studies, Ext 1) not yet looked at, but
Standard's Paper 1 is shared with Advanced so most of this transfers.

---

## The goal

Tag every English Standard question on two axes so the app can filter by module
and by text:

**Axis 1 — module / section** (5 values, determined by paper + section):

| value | where | name |
|---|---|---|
| `short-answer` | Paper 1, Section I | Unseen-text short answers (Q1–5) |
| `common`       | Paper 1, Section II | Common Module — *Texts and Human Experiences* essay |
| `module-a`     | Paper 2, Section I  | *Language, Identity and Culture* |
| `module-b`     | Paper 2, Section II | *Close Study of Literature* |
| `module-c`     | Paper 2, Section III| *The Craft of Writing* |

**Axis 2 — text scope** (what the question is anchored to = the user's
"particular text / multitext / text-type" axis):

| value | meaning | carries |
|---|---|---|
| `prescribed-text`    | tied to ONE named prescribed text (the (a)/(b)/(c)… branches) | title, author, text-type |
| `prescribed-generic` | one essay valid for *any* text in that module's list ("your prescribed text") | module text-list ref |
| `unseen-single`      | short answer on one unseen stimulus text | text-type |
| `unseen-multi`       | short answer comparing 2+ unseen texts ("Text 1 and Text 3") | text-types |
| `composition`        | Module C craft-of-writing — no set text, based on form | writing forms + whether a reflection part |

Text-type vocabulary seen in the papers: `Prose Fiction`, `Poetry`, `Drama`
(incl. Shakespearean), `Nonfiction`, `Film`, `Media`/`Multimedia`. Short-answer
unseen text-types also include: Feature article, Magazine article/cover,
Interview, Memoir, Internet article, Illustration, Photograph, Image, Poem.

### Key nuance — module ↔ branch alternation
Each year, **one** module is examined by splitting into per-text branches
(a/b/c… each naming a prescribed text); the other essay modules are asked
generically ("your prescribed text"). NESA alternates **which** module gets the
branches. So `prescribed-text` vs `prescribed-generic` must be read per paper,
not assumed from the module. Examples:
- 2021 P2: **Module B** had 9 branches (Feed, Curious Incident, Namatjira …); A & C generic.
- 2024 P2: **Module A** had 11 branches (a–k); B & C generic.
- 2022 P1: the **Common** essay (Q6) had branches (a–n) by prescribed text.

---

## Authoritative exam structure (verified from source PDFs)

**Paper 1 — Texts and Human Experiences**
- Section I (20 marks): Q1–5 short answers on ~5–6 unseen texts. Individual Qs are
  3–6 marks. Some reference one text (`unseen-single`), some compare
  (`unseen-multi`, e.g. "Text 1 and Text 3", "Text 5 and Text 6").
- Section II (20 marks): one essay = `common`. Usually `prescribed-generic`;
  occasionally split into per-text branches (2022).

**Paper 2 — Modules** (three sections, 20 marks each)
- Section I  = `module-a`
- Section II = `module-b`
- Section III= `module-c` (imaginative/discursive/persuasive + a reflection part; often a stimulus image/quote)

### Per-paper map (which section carries the per-text branches)
- 2019 P1: SA Q1–5 (incl. Q3 multi Text1+Text3), Common Q6 = **branches a–n**.
- 2019 P2: Mod A = Q1–6 **by text-type/branch**, Mod B Q7 generic, Mod C Q8.
- 2020 P1: SA Q1–4 (Q3 multi Text3+Text4), Common Q5 generic.
- 2020 P2: Mod A Q1 generic, **Mod B Q2–7 branches**, Mod C Q8.
- 2021 P1: SA Q1–5, Common Q6 generic.
- 2021 P2: Mod A Q1 generic, **Mod B Q2 branches a–i**, Mod C Q3.
- 2022 P1: SA Q1–5, **Common Q6 branches a–n**.
- 2022 P2: Mod A Q1 generic, **Mod B Q2 branches**, Mod C Q3.
- 2023 P1: SA Q1–5, Common Q6 generic.
- 2023 P2: Mod A Q1, Mod B Q2, Mod C Q3 — all generic.
- 2024 P1 ("-cc"): SA Q1–5 (Q5 multi Text5+Text6), Common Q6 generic.
- 2024 P2: **Mod A Q1 branches a–k**, Mod B Q2 generic, Mod C Q3.
- 2025 P1: SA Q1–5, Common Q6 generic.
- 2025 P2: Mod A Q1, Mod B Q2 generic, Mod C Q3.

(Note: NESA essay stems name the prescribed-text LIST on a later page; the
prescribed titles per branch are printed in the branch heading, e.g.
"Question 2 (a) — Prose Fiction – M T Anderson, Feed (20 marks)".)

---

## Data problems found (must be handled before/while categorising)

**1. The deterministic split is incomplete.**
`content/english-standard/questions.json` (340 rows) is missing questions and
mislays branches:
- Dropped questions — e.g. real 2025 P1 has Q1–6; the file has only Q1,2,4,6
  (Q3, Q5 missing). Similar gaps elsewhere.
- Per-text branches (a,b,c…) are stored as unlabelled continuation slices
  (`q02-1.pdf … q02-9.pdf`, `partLabel: null`), not distinct parts; several have
  `marks: null`.
- The metadata that IS present (paperId, questionNumber, marks) is essentially
  correct and matches the source PDFs.

**2. Baked per-question PDFs are cross-contaminated (separate bug, affects the app).**
For **Paper 1**, the cropped `baked/qNN.pdf` files render **Paper 2** content.
Example: `papers/_work/english-standard-hsc-nesa-2025-hsc-english-standard-paper-1/baked/q01.pdf`
shows Paper 2's Module A essay ("…Module A prescribed texts…20 marks") instead of
the real 4-mark Text 1 short-answer question. `boundaries.json` for that paper is
CORRECT (Q1 = 4 marks, region on the right page); only the baking/crop step pulled
from the wrong source. Paper 2 crops sampled OK. Needs a re-bake of the Paper 1
set; independent of categorising. **Do not trust `baked/*.pdf` text for Paper 1.**

Consequence: the reliable ground truth for categorising is the **source PDFs**,
not the baked crops. `boundaries.json` marks are trustworthy; baked crops are not.

---

## File paths

- Content metadata (target for enrichment): `content/english-standard/questions.json`
  - null fields ready to fill: `type`, `topic`, `module`, `syllabusRefs`; will
    also need new `textScope`, `textTitle`, `textType`, `author`, `writingForms`.
- Papers index: `content/english-standard/papers-index.json`
- **Authoritative source PDFs**: `papers/English Standard/HSC-NESA/*.pdf`
  (14 current-syllabus papers; `-mg` = marking guidelines, `-cc` = clean copy).
- Per-paper work dirs: `papers/_work/<paperId>/`
  - `boundaries.json` — correct Q numbers/marks/regions (trust this)
  - `ocr.json` — positioned OCR tokens
  - `baked/qNN.pdf` — cropped per-question PDFs (**Paper 1 contaminated**)
  - `info.json` — page count, source path

Current-syllabus paperIds (from questions.json):
```
english-standard-hsc-nesa-2019-hsc-english-standard-p1 / -p2
english-standard-hsc-nesa-2020-hsc-english-standard-paper-1 / -paper-2
english-standard-hsc-nesa-2021-hsc-english-standard-p1 / -p2
english-standard-hsc-nesa-2022-hsc-english-standard-p1 / -p2
english-standard-hsc-nesa-2023-hsc-english-std-paper-1 / -paper-2
english-standard-hsc-nesa-2024-hsc-english-std-paper-1-cc / -paper-2
english-standard-hsc-nesa-2025-hsc-english-standard-paper-1 / -paper-2
```

---

## How to run it (next session)

The categorisation itself is an LLM parsing job — run **Haiku** over the source
PDFs, one question at a time, emitting structured output:

1. For each current-syllabus source PDF, segment into questions using
   `boundaries.json` (trustworthy marks/regions) OR re-parse section/question
   headers from `pdftotext` (headers are clean and self-labelling — the module,
   section, text-type and prescribed title are all printed in the headings).
2. Feed each question's text (and stimulus/heading) to Haiku with a fixed schema:
   `{module, textScope, textType?, textTitle?, author?, writingForms?, reflection?}`.
   Most cases are rule-derivable from the headings; Haiku is mainly for the
   ambiguous short-answer scope (single vs multi) and confirming generic vs branch.
3. Emit a sidecar `content/english-standard/categories.json` keyed by
   `paperId + questionNumber + branch`, then reconcile against `questions.json`
   (this reconciliation will surface the dropped questions from problem #1).
4. Separately: schedule a re-bake to fix the Paper 1 crop contamination (#2).

Because the exam structure is so regular, a large fraction can be done
deterministically from the headings; the Haiku pass is for scope disambiguation
and to generalise to trial papers / other English courses where headings vary.

### Other courses / suggested format work
User takes English (Standard/Advanced) only and doesn't know the exam formats of
the other subjects — for Maths/Physics/etc. the format taxonomy will need to be
proposed per subject before parsing. English Advanced Paper 1 == Standard Paper 1
(shared), so this model applies directly; Advanced Paper 2 has the same
Module A/B/C shape with different prescribed texts.

---

## Prescribed texts (English Standard, current syllabus 2019–2025)

**Machine-readable canonical vocabulary → `content/english-standard/categories.json`**
— the full controlled category list (modules, text-scopes, text-types) plus all 34
prescribed texts with stable `id`s and sub-selections. That JSON is what the Haiku
parser classifies against (emit `module` + `textScope` + `textId`/`textType`). The
list below is the human-readable mirror; keep the two in sync.

Verified from NESA source PDFs (Paper 1 Section II for Common; Paper 2 for
Modules A & B). **Lists are identical across 2019–2025** — no changes in this
range. 34 texts total (Common 14, Module A 11, Module B 9). Module C = none.
Branch-count cross-check: 2022 Common a–n=14, 2024 Mod A a–k=11, 2021 Mod B a–i=9.

### Common Module — Texts and Human Experiences (Paper 1, Sec II)
- Prose Fiction: Anthony Doerr, *All the Light We Cannot See*; Amanda Lohrey, *Vertigo*; George Orwell, *Nineteen Eighty-Four*; Favel Parrett, *Past the Shallows*
- Poetry: Rosemary Dobson, *Rosemary Dobson Collected* (Young Girl at a Window; Over the Hill; Summer's End; The Conversation; Cock Crow; Amy Caroline; Canberra Morning); Kenneth Slessor, *Selected Poems* (Wild Grapes; Gulliver; Out of Time; Vesper-Song of the Reverend Samuel Marsden; William Street; Beach Burial)
- Drama: Jane Harrison, *Rainbow's End*; Arthur Miller, *The Crucible*; William Shakespeare, *The Merchant of Venice*
- Nonfiction: Tim Winton, *The Boy Behind the Curtain* (Havoc: A Life in Accidents; Betsy; Twice on Sundays; The Wait and the Flow; In the Shadow of the Hospital; The Demon Shark; Barefoot in the Temple of Art); Malala Yousafzai & Christina Lamb, *I am Malala*
- Film: Stephen Daldry, *Billy Elliot*
- Media: Ivan O'Mahoney, *Go Back to Where You Came From* (Series 1: Eps 1–3, and The Response); Lucy Walker, *Waste Land*

### Module A — Language, Identity and Culture (Paper 2, Sec I)
- Prose Fiction: Henry Lawson, *The Penguin Henry Lawson Short Stories* (The Drover's Wife; The Union Buries Its Dead; Shooting the Moon; Our Pipes; The Loaded Dog); Andrea Levy, *Small Island*
- Poetry: Aitken, Boey & Cahill (eds), *Contemporary Asian Australian Poets* (Merlinda Bobis, This is where it begins; Miriam Wei Wei Lo, Home; Ouyang Yu, New Accents; Vuong Pham, Mother; Jaya Savige, Circular Breathing; Maureen Ten, Translucent Jade); Ali Cobby Eckermann, *Inside my Mother* (Trance; Unearth; Oombulgarri; Eyes; Leaves; Key)
- Drama: Ray Lawler, *Summer of the Seventeenth Doll*; Bernard Shaw, *Pygmalion*; Alana Valentine, *Shafana and Aunt Sarrinah*
- Nonfiction: Alice Pung, *Unpolished Gem*
- Film: Rachel Perkins, *One Night the Moon*; Rob Sitch, *The Castle*
- Media: Janet Merewether, *Reindeer in my Saami Heart*

### Module B — Close Study of Literature (Paper 2, Sec II)
- Prose Fiction: M T Anderson, *Feed*; Mark Haddon, *The Curious Incident of the Dog in the Night-time*
- Poetry: Robert Gray, *Coast Road* (Journey, the North Coast; Flames and Dangling Wire; Harbour Dusk; Byron Bay: Winter; Description of a Walk; 24 Poems); Oodgeroo Noonuccal (The Past; China … Woman; Reed Flute Cave; Entombed Warriors; Visit to Sun Yat-Sen Memorial Hall; Sunrise on Huampu River; A Lake Within a Lake)
- Drama: Scott Rankin, *Namatjira*; William Shakespeare, *A Midsummer Night's Dream*
- Nonfiction: Anna Funder, *Stasiland*
- Film: Peter Weir, *The Truman Show*
- Media: Simon Nasht, *Frank Hurley: The Man Who Made History*

### Module C — The Craft of Writing
No prescribed texts. Composition (imaginative/discursive/persuasive) + reflection,
usually from a stimulus (image/quote).
