---
title: "Supplementary Materials — Universal Gravitation and Gravitational Fields"
module: M5
lesson: "04"
script: script.md
---

# Supplementary Materials

The read-along reference for universal gravitation and gravitational fields: Newton's law of universal gravitation, the inverse-square behaviour, the gravitational field strength and its link to weight and to the acceleration due to gravity, the surface value of little-g, weighing the Earth, the variation of little-g with altitude, a data table of constants and bodies, and full worked solutions. Nothing here is spoken in the audio. Symbols: F = gravitational force (N); G = universal gravitational constant = 6.67 × 10⁻¹¹ N m² kg⁻²; M = mass of the large body, e.g. a planet (kg); m = mass of the small/second body (kg); r = distance between the centres of the two masses (m); g = gravitational field strength (N kg⁻¹) = acceleration due to gravity (m s⁻²); R = radius of the planet (m); h = altitude above the surface (m); W = weight = mg (N).

### Listing 1 — Newton's law of universal gravitation + worked Earth–Moon force
```text
NEWTON'S LAW OF UNIVERSAL GRAVITATION:
   Every mass attracts every other mass.

        F = G M m / r²        (units of F: newtons, N)

   G = 6.67 × 10⁻¹¹ N m² kg⁻²   (universal gravitational constant)
   M, m = the two masses (kg)
   r    = distance CENTRE-to-CENTRE (m)   ← NOT surface to surface

KEY FEATURES (each is examinable):
   • proportional to the PRODUCT of the masses  → double either mass, double F
   • INVERSE-SQUARE in distance  → double r, F → quarter  ("twice as far, a quarter the pull")
   • always ATTRACTIVE (only one kind of mass)
   • mutual (Newton's 3rd law): Earth pulls apple = apple pulls Earth (equal, opposite)
   • G is tiny → gravity is the WEAKEST fundamental force; only matters at planetary scale.

WORKED — force between Earth and Moon:
   M_Earth = 5.97 × 10²⁴ kg,  m_Moon = 7.35 × 10²² kg,  r = 3.84 × 10⁸ m
   F = G M m / r²
     = (6.67 × 10⁻¹¹)(5.97 × 10²⁴)(7.35 × 10²²) / (3.84 × 10⁸)²
   numerator  = 2.93 × 10³⁷
   denominator= (3.84 × 10⁸)² = 1.47 × 10¹⁷
   F = 2.93 × 10³⁷ / 1.47 × 10¹⁷ ≈ 1.98 × 10²⁰ N  ≈ 2 × 10²⁰ N
```

### Listing 2 — Inverse-square behaviour (what happens to F as r changes)
Because F ∝ 1 / r², whatever you multiply the distance by, you square it and divide.

| Distance changes to… | r factor | Force is multiplied by | Force becomes |
|----------------------|----------|------------------------|---------------|
| half as far          | ½        | 1 / (½)² = 4           | 4 × stronger  |
| same                 | 1        | 1                      | unchanged     |
| twice as far         | 2        | 1 / 2² = 1/4           | one quarter   |
| three times as far   | 3        | 1 / 3² = 1/9           | one ninth     |
| four times as far    | 4        | 1 / 4² = 1/16          | one sixteenth |

Memory hook: **"twice as far, a quarter the pull."** The trap is halving (÷2) instead of quartering (÷4) — always square the distance factor.

### Listing 3 — Gravitational field strength g, and why it equals the acceleration due to gravity
```text
GRAVITATIONAL FIELD STRENGTH: force per unit mass on a small test mass.
        g = F / m            (units: newtons per kilogram, N kg⁻¹)

DERIVE g AROUND A PLANET (the m cancels):
        F = G M m / r²                       (Newton's law on a test mass m)
        g = F / m = (G M m / r²) / m
        g = G M / r²          ← field depends ONLY on M and r, NOT on the test mass

CONSEQUENCE: the test mass cancels → every object has the SAME g at a given point
   → all objects fall with the SAME acceleration (feather & hammer on the Moon).

WHY g (field, N kg⁻¹) = g (acceleration, m s⁻²) — the SAME number:
        Weight from Newton's 2nd law:      W = m a = m g_acceleration
        Weight from the field definition:  W = m g_field
        Same W, same m  →  g_acceleration = g_field
   The units N kg⁻¹ and m s⁻² are identical: 1 N kg⁻¹ = 1 m s⁻².
```

### Listing 4 — g at Earth's surface, and "weighing the Earth" (rearranging for M)
```text
FIELD STRENGTH AT THE SURFACE (r = R, the planet's radius):
        g = G M / R²

WORKED — Earth's surface value:
   M_Earth = 5.97 × 10²⁴ kg,  R_Earth = 6.37 × 10⁶ m,  G = 6.67 × 10⁻¹¹
        g = (6.67 × 10⁻¹¹)(5.97 × 10²⁴) / (6.37 × 10⁶)²
          = 3.98 × 10¹⁴ / 4.06 × 10¹³
          ≈ 9.8 N kg⁻¹   (= 9.8 m s⁻²)   ← this is where "9.8" comes from

WEIGHING THE EARTH (rearrange the surface equation for M):
        g = G M / R²      →      M = g R² / G
   Everything on the right is measurable:
        g ≈ 9.8 (drop objects),  R known (geometry),  G measured by Cavendish (1798).
        M = (9.8)(6.37 × 10⁶)² / (6.67 × 10⁻¹¹)
          = (9.8)(4.06 × 10¹³) / (6.67 × 10⁻¹¹)
          ≈ 6.0 × 10²⁴ kg    ← the mass of the Earth, found without leaving the lab
```

