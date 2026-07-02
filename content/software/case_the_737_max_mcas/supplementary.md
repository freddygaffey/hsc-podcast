---
title: "Supplementary Materials — The 737 MAX and MCAS"
module: PM11
year: 11
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the 737 MAX case study. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 is the timeline; Listing 2 is a runnable contrast of
single-sensor versus cross-checked control; Listing 3 maps the engineering lessons onto the module.

### Listing 1 — Timeline (reference)
```text
2011        Boeing launches the 737 MAX: re-engine the existing 737 with larger, more efficient
            engines, kept marketable as the "same type" so airlines avoid costly new pilot training.
~2012-16    The bigger engines, mounted further forward and up, give a nose-up pitching tendency at
            high angle of attack. Boeing adds MCAS (Maneuvering Characteristics Augmentation System):
            software that automatically trims the nose DOWN to make the MAX handle like the old 737.
            MCAS reads ONE angle-of-attack sensor (of the two fitted). No cross-check. Most pilots are
            not told MCAS exists; it is largely absent from the manuals and training.
2017        737 MAX enters commercial service.
29 Oct 2018 LION AIR FLIGHT 610 (737 MAX 8) crashes into the Java Sea ~13 minutes after take-off from
            Jakarta. A miscalibrated angle-of-attack sensor feeds a false reading; MCAS repeatedly
            trims the nose down; the crew cannot recover. All 189 people on board are killed.
Nov 2018    Boeing/FAA issue a bulletin pointing pilots to the runaway-stabiliser-trim procedure --
            but MCAS itself is still barely explained. The fleet keeps flying.
10 Mar 2019 ETHIOPIAN AIRLINES FLIGHT 302 (737 MAX 8) crashes ~6 minutes after take-off from Addis
            Ababa near Bishoftu, in a strikingly similar sequence. All 157 people on board are killed.
Mar 2019    Aviation regulators worldwide ground the entire 737 MAX fleet. Total lives lost: 346.
2019-20     Investigations fault the single-sensor design, MCAS's authority, and the lack of
            disclosure/training, alongside commercial and regulatory pressure.
Nov 2020+   The MAX returns to service after MCAS is re-designed: it compares BOTH sensors and will
            not activate if they disagree; it acts only once per event; its authority is limited; and
            pilots are trained on it. Boeing pays billions in settlements and penalties.
```

### Listing 2 — One sensor versus a cross-check: the core engineering lesson (Python, runnable)
```python
def mcas_single_sensor(aoa_reading, threshold=15.0):
    """THE FLAW: trust ONE angle-of-attack sensor. If that one sensor lies, the system acts on the lie."""
    return "push nose down" if aoa_reading > threshold else "no action"


def mcas_dual_sensor(aoa_left, aoa_right, threshold=15.0, max_disagree=5.5):
    """THE FIX: compare BOTH sensors. If they DISAGREE, distrust the data and do nothing -- a fail-safe --
    rather than act on a possibly-faulty reading."""
    if abs(aoa_left - aoa_right) > max_disagree:
        return "sensors disagree -> stand down (fail-safe)"
    angle = (aoa_left + aoa_right) / 2          # they agree -> safe to use (a simple sensor fusion)
    return "push nose down" if angle > threshold else "no action"


# A faulty LEFT sensor reads 25 degrees (jammed high); the true angle (right sensor) is a safe 2.
assert mcas_single_sensor(25.0) == "push nose down"                 # acts on the lie -> nose into the ground
assert mcas_dual_sensor(25.0, 2.0).startswith("sensors disagree")   # cross-check catches it -> stands down
# When both sensors agree on a genuinely high angle, the system acts as intended.
assert mcas_dual_sensor(18.0, 17.5) == "push nose down"
# When both agree it is safe, it stays quiet.
assert mcas_dual_sensor(2.0, 2.5) == "no action"
print("Single sensor trusts the lie; the dual-sensor cross-check catches the disagreement and stands down.")
```

### Listing 3 — The engineering lessons, mapped to the module (reference)
```text
The 737 MAX is "Sense-Think-Act with a broken SENSE": the Think and Act worked exactly as written --
they were just fed a lie by one sensor, and built to trust it.

1  REDUNDANCY / NO SINGLE POINT OF FAILURE
   A safety-critical input must not depend on ONE sensor. Compare two (or three) and cross-check; on
   disagreement, distrust the data. (7.3 sensors; 8.1 validate readings; Listing 2.)

2  A CONTROL SYSTEM IS ONLY AS TRUSTWORTHY AS ITS SENSOR
   Closed-loop control corrects toward what it MEASURES. Feed it a false measurement and it will
   "correct" the aircraft straight into danger -- confidently. (9.1 closed loop; 8.1 calibrate/validate.)

3  AUTONOMY MUST NOT QUIETLY OVERRIDE THE HUMAN
   MCAS acted repeatedly, was hard to override, and pilots were not even told it existed. Autonomous
   control needs disclosure, an easy override, a fail-safe, and a human kept in the loop. (9.2 autonomy
   features + fail-safe; 8.3 design WITH users / transparency; 10.4 a S-A-F-E control interface.)

4  TEST THE FAILURE PATHS, NOT JUST THE HAPPY PATH
   "What if a sensor is wrong?" had to be a tested case. Unit-test the faulty/boundary inputs in
   simulation before flight. (10.5 effectiveness + repeatability, B-P-F test data; 10.1 simulate first.)

5  DON'T LET COMMERCIAL PRESSURE REMOVE SAFETY
   The drive to avoid retraining shaped the design. Echoes Therac-25 removing hardware interlocks: when
   cost or schedule quietly overrules safety engineering, people die.

CASHED IN BY: PM11 9.1 (open vs closed loop), 9.2 (autonomous control), 7.3 (sensors/redundancy),
8.3 (safety + inclusive design). A companion to case_therac_25 (control + safety + testing).
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| B-P-F | Boundary · Path coverage · Faulty-and-abnormal | Categories of test data (actual vs expected) |
| MCAS | Maneuvering Characteristics Augmentation System | The flight-control software implicated in the Boeing 737 MAX crashes |
| S-A-F-E | Status · Abort · Feedback · Errors | Design principles for a safe control interface |
| Sense-Think-Act | Sense · Think · Act | The repeating control loop of an autonomous / mechatronic system |
