---
title: "Supplementary Materials — Module Summary: Software Engineering Project"
module: SEE
year: 12
lesson: "23–26"
script: script.md
---

# Supplementary Materials

The one-page revision references for the whole Software Engineering Project module. Nothing
here is spoken in the audio — it's the read-along sheet. Listing 1 is the master mnemonic
table; Listing 2 is the key-terms checklist by topic.

### Listing 1 — Master mnemonic table (every SEE mnemonic + full expansion)
```text
EXAM-DUMP MARQUEE HOOKS (write these first):
  DiP-PP  ·  "Waterfall Falls once; Agile Goes around"  ·  Scope-Time-Cost  ·  I-F-N  ·  C-E-R

CH 23 — DEFINING & IDEATING
  FUN vs PERF        = Functional (what it does) vs non-functional / Performance (how well)
  "measurable, testable, with acceptance criteria"  ·  "boundaries stop scope creep"
  TECO               = feasibility: Technical, Economic, Cost-and-schedule, Operational
  B-M-S              = ideation: Brainstorm, Mind-map, Storyboard
  C-T-I-M            = build-toolkit: Code generation, Testing+debugging, Installation, Maintenance
  DiP-PP             = implementation methods: Direct (cheap/fast/no fallback), Phased
                       (piece-at-a-time), Parallel (both at once = safe but costly), Pilot
                       (small group first).  "Direct is cheap and risky; Parallel is safe and expensive."

CH 24 — PLANNING & MANAGING
  "Waterfall Falls once"  = single sequential pass, plan up front, stable requirements
  "Agile Goes around"     = iterative sprints, evolving requirements, working software each loop
  P-S-R-R            = Agile ceremonies: Plan, Standup, Review (product), Retro (process)
                       (work = user stories: "as a [user], I want [x], so that [benefit]")
  "WAgile = Waterfall gates + Agile sprints"  ·  "plan big, build small"
  Scope-Time-Cost    = the project triangle (quality in the middle; fix two, the third gives)
  "critical path = the longest dependent chain = zero slack" (a slip there slips the whole project)
  I-F-N              = client communication: Involve(+empower), enable Feedback, Negotiate
  PABT               = ethical areas: Privacy, Accessibility, Bias, Transparency
  3C                 = quality assurance: Criteria, Continual checking, Compliance
  C-U-P-S            = quality criteria: Correctness, Usability, Performance, Security
  "QA prevents; testing detects"

CH 25 — BUILDING
  REFF               = why build incrementally: Risk reduction, Early feedback, Flexibility,
                       Frequent value
  S-R-I              = quality while building: Standards, Review, continuous Integration
  T-B-E-D            = presentation audiences: Technical, Business, End-users, Decision-makers
  P-S-D-B-N          = presentation arc: Problem, Solution, Demo, Benefits, Next steps
  T-E-I-S            = back-end concerns ("the back end TEASEs the front end"): Technology,
                       Error handling, Interfacing, Security
  R-C-B-M-T          = version-control concepts: Repository, Commit, Branch, Merge, Tag
  3-2-1              = backup rule: 3 copies, on 2 media, 1 off-site
  "Major breaks, Minor adds, Patch fixes"  = semantic versioning
  T-R-P              = blocker types: Technical, Resource, Process
  S-P-O              = help ladder: Self-search, Peers, Outsource/escalate
  S-W-M-P            = prototype fidelity ladder: Sketch, Wireframe, Mockup, Prototype
                       (UI quality reuses POUR + Nielsen heuristics)

CH 26 — TESTING & EVALUATING
  O-S-A-E-S ("oh-seas") = test-plan components: Objectives, Scope, Approaches, Environments, Schedule
  "Black sees nothing, White sees the code, Grey sees a bit"  = box testing methods
  path + boundary    = test-data set (every road through + the edges) [Year 11]
  "measure-optimise-measure"  = profile first, change, measure again (no guessing)
  C-S-A              = feedback handling: Collect, Synthesise, Act (prioritise on impact-vs-effort)
  C-E-R              = evaluation: Criteria, Evidence, Reflection (a judgement, not a feelings summary)

SYNTHESIS: the major project REUSES the whole course — Year 11 lifecycle/algorithms, OOP objects,
the PFW web stack, SSA security (CIA-AAA), and SA automation/ethics — inside one real build.
```

