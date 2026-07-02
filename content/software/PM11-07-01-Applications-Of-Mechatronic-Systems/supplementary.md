---
title: "Supplementary Materials — Applications of Mechatronic Systems"
module: PM11
year: 11
lesson: "7.1"
script: script.md
---

# Supplementary Materials

A runnable model of the smallest complete mechatronic system, plus revision references for the
application fields and the Sense-Think-Act shape. Nothing here is spoken in the audio — it's the
read-along reference. The narration points at each by label only.

### Listing 1 — An automatic door: the smallest complete Sense-Think-Act system (Python, runnable)
```python
class AutomaticDoor:
    """Smallest complete mechatronic system: Sense -> Think -> Act.
    The open/shut state is encapsulated; sensor readings come in as inputs."""

    def __init__(self):
        self.is_open = False                      # encapsulated state (OOP from last module)

    def update(self, motion_detected, path_clear):
        # SENSE: motion_detected + path_clear are the sensor readings (inputs).
        # THINK: decide from the readings — and never move while the beam is blocked (safety).
        if path_clear:
            if motion_detected and not self.is_open:
                self.is_open = True               # ACT: drive the motor open
            elif not motion_detected and self.is_open:
                self.is_open = False              # ACT: drive the motor closed
        return self.is_open


door = AutomaticDoor()
assert door.update(motion_detected=True,  path_clear=True)  is True    # someone approaches -> opens
assert door.update(motion_detected=False, path_clear=True)  is False   # they leave         -> closes
assert door.update(motion_detected=True,  path_clear=False) is False   # path blocked       -> stays shut (safety)
print("Automatic-door (Sense-Think-Act) assertions passed.")
```

### Listing 2 — Mechatronic applications by field (reference)
```text
NAME THE FIELD · A SYSTEM · ITS DOMINANT REQUIREMENT

Field            Example systems                                  Dominant requirement
--------------   ----------------------------------------------   ---------------------------------
Manufacturing    factory robots, conveyors, quality control       precision, speed, reliability (long runs)
Transportation   ABS, cruise control, autopilot, auto gearbox     safety + real-time response (lives at stake)
Healthcare       surgical robots, prosthetics, insulin pumps      extreme precision + strict safety standards
Consumer         load-sensing washing machines, phone auto-       cost-effectiveness + ease of use
                 brightness, force-feedback game controllers
Agriculture      automated irrigation, GPS-guided tractors,       reliability in harsh outdoor conditions
                 livestock monitoring

SHARED JOBS every mechatronic system performs (one or more):
  Monitoring & measurement  ·  Control & regulation  ·  Automation & assistance  ·  Safety & protection
```

### Listing 3 — The same Sense-Think-Act shape across different systems (reference)
```text
SENSE  ->  THINK  ->  ACT   (one shape, very different devices)

System              SENSE (sensor)                THINK (decision)               ACT (actuator / end-effector)
-----------------   ---------------------------   ----------------------------   -----------------------------
Automatic door      motion + safety beam          clear AND someone there? open  door motor
Thermostat/heater   temperature sensor            below target? heat on          heater  (a CLOSED loop)
Anti-lock brakes    wheel-speed sensors           wheel locking up? release      brake actuator (pulses)
Robot vacuum        bump + cliff + dirt sensors   obstacle? turn; dirt? clean    drive motors + brushes
Washing machine     load weight + water level     choose cycle / water / spin    inlet valve, drum motor, heater

The four S-M-E-M fields in one build:
  Software (the THINK) · Mechanical (the moving parts) · Electronics (sensors/actuators/wiring) · Mathematics (control + timing)
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| OOP | Object-Oriented Programming | A paradigm structuring software around objects that bundle data and behaviour |
| S-M-E-M | Software · Mechanical · Electronics · Maths | The knowledge fields combined in a mechatronic build |
| Sense-Think-Act | Sense · Think · Act | The repeating control loop of an autonomous / mechatronic system |
