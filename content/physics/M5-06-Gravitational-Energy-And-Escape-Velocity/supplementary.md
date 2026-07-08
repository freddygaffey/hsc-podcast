---
title: "Supplementary Materials — Gravitational Energy and Escape Velocity"
module: M5
lesson: "06"
script: script.md
---

# Supplementary Materials

The read-along reference for gravitational energy and escape velocity: the gravitational potential energy \(U=-GMm/r\) and why its sign is negative, its reconciliation with the Year 11 formula \(mgh\), the total energy of a circular orbit and the fixed \(+1,-2,-1\) relationship between kinetic, potential and total energy, the worked energy cost of raising an orbit, the derivation and value of escape velocity, a quick-reference data table, and full worked solutions to the closing questions. Nothing here is spoken in the audio. Symbols: G = universal gravitational constant = 6.67 × 10⁻¹¹ N m² kg⁻²; M = mass of the central body (kg); m = mass of the orbiting/escaping object (kg); r = distance from the CENTRE of the central body (m); R = radius of the Earth = 6.37 × 10⁶ m; U = gravitational potential energy (J); K = kinetic energy (J); E = total mechanical energy (J); v = speed (m s⁻¹); v_esc = escape velocity (m s⁻¹). For the Earth GM = 3.98 × 10¹⁴ m³ s⁻² and M = 5.97 × 10²⁴ kg.

### Listing 1 — Gravitational potential energy: U = −GMm/r (sign, mgh limit, worked value)
```text
DEFINITION (zero of energy chosen at infinity):
        U = − G M m / r          ← "zero at infinity, negative everywhere"

WHY NEGATIVE:
   • U = 0 at r = ∞ (masses infinitely apart, no interaction)
   • gravity is ATTRACTIVE → positive work needed to drag a mass out to infinity
   • so every finite r has LESS energy than infinity (< 0) → U is negative
   • smaller r  →  deeper in the well  →  MORE negative

RECONCILES WITH YEAR-11 mgh (near-surface limit):
   ΔU from R to R+h  = −GMm/(R+h) − (−GMm/R)
                     =  GMm [ 1/R − 1/(R+h) ]
                     =  GMm · h / [ R(R+h) ]
        for h << R:  ≈ GMm h / R²  =  m h (GM/R²)  =  m g h
   → mgh is just the change in −GMm/r for small hops (g = GM/R²).

WORKED — U of a 500 kg satellite sitting at the Earth's surface (r = R):
   U = −(3.98 × 10¹⁴)(500) / (6.37 × 10⁶)
     = −1.99 × 10¹⁷ / 6.37 × 10⁶
     ≈ −3.12 × 10¹⁰ J        (negative — it is bound to the Earth)
```

### Listing 2 — Total energy of a circular orbit (K, U, E and the +1, −2, −1 pattern)
```text
KINETIC (use v² = GM/r from the orbital-velocity result, M5-05):
        K = ½ m v² = ½ m (GM/r)  =  + G M m / (2r)

POTENTIAL:
        U = − G M m / r          =  − 2 × [ G M m / (2r) ]

TOTAL:
        E = K + U = GMm/2r − GMm/r  =  − G M m / (2r)     ← crown-jewel result

THE FIXED RATIO (in units of the chunk  GMm/2r ):
        K : U : E   =   +1 : −2 : −1
   → know any one, the other two are forced.  (This is the virial theorem.)

WHAT THE SIGN MEANS:
        E < 0  →  BOUND (trapped in the well, orbits forever)
        E = 0  →  just barely escapes (coasts to infinity, arrives at rest)
        E > 0  →  UNBOUND (flies away on a hyperbola, never returns)

"HIGHER IS SLOWER BUT BIGGER-ENERGY":  E = −GMm/2r with r on the bottom of a
   negative fraction → bigger r makes E LESS negative → total energy RISES toward 0,
   even though the speed v = √(GM/r) FALLS. The potential term (−2) beats the
   kinetic term (+1).

WORKED — 500 kg satellite at r = 7.0 × 10⁶ m:
   K = (3.98×10¹⁴)(500)/(2·7.0×10⁶) = 1.99×10¹⁷/1.4×10⁷ ≈ +1.42 × 10¹⁰ J
   U = −(3.98×10¹⁴)(500)/(7.0×10⁶)                       ≈ −2.84 × 10¹⁰ J
   E = K + U                                             ≈ −1.42 × 10¹⁰ J   (= −K ✓)
```

### Listing 3 — Energy to change orbit (worked: raise a satellite)
```text
Energy that must be SUPPLIED to raise a satellite from radius r₁ to a higher r₂:

        E_supplied = E(r₂) − E(r₁)
                   = −GMm/(2r₂) − ( −GMm/(2r₁) )
                   =  (GMm/2) · ( 1/r₁ − 1/r₂ )        ← positive, since r₂ > r₁

WORKED — m = 500 kg, r₁ = 7.0 × 10⁶ m, r₂ = 1.4 × 10⁷ m, GM = 3.98 × 10¹⁴:
   GMm/2 = (3.98 × 10¹⁴)(500)/2                 = 9.95 × 10¹⁶
   1/r₁  = 1/(7.0 × 10⁶)                         = 1.43 × 10⁻⁷
   1/r₂  = 1/(1.4 × 10⁷)                         = 7.14 × 10⁻⁸
   bracket = 1.43 × 10⁻⁷ − 7.14 × 10⁻⁸          = 7.14 × 10⁻⁸
   E_supplied = (9.95 × 10¹⁶)(7.14 × 10⁻⁸)      ≈ 7.1 × 10⁹ J

STING IN THE TAIL: the satellite ends up SLOWER in the higher orbit
   (v = √(GM/r) falls), yet you had to ADD ≈ 7.1 × 10⁹ J — total energy rose.
   Reason from E = −GMm/2r, never from speed alone.
```

