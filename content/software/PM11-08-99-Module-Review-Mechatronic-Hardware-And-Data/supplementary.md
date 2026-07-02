---
title: "Supplementary Materials — Module Review: Mechatronic Hardware and Data"
module: PM11
year: 11
lesson: "7–8"
script: script.md
---

# Supplementary Materials

The read-along revision pack for Chapters 07–08. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 is the master mnemonic table; Listing 2 is one
integrated runnable example tying the threads together; Listing 3 is the key-terms checklist by lesson.

### Listing 1 — Master mnemonic table for Chapters 07–08 (the exam-dump) (reference)
```text
THE SPINE (write this first):  SENSE -> THINK -> ACT   (S-T-A)
  every mechatronic system senses (sensor), thinks (controller algorithm), acts (actuator/end-effector)

CH 07 — FOUNDATIONS
  S-M-E-M   the four fields: Software · Mechanical · Electronics · Maths   ("MECHanics + elecTRONICS + code")
  C-M-I     a microcontroller = a whole computer on a chip: CPU core + Memory + I/O pins  (a CPU is just the processor)
  F-D-E     the processor's heartbeat: Fetch -> Decode -> Execute  (runs opcodes from its instruction set)
  "address is where, data is what"   address register = a memory location; data register = a value
  S-A-E     the device trio: Sensor (input/measure) · Actuator (output/move) · End-effector (the tool that does the job)
            "actuator MOVES; end-effector is the tool the motion drives"  (motor vs the gripper it works)
  P-C-R-I   choose a component by: Performance · Cost · Reliability · Integration  (then the dominant requirement)
  analog -> ANALOG-TO-DIGITAL CONVERTER -> a number   (digital sensors go straight to a pin)

CH 08 — DATA & INTEGRATION
  M-C-D-O   four data streams: Measurement · Control · Diagnostic · Optimisation
  "diagnostic asks is-it-healthy?;  optimisation asks can-it-do-better?"   (purpose decides, not the numbers)
  "polling asks; interrupts tell"   (+ sampling rate: too slow miss events, too fast waste resources)
  process raw -> useful:  CALIBRATE -> FILTER (moving average) -> VALIDATE (range-check)
  T-I-U     every log entry: Timestamp · Identity · Units  (+ access control, backups, retention) [SE-11-04]
  V-I-P     Voltage · current I · Power ;   P = V x I  ("power = volts x amps") ;   Ohm: V = I x R
  "amp-hours over amps gives hours"  (battery runtime, ~80% usable) ;  "the actuator dominates the budget"
  "power lines feed, data lines talk, on one common ground"  ;  NEVER run an actuator off a controller pin (use a driver)
  S-A-I-D   specialist requirements: Safety · Adaptability · Independence · Diverse-I/O  (+reliability +affordability)
  "design WITH users, not FOR them"  ;  V-A-H feedback (Visual/Audio/Haptic)  ;  curb-cut effect [SE-11-05]
```

### Listing 2 — One integrated example: sense → clean → decide (the threads combined) (Python, runnable)
```python
class Thermostat:
    """Ties Ch 07-08 together: take sensor MEASUREMENT data, reject a faulty reading (DIAGNOSTIC),
    FILTER it, then decide the ACTUATOR — a preview of the closed-loop control coming in Ch 09."""

    def __init__(self, setpoint_c, valid_range=(-10, 60)):
        self.setpoint = setpoint_c
        self.low, self.high = valid_range
        self.history = []

    def feed(self, reading_c):
        # DATA (8.1): a reading outside the valid range is a fault -> discard it.
        if reading_c < self.low or reading_c > self.high:
            return None
        self.history.append(reading_c)
        return reading_c

    def smoothed(self, window=3):
        chunk = self.history[-window:]          # FILTER: moving average over recent readings
        return sum(chunk) / len(chunk)

    def fan_on(self):
        # THINK: the fan (actuator) runs only while the smoothed temperature is above setpoint.
        return self.smoothed() > self.setpoint


warm = Thermostat(setpoint_c=22.0)
assert warm.feed(99.0) is None              # DIAGNOSTIC: glitch rejected before it can corrupt control
for r in [22.4, 22.6, 22.5]:
    warm.feed(r)
assert warm.fan_on() is True                # smoothed 22.5 > 22.0 -> fan ON

cool = Thermostat(setpoint_c=22.0)
for r in [21.0, 21.2, 21.1]:
    cool.feed(r)
assert cool.fan_on() is False               # smoothed 21.1 < 22.0 -> fan OFF
print("Integrated thermostat (sense -> clean -> decide) checks passed.")
```

### Listing 3 — Key-terms checklist by lesson (Chapters 07–08) (reference)
```text
[ ] 7.1 Applications: mechatronics = S-M-E-M fields fused to Sense-Think-Act on the physical world;
        applications by field each with a DOMINANT requirement; traps = only-mechanical / doesn't-sense-and-act.
[ ] 7.2 Computing hardware: microcontroller (C-M-I, whole computer on a chip) vs CPU (processor only);
        instruction set + opcodes; address vs data registers (where vs what); F-D-E cycle; hardware shapes code.
[ ] 7.3 Devices (S-A-E): sensors — motion (PIR/accelerometer/encoder), light (photocell/photodiode);
        actuators — hydraulic (force = pressure x area, huge force); end-effectors — grippers (parallel/angular/
        vacuum/magnetic); actuator-vs-end-effector; analog vs digital + ADC; choose via P-C-R-I.
[ ] 8.1 Device data: four streams M-C-D-O; diagnostic vs optimisation (purpose decides); obtain (polling/interrupts,
        sampling rate); process (calibrate/filter/validate); store safely with T-I-U [SE-11-04].
[ ] 8.2 Power & wiring: V-I-P + P = V x I; power budget (actuator dominates, +20% margin); battery sizing
        (amp-hours over amps, ~80% usable); wiring diagram = power lines vs data lines + one common ground;
        never drive an actuator off a controller pin (use a driver); fuse/gauge/strain-relief/isolation/E-stop.
[ ] 8.3 Accessibility: specialist requirements S-A-I-D (+reliability/affordability); design WITH not FOR;
        alternative inputs (switch/voice/eye-gaze) + V-A-H feedback; universal design + the curb-cut effect [SE-11-05].

BRIDGE -> Ch 09: we have the devices, their data, and the power/wiring. Next we write the THINK —
the control algorithms (open vs closed loop, autonomous control) that turn readings into actions.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| CPU | Central Processing Unit | The processor that executes program instructions |
| M-C-D-O | Measurement · Control · Diagnostic · Optimisation | The four data streams a mechatronic system handles |
| P-C-R-I | Performance · Cost · Reliability · Integration | Criteria for choosing a hardware component |
| S-A-E | Sensor · Actuator · End-effector | The mechatronic device trio (input, output, tool) |
| S-A-I-D | Safety · Adaptability · Independence · Diverse I/O | The specialist (accessibility) requirements checklist |
| S-M-E-M | Software · Mechanical · Electronics · Maths | The knowledge fields combined in a mechatronic build |
| Sense-Think-Act | Sense · Think · Act | The repeating control loop of an autonomous / mechatronic system |
| T-I-U | Timestamp · Identity (which sensor) · Units | What to record with device/sensor data |
| V-A-H | Visual · Audio · Haptic | Multi-modal feedback channels |
| V-I-P | Voltage · current (I) · Power | The electrical quantities (P = V × I) |
