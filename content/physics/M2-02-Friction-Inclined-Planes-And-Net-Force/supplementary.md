---
title: "Supplementary Materials — Friction, Inclined Planes and Resolving Forces"
module: M2
lesson: "02"
script: script.md
---

# Supplementary Materials

Force resolution on slopes, friction, and worked solutions. Nothing here is spoken in the audio — it is the read-along reference. Symbols: m = mass; g ≈ 9.8 m s⁻²; θ = slope angle to the horizontal; N = normal force; f = friction force.

### Listing 1 — Resolving forces on an inclined plane
```text
Tilt the axes: one ALONG the slope, one PERPENDICULAR (into) the slope.
The weight (mg, straight down) resolves into:
   ALONG the slope (down-slope):       mg sin θ      ← drives the sliding
   PERPENDICULAR (into the surface):   mg cos θ      ← pressed into the slope

PERPENDICULAR balance (no acceleration into surface):  N = mg cos θ   (< mg !)
ALONG the slope (Newton's 2nd law):    F_net = mg sin θ − f = m a

⚠ Hook: steeper slope → slides more easily → down-slope force grows → sin (grows to 1 at 90°).
   At θ = 0 (flat): N = mg cos0 = mg (full weight) ; down-slope mg sin0 = 0 (no slide).
```

### Listing 2 — Worked examples: blocks on inclines
```text
(A) Frictionless incline, θ = 30°:  a = g sinθ = 9.8 × 0.5 = 4.9 m s⁻² (mass cancels!)
(B) Frictionless, θ = 20° (Q2):     a = g sin20° = 9.8 × 0.342 ≈ 3.35 m s⁻²
(C) m = 1 kg, θ = 30°, friction 2 N up-slope:
    down-slope = mg sinθ = 1×9.8×0.5 = 4.9 N ;  F_net = 4.9 − 2 = 2.9 N ;  a = 2.9/1 = 2.9 m s⁻²
(D) m = 4 kg, θ = 30°, friction 10 N (Q4):
    down-slope = 4×9.8×0.5 = 19.6 N ;  F_net = 19.6 − 10 = 9.6 N ;  a = 9.6/4 = 2.4 m s⁻²
(E) Skier m = 60 kg, θ = 25°, friction 100 N, from rest, after 50 m (Q5):
    down-slope = 60×9.8×sin25° ≈ 60×9.8×0.423 ≈ 249 N ;  F_net = 249 − 100 = 149 N
    a = 149/60 ≈ 2.5 m s⁻² ;  v² = u² + 2as = 0 + 2(2.5)(50) = 250 → v ≈ 15.8 m s⁻¹
```

### Listing 3 — Worked example: friction on a flat surface (static → kinetic)
```text
Crate m = 20 kg on level ground. Max static friction = 50 N; kinetic friction = 45 N.
   Push 10 N → static friction = 10 N → net 0 → STATIONARY (1st law)
   Push 20 N → static friction = 20 N → net 0 → STATIONARY
   Push 51 N → exceeds max static (50 N) → crate BREAKS FREE, starts sliding
   Push 60 N (now sliding): F_net = 60 − 45 (kinetic) = 15 N → a = 15/20 = 0.75 m s⁻²

Static friction ADJUSTS up to a maximum; kinetic friction is roughly constant (< max static).
Friction depends on the NORMAL force and the surfaces — NOT on contact area or speed.
```

### Listing 4 — Friction facts and equilibrium on a slope
```text
FRICTION:
  • acts ALONG the surface, opposing motion (or the tendency to move)
  • STATIC: matches the applied force up to a maximum (object not yet moving)
  • KINETIC: roughly constant, acts while sliding (usually a bit < max static)
  • depends on: normal force + surface roughness (coefficient).  NOT area, NOT speed.

EQUILIBRIUM on a slope (block stationary):
  static friction (up-slope) = mg sinθ exactly (balances the down-slope component).
  Block slips when mg sinθ exceeds the maximum static friction (the "angle of repose").

ON A SLOPE the friction depends on N = mg cosθ, which is why steeper slopes (smaller cosθ)
give less friction even as the down-slope pull (mg sinθ) grows.
```
