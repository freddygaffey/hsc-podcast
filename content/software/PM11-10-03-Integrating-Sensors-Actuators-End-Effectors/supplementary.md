---
title: "Supplementary Materials — Integrating Sensors, Actuators and End Effectors"
module: PM11
year: 11
lesson: "10.3"
script: script.md
---

# Supplementary Materials

The read-along reference for the integration lesson. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 integrates a sensor, actuator and end-effector into a
pick-and-place sequence; Listing 2 shows one interface driving many devices; Listing 3 is the reference.

### Listing 1 — Integrate a sensor, actuator and end-effector: a pick-and-place sequence (Python, runnable)
```python
# A clean INTERFACE per device type: every sensor has read(); every driven device has drive().
class PositionSensor:
    def __init__(self, value):
        self._value = value
    def read(self):                       # SENSE
        return self._value

class ArmActuator:
    def __init__(self):
        self.position = 0
    def drive(self, target):              # ACT: move
        self.position = target

class Gripper:                            # the END-EFFECTOR
    def __init__(self):
        self.closed = False
    def drive(self, close):               # EFFECT: do the job
        self.closed = close


class PickAndPlace:
    """Integration: the control logic talks to each device only through its interface --
    it never needs to know HOW a device works internally (program to the interface)."""
    def __init__(self, sensor, arm, gripper):
        self.sensor, self.arm, self.gripper = sensor, arm, gripper

    def run(self):
        target = self.sensor.read()       # 1. SENSE where the object is
        self.arm.drive(target)            # 2. ACT: move the arm there  (order matters)
        self.gripper.drive(True)          # 3. EFFECT: close the gripper to grab it
        return self.arm.position, self.gripper.closed


robot = PickAndPlace(PositionSensor(75), ArmActuator(), Gripper())
position, closed = robot.run()
assert position == 75          # arm moved to the sensed object position
assert closed is True          # gripper closed on it
print("Pick-and-place: arm at", position, "| gripper closed:", closed)
```

### Listing 2 — One interface, many devices: polymorphic drive and emergency stop (Python, runnable)
```python
class Device:
    """Every device shares the SAME interface: drive() and stop(). The control logic can treat
    a motor, a pump and a gripper identically -- that's polymorphism (OOP) applied to hardware."""
    def __init__(self, name):
        self.name = name
        self.active = False
    def drive(self):
        self.active = True
    def stop(self):
        self.active = False


def stop_all(devices):
    for d in devices:                 # ONE loop halts every device through the same interface
        d.stop()


devices = [Device("drive motor"), Device("pump"), Device("gripper")]
for d in devices:
    d.drive()
assert all(d.active for d in devices)        # all running

stop_all(devices)
assert not any(d.active for d in devices)    # one polymorphic stop reached every device
print("Uniform interface drove then stopped", len(devices), "different device types with one loop.")
```

### Listing 3 — Integration via interfaces: revision reference (reference)
```text
THE PROBLEM: each device has different connections, data formats and timing. Mixing those details
into the control logic gives tangled, untestable code.

THE FIX -- INTERFACE ABSTRACTION: define WHAT a device does, not HOW.
  a SENSOR interface = read()        (return a value)
  a driven device (ACTUATOR / END-EFFECTOR) interface = drive() / set_output()  (+ stop())
  The control logic talks ONLY to the interface -> "PROGRAM TO THE INTERFACE, NOT THE DEVICE."

BENEFITS (this is OOP abstraction + polymorphism, applied to hardware):
  MODULARITY     swap a device for another that implements the same interface -> no change to control logic
  TESTABILITY    drop in SIMULATED devices behind the same interface (10.1) -> test with no hardware
  MAINTAINABILITY  device drivers stay separate from application logic
  FLEXIBILITY    one control loop drives many device types (polymorphism)

INTEGRATING S-A-E FOR A TASK (order + timing matter):
  1. SENSE   read the sensor(s); fuse/interpret multiple readings if needed
  2. ACT     drive the actuator(s) to position           <- must happen BEFORE the end-effector acts
  3. EFFECT  drive the end-effector (gripper/tool) to do the job
  e.g. pick-and-place: read object position -> move arm there -> close gripper.
  Wrong order (close the gripper before the arm arrives) grabs nothing -> sequencing is part of the code.

SAFETY: a shared stop()/emergency-stop across the interface halts every device together (from 9.4).
```
