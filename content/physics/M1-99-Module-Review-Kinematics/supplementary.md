---
title: "Supplementary Materials — Module Review: Kinematics"
module: M1
lesson: "99"
script: script.md
---

# Supplementary Materials

A consolidated reference for the whole Kinematics module, plus worked integrated solutions. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The Kinematics toolkit (all four episodes)
```text
QUANTITIES (M1-01):  scalars — distance, speed.  Vectors (D-V-A) — displacement, velocity, acceleration.
   speed = distance/time ;  velocity = displacement/time ;  a = (v − u)/t.  Choose + direction; stay consistent.

GRAPHS (M1-02):  "gradient climbs the ladder, area descends it"
   slope of s–t = v ;  slope of v–t = a ;  area under v–t = s.
   horizontal: s–t → at rest ;  v–t → constant velocity.   area below t-axis = negative displacement.

EQUATIONS (M1-03) — constant a only:
   v = u + a t            (no s)
   s = u t + ½ a t²       (no v)
   v² = u² + 2 a s        (no t)
   s = ½(u + v) t         (no a)
   Gravity: g ≈ 9.8 m s⁻² down.  "from rest" ⇒ u = 0.  Top of a throw: v = 0, a still = g.

VECTORS / 2D (M1-04):
   resolve: horizontal = V cosθ, vertical = V sinθ  (θ from horizontal; "adjacent = cos, opposite = sin")
   recombine: magnitude = √(Vx² + Vy²),  direction = tan⁻¹(Vy/Vx)
   relative velocity: v(A relative to B) = v(A) − v(B).  Perpendicular components are INDEPENDENT.
```

### Listing 2 — Worked integrated solutions
```text
(Car: rest → 24 m s⁻¹ in 8 s, then 24 m s⁻¹ for 10 s)
   a = 24/8 = 3 m s⁻² ;  s = ½·8·24 + 10·24 = 96 + 240 = 336 m

(Projectile: 25 m s⁻¹ at 30° above horizontal)
   vertical u = 25 sin30° = 12.5 m s⁻¹ ;  to top (v=0): 0 = 12.5 − 9.8t → t ≈ 1.3 s

(Q1: rest → 12 m s⁻¹ in 4 s, then 6 s constant)  a = 12/4 = 3 m s⁻² ; s = ½·4·12 + 6·12 = 24 + 72 = 96 m
(Q3: up at 19.6 m s⁻¹, up +, a = −9.8)  t = 19.6/9.8 = 2 s ; s: 0 = 19.6² − 19.6s → s ≈ 19.6 m
(Q4: boat 5 across, river 12)  R = √(5² + 12²) = 13 m s⁻¹, tan⁻¹(12/5) ≈ 67° downstream
(Q5: horizontal throw 15 m s⁻¹, t = 3 s)  height = ½·9.8·3² ≈ 44 m ; range = 15·3 = 45 m
(Q6: 10 → 30 m s⁻¹ over 200 m)  v²=u²+2as: 900 = 100 + 400a → a = 2 m s⁻² ; v=u+at → t = 10 s ;
   graph check: trapezium area = ½(10+30)·10 = 200 m ✓
```

### Listing 3 — Mnemonic / rule registry (M1)
| Topic | Hook |
|-------|------|
| Vector trio of motion | **D-V-A** (displacement, velocity, acceleration — each needs a direction) |
| Graph rules | "gradient climbs the ladder (s–t→v, v–t→a), area descends it (v–t→s)" |
| Equation choice | **SUVAT** + "spot the missing variable, pick the equation that omits it" |
| Resolving vectors | "adjacent = cos, opposite = sin" (angle from horizontal: horizontal = V cosθ) |
| Relative velocity | **A − B**: v(A relative to B) = v(A) − v(B) |
| Under gravity | g ≈ 9.8 down; "from rest" ⇒ u = 0; top of throw v = 0 (a still g) |

### Listing 4 — Distance vs displacement from a velocity-time graph (with a reversal)
```text
v–t graph: 0 → 10 m s⁻¹ over 0–2 s; constant 10 for 2–5 s; falls 10 → −6 m s⁻¹ over 5–9 s.

Positive area (0–5 s): triangle ½·2·10 = 10 m  +  rectangle 3·10 = 30 m  = 40 m
Falling section: part ABOVE axis ≈ +6 m ;  part BELOW axis ≈ −9 m (motion reversed)

DISPLACEMENT (net)  = 40 + 6 − 9 = 37 m   (areas signed — subtract the below-axis part)
DISTANCE (total)    = 40 + 6 + 9 = 55 m   (areas all added — direction ignored)

Read the verb: "displacement" → net (sign the areas) ; "distance" → total (add magnitudes).
```
