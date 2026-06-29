---
title: "Supplementary Materials — The Denver Airport Baggage System"
module: SEE
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Denver Airport baggage case study. Nothing here is spoken in the audio —
the narration points at each listing by label only. Listing 1 is the timeline; Listing 2 models the
critical-path / fallback lesson; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
Early 1990s Denver builds a brand-new airport (DIA) and decides on an extraordinarily ambitious, fully
            AUTOMATED baggage system: ~30 km of track and thousands of self-guiding cart "telecars" to
            whisk every bag across the airport with no human handlers. Hugely complex, never built at this
            scale before. Crucially, the airport's opening is planned AROUND this system finishing.
1993-94     Testing is a disaster: telecars jam, crash, and pile up; bags are mangled, misrouted, and flung
            out; clothes end up strewn across the tracks. The system cannot be made reliable in time.
1994-95     The baggage system delays the WHOLE airport's opening by about 16 months. The delay alone costs
            on the order of US$1 million PER DAY; the system itself runs massively over budget (hundreds of
            millions). The airport finally opens in 1995 only after a conventional MANUAL backup is built.
2005        The automated system -- expensive to run and never reliable -- is abandoned entirely; the
            airport runs on conventional baggage handling. A landmark software-engineering project failure.
Causes      Over-ambitious scope; complexity badly underestimated; an unrealistic, fixed deadline; late
            requirement changes from airlines; too little time to test; and no fallback -- the risky system
            sat on the airport's critical path with nothing behind it.
```

### Listing 2 — Why one risky subsystem sank the whole project (Python, runnable)
```python
# How many months until each subsystem is ready. The airport can't open until everything REQUIRED is ready.
subsystems = {
    "terminal":                30,
    "runways":                 28,
    "manual_baggage_fallback": 30,
    "automated_baggage":       46,   # the ambitious, unproven system -- runs badly late
}

def open_month(required):
    """The project finishes when its LAST required piece is ready -- the CRITICAL PATH (the long pole)."""
    return max(required)


# PLAN A (what they did): bet the whole opening on the automated system, with NO fallback.
plan_a = open_month([subsystems["terminal"], subsystems["runways"], subsystems["automated_baggage"]])
assert plan_a == 46                      # the risky subsystem is the long pole -> it drags everything

# PLAN B: keep a conventional manual fallback so the airport does NOT depend on the risky system finishing.
plan_b = open_month([subsystems["terminal"], subsystems["runways"], subsystems["manual_baggage_fallback"]])
assert plan_b == 30                      # opens on time; the automated system can be added later, safely

assert plan_a - plan_b == 16             # ~16 months of delay came from having no fallback
print("No fallback -> opens month", plan_a, "(16 months late). With a fallback -> opens month", plan_b, ".")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
Denver's baggage system is the classic SOFTWARE-ENGINEERING-PROJECT failure: not a coding bug, but a
project-management and feasibility failure.

1  FEASIBILITY FIRST -- TECO
   Was it Technically feasible, at that scale, in that time? No -- and a TECO check (Technical, Economic,
   Cost/schedule, Operational feasibility) should have said so. Ambition outran what was achievable.
   (SEE 23-01 requirements & feasibility.)

2  SCOPE-TIME-COST: you cannot fix all three
   The scope was enormous and the deadline was fixed (the airport was being built around it), so cost and
   quality took the hit. When scope and time are locked, something has to give. (SEE 24-04 project triangle.)

3  CRITICAL PATH + A FALLBACK: don't put an unproven system on the long pole with no backup
   The whole airport's opening depended on the riskiest, most novel subsystem. With a manual fallback in
   parallel, the airport could have opened on time and added automation later. (SEE 24-04 critical path;
   Listing 2.)

4  CHOOSE THE IMPLEMENTATION METHOD FOR THE RISK -- DiP-PP
   They effectively went DIRECT / big-bang (cut straight to the new system, airport-wide, no fallback) on
   something brand-new and unproven -- the riskiest possible choice. A PILOT (one concourse first) or
   PARALLEL run (manual + automated together) would have contained the risk. DiP-PP = Direct, Phased,
   Parallel, Pilot. (SEE 23-03 implementation methods.)

ALSO: late requirement changes + too little testing time. CASHES INTO: SEE 23-01 (feasibility/boundaries),
23-03 (implementation method/direct-risk). Companion to case_the_healthcare_gov_launch and case_the_knight_capital_glitch.
```
