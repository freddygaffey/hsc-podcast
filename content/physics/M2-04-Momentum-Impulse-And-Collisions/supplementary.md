---
title: "Supplementary Materials — Momentum, Impulse and Collisions"
module: M2
lesson: "04"
script: script.md
---

# Supplementary Materials

Momentum, impulse, and collision analysis with worked solutions. Nothing here is spoken in the audio — it is the read-along reference. Symbols: p = momentum; m = mass; v, u = velocities; F = force; t = time; KE = kinetic energy.

### Listing 1 — Momentum and impulse
```text
MOMENTUM:   p = m v       (VECTOR; kg m s⁻¹; sign = direction in 1-D)
IMPULSE:    Δp = F Δt     (change in momentum; kg m s⁻¹ = N s)
            = area under a FORCE–TIME graph
            (this is Newton's 2nd law over time: F t = m Δv)

SAFETY PRINCIPLE: Δp is fixed by the situation, so for a given Δp,
   longer time  ⇒  smaller force.  "Extend the time, cut the force."
   (airbags, crumple zones, seatbelts, bending knees, follow-through)

CONSERVATION OF MOMENTUM (closed system, no external net force):
   Σ(m v) before  =  Σ(m v) after
   Follows from Newton's 3rd law: equal & opposite forces × equal time
   ⇒ equal & opposite impulses ⇒ changes cancel.
```

### Listing 2 — Worked collisions (conservation of momentum)
```text
(A) Stick-together: 1000 kg at 20 m s⁻¹ hits stationary 1500 kg, lock together:
    before: 1000×20 + 0 = 20 000 ;  after: 2500 × v  →  v = 8 m s⁻¹
(B) Q4: 3 kg at 4 m s⁻¹ hits stationary 1 kg, stick:
    12 = 4v → v = 3 m s⁻¹.  KE: before ½·3·4²=24 J ; after ½·4·3²=18 J → NOT conserved (inelastic)
(C) Q5: 60 kg at 3 m s⁻¹ hits stationary 40 kg; 60 kg continues at 1 m s⁻¹:
    180 = 60×1 + 40v → 40v = 120 → v = 3 m s⁻¹
    KE before = ½·60·3² = 270 J ; after = ½·60·1² + ½·40·3² = 30 + 180 = 210 J → inelastic (60 J lost)
(D) Recoil (start at rest, total p = 0): 2 kg rifle, 0.01 kg bullet at 400 m s⁻¹:
    bullet p = 4 kg m s⁻¹ fwd → rifle p = 4 back → rifle recoil = 4/2 = 2 m s⁻¹ back
```

### Listing 3 — Worked impulse problems
```text
(A) 0.2 kg ball at 15 m s⁻¹ caught, stopped in 0.3 s:
    Δp = mΔv = 0.2 × 15 = 3 kg m s⁻¹ ;  F = Δp/t = 3/0.3 = 10 N
    (catch over 0.6 s instead → F = 3/0.6 = 5 N — extend time, cut force)
(B) Q2: 0.5 kg ball 8 m s⁻¹ → rebounds at 6 m s⁻¹ (take initial as +):
    p_i = 0.5×8 = +4 ;  p_f = 0.5×(−6) = −3
    Impulse = p_f − p_i = −3 − 4 = −7 kg m s⁻¹ (i.e. 7 N s in the rebound direction)
    ⚠ rebound REVERSES sign — that's why the impulse (7) exceeds either momentum alone.
```

### Listing 4 — Elastic vs inelastic collisions
| | Momentum | Kinetic energy |
|---|----------|----------------|
| **Elastic** | conserved | **conserved** (KE after = KE before) |
| **Inelastic** | conserved | **NOT conserved** (some → heat, sound, deformation) |
| **Perfectly inelastic** (stick together) | conserved | NOT conserved — maximum KE lost |

```text
KEY: momentum is conserved in ALL closed-system collisions;
     kinetic energy is conserved ONLY in elastic collisions.
METHOD: use momentum to find the velocities; use KE (before vs after) to classify
        the collision / find energy transformed. Don't assume KE is conserved.
```
