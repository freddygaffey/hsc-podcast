---
title: "Supplementary Materials — The Therac-25"
module: OOP11
year: 11
lesson: "case-study"
script: script.md
---

# Supplementary Materials

Read-along reference for the Therac-25 episode. Nothing here is spoken in the audio — it
is the engineering detail behind the story. The narration refers to each listing by label.

### Listing 1 — Timeline
```text
1976–1982   Therac-6 and Therac-20 in service. Safety enforced by HARDWARE
            interlocks: physical fuses/switches that make an unsafe beam
            configuration electrically impossible. Software bugs present but
            silently covered by the hardware — so never noticed.

~1982       AECL designs the Therac-25. Hardware interlocks REMOVED; the safety
            guarantee is moved entirely into software. Code is reused from the
            older Theracs and trusted without rigorous re-testing.

1985-06     First overdose (Marietta, Georgia). Patient seriously injured.
1985–1986   Further accidents: Ontario; Yakima, Washington; Tyler, Texas.
            Manufacturer cannot reproduce the fault and reports the machine
            cannot have overdosed anyone.

1986-03/04  Two accidents weeks apart at Tyler, Texas. Physicist Fritz Hager,
            with the operator, painstakingly reproduces the fault on demand —
            "Malfunction 54" delivered with a massive measured overdose.

1987        Final accident (Yakima). Machines investigated, modified, and
            recalled; regulators (FDA) involved.

Outcome     ≥6 massive radiation overdoses, 1985–1987. 3–4 patients died;
            others permanently injured. Now a foundational software-engineering
            case study worldwide.

Root causes 1. Safety moved hardware → software, trusting software alone.
            2. Race condition: fast (<~8 s) prescription edit corrupted the
               machine's hidden state → strong beam fired, target NOT in place.
            3. One-byte counter overflow: a safety check ran only when the
               counter == 0; when it wrapped to zero, the check was skipped.
            4. Cryptic UI ("Malfunction 54") + "no dose given" → operators
               re-fired, overdosing again.
            5. No independent code review, no rigorous/concurrency testing,
               reused code trusted without re-verification.
```

### Listing 2 — The unguarded state: an invalid (lethal) combination can sit there silently
```python
# The Therac-25 failure, in OOP terms: state set directly, with NO guard.
# Nothing forces the safety invariant, so an invalid combination is reachable.

class TheracUnsafe:
    def __init__(self):
        self.beam_power = "low"      # "low" (electron) or "high" (x-ray)
        self.target_in_place = True  # the metal target that spreads the beam

    # Two independent setters. Neither knows about the other. A race between
    # them (fast operator edit vs. slow hardware move) can leave the object
    # in the forbidden state: high power AND target absent.
    def set_power(self, power):
        self.beam_power = power      # no check

    def set_target(self, in_place):
        self.target_in_place = in_place  # no check

    def fire(self):
        # No invariant check before firing — it just fires whatever it is.
        deliver_beam(self.beam_power, self.target_in_place)

# INVALID, lethal state is reachable and silent:
m = TheracUnsafe()
m.set_power("high")          # selecting x-ray mode
m.set_target(False)          # hardware hasn't moved the target in yet
m.fire()                     # HIGH-power beam, target absent -> overdose
```

### Listing 3 — The fix: encapsulated state with an enforced invariant (an unsafe state is impossible)
```python
# The same object, encapsulated. State is private; every change goes through
# one guarded operation that REFUSES to leave the object unsafe.
# Invariant: if beam_power == "high", then target_in_place MUST be True.

class TheracSafe:
    def __init__(self):
        self._beam_power = "low"
        self._target_in_place = True
        self._check_invariant()

    def _check_invariant(self):
        # The single rule that must ALWAYS hold. Violating it is impossible
        # because no public path can leave the object in a violating state.
        if self._beam_power == "high" and not self._target_in_place:
            raise UnsafeStateError(
                "Refusing unsafe state: high beam power with target absent."
            )

    def configure(self, power, target_in_place):
        # ONE controlled door. The change is validated as a whole, atomically,
        # before it is committed — a fast edit cannot tear it in half.
        if power == "high" and not target_in_place:
            raise UnsafeStateError("Rejected: high power requires target in place.")
        self._beam_power = power
        self._target_in_place = target_in_place
        self._check_invariant()

    def fire(self):
        self._check_invariant()      # last line of defence before the beam
        deliver_beam(self._beam_power, self._target_in_place)

# The lethal combination can no longer be reached or fired:
m = TheracSafe()
m.configure("high", target_in_place=False)   # raises UnsafeStateError — blocked
```

### Listing 4 — The safety invariant in NESA pseudocode
```text
BEGIN ConfigureBeam(requestedPower, targetInPlace)
    // The invariant that must ALWAYS hold before any firing.
    IF requestedPower = "high" AND targetInPlace = FALSE THEN
        REJECT configuration            // unsafe state is forbidden
        RAISE error "high power requires target in place"
    ELSE
        beamPower ← requestedPower       // commit the change atomically
        target    ← targetInPlace
    ENDIF
END ConfigureBeam

BEGIN Fire
    IF beamPower = "high" AND target = FALSE THEN
        ABORT                            // re-check before firing — defence in depth
    ELSE
        DELIVER beam USING beamPower, target
    ENDIF
END Fire
```

### Listing 5 — "What would have caught it": a QA / grey-box checklist
```text
INDEPENDENCE OF TESTING (would have surfaced the author's blind spot)
[ ] Independent code review by engineers who did NOT write the code.
[ ] A formal, documented test plan reviewed by someone other than the author.
[ ] Reused code re-verified in its NEW context (no hardware net behind it).

GREY-BOX / RISK-BASED TESTING (targets the actual danger points)
[ ] Identify the safety invariant: high power => target in place. Test it directly.
[ ] Attack the shared internal state: can two changes leave it inconsistent?
[ ] Concurrency/timing tests: operator edits the prescription FASTER than the
    hardware can move the target (the < ~8 second race) — does state tear apart?
[ ] Boundary test the one-byte counter: fire at the instant it overflows to 0 —
    is any safety check skipped?

DEFENCE IN DEPTH (so no single failure reaches a patient)
[ ] Keep an independent HARDWARE interlock as a physical backstop to the software.
[ ] Cross-check the software's belief about the state against a real sensor.

HONEST INTERFACE (so humans are not misled)
[ ] Error messages state the HAZARD, not a cryptic code ("Malfunction 54").
[ ] A misfire must HALT and force a check — never report "no dose" and invite a retry.

Data/state qualities to argue from (mnemonic I-C-F-S):
  Integrity   — the machine's record of its state must match physical reality.
  Consistency — the state must agree with itself (power and target never disagree).
  Flexibility — change is allowed, but only through guarded, validated operations.
  Security    — only authorised, validated paths may alter safety-critical state.
```
