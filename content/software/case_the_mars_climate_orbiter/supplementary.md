---
title: "Supplementary Materials — The Mars Climate Orbiter"
module: OOP11
year: 11
lesson: "case-study"
script: script.md
---

# Supplementary Materials

Read-along reference for the Mars Climate Orbiter episode. Nothing here is spoken in the
audio — it's the companion to the narration. Every listing is referenced from the script
by label.

### Listing 1 — Timeline of the mission and the loss
```text
1998-12-11  Mars Climate Orbiter launched (~US$125M mission)
1998–1999   9.5-month cruise; thrusters fire periodically to bleed off reaction-wheel
            spin (angular-momentum "desaturation" / "des-at"), each firing nudging the craft
            Ground software (Lockheed Martin, spacecraft side) reports thruster impulse
            in IMPERIAL pound-force-seconds (lbf·s)
            Navigation software (NASA/JPL, nav side) reads it as METRIC newton-seconds (N·s)
            Conversion factor never applied: 1 lbf·s ≈ 4.45 N·s
1999 (late) Navigators see a persistent trajectory discrepancy; concern raised but never
            escalated to a formal "halt the manoeuvre" decision
1999-09-23  Mars Orbit Insertion. Planned closest approach ~140–150 km;
            survival floor ~80 km. Actual closest approach ~57 km — far too low.
            Craft passes behind Mars, loses signal ~30 s early, never re-acquired.
            Lost in the upper atmosphere from aerodynamic stress / heating.
            Mishap Investigation Board root cause: failure to use metric units in a
            ground-software file, i.e. an unspecified, unchecked interface contract.
```

### Listing 2 — The defect: one value, two meanings across the interface
```python
# Illustration of the unit-mismatch interface (NOT NASA's real code).
# Each module is internally correct. The defect lives in the SEAM between them:
# the contract never pinned down the units, so the same number means two things.

# --- Lockheed Martin: spacecraft module (PRODUCER) ---
def report_thruster_impulse():
    impulse = 4.45          # value is in POUND-FORCE-SECONDS (imperial)
    return impulse          # ...but the unit is not carried with the number

# --- NASA / JPL: navigation module (CONSUMER) ---
def apply_thruster_impulse(impulse):
    # silently ASSUMES the number arrives in NEWTON-SECONDS (metric)
    update_trajectory(impulse)   # off by a factor of ~4.45 every single firing

# Both functions run flawlessly. Neither has a "bug".
# The system is wrong because the INTERFACE CONTRACT (the units) was never agreed.
# A complete signature would have made the unit part of the promise, e.g.:
#     def report_thruster_impulse() -> "newton_seconds": ...
```

### Listing 3 — The broken handoff as NESA-style pseudocode
```text
BEGIN ThrusterImpulseHandoff
    // Producer module (spacecraft software)
    impulse ← total push from thruster firing      // measured in pound-force-seconds
    SEND impulse TO navigation software             // unit NOT sent with the value

    // Consumer module (navigation software)
    RECEIVE impulse FROM spacecraft software
    // CONTRACT GAP: navigation assumes newton-seconds, no check, no conversion
    IF units of impulse ARE NOT confirmed metric THEN
        // this check was never written — so the error passed silently
        trajectory ← WRONG by factor of 4.45
    ENDIF
    UPDATE trajectory USING impulse
END ThrusterImpulseHandoff
```

### Listing 4 — "What would have caught it": an interface-contract checklist
```text
Any ONE of these, done properly, would have saved the orbiter:

[ ] DOCUMENT the interface contract: for every value crossing a module boundary,
    state its name, type, UNITS, valid range, and assumptions — not just "a number".
[ ] MAKE UNITS PART OF THE SIGNATURE: encode the unit in the name / type / docstring
    so a reviewer (or the type system) can see a mismatch.
[ ] INTEGRATION-TEST THE TWO MODULES TOGETHER (subsystem testing): feed a known push
    in on one side and assert the expected movement out the other. The factor-of-4.45
    error is invisible to unit tests and screams the instant the modules are wired up.
[ ] SANITY-CHECK AT THE BOUNDARY: range/plausibility checks on incoming values reject
    impulses that are ~4.45x off.
[ ] ESCALATION PROCESS: give engineers a formal channel to HALT a critical manoeuvre
    when reality and prediction disagree — don't rely on informal "bad feelings".
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| JPL | Jet Propulsion Laboratory | NASA's centre for robotic space missions (Mars Climate Orbiter case study) |
| NASA | National Aeronautics and Space Administration | The US space agency (referenced in several engineering-failure case studies) |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
