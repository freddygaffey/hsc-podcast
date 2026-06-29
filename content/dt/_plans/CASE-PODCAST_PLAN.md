# CASE — Case Studies podcast plan

The case studies are the **stories** of the Design & Technology course. They're not where the
syllabus content is taught — they're where it's made *memorable*. Each one is a self-contained
narrative episode (STYLE §5.7): one real product, told like a documentary — the people, the
stakes, what went right or wrong, and why. The syllabus tie-in happens *later*, when a teaching
episode points back ("remember the Edsel? that's what happens when market research is read
wrong"). So these episodes only have to do one thing: **be genuinely interesting and stick.**

This subject leans hard on case studies because the HSC does. The *Innovation and Emerging
Technologies* section (Section I + the extended response) is, in practice, "talk about a real
innovation using the syllabus factors." A student who can tell the Flow Hive story cold, and
contrast it with a famous flop, walks into that exam with a ready-made answer.

## Source material

All five come from the course PowerPoints, now in `resources/extracted/notes/`:

- `12dt-flowhive-casestudy-1.md` — the Flow Hive (the **success / innovation** case study).
- `copy-of-12dt-case-study-failed-design-1.md` — four **failed / flawed designs**: Ford Edsel,
  Apple Newton, Microsoft Zune, Central Park (Sydney).

## The episodes (CASE module)

One story per episode. Kept tighter than the 25–35 min Veritasium ideal — this is a lighter
subject, so aim **~8–15 minutes** each: a real arc, no padding.

| Folder | Story | Verdict | Cashes in later at |
|---|---|---|---|
| `case_flow_hive` | Two beekeepers reinvent honey harvesting; crowdfunding record | **Success** | H3.1 success factors, H3.2 creativity, H6.2 emerging tech, H2.2 ethics/environment |
| `case_ford_edsel` | Ford's $250M "sure thing" car flops in 3 years | **Failure** | H1.1 factors / success & failure, H2.1 timing & trends |
| `case_apple_newton` | Apple's PDA — right idea, wrong decade | **Noble failure** | H1.1 success & failure, H6.2 emerging tech, H3.1 timing |
| `case_microsoft_zune` | Microsoft's iPod-killer that nobody bought | **Failure** | H1.1 factors, H2.1 trends, design process (marketing) |
| `case_central_park_sydney` | Award-winning green building that under-delivers | **Mixed / flawed** | H1.1 factors, H2.2 sustainability, life cycle analysis |

The success-vs-failure pairing is deliberate: the HSC's favourite question is "what makes a
design succeed or fail?" Five stories give the student a flop for every factor and one triumph
to anchor the lot.

## How to teach them engagingly (the narrative recipe)

Each script follows the same documentary beats (no headings read aloud):

1. **Cold open** — drop straight into the most gripping moment (the crowd at the Edsel launch;
   the $2 million raised in a day; Steve Jobs waving his ten fingers — "God gave us ten
   styluses"). Hook first, context second.
2. **The people & the problem** — who made it, what need they were chasing. Stories are
   remembered through people, not specs.
3. **The build** — the prototypes, the breakthroughs, the decisions. The Flow Hive's "split the
   cells vertically" moment; the Edsel's secrecy marketing.
4. **The turn** — the launch and what actually happened. Where the money/honey/hype met reality.
5. **The autopsy** — *why*, in plain language. This is where the syllabus factors hide in the
   story without being named as a checklist.
6. **The legacy / payoff** — what it left behind (the Newton's ARM chip → every smartphone).
7. **One-line cliff-hanger to the syllabus** — a single sentence that flags "a later lesson
   will pull the factors out of this" without breaking the spell.

Keep the syllabus vocabulary *out* of the narration body — name the factors only in the
`supplementary.md` "what to take into the exam" appendix, so the story stays a story.

## The factors, recorded once (reuse this exact wording everywhere)

These two lists are what the case studies illustrate. Coin the mnemonic **once here**, reuse it
identically in every teaching episode and recap (STYLE §5.4).

**The 11 factors affecting design (H1.1) — mnemonic "FFA EQ NEW LOAd":**
the eleven the syllabus lists are **Appropriateness of the solution, Needs, Function,
Aesthetics, Finance, Ergonomics, Work health & safety, Quality, Short- & long-term
environmental consequences, Obsolescence, Life cycle analysis.** Teach the memory hook as a
short story: *a design has to do its job (Function, Needs, Appropriateness), look and feel right
(Aesthetics, Ergonomics), be affordable and safe (Finance, WHS), be well made (Quality), and not
wreck the planet across its life (Environmental, Obsolescence, Life cycle analysis).* The Failed
Design deck opens with "there are 11 — write them down" for exactly this reason.

**The 6 factors affecting the success of an innovation (H3.1) — mnemonic "TEMPLE":**
- **T** — **Timing** (the Flow Hive landed in the middle of the "save the bees" moment)
- **E** — **Emerging/available technologies** (3D printing & injection moulding made it possible)
- **M** — **Marketing strategies** (crowdfunding video, 200k Facebook followers)
- **P** — **Political factors** (government innovation support — or, for Flow, the lack of it)
- **L** — **Legal & economic factors** (the patent filed *before* crowdfunding; IP vs. copycats)
- **E** — **Era: historical & cultural influences** (tradition of smoking bees vs. a new way)

> "An innovation succeeds inside a **TEMPLE**." Every case study is graded against these six.

## Case-study master list (story · file · cashed in by)

| Story | File | Lessons that point back |
|---|---|---|
| Flow Hive (success) | `case_flow_hive` | H3.1, H3.2, H6.2, H2.2 |
| Ford Edsel (failure) | `case_ford_edsel` | H1.1, H2.1 |
| Apple Newton (failure) | `case_apple_newton` | H1.1, H6.2, H3.1 |
| Microsoft Zune (failure) | `case_microsoft_zune` | H1.1, H2.1 |
| Central Park Sydney (flawed) | `case_central_park_sydney` | H1.1, H2.2 |

## Recommended production order

1. `case_flow_hive` — the flagship success; the one every exam answer can lean on.
2. `case_ford_edsel` — the classic flop; richest factors-affecting-design story.
3. `case_apple_newton` — "too early" failure with a great legacy twist.
4. `case_microsoft_zune` — design-process / marketing failure.
5. `case_central_park_sydney` — local, sustainability-flavoured, "looks green but isn't" twist.
