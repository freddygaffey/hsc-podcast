# _plans/ — per-module episode plans

This folder holds the **plans that drive script generation** — one file per module,
named `<MODULE>-PODCAST_PLAN.md`.

They are the **output of** `../pipeline/GENERATE_PLAN_PROMPT.md` and the **input to**
`../pipeline/GENERATE_EPISODE_PROMPT.md`. A plan gives each episode its *seeds*
(dot-points, recaps, interleaving, mnemonics, worked examples); `../pipeline/STYLE.md` gives the
*form*; `../pipeline/AUTHORING.md` gives the *files*.

## Modules

Module codes, names and year split come from `../subject.json` (`groupNames` / `yearMap`).

**Year 11 (Preliminary):**

- `P1-PODCAST_PLAN.md` — **P1 Design Fundamentals** (P1.1) — 6 episodes. Design theory & practice,
  the work of designers, the design process (DRIPER), the 11 factors affecting design.
- `P2-PODCAST_PLAN.md` — **P2 Design Processes & Production** (P2.1/P2.2/P4.2/P6.1/P6.2) —
  7 episodes. Settings, scales of production, materials/tools, WHS, environmental & social issues,
  computer-based technologies.
- `P3-PODCAST_PLAN.md` — **P3 Management, Communication & Research** (P3.1/P4.1/P4.3/P5.1/P5.2/P5.3)
  — 9 episodes. Creativity, design teams, briefs, market & user research, communication, project
  management, evaluation.

**Year 12 (HSC):**

- `H1-PODCAST_PLAN.md` — **H1 Designing & Producing / Major Design Project**
  (H1.1/H1.2/H4.1/H4.2/H4.3/H5.1/H5.2/H6.1) — 12 episodes (incl. a mid-module review). Proposal,
  factors & success/failure, designers' practice, research, resources & safety, industrial
  practice, management (ATF), communication, evaluation.
- `H2-PODCAST_PLAN.md` — **H2 Innovation & Emerging Technologies** (H2.1/H2.2/H3.1/H3.2/H6.2) —
  9 episodes. The written-exam module: TEMPLE success factors, entrepreneurship, trends, history/
  culture, ethics, creativity, emerging tech, and the Section III extended-response engine.

**Case Studies:**

- `CASE-PODCAST_PLAN.md` — **CASE Case Studies** — 5 narrative episodes (Flow Hive + four flops).
  Story-first; cashed in by the H1/H2/H3 teaching episodes. See its own master list.

## Conventions (all modules)

- **Episode = one syllabus section = one folder.** `content/dt/<MODULE-LL-Title>/` holds
  `script.md`, `supplementary.md`, `quiz.json`, and the generated `<voice>.m4a` files. The module
  code is in the folder name (e.g. `P1-04-...`); the section number is the `lesson:` in frontmatter.
- **Oversized sections split** into `-Part-1` / `-Part-2` (same lesson number) — e.g.
  `P1-04`/`P1-05` for the 11 factors.
- **Module reviews** (`STYLE.md` §5.3): `XX-99-Module-Review-...` — one per module, plus a
  mid-module review where a block exceeds ~8 episodes (H1 has `H1-06-Mid-Module-Review-...`).
- **Case studies** (`STYLE.md` §5.7): `case_...`, story-first, tied in later by teaching episodes.
- **Marquee mnemonics** — listed below; keep the wording **identical everywhere** they recur so
  the spaced-repetition recaps line up across episodes.

## Marquee mnemonics (the master list — reuse wording verbatim, STYLE §5.4)

