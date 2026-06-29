---
title: "Supplementary Materials — Implementing Closed Loop Control"
module: PM11
year: 11
lesson: "10.2"
script: script.md
---

# Supplementary Materials

The read-along reference for the closed-loop implementation lesson. Nothing here is spoken in the audio —
the narration points at each listing by label only. Listing 1 implements a proportional controller;
Listing 2 refines it into a PID controller; Listing 3 is the pseudocode + revision reference.

### Listing 1 — A proportional closed-loop controller (Python, runnable)
```python
def plant(temp_c, power_pct):
    """The simulated system being controlled: power warms it; it also cools toward 18 C."""
    return temp_c + power_pct * 0.01 - (temp_c - 18) * 0.02


class ProportionalController:
    def __init__(self, kp, out_min=0, out_max=100):
        self.kp = kp
        self.out_min, self.out_max = out_min, out_max

    def output(self, setpoint, measured):
        error = setpoint - measured                              # error = setpoint - measured
        command = self.kp * error                               # correction proportional to error
        return max(self.out_min, min(self.out_max, command))    # CLAMP to the actuator's safe range (SE-11-07)


controller = ProportionalController(kp=20)
SETPOINT, temp = 25.0, 18.0
for _ in range(200):
    temp = plant(temp, controller.output(SETPOINT, temp))

# Proportional-only gets CLOSE but leaves a small steady-state offset below the setpoint.
assert temp < SETPOINT                 # never quite reaches it
assert SETPOINT - temp < 1.0           # but settles within a degree
print("Proportional only -> settled at", round(temp, 2), "C (setpoint 25) - small steady-state offset")
```

### Listing 2 — Refine it into a PID controller: kill the offset, tame the overshoot (Python, runnable)
```python
def plant(temp_c, power_pct):
    return temp_c + power_pct * 0.01 - (temp_c - 18) * 0.02


class PIDController:
    """P + I + D. The INTEGRAL removes the steady-state offset; the DERIVATIVE damps overshoot.
    This is the performance-enhancing refinement of the proportional controller (SE-11-08)."""

    def __init__(self, kp, ki, kd, out_min=0, out_max=100):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.out_min, self.out_max = out_min, out_max
        self.integral = 0.0
        self.prev_error = 0.0

    def output(self, setpoint, measured, dt=1.0):
        error = setpoint - measured
        self.integral += error * dt                 # I: accumulate PAST error -> removes offset
        derivative = (error - self.prev_error) / dt # D: rate of change -> predicts/damps overshoot
        self.prev_error = error
        command = self.kp * error + self.ki * self.integral + self.kd * derivative
        return max(self.out_min, min(self.out_max, command))    # CLAMP (always limit the actuator)


controller = PIDController(kp=20, ki=0.5, kd=5)
SETPOINT, temp = 25.0, 18.0
peak = temp
for _ in range(400):
    temp = plant(temp, controller.output(SETPOINT, temp))
    peak = max(peak, temp)

assert abs(temp - SETPOINT) < 0.1      # PID reaches the setpoint - offset eliminated
assert peak < SETPOINT + 0.5           # and barely overshoots (the derivative term damps it)
print("PID -> settled at", round(temp, 2), "C, peak", round(peak, 2), "- offset gone, overshoot tiny")
```

### Listing 3 — The closed-loop algorithm in NESA pseudocode + PID reference (reference)
```text
CLOSED-LOOP CONTROL LOOP — NESA pseudocode:
  BEGIN ControlLoop
      SET setpoint TO the desired value
      REPEAT
          measured = READ sensor                       // SENSE
          error    = setpoint - measured               // COMPARE
          command  = controlAlgorithm(error)           // e.g. Kp * error  (proportional)
          command  = CLAMP command BETWEEN out_min AND out_max   // never exceed the actuator's limits
          DRIVE actuator WITH command                  // CORRECT
      UNTIL stopped
  END

PROPORTIONAL (P):  output = Kp x error
  simple; bigger error -> bigger push. Downside: a small STEADY-STATE OFFSET remains (never fully arrives).

PID = Proportional + Integral + Derivative:  output = Kp*error + Ki*(sum of error) + Kd*(change in error)
  P  -> the PRESENT : react to the current error
  I  -> the PAST    : accumulate past error -> ELIMINATES the steady-state offset
  D  -> the FUTURE  : react to how fast error is changing -> DAMPS overshoot/oscillation
  ("P for the present, I for the past, D predicts the future")

ENHANCING PERFORMANCE (SE-11-08 refine): start with P, add I to remove the offset, add D to smooth the
approach. TUNE the gains: too much gain -> overshoot/oscillation (from 9.1); always CLAMP the output so a
big command can't drive the actuator past its safe limit. Tune SAFELY in the simulation first (10.1).
```
