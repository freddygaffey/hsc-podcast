---
title: "Supplementary Materials — Sensors, Actuators and End Effectors"
module: PM11
year: 11
lesson: "7.3"
script: script.md
---

# Supplementary Materials

The read-along reference for the devices lesson. Nothing here is spoken in the audio — the
narration points at each listing by label only. Listing 1 maps the S-A-E trio onto one machine;
Listing 2 is a runnable component-selection model; Listing 3 is the revision reference.

### Listing 1 — The S-A-E trio on one machine: a pick-and-place robotic arm (reference)
```text
ONE TASK, THREE DEVICE ROLES — map them onto Sense -> Think -> Act:

  ROLE            DEVICE on the arm              What it does                         S-T-A stage
  -------------   ----------------------------   ----------------------------------   -----------
  SENSOR (input)  light sensor + position        measures the world (is a part        SENSE
                  encoder on each joint          there? where is each joint?)
  (controller)    the microcontroller            decides the next move                THINK
  ACTUATOR        servo motor at each joint       CREATES the motion (swings the       ACT
  (output)                                        arm into position)
  END-EFFECTOR    the gripper at the arm's tip    DOES the actual job (grasps the      ACT
                                                  part) — the "hand"

  THE DISTINCTION THE EXAM FISHES FOR:
    actuator    = the thing that MOVES (the muscle that creates motion/force)
    end-effector = the TOOL that motion drives (the hand/gripper/drill that does the task)
  A motor is an actuator; the gripper it opens and closes is the end-effector.

  Signals: a DIGITAL sensor sends 0/1 straight to the controller's I/O pins; an ANALOG sensor
  (a varying voltage) must pass through an ANALOG-TO-DIGITAL CONVERTER first so the chip can read it.
```

### Listing 2 — Choosing an end-effector by matching specs to requirements (Python, runnable)
```python
class Gripper:
    """An end-effector option, with the specs that decide if it fits a task."""

    def __init__(self, kind, max_force_n, precision_mm, cycle_time_s):
        self.kind = kind
        self.max_force_n = max_force_n          # how hard it can grip (Newtons)
        self.precision_mm = precision_mm        # positioning error (smaller = better)
        self.cycle_time_s = cycle_time_s        # seconds per pick (smaller = faster)

    def fits(self, need_force_n, need_precision_mm, need_speed_s):
        # Meets the task only if it is strong enough, precise enough, AND fast enough.
        return (self.max_force_n >= need_force_n
                and self.precision_mm <= need_precision_mm
                and self.cycle_time_s <= need_speed_s)


# Task: place delicate circuit boards — light grip, tight positioning, 2 s per cycle.
NEED_FORCE, NEED_PRECISION, NEED_SPEED = 5, 0.5, 2.0

options = [
    Gripper("Parallel jaw", 50, 0.10, 1.5),
    Gripper("Angular",      30, 0.05, 2.0),
    Gripper("Vacuum",       20, 0.30, 1.0),
    Gripper("Magnetic",    100, 0.50, 1.2),
]

suitable = [g for g in options if g.fits(NEED_FORCE, NEED_PRECISION, NEED_SPEED)]
# Among those that fit, pick on the DOMINANT requirement: precision (delicate boards).
best = min(suitable, key=lambda g: g.precision_mm)

assert len(suitable) == 4                 # all four clear the numeric thresholds
assert best.kind == "Angular"             # ...so choose on the dominant requirement
print("Chosen end-effector:", best.kind, "(±", best.precision_mm, "mm)")
```

### Listing 3 — Revision reference: sensors, actuators, end-effectors (reference)
```text
SENSORS  (input — measure the world; the SENSE in Sense-Think-Act)
  MOTION       PIR (passive infrared) : presence/movement, 3-7 m, slow (1-3 s) — security lights
               accelerometer          : acceleration/tilt, fast (ms), high precision — gesture/impact
               encoder                : rotation/position by counting pulses, very precise — motor control
  LIGHT LEVEL  photocell (LDR)        : resistance changes with light, cheap, rough — day/night switching
               photodiode             : current proportional to light, fast + precise — optical comms
  Five specs to weigh: Range · Accuracy · Precision · Response time · Resolution
  Signal type: digital (0/1, straight to the pin) vs analog (needs an analog-to-digital converter)

ACTUATORS  (output — create motion/force; part of the ACT)
  HYDRAULIC   pressurised fluid -> piston; force = pressure x area; HUGE force (excavators,
              presses, aircraft surfaces); high power, needs a pump
  (also)      electric motors/servos (precise, clean), pneumatic (air, fast/light)

END-EFFECTORS / MANIPULATORS  (the working tool at the tip — the "hand"; finishes the ACT)
  GRIPPERS    parallel jaw : cylinders/consistent shapes, precise
              angular      : varied/delicate items, very precise
              vacuum       : flat, light items (suction)
              magnetic     : ferrous metal only, simple on/off
  (also)      drills, welders, spray heads — whatever performs the task

CHOOSING ANY COMPONENT — balance P-C-R-I:
  Performance (accuracy/speed/range) · Cost · Reliability (durability/environment) · Integration (size/interface)
  Then decide on the task's DOMINANT requirement (precision? force? speed? cost?).
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| P-C-R-I | Performance · Cost · Reliability · Integration | Criteria for choosing a hardware component |
| S-A-E | Sensor · Actuator · End-effector | The mechatronic device trio (input, output, tool) |
| Sense-Think-Act | Sense · Think · Act | The repeating control loop of an autonomous / mechatronic system |
