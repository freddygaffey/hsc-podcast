---
title: "Supplementary Materials — Device Data and Diagnostics"
module: PM11
year: 11
lesson: "8.1"
script: script.md
---

# Supplementary Materials

The read-along reference for the data lesson. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 distinguishes diagnostic from optimisation data;
Listing 2 is a runnable raw-to-useful data pipeline; Listing 3 is the obtaining-processing-storing reference.

### Listing 1 — Diagnostic data vs optimisation data (the examinable distinction) (reference)
```text
THE FOUR DATA STREAMS a mechatronic system handles — M-C-D-O:
  MEASUREMENT data   raw sensor readings of the world (temperature, distance, position)
  CONTROL data       the commands sent out (motor speed, valve open/closed, setpoints)
  DIAGNOSTIC data    the system's own HEALTH — fault logs, error codes, uptime, overheat events
  OPTIMISATION data  performance history used to TUNE — response times, energy use, cycle counts

DIAGNOSTIC vs OPTIMISATION — say it this way:
  DIAGNOSTIC asks  "Is it healthy / what went wrong?"   -> detect & fix faults, maintenance
       e.g. "motor stalled at 14:03", error code E07, sensor-out-of-range count
  OPTIMISATION asks "Can it do the job better?"          -> tune settings, save energy, go faster
       e.g. average cycle time fell from 2.1 s to 1.8 s after raising fan response

  Same numbers can serve both: a temperature log is DIAGNOSTIC when you hunt a fault,
  OPTIMISATION when you tune the setpoint. The PURPOSE decides which it is.
```

### Listing 2 — From raw sensor stream to a control decision: catch, calibrate, smooth, optimise (Python, runnable)
```python
def is_faulty(value, low, high):
    """DIAGNOSTIC check: a reading outside the sensor's valid range signals a fault."""
    return value < low or value > high

def calibrate(raw_value, offset):
    """PROCESS step 1: apply a calibration offset so the sensor reads true."""
    return raw_value + offset

def moving_average(values, window=3):
    """PROCESS step 2: smooth noise by averaging each value with its recent neighbours."""
    smoothed = []
    for i in range(len(values)):
        chunk = values[max(0, i - window + 1): i + 1]
        smoothed.append(sum(chunk) / len(chunk))
    return smoothed

def fan_speed_for(temp_c, setpoint_c):
    """OPTIMISATION: the further above setpoint, the harder the fan runs (clamped 0..100)."""
    error = temp_c - setpoint_c
    return 0 if error <= 0 else min(100, int(error * 20))


# A stream of noisy raw readings from a temperature sensor (deg C) — one is a glitch.
raw = [21.8, 22.2, 99.0, 22.1, 22.3]          # 99.0 is a sensor glitch

# DIAGNOSTIC: catch the out-of-range glitch BEFORE it corrupts the control decision.
faults = [v for v in raw if is_faulty(v, low=-10, high=60)]
assert faults == [99.0]

# PROCESS: drop the glitch, calibrate (+0.5), then smooth the stream.
clean = [calibrate(v, 0.5) for v in raw if not is_faulty(v, -10, 60)]
smoothed = moving_average(clean, window=3)
final_temp = round(smoothed[-1], 2)

# OPTIMISATION: use the cleaned, smoothed temperature to set the fan.
SETPOINT = 22.0
fan = fan_speed_for(final_temp, SETPOINT)

assert final_temp > SETPOINT                   # we're a little above target...
assert fan > 0                                 # ...so the fan runs
print("clean:", [round(c, 2) for c in clean], "| smoothed final:", final_temp, "| fan %:", fan)
```

### Listing 3 — Obtaining, processing and safely storing device data (reference)
```text
OBTAINING the data (how a reading gets in):
  POLLING     the controller asks each sensor on a schedule  ("polling asks")
  INTERRUPTS  the sensor signals the controller when something happens ("interrupts tell")
  SAMPLING RATE = how often you read. Too slow -> you miss events; too fast -> wasted CPU + storage.
  Analog signal -> ANALOG-TO-DIGITAL CONVERTER -> a number (carried over from 7.3).

PROCESSING the data (raw -> useful):
  CALIBRATE  correct a known offset/scale so the reading is true
  FILTER     smooth noise (e.g. a moving average) so one glitch doesn't swing the control
  VALIDATE   range-check every reading (PF11 data-dictionary constraints) — reject the impossible

STORING it safely (SE-11-04 — collect / use / store):
  Every log entry wears T-I-U:  Timestamp · Identity (which sensor) · Units  (+ a consistent format)
  Local store = fast, for real-time control;  cloud = for later analysis.
  Access control (who may read operational vs config data) · backups of calibration/config ·
  a retention policy (how long to keep history). Never trust or store a value you didn't validate.
```
