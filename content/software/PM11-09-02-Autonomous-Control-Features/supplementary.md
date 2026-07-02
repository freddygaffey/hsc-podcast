---
title: "Supplementary Materials — Autonomous Control Features"
module: PM11
year: 11
lesson: "9.2"
script: script.md
---

# Supplementary Materials

The read-along reference for the autonomy lesson. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 is a runnable autonomous line-follower; Listing 2 is the
autonomous control loop in NESA pseudocode; Listing 3 is the revision reference (levels + features).

### Listing 1 — An autonomous line-following robot: decide with no human, fail safe (Python, runnable)
```python
def decide(left_on_line, right_on_line):
    """The autonomy: a tiny state machine that keeps the line centred — and crucially,
    it returns an action with NO human input. The last branch is the FAIL-SAFE."""
    if left_on_line and right_on_line:
        return "forward"        # both sensors on the line -> go straight
    if left_on_line and not right_on_line:
        return "turn_left"      # drifting right -> self-correct to the left
    if right_on_line and not left_on_line:
        return "turn_right"     # drifting left  -> self-correct to the right
    return "search"             # FAIL-SAFE: line lost -> stop & search, never barrel on blindly


# An autonomous run: a stream of (left, right) sensor readings, each decided WITHOUT a human.
readings = [(True, True), (True, False), (False, True), (False, False)]
actions = [decide(l, r) for (l, r) in readings]

assert actions == ["forward", "turn_left", "turn_right", "search"]
assert decide(False, False) == "search"      # line lost MUST fail safe, never "forward"
print("Autonomous line-follower decisions:", actions)
```

### Listing 2 — The autonomous control loop in NESA pseudocode (reference)
```text
BEGIN AutonomousControl
    REPEAT                                   // runs on its own — NO human in the loop
        readings = READ all sensors          // CONTINUOUS sensing
        IF a safety interlock is tripped THEN
            ENTER safe state (stop / shut down)     // FAIL-SAFE: catch the dangerous unexpected
        ELSE
            action = DECIDE from readings            // DECISION logic (rules / a state machine)
            DO action                                // ACT
            // next loop re-reads the result and self-corrects -> a closed loop (from 9.1)
        ENDIF
    UNTIL powered off

  Contrast — REMOTE / MANUAL control:  WAIT for a human command -> DO exactly that command.
  (No autonomous DECIDE step; the human is the brain.)
END
```

### Listing 3 — Autonomy levels and the features of autonomous code (reference)
```text
AUTONOMOUS = the system DECIDES for itself, with no human in the loop.  (Not "it has a motor".)

THE FOUR FEATURES of an autonomous control algorithm — S-D-A-F:
  S  continuous SENSING        always watching the world (many readings per second)
  D  DECISION logic            rules or a STATE MACHINE turning readings into actions
  A  ADAPT / self-correct      closed-loop feedback (9.1) — measure the result, correct next loop
  F  FAIL-SAFE                 handle uncertainty + edge cases; on danger, stop / safe state / fallback

AUTONOMY LEVELS (a spectrum, 0 -> 5):
  0  Manual         human controls everything (remote-controlled arm)
  1  Assistance     simple automatic task, human can override (auto door)
  2  Partial        handles routine ops, human supervises (robot mower)
  3  Conditional    decides from sensor data, human ready to take over (self-parking)
  4  High           handles most situations, human only for edge cases (adaptive industrial robot)
  5  Full           operates entirely independently (autonomous spacecraft navigation)

SAFETY FOR AUTONOMY:
  SAFETY INTERLOCK  an automatic check that BLOCKS a dangerous action before it happens
  FALLBACK          a backup plan when the primary action fails -> graceful degradation, not collapse
  "keep a human in the loop for the critical decisions"  ;  test autonomous behaviour exhaustively

AUTONOMOUS vs REMOTE/MANUAL: autonomy is the DECIDE-without-a-human step. Remote control = a human
decides and the machine obeys. The motor can be identical; the difference is WHO decides.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| S-D-A-F | Sensing · Decision logic · Adapt/self-correct · Fail-safe | The four features of an autonomous control algorithm |