### Listing 2 — Key-terms checklist by topic
```text
[ ] 23-01 Requirements & feasibility: functional (what) vs non-functional/Performance (how well,
        e.g. speed/security/usability); measurable + testable + acceptance criteria; scope
        boundaries stop scope creep; feasibility TECO (Technical/Economic/Cost-schedule/Operational).
[ ] 23-02 Ideation & modelling: ideation B-M-S (Brainstorm/Mind-map/Storyboard); modelling tools
        (DFD, structure chart, class diagram) carried in; build-toolkit C-T-I-M; justify = name the
        tool + mechanism + why.
[ ] 23-03 Implementation methods (DiP-PP): Direct (big-bang, cheap, no fallback); Phased (gradual,
        learn as you go); Parallel (run old+new together = safety net + verify, but costly);
        Pilot (whole system to a small group first). Choose by the cost of failure.
[ ] 24-01 Waterfall: sequential, all requirements up front, no cheap going back; best for STABLE
        requirements; "Waterfall Falls once"; advantage/disadvantage = FEATURE + CONSEQUENCE.
[ ] 24-02 Agile: iterative sprints delivering working software; requirements evolve; ceremonies
        P-S-R-R (Plan/Standup/Review=product/Retro=process); user stories; "Agile Goes around".
[ ] 24-03 WAgile hybrid: Waterfall gates (governance/sign-off) + Agile sprints (the building);
        "plan big, build small"; answer = mechanism + when/how, not "combines both".
[ ] 24-04 PM tools & Gantt: Scope-Time-Cost triangle (pick two; quality suffers); Gantt = bars over
        time + dependency arrows; CRITICAL PATH = longest dependent chain = zero slack -> any slip
        slips the project.
[ ] 24-05 Social/ethical/communication: communication I-F-N (Involve+empower / Feedback / Negotiate);
        ethics PABT (Privacy / Accessibility / Bias / Transparency); negotiation = clarify ->
        assess -> options -> document.
[ ] 24-06 Quality assurance: 3C (Criteria / Continual checking / Compliance); quality criteria
        C-U-P-S (Correctness / Usability / Performance / Security); "QA prevents; testing detects".
[ ] 25-01 Building: incremental (REFF = Risk reduction / Early feedback / Flexibility / Frequent
        value); quality while building S-R-I (Standards / Review / continuous Integration).
[ ] 25-02 Presenting: audiences T-B-E-D (Technical / Business / End-users / Decision-makers); arc
        P-S-D-B-N (Problem / Solution / Demo / Benefits / Next steps); slide minimalism.
[ ] 25-03 Algorithms/docs/back end: T-E-I-S (Technology / Error handling / Interfacing / Security);
        reuses PFW request flow + SSA security (CIA-AAA, hash one-way/encrypt two-way, supply chain).
[ ] 25-04 Backup & version control: R-C-B-M-T (Repository/Commit/Branch/Merge/Tag); 3-2-1 backup
        rule; semantic versioning (Major breaks / Minor adds / Patch fixes); commit small, branch
        per feature, tag releases.
[ ] 25-05 Overcoming difficulties: blocker types T-R-P (Technical/Resource/Process); strategy ladder
        S-P-O (Self-search -> Peers -> Outsource/escalate).
[ ] 25-06 Prototype & UI: fidelity ladder S-W-M-P (Sketch/Wireframe/Mockup/Prototype); low-fidelity
        first (cheap to change); UI quality via POUR (WCAG) + Nielsen heuristics.
[ ] 26-01 Testing & optimisation: test plan O-S-A-E-S (Objectives/Scope/Approaches/Environments/
        Schedule), traced to requirements + QA criteria; box methods (Black=behaviour, White=code,
        Grey=partial); path + boundary test data; measure-optimise-measure.
[ ] 26-02 Feedback analysis: C-S-A (Collect / Synthesise / Act); prioritise on impact-vs-effort;
        watch representativeness/bias in the feedback sample.
[ ] 26-03 Evaluating: C-E-R (Criteria / Evidence / Reflection); criteria from requirements + C-U-P-S;
        evidence = actual-vs-expected test results + synthesised feedback; reflection = a justified
        judgement, not a feelings summary.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| AAA | Authentication · Authorisation · Accountability | The three access-security pillars: prove who you are, check what you may do, and keep a traceable record |
| B-M-S | Brainstorm · Mind-map · Storyboard | Ideation techniques for generating design ideas |
| C-E-R | Criteria · Evidence · Reflection | Structure for evaluating a solution against its criteria |
| C-S-A | Collect · Synthesise · Act | How to handle user feedback (prioritise by impact vs effort) |
| C-T-I-M | Code generation · Testing and debugging · Installation · Maintenance | What a build toolkit supports |
| C-U-P-S | Correctness · Usability · Performance · Security | Software quality criteria |
| CIA | Confidentiality · Integrity · Availability | The three core information-security properties (the security triad) |
| DFD | Data Flow Diagram | A model showing how data moves between processes, stores and external entities |
| DiP-PP | Direct · Phased · Parallel · Pilot | The changeover / implementation (installation) methods for deploying a new system |
| I-F-N | Involve (and empower) · Feedback · Negotiate | Principles for communicating effectively with a client during a project |
| O-S-A-E-S | Objectives · Scope · Approaches · Environments · Schedule | The components of a test plan |
| OOP | Object-Oriented Programming | A paradigm structuring software around objects that bundle data and behaviour |
| P-S-D-B-N | Problem · Solution · Demo · Benefits · Next steps | The arc of a solution presentation |
| P-S-R-R | Plan · Standup · Review (product) · Retro (process) | The Agile ceremonies |
| PABT | Privacy · Accessibility · Bias · Transparency | Checklist of the main ethical issues to weigh in an automated/AI system |
| POUR | Perceivable · Operable · Understandable · Robust | The four WCAG accessibility principles for web content |
| QA | Quality Assurance | The processes that build quality into a product, not just test for defects |
| R-C-B-M-T | Repository · Commit · Branch · Merge · Tag | Core version-control concepts |
| S-P-O | Self-search · Peers · Outsource/escalate | The help ladder for overcoming development difficulties |
| S-R-I | Standards · Review · continuous Integration | How to keep quality high while building |
| S-W-M-P | Sketch · Wireframe · Mockup · Prototype | The prototype fidelity ladder |
| T-B-E-D | Technical · Business · End-users · Decision-makers | The presentation audiences |
| T-E-I-S | Technology · Error handling · Interfacing · Security | Back-end engineering concerns |
| T-R-P | Technical · Resource · Process | Types of project blocker |
| TECO | Technical · Economic · Cost-and-schedule · Operational | The dimensions weighed in a feasibility study before committing to a project |
| UI | User Interface | The parts of a system a user directly interacts with |
| WCAG | Web Content Accessibility Guidelines | The W3C standard defining how to make web content accessible (see POUR) |
