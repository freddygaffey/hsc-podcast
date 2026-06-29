---
title: "Supplementary Materials — Designing Accessible Mechatronic Systems"
module: PM11
year: 11
lesson: "8.3"
script: script.md
---

# Supplementary Materials

The read-along reference for the accessibility lesson. Nothing here is spoken in the audio — the
narration points at each listing by label only. Listing 1 is the specialist-requirements checklist
with worked examples; Listing 2 is a runnable accessible control; Listing 3 is the universal-design reference.

### Listing 1 — Specialist requirements (S-A-I-D) and worked assistive examples (reference)
```text
SPECIALIST REQUIREMENT = a requirement that comes from the USER'S specific disability and shapes
the design. The golden rule first:  DESIGN *WITH* USERS, NOT *FOR* THEM  (consult the real users).

S-A-I-D — the specialist-requirements checklist:
  SAFETY        reduced ability to react fast -> robust safety: low-force emergency stops,
                force limits, timeouts, fail-safe behaviour
  ADAPTABILITY  adjustable to the individual (sensitivity, interface height, input method);
                needs change over time -> user-adjustable settings
  INDEPENDENCE  preserve dignity + autonomy: the user does it themselves, with privacy
  DIVERSE I/O   alternative INPUTS (switch, voice, eye-gaze) + multi-modal FEEDBACK (V-A-H)
  (+ also)      RELIABILITY (people depend on it daily) and AFFORDABILITY (it must be reachable in cost)

WORKED EXAMPLES — name the device, then its dominant specialist requirements:
  Powered wheelchair      safe low-force/sip-puff control, reliability, reach-appropriate controls,
                          independence (user drives unaided)
  Prosthetic hand         adjustable grip force (won't crush), comfort/weight, intuitive control,
                          reliability (worn all day)
  Eye-gaze comms aid       gaze input + dwell-to-select, clear multi-modal feedback, fatigue-aware
                          timing, dignity (the user's own voice)
```

### Listing 2 — An accessible force control: gentle threshold, force limit, emergency stop (Python, runnable)
```python
class AccessibleControl:
    """A control sized to the individual: activates at a gentle fraction of the user's own
    comfortable force, refuses dangerous force, and honours an emergency stop."""

    def __init__(self, user_max_force_n, safety_limit_n=50):
        self.threshold = user_max_force_n * 0.3    # ADAPTABILITY: activate at 30% of what the user can manage
        self.safety_limit = safety_limit_n         # SAFETY: never let the actuator exceed this force
        self.stopped = False

    def emergency_stop(self):
        self.stopped = True                        # SAFETY: a latched stop — nothing moves until reset

    def activate(self, applied_force_n):
        if self.stopped:
            return "stopped"
        if applied_force_n > self.safety_limit:
            return "blocked"                       # force-limit safety overrides everything
        return "on" if applied_force_n >= self.threshold else "off"


# A user who can comfortably apply only about 15 N -> a gentle 4.5 N activation threshold.
control = AccessibleControl(user_max_force_n=15)
assert round(control.threshold, 1) == 4.5
assert control.activate(2.0) == "off"        # a light, accidental brush: no activation
assert control.activate(5.0) == "on"         # a deliberate press above the gentle threshold
assert control.activate(60.0) == "blocked"   # over the safety limit: refused
control.emergency_stop()
assert control.activate(5.0) == "stopped"    # after the emergency stop, nothing moves
print("Accessible control checks passed.")
```

### Listing 3 — Universal design and accessible interfaces (reference)
```text
UNIVERSAL / INCLUSIVE DESIGN — design from the start for the widest range of people.
  THE CURB-CUT EFFECT: build for the margins and everyone benefits (ramps help prams + trolleys too).

The 7 principles of universal design (condensed):
  1 Equitable use        useful to people with diverse abilities
  2 Flexibility          accommodates preferences + abilities (multiple ways to do a thing)
  3 Simple & intuitive   easy regardless of experience
  4 Perceptible info     communicates to all (so use V-A-H feedback)
  5 Tolerance for error  accidental actions don't cause harm
  6 Low physical effort  comfortable, minimal force
  7 Size & space         reachable approach + use (reach envelope ~600-1000 mm is the sweet spot)

ALTERNATIVE INPUTS (not everyone can use a button/joystick):
  switch (head/sip-puff/blink) · voice (must handle varied speech) · eye-gaze (dwell to select)

MULTI-MODAL FEEDBACK — V-A-H:  Visual · Audio · Haptic (vibration).  Offer more than one channel.

SAFETY for users who can't react quickly:
  multiple low-force emergency stops (large, ~50 mm, 2-5 N) · force limiting · inactivity timeout ·
  automatic shutdown on sensor failure or boundary violation.

WHY (SE-11-05): accessible design is an ETHICAL + LEGAL obligation (equal access, anti-discrimination),
and good engineering — it makes systems more robust and usable for everyone.
```
