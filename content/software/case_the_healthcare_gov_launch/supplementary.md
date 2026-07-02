---
title: "Supplementary Materials — The Healthcare.gov Launch"
module: SEE
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Healthcare.gov launch case study. Nothing here is spoken in the audio —
the narration points at each listing by label only. Listing 1 is the timeline; Listing 2 models the
load-testing failure; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
2010-13     Under the Affordable Care Act, the US government builds Healthcare.gov -- a federal website
            where millions would shop for and enrol in health insurance. It must integrate dozens of
            agencies, insurers and data sources, and is built by many separate contractors with a
            government agency (CMS) as the overwhelmed integrator. The launch date -- 1 October 2013 --
            is fixed and political: it cannot slip.
Build       Requirements are finalised late and keep changing; the schedule is squeezed; end-to-end and
            load testing are pushed to the very end -- only days before launch -- leaving no time to fix
            what the tests reveal.
1 Oct 2013  Launch. The site immediately collapses under load and errors. Of the millions who visit, almost
            no one can complete an enrolment (reportedly a literal handful on day one). A national flagship
            project fails in public.
Oct-Dec     A "tech surge" rescue team (including experienced web engineers) is brought in. They triage the
            worst problems, add capacity, fix the integration, and test under realistic load. By December
            2013 the site largely works and millions enrol.
Lesson      Not one bad line of code, but a project squeezed by a fixed deadline, with rushed requirements,
            a waterfall crunch, and no realistic load testing until it was too late.
```

### Listing 2 — Why "it passed our test" meant nothing: load testing (Python, runnable)
```python
def serve(capacity, demand):
    """A system can handle up to `capacity` concurrent users; everyone beyond that is turned away."""
    served = min(capacity, demand)
    failed = max(0, demand - capacity)
    return served, failed


CAPACITY = 1_100        # what the system was actually built/tested to handle (concurrent users)
EXPECTED = 1_000        # the modest load they planned and tested against
ACTUAL   = 250_000      # the real launch-day demand

# Tested ONLY against the hoped-for load -> it passes, and everyone feels safe.
served_test, failed_test = serve(CAPACITY, EXPECTED)
assert failed_test == 0                       # 0 failures -> "the test passed!"

# Real launch load -> catastrophe: almost everyone is turned away.
served_real, failed_real = serve(CAPACITY, ACTUAL)
assert failed_real > 0
assert served_real / ACTUAL < 0.01            # under 1% of users actually get through
print("At the tested load (", EXPECTED, "): 0 failures. At real load (", ACTUAL, "):",
      failed_real, "fail --", round(served_real / ACTUAL * 100, 2), "% served.",
      "Load-test at REAL scale, not hoped-for scale.")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
Healthcare.gov is the classic FIXED-DEADLINE + WATERFALL + NO-LOAD-TESTING project meltdown.

1  A FIXED, IMMOVABLE DEADLINE + LATE/RUSHED REQUIREMENTS = trouble
   The launch date could not move and requirements were still changing late. Feasibility (TECO --
   Technical/Economic/Cost-schedule/Operational) was never honestly reconciled with the deadline.
   (SEE 23-01 requirements & feasibility.)

2  WATERFALL UNDER A DEADLINE CRUSHES TESTING ("Waterfall Falls once")
   Waterfall does each phase once, in order, with testing near the END. When the schedule slips and the
   deadline can't, the end -- testing -- gets compressed to nothing. There was no working, integrated
   system to try until it was far too late. An iterative/Agile approach would have produced something
   testable much earlier. (SEE 24-01 waterfall vs 24-02 agile.)

3  LOAD / PERFORMANCE TESTING MUST USE REALISTIC SCALE, EARLY
   "It passed our test" is worthless if the test load isn't realistic. They tested for ~hundreds/low
   thousands; hundreds of thousands arrived. Test at REAL expected scale, and do it early enough to fix
   what you find. (SEE 26-01 testing -- including load/performance testing.)

4  INTEGRATION + SINGLE ACCOUNTABILITY
   Many contractors, no single owner accountable for the whole system end-to-end -> the pieces didn't fit
   and no one held the integration. Big projects need clear ownership and continuous integration testing.

5  EVALUATE + RECOVER -- C-E-R
   The "tech surge" recovery worked by measuring against real Criteria, gathering Evidence (real load,
   real errors), and Reflecting to prioritise fixes. Honest evaluation is how you climb out. (SEE 26-03.)

CASHES INTO: SEE 23-01 (requirements/feasibility), 24-01 (waterfall risk), 26-01 (testing/load), 26-03
(evaluation). Companion to case_the_denver_airport_baggage and case_the_knight_capital_glitch.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| C-E-R | Criteria · Evidence · Reflection | Structure for evaluating a solution against its criteria |
| CMS | Content Management System | Software for creating and managing website content without hand-coding each page |
| TECO | Technical · Economic · Cost-and-schedule · Operational | The dimensions weighed in a feasibility study before committing to a project |
