---
title: "Supplementary Materials — Module Review: Programming and Building Mechatronics"
module: PM11
year: 11
lesson: "7–10"
script: script.md
---

# Supplementary Materials

The whole-module revision pack for Programming Mechatronics (Chapters 07–10). Nothing here is spoken in
the audio — the narration points at each listing by label only. Listing 1 is the master mnemonic table;
Listing 2 is one capstone runnable tying the module together; Listing 3 is the build-project checklist.

### Listing 1 — Master mnemonic table for the whole module (the exam-dump) (reference)
```text
THE SPINE:  SENSE -> THINK -> ACT  (S-T-A)  ·  the four fields S-M-E-M (Software/Mechanical/Electronics/Maths)

CH 07 FOUNDATIONS
  applications across fields, each with a DOMINANT requirement
  C-M-I  microcontroller = CPU core + Memory + I/O pins on a chip (a CPU is just the processor)
  F-D-E  Fetch-Decode-Execute  ·  "address is where, data is what" (address vs data registers)
  S-A-E  Sensor / Actuator / End-effector  ·  "actuator moves; end-effector does the job"
  P-C-R-I  choose a component: Performance / Cost / Reliability / Integration  ·  analog -> ADC

CH 08 DATA & INTEGRATION
  M-C-D-O  data streams: Measurement / Control / Diagnostic / Optimisation
  "diagnostic asks is-it-healthy?; optimisation asks can-it-do-better?"  ·  "polling asks; interrupts tell"
  process: calibrate -> filter -> validate  ·  T-I-U log entry: Timestamp / Identity / Units
  V-I-P  Voltage / current I / Power ;  P = V x I  ·  "amp-hours over amps gives hours" (battery)
  "power lines feed, data lines talk, on one common ground"  ·  never run an actuator off a controller pin
  S-A-I-D  specialist requirements: Safety / Adaptability / Independence / Diverse-I-O  ·  "design WITH, not FOR"
  V-A-H feedback (Visual/Audio/Haptic)  ·  the curb-cut effect

CH 09 CONTROL ALGORITHMS
  "closed loops listen; open loops are blind"  ·  M-C-C  Measure-Compare-Correct (error = setpoint - measured)
  S-D-A-F  autonomous code: Sensing / Decision / Adapt / Fail-safe  ·  "autonomous = decides without a human"
  S-T-E-A  state machine: States / Transitions / Events / Actions  ·  hysteresis: "two limits, not one, stops the chatter"
  DOF = degrees of freedom = independent ways to move  ·  "one conductor, clean interfaces" (subsystem composition)

CH 10 PROGRAMMING & BUILDING
  S-C-F  simulate first: Safe / Cheap / Fast  ·  "low-fidelity first"  ·  "validate against known results"
  P-I-D  "P present, I past, D predicts the future"  ·  always CLAMP the output
  "program to the interface, not the device"  (integrate S-A-E devices; modular + testable)
  S-A-F-E control UI: Status / Abort / Feedback / Errors-validated  ·  "never hide state"
  E-R  unit tests: Effectiveness / Repeatability  ·  reuse FIRST, U-S-S (OOP) + B-P-F test data (PF11)  ·  document (SE-11-09)
```

### Listing 2 — Capstone: an accessible line-following delivery robot's control core (Python, runnable)
```python
def decide(left_on_line, right_on_line, estop):
    """The robot's THINK: autonomous decision (state-machine style) with a fail-safe AND an
    emergency stop -- it ties together autonomy (9.2), state machines (9.3) and safety (8.x)."""
    if estop:                                  # SAFETY overrides everything (S-A-F-E / fail-safe)
        return "stop"
    if left_on_line and right_on_line:
        return "forward"
    if left_on_line:
        return "turn_left"                     # self-correct toward the line (closed loop)
    if right_on_line:
        return "turn_right"
    return "search"                            # FAIL-SAFE: line lost -> don't barrel on


# UNIT TEST (E-R): effectiveness across all cases + the fail-safe + the emergency-stop path; repeatable.
cases = {
    (True,  True,  False): "forward",
    (True,  False, False): "turn_left",
    (False, True,  False): "turn_right",
    (False, False, False): "search",           # fail-safe: line lost
    (True,  True,  True):  "stop",             # emergency stop overrides the drive decision
}
for (left, right, estop), expected in cases.items():
    assert decide(left, right, estop) == expected

assert decide(False, False, False) == "search"     # line-lost ALWAYS fails safe (repeatable)
print("Capstone robot control: drive, fail-safe and emergency-stop cases all pass.")
```

