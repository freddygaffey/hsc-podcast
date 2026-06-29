---
title: "Supplementary Materials — Motion in a Straight Line: Distance, Displacement, Velocity and Acceleration"
module: M1
lesson: "01"
script: script.md
---

# Supplementary Materials

Definitions and worked numerical solutions for the foundations of kinematics. Nothing here is spoken in the audio — it is the read-along reference. Symbols: s = displacement; d = distance; v = velocity; a = acceleration; t = time. Sign convention: choose one direction as positive and state it.

### Listing 1 — The quantities of motion: scalar or vector, and units
| Quantity | Scalar or vector | Meaning | SI unit |
|----------|------------------|---------|---------|
| Distance (d) | scalar | total length of path travelled | metre (m) |
| Displacement (s) | **vector** | straight-line change in position (with direction) | metre (m) |
| Speed | scalar | rate of covering distance = distance / time | m s⁻¹ |
| Velocity (v) | **vector** | rate of change of displacement = displacement / time | m s⁻¹ |
| Acceleration (a) | **vector** | rate of change of velocity = Δv / t | m s⁻² |
| Time (t) | scalar | — | second (s) |

```text
Hook: the VECTOR trio of motion is Displacement, Velocity, Acceleration → "D-V-A"
(each needs a direction). Their scalar shadows are distance and speed.
average speed   = total distance / total time        (scalar)
average velocity = total displacement / total time    (vector)
acceleration    = (v − u) / t   = change in velocity / time   (final minus initial)
```

### Listing 2 — Distance vs displacement, speed vs velocity (there-and-back)
```text
THERE-AND-BACK (1D, take east as +):
  Walk 3 m east, then 1 m west.
  Distance      = 3 + 1 = 4 m                (scalar; path length)
  Displacement  = +3 − 1 = +2 m = 2 m east   (vector; net change)

SWIMMER (pool length 50 m, 100 s total):
  Swim 50 m to far wall, then 50 m back to start.
  Total distance      = 50 + 50 = 100 m
  Total displacement  = 0 m   (finishes at start)
  Average speed    = distance / time     = 100 / 100 = 1 m s⁻¹
  Average velocity = displacement / time = 0 / 100   = 0 m s⁻¹
  ⇒ average speed ≠ magnitude of average velocity when the path reverses.
```

### Listing 3 — Worked example: average speed vs average velocity (cyclist)
```text
Take EAST as positive.
  Leg 1: 200 m east in 20 s
  Leg 2: 80 m west in 10 s

Total distance      = 200 + 80 = 280 m
Total displacement  = +200 − 80 = +120 m = 120 m east
Total time          = 20 + 10 = 30 s

Average speed    = 280 / 30 ≈ 9.3 m s⁻¹            (scalar — no direction)
Average velocity = 120 / 30 = 4.0 m s⁻¹ east        (vector — state direction)
Note: 9.3 ≠ 4.0 because the cyclist doubled back (distance > |displacement|).
```

### Listing 4 — Worked example: distance and displacement (car, exam Q2)
```text
Take NORTH as positive.  Car: 600 m north, then 200 m south.
  Distance     = 600 + 200 = 800 m                 (scalar)
  Displacement = +600 − 200 = +400 m = 400 m north  (vector; sign + ⇒ north)
Trap: the displacement is 400 m north, NOT 800 m (that is the distance).
```

### Listing 5 — Worked example: acceleration and the sign of a (Δv = v − u)
```text
Take EAST as positive.   a = (v − u) / t

CASE A — slowing down (moving +, a negative):
  Car east: u = 20 m s⁻¹, v = 12 m s⁻¹, t = 4 s
  a = (12 − 20) / 4 = −8 / 4 = −2 m s⁻²
  Moving east (+) with a negative a ⇒ a opposes motion ⇒ SLOWING DOWN.

CASE B — speeding up (moving −, a negative):
  Ball west: u = −3 m s⁻¹, v = −7 m s⁻¹, t = 1 s
  a = (−7 − (−3)) / 1 = −4 / 1 = −4 m s⁻²
  Moving west (−) with a negative a ⇒ a is in the SAME direction as motion ⇒ SPEEDING UP.

⇒ A negative acceleration means "a points in the negative direction", NOT automatically "braking".
   Whether the object speeds up or slows down depends on the direction of its velocity.
```
