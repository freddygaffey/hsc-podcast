# Authoring an Episode (read this if you are generating episodes)

This is the **instruction sheet for whoever — human or AI — writes a new episode.** It
tells you the exact files to create and gives you fill-in templates. Follow it literally
and the TTS pipeline and viewer will both just work.

- `STYLE.md` — *how to write the spoken words* (tone, structure, exam value).
- `SUPPLEMENTARY.md` — *the full format contract and the why* behind everything here.
- **This file** — *the minimum you must produce, as a copyable recipe.*

---

## What you produce: exactly TWO text files

To author an episode you create **one folder** and put **two Markdown files** in it:

```
content/<EPISODE-KEY>/
    script.md          ← you write this
    supplementary.md   ← you write this
```

**You do NOT create the `.m4a` audio files.** The audio is generated from `script.md`
by `generate_all_voices.sh`, which drops one `<voice>.m4a` into the folder per voice.
Never invent, reference, or hand-author audio files. Your entire job is the two `.md`
files above.

### The folder name (`<EPISODE-KEY>`)

`MODULE-LL-Topic-Title` (or `case_descriptive_title` for a case study). See `STYLE.md`
§8 for the module codes and rules. Examples:

```
content/M7-05-The-Photoelectric-Effect/
content/case_ligo_detects_gravitational_waves/
```

The folder name has no extension and must match across the whole episode.

---

## File 1 — `script.md` (the spoken script)

Frontmatter, then the spoken body. **No equation blocks, no tables, no appendix in this
file** — anything you put here is read aloud by the TTS engine.

````markdown
---
title: "The Photoelectric Effect"
module: M7
lesson: "5"
kind: lesson                       # lesson | case-study | module-review
supplementary: supplementary.md    # always this literal value
---

NARRATOR: The entire spoken script goes here, as natural prose. Plain paragraphs
are read in the narrator voice. Follow STYLE.md for tone and structure.

QUESTION: An exam-style question, asked in the second voice.

NARRATOR: ...and the narrator continues. Reference supplementary material only by
its label, e.g. "the full derivation is in Listing 1" — never "as you can see
here", because the listener may not be looking.
````

Rules for `script.md`:

- **Frontmatter is required** with at least `title`, `module`, `lesson`, `kind`, and
  `supplementary: supplementary.md`.
- The body uses `NARRATOR:` / `QUESTION:` speaker labels (`STYLE.md` §3.1). Text before
  any label is the narrator. `[pause]` on its own line is a silent beat.
- It must be **self-contained and learnable audio-only** — someone who only listens, and
  never looks at the screen, must still understand the whole lesson.
- **No fenced blocks, no Markdown tables, no `## Appendix`.** Those belong in
  `supplementary.md`. If the engine sees them it will read them aloud.

---

## File 2 — `supplementary.md` (the read-along reference)

Frontmatter, a `# Supplementary Materials` heading, then the labelled listings. This
file is **shown to the user but never spoken**.

Physics supplementary material covers: key equations, step-by-step derivations, worked
numerical solutions, and small data tables. There is no code in this subject.

````markdown
---
title: "Supplementary Materials — The Photoelectric Effect"
module: M7
lesson: "5"
script: script.md                  # always this literal value
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing
here is spoken in the audio — it's the read-along reference.

### Listing 1 — Photoelectric equation, worked example
```text
K_max = hf − φ

f = 1.2 × 10^15 Hz,  φ = 2.3 eV = 3.68 × 10^-19 J

hf = (6.63 × 10^-34)(1.2 × 10^15) = 7.96 × 10^-19 J

K_max = 7.96 × 10^-19 − 3.68 × 10^-19 = 4.28 × 10^-19 J  (≈ 2.67 eV)
```

### Listing 2 — Work functions of selected metals
| Metal    | Work function φ (eV) |
|----------|----------------------|
| Caesium  | 2.1                  |
| Sodium   | 2.3                  |
| Zinc     | 4.3                  |
| Platinum | 5.7                  |
````

Rules for `supplementary.md`:

- **Frontmatter is required** with at least `title`, `module`, `lesson`, and
  `script: script.md`. Keep `module`/`lesson` identical to `script.md`.
- Every item is a `### Listing N — short description` heading followed by **one** fenced
  block (or one Markdown table). Number listings `1, 2, 3…` in the order the narration
  references them.
- **Equations, derivations, and worked numerical solutions** go in a ` ```text ` fence,
  one step per line so the working is easy to follow (`SUPPLEMENTARY.md` §3).
- **Small data tables** are written as plain Markdown tables.
- The narration references each listing by label and never depends on seeing it.
- **No images, diagrams, or binary assets.** Text only — describe any figure in words in
  the narration.

---

## Final checklist (every episode, every time)

- [ ] One folder `content/<EPISODE-KEY>/` named per `STYLE.md` §8.
- [ ] It contains **exactly two files you wrote**: `script.md` and `supplementary.md`.
- [ ] You did **not** create any `.m4a` file — the pipeline does that.
- [ ] `script.md`: required frontmatter incl. `supplementary: supplementary.md`;
      `NARRATOR:`/`QUESTION:` body; self-contained audio-only; **no fenced blocks/tables/appendix**.
- [ ] `supplementary.md`: required frontmatter incl. `script: script.md`;
      `# Supplementary Materials` heading; `### Listing N —` items, each one fenced block
      or Markdown table.
- [ ] Equations/derivations are in a `text` fence; data is in a Markdown table.
- [ ] The narration references each listing by label and never depends on seeing it.
- [ ] Work committed to git in a small, focused commit (commit **per episode**).

Follow the templates above — there are no example episodes in `content/` yet (clean
slate), so name your first one per `STYLE.md` §8.
