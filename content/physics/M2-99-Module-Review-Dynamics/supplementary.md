---
title: "Supplementary Materials — Module Review: Dynamics"
module: M2
lesson: "99"
script: script.md
---

# Supplementary Materials

A consolidated reference for the whole Dynamics module, with worked integrated solutions. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The Dynamics toolkit (all four episodes)
```text
FORCES & NEWTON'S LAWS (M2-01):  force = vector (N); net force = vector sum.
   1st: no net force ⇒ rest or constant velocity.   2nd: F_net = m a (a ∥ F_net).
   3rd: F(A on B) = −F(B on A), different objects.   mass (kg, scalar) ≠ weight (N, = mg).

INCLINES & FRICTION (M2-02):  down-slope = mg sinθ ; into-slope = mg cosθ ; N = mg cosθ.
   F_net(along) = mg sinθ − friction ;  frictionless a = g sinθ (mass-independent).

WORK & ENERGY (M2-03):  W = F s ;  KE = ½mv² ;  net work = ΔKE ;  ΔU = mgΔh.
   No friction ⇒ mechanical energy conserved: mgΔh = ½mv².  P = ΔE/t = Fv.  ("transformed, not lost")

MOMENTUM (M2-04):  p = mv (vector) ;  impulse Δp = FΔt (area under F–t).
   Closed system: Σmv before = Σmv after.  Momentum conserved in ALL collisions;
   KE conserved ONLY in elastic.
```

### Listing 2 — Worked integrated solutions
```text
(Block down rough incline: m=2 kg, 30°, friction 4 N, slope 5 m)
  FORCES: mg sinθ = 2·9.8·0.5 = 9.8 N ; F_net = 9.8 − 4 = 5.8 N ; a = 2.9 m s⁻²
          v² = 2·2.9·5 = 29 → v ≈ 5.4 m s⁻¹
  ENERGY: Δh = 5·sin30° = 2.5 m ; PE = 2·9.8·2.5 = 49 J ; friction work = 4·5 = 20 J
          KE = 49 − 20 = 29 J = ½·2·v² → v ≈ 5.4 m s⁻¹  (same answer ✓)

(Car collision: 1000 kg @20 + stationary 1500 kg, stick)
  momentum: 20000 = 2500v → v = 8 m s⁻¹
  KE: before ½·1000·20² = 200 000 J ; after ½·2500·8² = 80 000 J → 120 000 J transformed (inelastic)

(Frictionless incline Q3: 3 kg, 25°)  a = g sin25° ≈ 4.1 m s⁻² ; v² = 2·4.1·4 ≈ 33 → v ≈ 5.7 m s⁻¹
(Drop Q4: 0.2 kg, 3 m)  v = √(2·9.8·3) ≈ 7.7 m s⁻¹ ; impulse = mΔv = 0.2·7.7 ≈ 1.5 kg m s⁻¹
(Recoil Q5: 60 kg back at 2 → 40 kg)  0 = 60(−2) + 40v → v = 3 m s⁻¹ fwd
(Collision Q6: 2 kg @5 → 1 m s⁻¹; 3 kg)  10 = 2 + 3v → v ≈ 2.7 m s⁻¹ ; KE 25 → ~12 J → inelastic
(Braking: 1000 kg @30, brake 6000 N)  KE = ½·1000·30² = 450 000 J = 6000·d → d = 75 m (∝ v²)
```

### Listing 3 — Mnemonic / rule registry (M2)
| Topic | Hook |
|-------|------|
| Newton's three laws | **I, F, A** — Inertia, F = ma, Action-reaction (different objects) |
| Mass vs weight | mass = kg scalar (constant); weight = N vector = mg |
| Inclined plane | down-slope = mg sinθ, into-slope/normal = mg cosθ; "steeper → more sliding → sine" |
| Energy | "transformed, not destroyed"; mgh = ½mv² (mass-independent) |
| Power | P = ΔE/t = Fv |
| Momentum/collisions | "momentum always conserved; KE only if elastic"; impulse "extend time, cut force" |

### Listing 4 — Which approach? (forces vs energy vs momentum)
```text
FORCES / Newton's 2nd law  → need an acceleration, a force, or a TIME; inclined planes.
ENERGY (conservation)      → heights & speeds with NO time; start/end states; work, power.
MOMENTUM (conservation)    → COLLISIONS, explosions, recoil (then use KE to classify).

Decision tree:
   collision / explosion?      → momentum first (+ KE to classify elastic vs inelastic)
   heights & speeds, no time?  → energy
   need force / acceleration / time? → Newton's laws
All three AGREE (work-energy = 2nd law over distance; impulse = 2nd law over time) —
use the quickest, and cross-check with a second method if time allows.
```
