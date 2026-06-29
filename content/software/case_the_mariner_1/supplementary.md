---
title: "Supplementary Materials — Mariner 1"
module: PF11
year: 11
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Mariner 1 case study. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 is the timeline; Listing 2 demonstrates the missing-smoothing
bug in runnable code; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
1962        NASA's Mariner program aims to send the first US spacecraft to another planet -- Mariner 1,
            a flyby of Venus. The launch vehicle is an Atlas-Agena rocket, steered in its early flight by
            ground-based radar guidance feeding commands to the rocket's onboard guidance.
22 Jul 1962 Mariner 1 launches from Cape Canaveral. Soon after lift-off, the rocket's guidance antenna
            performs poorly and the booster loses its lock on the smooth ground-guidance signal, falling
            back on its onboard guidance equations -- which contained a transcription error.
+~290 sec   With the noisy data and the flawed equation, the software issues erratic steering commands.
            The rocket veers toward a dangerous trajectory; the range safety officer sends the destruct
            command about 290 seconds after lift-off, destroying the vehicle over the Atlantic.
After       Investigators trace the software fault to a missing "overbar" -- a small bar written over a
            symbol in the hand-transcribed guidance equation, telling the program to use a SMOOTHED
            (averaged) value of the radius rate. Omitted, the code reacted to raw noise as if it were real
            motion. Cost: about US$18 million (1962). Arthur C. Clarke called it "the most expensive
            hyphen in history". (The popular "missing hyphen" is really this missing overbar.)
```

### Listing 2 — The missing "overbar": why smoothing mattered (Python, runnable)
```python
def steer(rate, gain=10):
    """Steering correction, proportional to the measured radius-rate. Feed it raw, noisy data and a
    single noise spike produces a wild correction."""
    return gain * rate

def smoothed_rate(samples):
    """What the missing OVERBAR meant: AVERAGE the recent samples to smooth out noise before steering."""
    return sum(samples) / len(samples)


# True motion is a steady ~0.1, but the degraded antenna delivers a noisy spike (the 5.0).
noisy = [0.1, 0.1, 5.0, 0.1, 0.1]

# WITHOUT the overbar: steer on each raw sample -> the spike becomes a wild steering command.
raw_corrections = [steer(r) for r in noisy]
assert max(raw_corrections) == 50.0                     # the noise spike -> a 50-unit lurch

# WITH the overbar (smoothing): average first -> the spike is absorbed, the correction stays sane.
smoothed_correction = steer(smoothed_rate(noisy))
assert smoothed_correction < max(raw_corrections) / 4   # far smaller than the raw spike (10.8 vs 50)
print("No smoothing: a noise spike -> a wild", max(raw_corrections),
      "lurch. Smoothed:", round(smoothed_correction, 1), "-- absorbed, not amplified.")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
Mariner 1 is a TINY-ERROR, HUGE-CONSEQUENCE story: a single missing symbol in how a formula was written
into code lost a spacecraft.

1  A SMALL TRANSCRIPTION / SYNTAX ERROR CAN BE CATASTROPHIC
   The bug was not a grand design flaw -- it was one missing overbar when a formula was copied into code.
   Getting the code to faithfully match the intended logic is the whole game. (PF11 4.7 error types:
   a transcription slip sits between a syntax error and a logic error -- the code ran, but computed the
   wrong thing.)

2  REVIEW + TEST THE CODE AGAINST THE SPECIFICATION
   A careful review or a test comparing the coded equation to the intended one would have caught a missing
   symbol. You verify code does what the spec says, not just that it runs. (PF11 4.6 test data; desk checking.)

3  TEST THE DEGRADED / NOISY CASE, NOT JUST THE CLEAN ONE
   The flaw only bit once the hardware fed noisy data. The smoothing existed precisely for that case --
   and it was the untested case that mattered. Test faulty/boundary inputs, not only the happy path. (4.6)

4  THE SAFETY NET WAS WHAT FAILED
   The hardware antenna glitch alone was survivable -- IF the smoothing had been there to absorb the noise.
   The missing overbar removed the very safeguard meant for that situation. (A recurring pattern: a small
   omission disables the protection that would have saved you -- compare case_therac_25's removed interlocks.)

"THE MOST EXPENSIVE HYPHEN IN HISTORY" (Arthur C. Clarke). CASHES INTO: PF11 4.7 (errors), 4.6 (test data).
Companion to case_the_y2k_bug (a representational choice/slip with outsized, delayed cost).
```