| Mnemonic | What it encodes | Outcome | First taught |
|---|---|---|---|
| **FFA EQ NEW LOAd** | The 11 factors affecting design (Appropriateness, Needs, Function, Aesthetics, Finance, Ergonomics, WHS, Quality, Environmental consequences, Obsolescence, Life cycle analysis) | P1.1 / H1.1 | P1-04, reused H1-03 & CASE |
| **DRIPER** | Design process cycle: Define → Research → Ideate → Produce → Evaluate → Refine | P1.1 | P1-03, reused everywhere |
| **DCIC** | Production settings: Domestic → Community → Industrial → Commercial | P2.1 | P2-01, reused H1-08 |
| **JBM** | Scales of production: Job (one-off) → Batch → Mass | P6.1 | P2-02, reused H1-08 |
| **CPA FACE** | Material-selection criteria: Characteristics, Properties, Availability, Function, Appearance, Cost, Environmental | P4.2 | P2-03, reused H1-07 |
| **ES-EAP** | Hierarchy of control: Eliminate, Substitute, Engineering, Administrative, PPE | P4.2 | P2-04, reused H1-07 |
| **PC SCIE** | Environmental & social issues: Personal values, Cultural beliefs, Sustainability, Safety/health, Community needs, Individual needs, Equity | P2.2 | P2-05 |
| **MR SCP** | Computer-based tech applications: Modelling, Research, Simulation/graphics, Communication, Presentation | P6.2 | P2-06 |
| **SCAMPER** | Ideation: Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse | P3.1 | P3-01, reused H2-06 |
| **QISOTS** | Research methods: Questionnaires, Interviews, Surveys, Observation, Tests/experiments, Statistical analysis (over qual/quant) | P5.3 | P3-05, reused H1-05/10 |
| **NCC / NICe** | Brief contents (Need, Constraints, Criteria) → MDP proposal (Need, areas of Investigation, Criteria) | P4.1 / H4.1 | P3-03 → H1-02 |
| **RV GS-CDT D** | Factors affecting management (Resources, Values, Goals, Standards, Costs/benefits, Decisions, Tasks, Documentation) | P5.1 | P3-07, reused H1-09 |
| **SMMR / V-WGVA / CAE** | Communication process (Sender, Message, Medium, Receiver) / forms (Verbal, Written, Graphical, Visual, Audio) / criteria (Clarity, Appropriateness, Ease) | P5.2 | P3-06, reused H1-10 |
| **BMA / ISE** | Evaluation timing (Before, Mid, After) / impact levels (Individual, Society, Environment) | P4.3 / H4.3 | P3-08 → H1-11 |
| **ATF** | MDP management plans: Action, Time, Finance | H5.1 | H1-09 |
| **SEE / SPPC** | Resource-selection factors (Safety, Ethical, Environmental) / industrial practices (Safe work, Production techniques, Process selection, Collaborative teams) | H4.2 / H6.1 | H1-07 / H1-08 |
| **TEMPLE** | 6 factors affecting innovation success: Timing, Emerging tech, Marketing, Political, Legal/economic, Era | H3.1 | H2-01, reused CASE |
| **SPEEG / C-CWT** | Trend drivers (Social, Political, Economic, Environmental, Global) / historical-cultural influences (Change/trends, Cultural diversity, Work, Technological change) | H2.1 | H2-03 / H2-04 |
| **SIRRI** | Ethical/environmental issues: Sustainable tech, IP, Rights/responsibilities of designer, Responsibilities to society, Impact on Australian society | H2.2 | H2-05 |
| **LESEE** | Emerging-tech implications: Legal, Ethical, Social, Economic, Ecological | H6.2 | H2-07 |
| **GASP-I** | Agencies of innovation: Government, Associations/standards, Sponsors/funders, Patent/IP offices, Industry | H3.1 | H2-02 |

> **The headline exam trap:** don't confuse **FFA EQ NEW LOAd** (11 factors affecting *design*,
> H1.1) with **TEMPLE** (6 factors affecting *innovation success*, H3.1). Both are examined, often
> in the same paper.

## Case-study master list (story · file · cashed in by)

(Full version in `CASE-PODCAST_PLAN.md`.)

| Story | File | Lessons that point back |
|---|---|---|
| Flow Hive (success) | `case_flow_hive` | H1-03, H2-01, H2-02, H2-05, H2-06, H2-07; P3-04 |
| Ford Edsel (failure) | `case_ford_edsel` | H1-03, H2-01; P3-04 (market research misread) |
| Apple Newton (noble failure) | `case_apple_newton` | H1-03, H2-01, H2-06, H2-07 |
| Microsoft Zune (failure) | `case_microsoft_zune` | H1-03, H2-01, H2-03 (trend timing) |
| Central Park Sydney (flawed) | `case_central_park_sydney` | H1-03, H1-11, P1-05, P2-05, H2-05 |

## Status

- **Plans: COMPLETE** — P1, P2, P3, H1, H2 and CASE all written.
- **Built: _none yet_** — next run `../pipeline/GENERATE_EPISODE_PROMPT.md` to turn plan seeds into
  `script.md` per episode (and start the voice daemon in parallel).
- **Reference episode:** `../_example-episode/` (the worked two-file format + quiz).
