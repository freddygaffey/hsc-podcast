---
title: "Supplementary Materials — Velocity-Time and Displacement-Time Graphs"
module: M1
lesson: "02"
script: script.md
---

# Supplementary Materials

Graph-reading rules and worked solutions for motion graphs. Nothing here is spoken in the audio — it is the read-along reference. Symbols: s = displacement; v = velocity; a = acceleration; t = time.

### Listing 1 — The three graph-reading rules
| Graph | Gradient (slope) gives… | Area under the line gives… |
|-------|-------------------------|----------------------------|
| Displacement–time (s vs t) | **velocity** (v) | (no physical meaning) |
| Velocity–time (v vs t) | **acceleration** (a) | **displacement** (s) |

```text
Hook — "gradient climbs the ladder, area descends it":
   slope of s–t  → v        (one rung up)
   slope of v–t  → a        (next rung up)
   area under v–t → s        (back down)

Line shapes:
   s–t horizontal  → at REST (v = 0)
   s–t straight slope → constant velocity ;  s–t curve → accelerating (v changing)
   v–t horizontal  → CONSTANT VELOCITY (a = 0, NOT at rest)
   v–t straight slope → constant acceleration ;  v–t crosses t-axis → reverses direction

Instantaneous velocity on a curved s–t graph = gradient of the TANGENT at that point.

Units check: slope of v–t = (m s⁻¹)/s = m s⁻²  → acceleration.
             area of v–t  = (m s⁻¹)(s) = m     → displacement.
```

### Listing 2 — Worked example: reading a velocity-time graph
```text
GRAPH: v rises in a straight line 0 → 20 m s⁻¹ over 0–10 s, then constant 20 m s⁻¹ for 10–30 s.

Acceleration in phase 1 = gradient = rise / run
   a = (20 − 0) / (10 − 0) = 20 / 10 = 2.0 m s⁻²
Acceleration in phase 2 = 0 (horizontal line → constant velocity)

Total displacement = AREA under the whole line:
   Phase 1 (triangle): ½ × base × height = ½ × 10 × 20 = 100 m
   Phase 2 (rectangle): width × height   = 20 × 20      = 400 m
   Total s = 100 + 400 = 500 m

Exam Q3 check (rest → 30 m s⁻¹ in 12 s):
   a = 30 / 12 = 2.5 m s⁻²
   s = ½ × 12 × 30 = 180 m   (triangle — don't forget the ½)
```

### Listing 3 — Worked example: reading a displacement-time graph
```text
GRAPH: s rises 0 → 60 m over 0–6 s; horizontal at 60 m for 6–10 s; falls 60 → 0 m over 10–13 s.

Phase 1: v = gradient = 60 / 6 = +10 m s⁻¹     (constant positive velocity)
Phase 2: v = gradient = 0                       (horizontal → AT REST at 60 m)
Phase 3: v = gradient = (0 − 60) / 3 = −20 m s⁻¹ (moving back toward start, negative direction)

⇒ From an s–t graph you take GRADIENTS ONLY, to get velocity (its sign = direction).
```

### Listing 4 — Distance vs displacement from a velocity-time graph
```text
Area ABOVE the t-axis = positive displacement ;  area BELOW = negative displacement.

Example: area above = 40 m, then object reverses, area below = 15 m.
   DISPLACEMENT (net)  = 40 − 15 = 25 m in the positive direction   (areas SUBTRACT)
   DISTANCE (total)    = 40 + 15 = 55 m                              (areas ADD)

Same graph, two answers — read the verb: "displacement" → net (subtract);
"distance" → total (add). (Ties back to M1-01: net vs total.)
```
