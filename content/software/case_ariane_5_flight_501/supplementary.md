---
title: "Supplementary Materials — Ariane 5 Flight 501"
module: OOP11
year: 11
lesson: "case-study"
script: script.md
---

# Supplementary Materials

Read-along reference for the Ariane 5 Flight 501 episode. Nothing here is spoken in the
audio — it is the reading companion for the story. The code is a simplified, illustrative
reconstruction of the fatal data conversion, not the original Ada source from the flight.

### Listing 1 — The unprotected 64-bit-to-16-bit conversion, and where the guard belonged
```python
# Simplified illustration of the Ariane 5 navigation fault (NOT the real flight code).
# A 64-bit float holding horizontal velocity (BH) is squeezed into a 16-bit signed int.

INT16_MAX =  32767     # largest value a 16-bit SIGNED integer can hold
INT16_MIN = -32768     # smallest value a 16-bit SIGNED integer can hold

def to_int16_UNGUARDED(value_64bit_float: float) -> int:
    # What actually shipped: no range check, because on Ariane 4 this value
    # was PROVEN never to exceed the 16-bit range, so the guard was omitted
    # (also to save CPU time under tight performance budgets).
    return int(value_64bit_float)          # on Ariane 5: OVERFLOW / operand error → unhandled → SRI shuts down

def to_int16_GUARDED(value_64bit_float: float) -> int:
    # What SHOULD have been there once the code was reused in a new rocket:
    n = int(value_64bit_float)
    if n > INT16_MAX or n < INT16_MIN:     # the boundary check that was missing
        # Handle gracefully: clamp, flag the condition, or raise a HANDLED exception —
        # anything except blindly converting and letting the unit die.
        raise OverflowError(f"BH={n} exceeds 16-bit range; cannot represent")
    return n

# On Ariane 4: horizontal velocity stayed small → fit every time → no fault ever seen.
# On Ariane 5: faster, steeper climb → BH ≈ 5x larger → exceeded 32767 → overflow at ~37 s.
# Both the PRIMARY and BACKUP units ran this SAME unguarded code → both failed identically.
```

### Listing 2 — Timeline of Flight 501 (4 June 1996)
```text
~10 years / ~US$7B   Ariane 5 developed; navigation software REUSED from the proven Ariane 4.
T  =  0 s            Lift-off from Kourou, French Guiana. Maiden flight (Flight 501).
                     Payload: 4x Cluster science satellites (~US$370M, irreplaceable).
T  ~  0-36 s         Flight nominal. Telemetry normal. Both navigation units (SRI) running.
T  ~  37 s           Ariane 5's higher horizontal velocity (BH) overflows the 16-bit
                     conversion. Operand error is UNHANDLED. Backup SRI had already failed
                     the SAME way milliseconds earlier (identical code, identical data).
T  ~  37 s           Failed unit puts DIAGNOSTIC data on the bus; guidance computer reads
                     it as FLIGHT data → commands nozzles hard over to "correct".
T  ~  37 s           Rocket slews sideways at supersonic speed; aerodynamic loads begin
                     to break the vehicle apart; boosters separate.
T  ~  39 s           Automatic self-destruct fires. Vehicle and payload destroyed.
Aftermath           No injuries (debris fell on marshland). Inquiry Board (Lions report)
                     finds: reused component, never re-tested against Ariane 5's profile.
```

### Listing 3 — "What would have caught it": a reuse re-test checklist (NESA pseudocode)
```text
BEGIN ReverifyReusedComponent
    GET component                          // e.g. the Ariane 4 navigation software
    GET newEnvironment                     // e.g. the Ariane 5 flight profile

    // 1. SURFACE THE BURIED ASSUMPTIONS
    FOR each assumption IN component.testedAssumptions
        IF assumption NOT valid IN newEnvironment THEN
            FLAG assumption AS at-risk     // e.g. "BH always fits in 16 bits" — FALSE on Ariane 5
        ENDIF
    NEXT assumption

    // 2. INTEGRATION / REGRESSION TEST IN THE REAL NEW CONTEXT
    realData ← realistic data FROM newEnvironment   // actual Ariane 5 trajectory, not Ariane 4's
    RUN component WITH realData INSIDE newSystem
    IF behaviour differs FROM expected THEN
        REJECT reuse UNTIL fixed
    ENDIF

    // 3. WHITE / GREY-BOX BOUNDARY TEST OF THE CHANGED PATHS
    FOR each conversion OR narrowing OF a data type IN component
        maxIn ← largest value that can reach this line IN newEnvironment
        IF maxIn > destinationType.MAX OR minIn < destinationType.MIN THEN
            FAIL "overflow possible — add a range check / handle the exception"
        ENDIF
        TEST value AT boundary, JUST BELOW, AND JUST ABOVE   // boundaries are where bugs hide
    NEXT conversion

    // 4. CHECK REDUNDANCY IS REAL, NOT JUST DUPLICATED
    IF primary AND backup RUN identical code THEN
        WARN "shared flaw will fail both at once — redundancy != safety"
    ENDIF
END ReverifyReusedComponent
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| CPU | Central Processing Unit | The processor that executes program instructions |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
