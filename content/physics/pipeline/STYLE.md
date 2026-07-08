# Physics — style overrides

Physics follows the shared conventions in
[`_template-subject/pipeline/STYLE.md`](../../_template-subject/pipeline/STYLE.md) and
`GENERATE_EPISODE_PROMPT.md`, with the physics-specific rules below. Where they conflict,
this file wins for physics.

## Case studies (the experiments deck)

Source of truth is the curated doc `content/physics/sources/experiments/physics-experiments.md`
(a real HSC student's work, star-rated for HSC relevance). Treat it as authoritative — don't
"improve" its physics or invent detail it doesn't contain.

- **`supplementary.md` is the doc, near-verbatim.** It's sliced straight from the source
  (`tools/build_physics_cases.py`) with the experiment's images inline, in context — not
  clustered at the top. Do **not** paraphrase or re-order it; it is the faithful reference.
- **`script.md` is the narrated story** built *from* that supplementary — gripping, human,
  the drama and the "why it mattered." Follow §5.7 (case study): one real story, **no**
  spaced-rep opener, **no** forced interleaving, **no** exam framing during the story.

### Narrative style — Veritasium (required)
Write these like a **Veritasium video**, per the shared
[`CASE_STUDY_LESSON_PLAN.md`](../../_template-subject/pipeline/CASE_STUDY_LESSON_PLAN.md) —
that spec is the detailed arc; follow it. In short:
- **Cold-open hook (≤60s):** a question people get wrong, a paradox, or a moment where
  everything's at stake. Never open with "today we'll learn about X."
- **Lead with the mystery, person, or crisis; the physics is the *payoff*, not the premise.**
- **Set the stage** (what people believed and why they were wrong) → build the tension →
  the experiment → the payoff and why it mattered.
- It only has to be **genuinely gripping** — vivid, well-paced, a real hook-and-payoff arc.

Difference from the shared guide: physics case studies are **tight Veritasium *shorts*, not
25–35 min documentaries** — hold the same craft and arc, but at the star-scaled length below
(the source is only 2–4 pages). Same tension and payoff, less runtime.

### Length — scales with the star rating (override)
Case studies are **shorter** than the shared ~4,500–6,500 (§ length), and **length scales with
the doc's star rating** — more stars = more HSC-important = longer and more detailed:

| Priority | Target | Words (~150 wpm) |
|---|---|---|
| ⭐⭐⭐ | ~13–16 min | ~2,000–2,500 |
| ⭐⭐ | ~9–12 min | ~1,400–1,900 |
| ⭐ | ~5–8 min | ~800–1,300 |

These are guides, not fences — the source is only 2–4 pages, so **tell it tight and interesting,
don't pad to hit a number.** A ⭐ thought-experiment or derivation that lands in 6 minutes is a
6-minute episode. Depth comes from the story landing and from the extra method/significance a
3-star experiment earns, not from length for its own sake.

### Opening & framing
- **Open by naming the module** it belongs to, e.g. *"This is part of Module 8, From the
  Universe to the Atom…"* — so the listener is oriented before the story starts.
- The episode **title carries its star priority** (e.g. `⭐⭐⭐ Geiger–Marsden "gold foil"
  experiment`), from the doc's rating (more stars = more HSC-important).
- Close with a one-line pointer back to the related teaching episode (the "hook" link).
