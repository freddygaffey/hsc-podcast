---
title: "Supplementary Materials — Vectors and Motion in a Plane"
module: M1
lesson: "04"
script: script.md
---

# Supplementary Materials

Vector resolution, addition, and relative velocity — methods and worked solutions. Nothing here is spoken in the audio — it is the read-along reference. Symbols: V = a vector's magnitude; θ = angle.

### Listing 1 — Resolving and recombining vectors
```text
RESOLVE a vector of magnitude V at angle θ FROM THE HORIZONTAL:
   horizontal component (adjacent) = V cos θ
   vertical component  (opposite)  = V sin θ
   ⚠ "adjacent = cos, opposite = sin". If θ is measured FROM THE VERTICAL, they SWAP.

RECOMBINE two perpendicular components (Vx, Vy) into one resultant:
   magnitude  = √(Vx² + Vy²)            (Pythagoras)
   direction  = tan⁻¹(Vy / Vx)          (angle from the Vx axis)

GENERAL ADDITION (any angles): resolve every vector into east & north components,
   ADD all east components → ΣE, ADD all north components → ΣN,
   then recombine: magnitude = √(ΣE² + ΣN²), direction = tan⁻¹(ΣN/ΣE).
   (Perpendicular cases are just the easy special case — one component each.)
⚠ NEVER add magnitudes as scalars: 3 and 4 perpendicular make 5, not 7.
```

### Listing 2 — Worked example: resolving a vector
```text
(A) V = 10 units at 30° above horizontal:
   horizontal = 10 cos30° = 10 × 0.87 = 8.7 units
   vertical   = 10 sin30° = 10 × 0.50 = 5.0 units

(B) Exam Q1: V = 20 units at 60° above horizontal:
   horizontal = 20 cos60° = 20 × 0.50 = 10 units
   vertical   = 20 sin60° = 20 × 0.87 = 17.3 units

(C) Component addition (non-perpendicular): 100 m east, then 120 m at 30° N of E
   Leg 1: E = 100, N = 0
   Leg 2: E = 120 cos30° ≈ 104, N = 120 sin30° = 60
   ΣE = 204, ΣN = 60 → R = √(204² + 60²) ≈ 213 m, at tan⁻¹(60/204) ≈ 16° N of E
```

### Listing 3 — Worked examples: relative velocity (vector triangle)
```text
(A) Boat 4 m s⁻¹ across, river 3 m s⁻¹ downstream (perpendicular):
   resultant = √(4² + 3²) = √25 = 5 m s⁻¹
   direction = tan⁻¹(3/4) ≈ 37° downstream of straight across
   (Crossing TIME depends only on the 4 m s⁻¹ across-component — current is ⟂, so time unchanged.)

(B) Exam Q3: swimmer 1.5 m s⁻¹ across, river 2 m s⁻¹:
   resultant = √(1.5² + 2²) = √6.25 = 2.5 m s⁻¹, tan⁻¹(2/1.5) ≈ 53° downstream

(C) Exam Q5: plane 200 m s⁻¹ north, wind 50 m s⁻¹ east:
   ground velocity = √(200² + 50²) ≈ 206 m s⁻¹, tan⁻¹(50/200) ≈ 14° E of N
   To go due N: aim upwind (W of N) so the westward aim cancels the eastward wind.
```

### Listing 4 — Relative velocity: the rule and the three scenarios
```text
RULE:  velocity of A relative to B  =  v(A) − v(B)   (a VECTOR subtraction)
  To subtract v(B): reverse it (180°) and add head-to-tail, OR subtract components.

Two cars: A = 20 N, B = 20 E. v(A) − v(B) = 20 N + 20 W
   = √(20² + 20²) ≈ 28 m s⁻¹, directed NW (how A appears to B's driver).

Scenarios named by the syllabus:
   • boat on a flowing river   (boat velocity + current)
   • aeroplane in a crosswind  (airspeed + wind = ground velocity)
   • two moving cars           (v(A) − v(B))
Always give the answer as MAGNITUDE + DIRECTION.
```