### Listing 5 — g with altitude (worked: the ISS) + surface gravity of other bodies
```text
VARIATION WITH ALTITUDE h (r measured from the CENTRE):
        r = R + h       ← REFLEX: altitude given, ADD the radius first
        g(h) = G M / (R + h)²

WORKED — the International Space Station, h = 400 km above the surface:
   R = 6.37 × 10⁶ m,  h = 400 km = 0.4 × 10⁶ m
        r = R + h = 6.37 × 10⁶ + 0.4 × 10⁶ = 6.77 × 10⁶ m
        g = (6.67 × 10⁻¹¹)(5.97 × 10²⁴) / (6.77 × 10⁶)²
          = 3.98 × 10¹⁴ / 4.58 × 10¹³
          ≈ 8.7 N kg⁻¹   (≈ 89% of the surface value)

   → Gravity is still STRONG in low orbit. Astronauts float because they are in
     continuous FREE FALL (orbiting), not because gravity is absent =
     APPARENT WEIGHTLESSNESS. (Newton's cannon: falling = orbiting.)
```

Surface gravity is a competition between mass (top) and radius squared (bottom), so a small dense body can out-pull a large one:

| Body    | Mass (kg)        | Radius (m)       | g = GM/R² (N kg⁻¹) |
|---------|------------------|------------------|--------------------|
| Sun     | 1.99 × 10³⁰      | 6.96 × 10⁸       | ≈ 274              |
| Jupiter | 1.90 × 10²⁷      | 6.99 × 10⁷       | ≈ 24.8             |
| Earth   | 5.97 × 10²⁴      | 6.37 × 10⁶       | ≈ 9.8              |
| Mars    | 6.42 × 10²³      | 3.39 × 10⁶       | ≈ 3.7              |
| Moon    | 7.35 × 10²²      | 1.74 × 10⁶       | ≈ 1.6 (about 1/6 of Earth) |

### Listing 6 — Data table (constants and bodies, quick reference)
| Quantity | Symbol | Value |
|----------|--------|-------|
| Universal gravitational constant | G | 6.67 × 10⁻¹¹ N m² kg⁻² |
| Acceleration due to gravity (Earth surface) | g | 9.8 m s⁻² = 9.8 N kg⁻¹ |
| Mass of the Earth | M_E | 5.97 × 10²⁴ kg |
| Radius of the Earth | R_E | 6.37 × 10⁶ m |
| Mass of the Moon | M_M | 7.35 × 10²² kg |
| Radius of the Moon | R_M | 1.74 × 10⁶ m |
| Earth–Moon centre-to-centre distance | d | 3.84 × 10⁸ m |
| Mass of the Sun | M_S | 1.99 × 10³⁰ kg |

### Listing 7 — Worked solutions to the closing exam questions
```text
Q3 — Earth–Moon gravitational force. (3 marks)
   F = G M m / r²
     = (6.67 × 10⁻¹¹)(5.97 × 10²⁴)(7.35 × 10²²) / (3.84 × 10⁸)²
     = 2.93 × 10³⁷ / 1.47 × 10¹⁷
     ≈ 2 × 10²⁰ N
   Marks: formula + substitution · distance squared correctly · ≈ 2 × 10²⁰ N.

Q4 — field strength at 400 km altitude + weightlessness. (4 marks)
   r = R + h = 6.37 × 10⁶ + 0.4 × 10⁶ = 6.77 × 10⁶ m   (add altitude to radius!)
   g = G M / r² = (6.67 × 10⁻¹¹)(5.97 × 10²⁴) / (6.77 × 10⁶)²
     = 3.98 × 10¹⁴ / 4.58 × 10¹³ ≈ 8.7 N kg⁻¹
   Weightlessness: g is ≈ 89% of surface, so gravity is NOT absent; astronauts
     are in continuous free fall (orbit) → no contact force → apparent weightlessness.
   Marks: add h to R · substitute GM/r² · ≈ 8.7 N kg⁻¹ · free fall, not "no gravity".

Q5 — determining the mass of the Earth. (3 marks)
   Surface field:   g = G M / R²
   Rearrange:       M = g R² / G
     = (9.8)(6.37 × 10⁶)² / (6.67 × 10⁻¹¹)
     = (9.8)(4.06 × 10¹³) / (6.67 × 10⁻¹¹) ≈ 6.0 × 10²⁴ kg
   Marks: start from g = GM/R² · rearrange to M = gR²/G · link to Cavendish measuring G.
```
