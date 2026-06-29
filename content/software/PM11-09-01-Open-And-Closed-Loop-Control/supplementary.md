---
title: "Supplementary Materials — Open and Closed Loop Control"
module: PM11
year: 11
lesson: "9.1"
script: script.md
---

# Supplementary Materials

The read-along reference for the control lesson. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 runs an open-loop and a closed-loop controller side by
side; Listing 2 is the closed-loop algorithm in NESA pseudocode; Listing 3 is the revision reference.

### Listing 1 — Open loop vs closed loop, side by side (Python, runnable)
```python
def step_plant(temp_c, power_pct):
    """A tiny thermal model: heater power warms the room; the room also cools toward 18 C."""
    return temp_c + power_pct * 0.01 - (temp_c - 18) * 0.02

# OPEN LOOP: run a fixed power for a fixed time. It NEVER looks at the temperature — blind.
def open_loop(temp_c, power_pct=100, steps=12):
    for _ in range(steps):
        temp_c = step_plant(temp_c, power_pct)     # same power regardless of the result
    return round(temp_c, 1)

# CLOSED LOOP: measure -> compare to setpoint -> correct (proportional control) -> repeat.
def closed_loop(temp_c, setpoint_c, gain=50, steps=60):
    for _ in range(steps):
        error = setpoint_c - temp_c                # COMPARE: how far off are we?
        power_pct = max(0, min(100, error * gain)) # CORRECT: push proportional to the error (clamped 0..100)
        temp_c = step_plant(temp_c, power_pct)     # ACT, then loop back and re-measure
    return round(temp_c, 1)


START, SETPOINT = 18.0, 25.0
open_result = open_loop(START)
closed_result = closed_loop(START, SETPOINT)

# The open loop runs full power blindly and sails past the target; the closed loop settles near it.
assert abs(closed_result - SETPOINT) < 0.5     # closed loop converges to (near) the setpoint
assert abs(open_result - SETPOINT) > 0.5       # open loop misses — it never measured the result
print("open loop ->", open_result, "C |  closed loop ->", closed_result, "C  (setpoint", SETPOINT, "C)")
```

### Listing 2 — The closed-loop control algorithm in NESA pseudocode (reference)
```text
BEGIN ClosedLoopControl
    SET setpoint TO the desired value          // e.g. 25 degrees
    SET tolerance TO a small allowed error     // e.g. 0.5 degrees
    REPEAT
        measured = READ sensor                 // SENSE
        error = setpoint - measured            // COMPARE
        IF error > tolerance THEN
            INCREASE actuator output           // too low  -> push harder (proportional to error)
        ELSE IF error < -tolerance THEN
            DECREASE actuator output           // too high -> ease off
        ELSE
            HOLD actuator output               // within tolerance -> leave it
        ENDIF
    UNTIL system is stopped
END

  An OPEN-LOOP version has NO "measured", NO "error", NO feedback branch — it just:
    SET actuator output ; RUN for a fixed time ; STOP.   (blind)
```

### Listing 3 — Open vs closed loop: revision reference (reference)
```text
"CLOSED LOOPS LISTEN; OPEN LOOPS ARE BLIND."

                    OPEN LOOP                          CLOSED LOOP
  Feedback          none                               measures output + feeds it back
  Decides on        the input command only             the ERROR = setpoint - measured
  Adapts?           no — can't correct disturbances    yes — self-corrects
  Cost/complexity   simpler, cheaper, fewer sensors    more complex, dearer, needs a sensor
  Examples          microwave/toaster (set time),      thermostat, cruise control, autofocus,
                    sprinkler on a timer, basic 3D     robotic-arm position control
                    printer move

THE CLOSED-LOOP CYCLE — Measure, Compare, Correct (M-C-C), forever:
   measure the output -> compare to the setpoint (error) -> correct in proportion to the error -> repeat

KEY TERMS
  setpoint   the target value            error      setpoint minus measured (how far off)
  gain       how hard you push per unit of error    proportional control = correction grows with error
  feedback   NEGATIVE feedback opposes the error (stabilising — what control uses);
             POSITIVE feedback amplifies it (destabilising — e.g. an oscillator)
  stability  too LITTLE gain = slow; too MUCH gain = overshoot + oscillation, maybe instability
```
