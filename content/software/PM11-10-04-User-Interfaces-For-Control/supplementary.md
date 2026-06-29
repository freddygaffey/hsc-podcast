---
title: "Supplementary Materials — User Interfaces for Control"
module: PM11
year: 11
lesson: "10.4"
script: script.md
---

# Supplementary Materials

The read-along reference for the control-UI lesson. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 is a command-line control panel (commands in);
Listing 2 formats sensor data into operator feedback (status out); Listing 3 is the revision reference.

### Listing 1 — A command-line control panel: commands in, validated, with an always-available stop (Python, runnable)
```python
class ControlPanel:
    """A text UI for a mechatronic system. Commands IN, status OUT, and an Abort that's always
    available. Every command is VALIDATED before it touches the machine (the E in S-A-F-E)."""

    def __init__(self):
        self.position = 0
        self.stopped = False

    def handle(self, command):
        parts = command.split()
        verb = parts[0] if parts else ""

        if verb == "stop":
            self.stopped = True
            return "STOPPED"                                  # ABORT: always works, even mid-task
        if verb == "reset":
            self.stopped = False
            return "ready"
        if verb == "status":
            return f"position={self.position} stopped={self.stopped}"   # STATUS / FEEDBACK out

        if self.stopped:
            return "blocked: emergency stop active (reset first)"       # refuse to move while stopped
        if verb == "move":
            if len(parts) != 2:
                return "error: move needs one number"                   # ERRORS: validate shape
            try:
                target = int(parts[1])
            except ValueError:
                return "error: not a number"                            # ERRORS: validate type
            if not (0 <= target <= 100):
                return "error: out of safe range 0..100"                # ERRORS: reject unsafe value
            self.position = target
            return f"moving to {target}"
        return "error: unknown command"


ui = ControlPanel()
assert ui.handle("move 40") == "moving to 40"
assert ui.handle("move 999") == "error: out of safe range 0..100"   # unsafe command rejected
assert ui.handle("stop") == "STOPPED"
assert ui.handle("move 10").startswith("blocked")                   # commands blocked after a stop
assert ui.handle("reset") == "ready"
assert ui.handle("status") == "position=40 stopped=False"           # status shows the last SAFE state
print("Control panel: validated commands, blocked after stop, resumed after reset.")
```

### Listing 2 — Turn sensor data into clear operator feedback — never hide system state (Python, runnable)
```python
def format_status(sensor_readings):
    """The 'status out' half of the UI: turn raw sensor data into clear FEEDBACK for the operator,
    and FLAG a failed sensor instead of hiding it (hiding state is the dangerous mistake)."""
    lines = []
    for name, value, unit in sensor_readings:
        if value is None:
            lines.append(f"{name}: no reading  <-- WARNING")     # surface the fault
        else:
            lines.append(f"{name}: {value} {unit}")
    return "\n".join(lines)


status = format_status([("battery", 78, "%"), ("temperature", 41, "C"), ("range", None, "cm")])
assert "battery: 78 %" in status
assert "range: no reading  <-- WARNING" in status        # the failed sensor is flagged, not hidden
print(status)
```

### Listing 3 — Designing a control UI: principles and types (reference)
```text
A control UI is the system's VOICE: it takes the operator's commands IN and shows the system's state OUT.

DESIGN PRINCIPLES -- S-A-F-E:
  S  STATUS        always show clearly what the system is doing -- NEVER hide state from the operator
  A  ABORT         an emergency stop that is always available, obvious, and low-force (8.2/8.3) -- halts instantly
  F  FEEDBACK      turn sensor data into information the operator understands; flag faults/warnings
  E  ERRORS        validate every command; reject unsafe/invalid input with a clear message; confirm dangerous actions
  (+ ACCESSIBLE: design WITH users, offer alternative inputs + multi-modal V-A-H feedback -- from 8.3)

UI TYPES (pick to fit the system + user):
  status LED/light   simplest -- one bit of state          command line (CLI)  precise, scriptable, easy to log
  buttons / panel    physical controls + indicators        graphical dashboard rich status + controls on a screen
  A graphical UI maps the SAME underlying model: a "Move" button issues the same command the CLI's "move" does;
  a gauge shows the same sensor value the status line prints. Design the control logic once; the UI is a skin over it.

UI = the MANUAL / human-control complement to AUTONOMOUS control (9.2): even an autonomous system needs a UI to
  monitor it, override it, and stop it. Commands map to actions; sensor data maps to feedback.
```
