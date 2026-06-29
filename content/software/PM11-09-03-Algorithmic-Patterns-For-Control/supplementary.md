---
title: "Supplementary Materials — Algorithmic Patterns for Control"
module: PM11
year: 11
lesson: "9.3"
script: script.md
---

# Supplementary Materials

The read-along reference for the control-patterns lesson. Nothing here is spoken in the audio — the
narration points at each listing by label only. Listing 1 DEVELOPS a traffic-light state machine;
Listing 2 MODIFIES it to add a pedestrian request; Listing 3 is the patterns reference + pseudocode.

### Listing 1 — Develop: a traffic-light state machine (Python, runnable)
```python
# A state machine: each STATE has a duration; an EVENT (the timer running out) fires a TRANSITION.
DURATIONS = {"RED": 2, "GREEN": 3, "YELLOW": 1}        # ticks each state lasts
NEXT      = {"RED": "GREEN", "GREEN": "YELLOW", "YELLOW": "RED"}   # the transition table

def run(steps):
    state, timer = "RED", DURATIONS["RED"]
    sequence = []
    for _ in range(steps):
        sequence.append(state)            # ACTION: (here, just record which light is on)
        timer -= 1
        if timer <= 0:                    # EVENT: this state's time is up
            state = NEXT[state]           # TRANSITION to the next state
            timer = DURATIONS[state]
    return sequence

# RED lasts 2 ticks, GREEN 3, YELLOW 1, then back to RED.
assert run(6) == ["RED", "RED", "GREEN", "GREEN", "GREEN", "YELLOW"]
print("Traffic-light sequence:", run(7))
```

### Listing 2 — Modify: add a pedestrian request (a small, localised change) (Python, runnable)
```python
DURATIONS = {"RED": 2, "GREEN": 3, "YELLOW": 1}
NEXT      = {"RED": "GREEN", "GREEN": "YELLOW", "YELLOW": "RED"}

def run(steps, walk_at=None):
    state, timer = "RED", DURATIONS["RED"]
    sequence = []
    for i in range(steps):
        sequence.append(state)
        # THE MODIFICATION: a pending walk request ends GREEN at the next tick.
        # One new rule, in one place — the rest of the machine is untouched.
        if state == "GREEN" and walk_at is not None and i >= walk_at:
            timer = 1
        timer -= 1
        if timer <= 0:
            state = NEXT[state]
            timer = DURATIONS[state]
    return sequence

normal = run(6)                 # no request: GREEN runs its full 3 ticks
walk   = run(6, walk_at=2)      # WALK pressed at the first GREEN tick: GREEN ends early

assert normal == ["RED", "RED", "GREEN", "GREEN", "GREEN", "YELLOW"]
assert walk   == ["RED", "RED", "GREEN", "YELLOW", "RED", "RED"]   # GREEN cut short -> YELLOW sooner
print("normal:", normal, "| with walk request:", walk)
```

### Listing 3 — Control patterns and a generic state machine in pseudocode (reference)
```text
A STATE MACHINE has four parts — S-T-E-A:
  STATES        the distinct modes the system can be in (Idle, Running, Error...)
  TRANSITIONS   the allowed moves between states
  EVENTS        the triggers that fire a transition (a button, a sensor, a timer)
  ACTIONS       what happens on entering / leaving / while in a state (enable motor, sound alarm)

WHY a state machine beats a tangle of if-statements: it's clear, predictable, easy to TEST, and
easy to MODIFY — add a state or a transition in ONE place instead of threading flags everywhere.

GENERIC STATE MACHINE — NESA pseudocode:
  BEGIN StateMachine
      state = initial state
      REPEAT
          event = WAIT FOR / READ an event           // button, sensor, timer
          IF a transition exists for (state, event) THEN
              run EXIT action of the old state
              state = the new state
              run ENTRY action of the new state
          ENDIF
      UNTIL powered off
  END

OTHER CONTROL PATTERNS (pick the pattern that fits the job):
  THRESHOLD + HYSTERESIS   act when a reading crosses a limit; use TWO limits (a deadband) so the
                           output doesn't chatter on/off around a single point (e.g. heater on at 19,
                           off at 21 — not both at 20)
  TIMED SEQUENCE           fixed steps on a clock (an open-loop wash cycle)
  EVENT / INTERRUPT        respond the instant something happens, instead of polling for it
  SCHEDULING               coordinate many tasks; priority-based = the most critical/urgent runs first
                           (safety at the highest rate), rate-monotonic = faster tasks get priority

DEVELOP vs MODIFY (the dot-point verbs): DEVELOP = build the machine; MODIFY = change behaviour with a
small localised edit (Listing 2 added one rule); APPLY = map the pattern onto a real system.
```
