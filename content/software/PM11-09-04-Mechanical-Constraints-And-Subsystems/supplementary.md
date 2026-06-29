---
title: "Supplementary Materials — Mechanical Constraints and Subsystem Composition"
module: PM11
year: 11
lesson: "9.4"
script: script.md
---

# Supplementary Materials

The read-along reference for the constraints-and-composition lesson. Nothing here is spoken in the audio
— the narration points at each listing by label only. Listing 1 models a robot arm's degrees of freedom
and joint limits; Listing 2 composes subsystems under one coordinator; Listing 3 is the revision reference.

### Listing 1 — Degrees of freedom and motion constraints for a robot arm (Python, runnable)
```python
class RoboticArm:
    """3 joints + a gripper = 4 degrees of freedom. Each joint's angle RANGE is a motion
    constraint the software must respect — never command a joint past its limit."""

    JOINT_LIMITS = {                 # (min, max) angle in degrees = the constraint per joint
        "base":     (-180, 180),
        "shoulder": (-90, 90),
        "elbow":    (0, 135),
        "gripper":  (0, 90),
    }

    def degrees_of_freedom(self):
        return len(self.JOINT_LIMITS)              # 4 independent ways it can move

    def is_valid(self, **angles):
        # Every commanded angle must lie within that joint's allowed range.
        for joint, angle in angles.items():
            low, high = self.JOINT_LIMITS[joint]
            if not (low <= angle <= high):
                return False
        return True


arm = RoboticArm()
assert arm.degrees_of_freedom() == 4
assert arm.is_valid(base=45, shoulder=30, elbow=90, gripper=20) is True    # all within limits
assert arm.is_valid(elbow=200) is False                                    # elbow max is 135 -> rejected
print("DOF:", arm.degrees_of_freedom(), "| in-range move valid; out-of-range elbow rejected")
```

### Listing 2 — Composing subsystems under one coordinator (Python, runnable)
```python
class Subsystem:
    """A modular subsystem behind a CLEAN, uniform interface: command() and stop()."""
    def __init__(self, name):
        self.name = name
        self.state = "idle"
    def command(self, action):
        self.state = action
    def stop(self):
        self.state = "stopped"


class Robot:
    """COMPOSITION (has-a, from OOP): the robot HAS a drive, an arm and a vision subsystem.
    ONE coordinator (a single control authority) drives them all through the same interface."""
    def __init__(self):
        self.subsystems = {
            "drive":  Subsystem("drive"),
            "arm":    Subsystem("arm"),
            "vision": Subsystem("vision"),
        }
    def coordinate(self, plan):
        for name, action in plan.items():
            self.subsystems[name].command(action)
    def emergency_stop(self):
        for s in self.subsystems.values():      # one stop propagates to EVERY subsystem
            s.stop()


robot = Robot()
robot.coordinate({"vision": "scan", "drive": "forward", "arm": "ready"})
assert robot.subsystems["drive"].state == "forward"
robot.emergency_stop()
assert all(s.state == "stopped" for s in robot.subsystems.values())   # all halt together
print("Composed robot coordinated 3 subsystems, then emergency-stopped them all.")
```

### Listing 3 — Constraints and composition: revision reference (reference)
```text
DEGREES OF FREEDOM (DOF) = the number of INDEPENDENT ways a system can move.
  door hinge            1 DOF   rotation about one axis
  2-joint planar arm    2 DOF   X-Y position in a plane
  3D printer head       3 DOF   X, Y, Z translation
  gripper               1 DOF   open / close
  6-axis robot arm      6 DOF   full 3D position + orientation
  -> count DOF by counting the independent movements (each driven by its own actuator).

MOTION CONSTRAINTS = the physical limits the software must respect:
  joint angle ranges (min/max) · workspace reach (max + min) · payload + speed limits ·
  collisions / interference. Validate EVERY commanded move against these before sending it.

COMBINING SUBSYSTEMS (composition = OOP "has-a", applied to hardware):
  a robot HAS-A drive + arm + vision; each is a module behind a CLEAN INTERFACE.
  Coordination principles — "one conductor, clean interfaces":
    SINGLE control authority (one coordinator decides) · CLEAR communication protocols ·
    MODULAR interfaces (swap a subsystem without rewriting the rest) · FAILURE detection + recovery
    (one emergency stop halts every subsystem together).

VIABLE SUBSYSTEM = a working combination of Sensor + Actuator + End-effector (S-A-E) that
  achieves one job (e.g. vision sensor + arm actuators + gripper = a pick subsystem).

COLLISION / INTERFERENCE: when subsystems share a workspace they have DEPENDENCIES — coordinate
  their timing and keep a safety margin so moving parts don't hit each other.
```
