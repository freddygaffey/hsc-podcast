---
title: "Supplementary Materials — Forces and Newton's Three Laws"
module: M2
lesson: "01"
script: script.md
---

# Supplementary Materials

Definitions, the three laws, and worked solutions for the foundations of Dynamics. Nothing here is spoken in the audio — it is the read-along reference. Symbols: F = force; m = mass; a = acceleration; g = gravitational field strength ≈ 9.8 N kg⁻¹ (= 9.8 m s⁻²).

### Listing 1 — Force types, and mass vs weight
| | Mass | Weight |
|---|------|--------|
| What it is | amount of matter | gravitational force on the mass |
| Scalar/vector | scalar | vector (points down) |
| Unit | kilogram (kg) | newton (N) |
| Depends on location? | no — constant everywhere | yes — weight = m g |

```text
FORCE = a push or pull; a VECTOR, in newtons (N).
  Contact forces: applied push/pull, NORMAL force (⟂ to surface), TENSION (along a rope),
                  FRICTION (opposes motion, along surface), air resistance.
  Field forces (act at a distance): gravity (weight), electrostatic, magnetic.
Weight: W = m g   (e.g. 70 kg → 70 × 9.8 = 686 N down on Earth).
```

### Listing 2 — Newton's second law: the Dynamics→Kinematics chain
```text
F_net = m a    ⇒    a = F_net / m    (a is in the DIRECTION of F_net)

Method: (1) add ALL forces as vectors → F_net ;  (2) a = F_net/m ;  (3) feed a into SUVAT.

(A) F_net = 12 N, m = 4 kg, from rest, find v after 3 s:
    a = 12/4 = 3 m s⁻² ;  v = u + at = 0 + 3×3 = 9 m s⁻¹
(B) Car: F_net = 2500 N, m = 1000 kg → a = 2500/1000 = 2.5 m s⁻²
(C) Crate: applied 200 N, friction 50 N, m = 50 kg, from rest, find v after 4 s:
    F_net = 200 − 50 = 150 N ;  a = 150/50 = 3 m s⁻² ;  v = 0 + 3×4 = 12 m s⁻¹
(D) Perpendicular forces 3 N E + 4 N N: F_net = √(3²+4²) = 5 N at tan⁻¹(4/3) ≈ 53° N of E

Proportionalities (fixed m): a ∝ F_net (straight line through origin, gradient 1/m).
                  (fixed F): a ∝ 1/m.
```

### Listing 3 — Worked example: mass vs weight on Earth and Moon
```text
70 kg person.   Earth g = 9.8 N kg⁻¹ ;  Moon g = 1.6 N kg⁻¹.
  Earth weight = m g = 70 × 9.8 = 686 N (down)
  Moon: mass unchanged = 70 kg ;  Moon weight = 70 × 1.6 = 112 N (down)
⇒ MASS is constant; WEIGHT changes with location.
```

### Listing 4 — Newton's three laws and action-reaction pairs
```text
1st law (inertia): with NO net force, an object stays at rest or at constant velocity.
2nd law: F_net = m a (acceleration ∝ net force, in its direction; ∝ 1/mass).
3rd law: F(A on B) = −F(B on A) — equal magnitude, opposite direction,
         SAME type of force, acting on DIFFERENT objects ⇒ they do NOT cancel.

Action-reaction pairs (different objects):
   you push back on ground   ↔  ground pushes you forward (walking)
   rocket pushes gas down     ↔  gas pushes rocket up
   book pushes down on table  ↔  table pushes up on book

⚠ NOT an action-reaction pair: the weight of a book and the normal force on it.
  Those act on the SAME object (the book) and are different types — they merely BALANCE
  (equilibrium, net force zero). Action-reaction acts on different objects.
```
