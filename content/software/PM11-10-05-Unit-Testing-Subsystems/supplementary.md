---
title: "Supplementary Materials — Unit Testing Subsystems"
module: PM11
year: 11
lesson: "10.5"
script: script.md
---

# Supplementary Materials

The read-along reference for the unit-testing lesson. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 unit-tests a control algorithm for effectiveness and
repeatability; Listing 2 unit-tests a safety feature; Listing 3 is the revision reference.

### Listing 1 — Unit tests for a control algorithm: effectiveness, boundary, repeatability (Python, runnable)
```python
class MockSensor:
    """A TEST FIXTURE: a simulated sensor that returns scripted values -> repeatable, no hardware
    (real sensors are noisy and can't be replayed; the mock makes the test deterministic)."""
    def __init__(self, values):
        self.values = list(values)
        self.i = 0
    def read(self):
        value = self.values[self.i]
        self.i += 1
        return value


def command(setpoint, measured, gain=10, lo=0, hi=100):
    """The control algorithm UNDER TEST: proportional, clamped to the actuator's safe range."""
    return max(lo, min(hi, gain * (setpoint - measured)))

def run_against(sensor, setpoint, steps):
    return [command(setpoint, sensor.read()) for _ in range(steps)]


# EFFECTIVENESS: does it do the right thing? below target -> heat; at target -> off.
assert command(25, 20) == 50          # 10 * (25 - 20)
assert command(25, 25) == 0

# BOUNDARY / FAULTY input: a huge error is clamped to the safe maximum, never exceeds it.
assert command(1000, 0) == 100        # not 10000 -- the clamp holds

# REPEATABILITY: the same scripted readings give the same commands EVERY run (deterministic).
run_a = run_against(MockSensor([20, 22, 25]), 25, 3)
run_b = run_against(MockSensor([20, 22, 25]), 25, 3)
assert run_a == run_b == [50, 30, 0]

print("Unit tests passed -> effectiveness, boundary/clamp, repeatability:", run_a)
```

### Listing 2 — Unit-test a safety feature: the interlock must trip (Python, runnable)
```python
class SafetyError(Exception):
    pass

def safe_command(setpoint, measured, safety_limit=80):
    """Control algorithm WITH a safety interlock: refuse to run at or above the safety limit."""
    if measured >= safety_limit:
        raise SafetyError("over safety limit")
    return max(0, min(100, 10 * (setpoint - measured)))


# Normal reading: the controller heats as expected.
assert safe_command(25, 20) == 50

# Over-limit reading: the interlock MUST trip (testing the failure path, not just the happy path).
tripped = False
try:
    safe_command(25, 95)              # 95 C is above the 80 C safety limit
except SafetyError:
    tripped = True
assert tripped is True

print("Safety unit test passed: interlock trips above the limit; normal control unaffected.")
```

### Listing 3 — What unit tests must show, and how (reference)
```text
THE DOT-POINT asks unit tests to determine two things -- E-R:
  EFFECTIVENESS   does the control algorithm achieve its goal? (reach the setpoint / make the right command)
  REPEATABILITY   same input -> same result, run after run (DETERMINISTIC) -- so a pass means something

WHY SIMULATED DEVICES (fixtures / mocks): real hardware is slow, expensive, unsafe, and NOT repeatable
  (noisy sensors, timing). A mock/simulated device (from 10.1) behind the same interface (from 10.3) makes
  the test fast, safe, and repeatable. -> design-for-testability pays off here.

UNIT-TEST PRINCIPLES -- reuse FIRST (from OOP): Fast · Independent · Repeatable · Self-validating · Timely.
  ISOLATION = test ONE component alone (a unit), with mock devices standing in for the rest.
  Levels (from OOP) -- U-S-S: Unit (one component) -> Subsystem -> System.

WHAT TO TEST -- reuse B-P-F test data (from PF11 4.6):
  the happy PATH (normal input reaches the goal) · BOUNDARY values (the edges / limits, e.g. the clamp) ·
  FAULTY input + failure paths (a sensor spike, an over-limit reading -> the safety interlock must trip).
  Test what it SHOULD do AND what it should REFUSE to do.

DOCUMENT the results (SE-11-09): record each test, its input, expected vs actual, and pass/fail -- this
  manages + documents the project, gives confidence to change code, and is evidence the subsystem works.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| B-P-F | Boundary · Path coverage · Faulty-and-abnormal | Categories of test data (actual vs expected) |
| OOP | Object-Oriented Programming | A paradigm structuring software around objects that bundle data and behaviour |
| U-S-S | Unit · Subsystem · System | The levels of testing |