### Listing 3 — The real-world build project, end to end (reference)
```text
DESIGN/BUILD A MECHATRONIC SYSTEM FOR A REAL PROBLEM (SE-11-01..09) -- walk Sense-Think-Act:
e.g. an ACCESSIBLE line-following delivery robot.

  1  WHAT + WHY      mechatronics = S-M-E-M; outline the application + its dominant requirement (7.1)
  2  THE BRAIN       a microcontroller (C-M-I) runs the program; lean code for tight hardware (7.2)
  3  THE DEVICES     pick S-A-E: line/light sensors, drive motors (actuators), a tray/gripper (end-effector) (7.3)
  4  THE DATA        M-C-D-O; sample, filter, validate; log diagnostics (T-I-U) (8.1)
  5  POWER + WIRING  V-I-P budget (actuator dominates), size battery (amp-hours/amps), data vs power lines (8.2)
  6  ACCESSIBLE      specialist requirements S-A-I-D; design WITH users; V-A-H feedback; low-force e-stop (8.3)
  7  CONTROL         open vs closed loop (9.1); autonomous S-D-A-F (9.2); state machine S-T-E-A (9.3);
                     DOF + constraints + compose subsystems "one conductor, clean interfaces" (9.4)
  8  SIMULATE        model + test the control code first -- S-C-F; low-fidelity prototype (10.1)
  9  IMPLEMENT       closed-loop controller in code, P-I-D, clamp the output (10.2)
  10 INTEGRATE       drive the S-A-E devices "program to the interface, not the device" (10.3)
  11 USER INTERFACE  command it + show state, S-A-F-E (10.4)
  12 UNIT TEST       each component for E-R; B-P-F data; test failure paths; DOCUMENT results (10.5)

CASE STUDIES (what gets it wrong): 737 MAX MCAS (autonomy on one bad sensor) · Therac-25 (control + missing
  safety/testing) · DARPA Grand Challenge (autonomy + simulate-first, failure 2004 -> success 2005).

BRIDGE TO YEAR 12: control/autonomy -> Software Automation (AI) · safety + safe data -> Secure Software
  Architecture · the build + manage-and-document discipline -> the Software Engineering Project.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| AI | Artificial Intelligence | Software that performs tasks normally needing human intelligence |
| B-P-F | Boundary · Path coverage · Faulty-and-abnormal | Categories of test data (actual vs expected) |
| CPU | Central Processing Unit | The processor that executes program instructions |
| DARPA | Defense Advanced Research Projects Agency | The US defence R&D agency (ran the autonomous-vehicle Grand Challenge) |
| DOF | Degrees Of Freedom | The number of independent movements a mechatronic system (e.g. a robot arm) can make |
| M-C-C | Measure · Compare · Correct | The closed-loop control cycle (error = setpoint − measured) |
| M-C-D-O | Measurement · Control · Diagnostic · Optimisation | The four data streams a mechatronic system handles |
| MCAS | Maneuvering Characteristics Augmentation System | The flight-control software implicated in the Boeing 737 MAX crashes |
| OOP | Object-Oriented Programming | A paradigm structuring software around objects that bundle data and behaviour |
| P-C-R-I | Performance · Cost · Reliability · Integration | Criteria for choosing a hardware component |
| S-A-E | Sensor · Actuator · End-effector | The mechatronic device trio (input, output, tool) |
| S-A-F-E | Status · Abort · Feedback · Errors | Design principles for a safe control interface |
| S-A-I-D | Safety · Adaptability · Independence · Diverse I/O | The specialist (accessibility) requirements checklist |
| S-C-F | Safe · Cheap · Fast | Why to simulate before you build |
| S-D-A-F | Sensing · Decision logic · Adapt/self-correct · Fail-safe | The four features of an autonomous control algorithm |
| S-M-E-M | Software · Mechanical · Electronics · Maths | The knowledge fields combined in a mechatronic build |
| S-T-E-A | States · Transitions · Events · Actions | The parts of a state machine |
| Sense-Think-Act | Sense · Think · Act | The repeating control loop of an autonomous / mechatronic system |
| T-I-U | Timestamp · Identity (which sensor) · Units | What to record with device/sensor data |
| U-S-S | Unit · Subsystem · System | The levels of testing |
| UI | User Interface | The parts of a system a user directly interacts with |
| V-A-H | Visual · Audio · Haptic | Multi-modal feedback channels |
| V-I-P | Voltage · current (I) · Power | The electrical quantities (P = V × I) |
