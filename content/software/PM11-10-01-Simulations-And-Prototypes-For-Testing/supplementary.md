---
title: "Supplementary Materials — Simulations and Prototypes for Testing"
module: PM11
year: 11
lesson: "10.1"
script: script.md
---

# Supplementary Materials

The read-along reference for the simulation lesson. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 simulates a plant and tests control code against it;
Listing 2 simulates an imperfect sensor to test the handling code; Listing 3 is the revision reference.

### Listing 1 — Simulate the plant, validate it, then test the control code on it (Python, runnable)
```python
class TrackSim:
    """A SIMULATION of a robot on a 1-D track: software stands in for real hardware. It models
    position and a top speed (a realistic constraint), so control code can be tested with no board."""

    def __init__(self, position=0.0, max_step=1.0):
        self.position = position
        self.max_step = max_step                                   # speed limit per tick

    def move(self, command):
        step = max(-self.max_step, min(self.max_step, command))    # clamp to the speed limit
        self.position += step
        return round(self.position, 4)


def controller(target, measured, gain=0.5):
    return (target - measured) * gain          # closed-loop proportional command (from 9.1)


# 1) VALIDATE THE SIMULATION against known results before trusting it.
check = TrackSim()
assert check.move(0) == 0.0          # no command -> stays put
assert check.move(0.4) == 0.4        # a small command moves exactly that far
assert check.move(5.0) == 1.4        # a huge command is clamped to the 1.0 speed limit (0.4 + 1.0)

# 2) TEST THE CONTROL CODE against the simulation -- no hardware, no risk.
sim = TrackSim()
TARGET = 10.0
for _ in range(60):
    sim.move(controller(TARGET, sim.position))

assert abs(sim.position - TARGET) < 0.1      # the controller reached the target IN SIMULATION
print("Sim validated, and the controller reached", round(sim.position, 2), "with no hardware.")
```

### Listing 2 — Simulate an imperfect sensor to test the handling code (Python, runnable)
```python
def simulated_sensor(true_value, glitches):
    """Simulate a realistic, IMPERFECT sensor: mostly the true value, but inject KNOWN glitches
    so we can test that downstream code copes. Deterministic -> the test is repeatable."""
    for is_glitch in glitches:
        yield 999.0 if is_glitch else true_value

def reject_glitches(stream, low, high):
    return [v for v in stream if low <= v <= high]      # the validation we want to test


# Simulate a 25 C sensor that glitches on the 3rd and 5th readings; the handling must drop them.
readings = simulated_sensor(25.0, glitches=[False, False, True, False, True])
clean = reject_glitches(readings, low=-10, high=60)

assert clean == [25.0, 25.0, 25.0]           # 3 good readings kept, 2 glitches rejected
print("Simulated noisy sensor: glitches injected and correctly rejected before any hardware exists.")
```

### Listing 3 — Why simulate, fidelity, and simulation principles (reference)
```text
SIMULATE BEFORE YOU BUILD -- it's S-C-F:
  SAFE   you can't break expensive hardware or hurt anyone; explore failure modes freely
  CHEAP  no wasted motors/boards; a bug found in software costs nothing
  FAST   iterate in seconds, not days; rebuild a model instantly
  (the DARPA self-driving race is the classic lesson: simulate thousands of runs before the desert)

SIMULATION vs PROTOTYPE:
  SIMULATION = a software MODEL of the system's behaviour (the "plant") that your control code drives,
               so you test the code without real devices.
  PROTOTYPE  = an early physical build. LOW-FIDELITY first (rough, cheap, quick to change) ->
               HIGH-FIDELITY later (detailed, costly, close to the real thing). "low-fidelity first."

PRINCIPLES OF A GOOD SIMULATION:
  1. start simple, add complexity gradually
  2. include realistic constraints (noise, drift, speed/range limits, delays) -- that's what makes it useful
  3. test edge cases + failure modes safely (a stuck sensor, a lost signal)
  4. VALIDATE the model against known results (does the simple case match what you already know?)
  5. design for testability -- structure code so each component can be tested in isolation (-> 10.5 unit tests)

WHY THIS WHOLE MODULE'S CODE IS RUNNABLE SIMULATIONS: you test the control logic in software first;
the same abstraction patterns and control code then transfer to the real hardware.
```