### Listing 4 — Escape velocity: derivation, value, relation to orbital speed
```text
CONDITION TO JUST ESCAPE: reach infinity with zero speed
   → total energy at infinity = K(∞) + U(∞) = 0 + 0 = 0
   → energy conserved (gravity conservative) → total energy at surface = 0 too

        ½ m v_esc²  +  ( − G M m / r )  =  0
        ½ m v_esc²  =  G M m / r
        (m cancels — escape speed is INDEPENDENT of the object's mass)
        v_esc²      =  2 G M / r
        ─────────────────────────────
        v_esc = √( 2 G M / r )          ← ESCAPE VELOCITY
        ─────────────────────────────

RELATION TO ORBITAL SPEED (same r):
        v_orbit = √( G M / r )
        v_esc   = √2 · v_orbit   ≈ 1.41 × v_orbit      ← "root two to break free"

WORKED — escape from the Earth's SURFACE (r = R, nothing to add):
   2GM = 2(6.67 × 10⁻¹¹)(5.97 × 10²⁴) = 7.96 × 10¹⁴
   v_esc = √( 7.96 × 10¹⁴ / 6.37 × 10⁶ )
         = √( 1.25 × 10⁸ )
         ≈ 1.12 × 10⁴ m s⁻¹   (≈ 11.2 km s⁻¹)
   check: v_orbit(surface) = √(3.98×10¹⁴/6.37×10⁶) ≈ 7.9 × 10³ m s⁻¹;
          ×√2 ≈ 11.2 km s⁻¹ ✓
```

### Listing 5 — Data table (energy formulas and constants, quick reference)
| Quantity | Symbol / formula | Value / note |
|----------|------------------|--------------|
| Universal gravitational constant | G | 6.67 × 10⁻¹¹ N m² kg⁻² |
| Mass of the Earth | M_E | 5.97 × 10²⁴ kg |
| Radius of the Earth | R_E | 6.37 × 10⁶ m |
| GM for the Earth | GM_E | 3.98 × 10¹⁴ m³ s⁻² |
| Gravitational potential energy | U = −GMm/r | zero at infinity, negative everywhere |
| Kinetic energy (circular orbit) | K = +GMm/2r | positive |
| Total energy (circular orbit) | E = −GMm/2r | negative ⇒ bound |
| Energy ratio (circular orbit) | K : U : E | +1 : −2 : −1 (virial) |
| Escape velocity | v_esc = √(2GM/r) | = √2 × v_orbit |
| Escape velocity from Earth's surface | v_esc | ≈ 1.12 × 10⁴ m s⁻¹ (11.2 km s⁻¹) |
| Orbital velocity | v_orbit = √(GM/r) | M5-05 |

### Listing 6 — Worked solutions to the closing exam questions
```text
Q3 — escape velocity from the Earth's surface. (3 marks)
   v_esc = √(2GM/r),  r = R = 6.37 × 10⁶ m  (at the surface — nothing to add)
   2GM = 2(6.67 × 10⁻¹¹)(5.97 × 10²⁴) = 7.96 × 10¹⁴
   v_esc = √(7.96 × 10¹⁴ / 6.37 × 10⁶) = √(1.25 × 10⁸)
         ≈ 1.12 × 10⁴ m s⁻¹  (≈ 11.2 km s⁻¹)
   Marks: quote √(2GM/r) · use r = R · answer ≈ 11.2 km s⁻¹.  (m cancels.)

Q4 — energy to raise a 500 kg satellite from r₁ = 7.0×10⁶ m to r₂ = 1.4×10⁷ m. (4 marks)
   E_supplied = (GMm/2)(1/r₁ − 1/r₂)
             = (3.98×10¹⁴)(500)/2 · ( 1/7.0×10⁶ − 1/1.4×10⁷ )
             = (9.95×10¹⁶)(1.43×10⁻⁷ − 7.14×10⁻⁸)
             = (9.95×10¹⁶)(7.14×10⁻⁸)
             ≈ 7.1 × 10⁹ J
   Marks: energy = ΔE_total · use E = −GMm/2r · substitute · ≈ 7.1 × 10⁹ J (positive).

Q5 — derive v_esc from energy conservation; compare with v_orbit. (4 marks)
   To just escape: reach ∞ at rest ⇒ total energy = 0 there ⇒ (conserved) = 0 at surface:
        ½ m v_esc² − GMm/r = 0
        ½ m v_esc² = GMm/r
        v_esc² = 2GM/r           (m cancels)
        v_esc  = √(2GM/r)
   Compare:  v_orbit = √(GM/r)  ⇒  v_esc = √2 · v_orbit  ≈ 1.41 × v_orbit.
   Marks: set total energy = 0 (reach ∞ at rest) · surface energy equation ·
          cancel m to reach √(2GM/r) · relate to v_orbit by factor √2.
```
