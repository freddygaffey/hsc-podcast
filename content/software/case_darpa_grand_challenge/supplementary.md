---
title: "Supplementary Materials — The DARPA Grand Challenge"
module: PM11
year: 11
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the DARPA Grand Challenge case study. Nothing here is spoken in the audio —
the narration points at each listing by label only. Listing 1 is the timeline; Listing 2 is a runnable
"fail, iterate, succeed" simulation; Listing 3 maps the lessons onto the module.

### Listing 1 — Timeline (reference)
```text
2003        DARPA (the US Defense Advanced Research Projects Agency) announces the Grand Challenge:
            a prize for the first fully AUTONOMOUS (driverless) vehicle to complete a long desert course.
            The goal -- jump-start self-driving technology by turning a hard research problem into a race.
13 Mar 2004 FIRST GRAND CHALLENGE, ~240 km across the Mojave Desert. A near-total failure: NOT ONE of
            the 15 finalists finished. The best, Carnegie Mellon's "Sandstorm", managed only about
            12 km -- roughly 5% of the course -- before getting stuck on an embankment. Prize unclaimed.
8 Oct 2005  SECOND GRAND CHALLENGE, ~212 km. Eighteen months later, FIVE vehicles finish. Stanford's
            "Stanley" (led by Sebastian Thrun) wins in just under 7 hours; Carnegie Mellon's two cars
            come 2nd and 3rd. Stanley used laser range-finders (LIDAR) + cameras and MACHINE LEARNING
            to tell drivable ground from obstacles. From "nobody finished" to "five finished" in 18 months.
2007        DARPA URBAN CHALLENGE: autonomous vehicles navigate a mock town WITH traffic and road rules.
            Six finish; Carnegie Mellon's "Boss" wins.
Legacy      The Challenge seeded the modern self-driving industry -- many entrants went on to found or
            lead autonomous-vehicle programs. Proof that autonomy is reached by ITERATION, not first try.
```

### Listing 2 — Fail, iterate, succeed: tuning an autonomous run in simulation (Python, runnable)
```python
def run_course(caution, course_length=100):
    """SIMULATE a desert run. 'caution' = how much rough terrain the vehicle can safely handle.
    If the terrain is rougher than its caution, it gets stuck. Returns how far it got (km)."""
    distance = 0
    for km in range(course_length):
        roughness = (km * 7) % 10               # deterministic 'terrain' for each km, 0..9
        if caution >= roughness:
            distance += 1                       # handled this stretch -> keep going
        else:
            break                               # too rough for its caution -> stuck (a 2004-style stall)
    return distance


# 2004-style: too little caution -> it stalls early, like the ~12 km of a 240 km course.
assert run_course(caution=3) < 100

# THE ENGINEERING: iterate in simulation -- raise the caution and re-test -- until it finishes the whole course.
caution = 0
while run_course(caution) < 100:
    caution += 1                                # learn from each failed run, improve, try again

assert run_course(caution) == 100               # now it completes the course (the 2005 result)
print("Iterated to a vehicle that finishes the course; caution needed =", caution)
```

### Listing 3 — The lessons, mapped to the module (reference)
```text
The DARPA Grand Challenge is the POSITIVE counterpart to the cautionary tales: how autonomy is built RIGHT.

1  AUTONOMY IS REACHED BY ITERATION, NOT FIRST TRY
   2004 = total failure; 2005 = five finishers, 18 months later. Same teams, relentless test-fix-retest.
   Build, fail safely, learn, improve. (10.1 simulate + prototype; the "fail fast in software" idea.)

2  SIMULATE + PROTOTYPE TO ITERATE CHEAPLY AND SAFELY
   You can't crash a real car a thousand times. Teams simulated runs and tested on closed courses, so each
   failure cost time, not lives. Failure in the desert was the teacher. (10.1 S-C-F: Safe/Cheap/Fast; Listing 2.)

3  AUTONOMOUS CONTROL = SENSE-THINK-ACT WITH NO HUMAN
   Stanley sensed (LIDAR + cameras), decided (where is drivable ground? what speed is safe?), and acted
   (steer/throttle/brake) entirely on its own -- the S-D-A-F features made real. (9.2 autonomous control; 7.3 sensors.)

4  BETTER SENSING + SMARTER SOFTWARE WIN
   The 2005 winner fused multiple sensors and used MACHINE LEARNING to classify terrain, cutting mistakes
   dramatically. Redundant, well-interpreted sensing is the opposite of the 737 MAX's single trusted sensor.
   (7.3 sensors; 8.1 process/validate data; bridges to AI in Year-12 Software Automation.)

CONTRAST: case_the_737_max_mcas + case_therac_25 show autonomy/control done WRONG (single sensor, missing
safety, untested failure paths). DARPA shows it done RIGHT (redundant sensing, iterate-and-test, fail safely).
CASHED IN BY: PM11 9.2 (autonomous control), 10.1 (simulation/prototypes); bridges to Year-12 AI.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| AI | Artificial Intelligence | Software that performs tasks normally needing human intelligence |
| DARPA | Defense Advanced Research Projects Agency | The US defence R&D agency (ran the autonomous-vehicle Grand Challenge) |
| S-C-F | Safe · Cheap · Fast | Why to simulate before you build |
| S-D-A-F | Sensing · Decision logic · Adapt/self-correct · Fail-safe | The four features of an autonomous control algorithm |
