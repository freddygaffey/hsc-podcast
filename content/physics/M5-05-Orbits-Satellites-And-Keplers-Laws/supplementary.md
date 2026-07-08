---
title: "Supplementary Materials — Orbits, Satellites and Kepler's Laws"
module: M5
lesson: "05"
script: script.md
---

# Supplementary Materials

The read-along reference for orbits, satellites and Kepler's laws: the derivation of orbital velocity from gravity acting as the centripetal force, the "higher is slower" behaviour, Kepler's three laws, the derivation of Kepler's third law, the historical planetary data Kepler worked with, worked geostationary and low-orbit calculations, a comparison of low Earth versus geostationary orbits, a quick-reference data table, and full worked solutions to the closing questions. Nothing here is spoken in the audio. Symbols: G = universal gravitational constant = 6.67 × 10⁻¹¹ N m² kg⁻²; M = mass of the central body being orbited (kg); m = mass of the satellite/planet (kg); r = orbital radius, measured from the CENTRE of the central body (m); v = orbital (tangential) speed (m s⁻¹); T = orbital period (s); R = radius of the Earth = 6.37 × 10⁶ m; h = altitude above the surface (m); a_c = centripetal acceleration (m s⁻²).

### Listing 1 — Orbital velocity: gravity = centripetal force (derivation + worked speed)
```text
FOR A CIRCULAR ORBIT, GRAVITY IS THE CENTRIPETAL FORCE (same force, two names):

        F_gravity = F_centripetal
        G M m / r²  =  m v² / r          ← Newton's law = mv²/r

   Cancel m (satellite mass) and one r:
        G M / r  =  v²
        v = √( G M / r )        ← ORBITAL VELOCITY

KEY POINTS (each is examinable):
   • the satellite mass m CANCELS → orbital speed does NOT depend on the satellite's mass
   • speed set ONLY by the central mass M and the orbital radius r
   • r is measured from the CENTRE of the central body  (altitude given → add R first)

WORKED — orbital speed of the ISS, altitude h = 400 km:
   r = R + h = 6.37 × 10⁶ + 0.4 × 10⁶ = 6.77 × 10⁶ m
   GM = (6.67 × 10⁻¹¹)(5.97 × 10²⁴) = 3.98 × 10¹⁴
   v = √( 3.98 × 10¹⁴ / 6.77 × 10⁶ )
     = √( 5.88 × 10⁷ )
     ≈ 7.67 × 10³ m s⁻¹   (≈ 7.7 km s⁻¹ ≈ 27 600 km h⁻¹)
   Period:  T = 2πr / v = 2π(6.77 × 10⁶) / 7.67 × 10³ ≈ 5.55 × 10³ s ≈ 92 min
```

### Listing 2 — "Higher is slower": orbital speed falls as radius grows
Because \(v = \sqrt{GM/r}\), speed is inversely proportional to the square root of the radius: raise the orbit, and the speed drops (while the total energy rises toward zero — proved next episode).

| Orbit | Orbital radius r (m) | Orbital speed v = √(GM/r) (m s⁻¹) |
|-------|----------------------|-----------------------------------|
| Low Earth orbit (ISS, ~400 km) | 6.77 × 10⁶ | ≈ 7.67 × 10³ (≈ 7.7 km s⁻¹) |
| Medium (~2 000 km) | 8.37 × 10⁶ | ≈ 6.9 × 10³ |
| GPS (~20 200 km) | 2.66 × 10⁷ | ≈ 3.9 × 10³ |
| Geostationary (~35 800 km) | 4.22 × 10⁷ | ≈ 3.07 × 10³ (≈ 3.1 km s⁻¹) |

Memory hook: **"higher is slower but bigger-energy."** The trap is assuming a higher orbit means a faster satellite — speed falls with height; total energy rises.

### Listing 3 — Kepler's three laws of planetary motion
```text
MNEMONIC: "Every Astronomer Pauses"  →  Ellipse, Area, Period

1. LAW OF ELLIPSES:
   Each planet moves in an ELLIPSE with the Sun at ONE FOCUS (not the centre).

2. LAW OF EQUAL AREAS:
   The line from the Sun to a planet sweeps out EQUAL AREAS in EQUAL TIMES.
   → planet moves FASTEST when nearest the Sun, SLOWEST when furthest.
   (This is conservation of angular momentum.)

3. LAW OF PERIODS:
   T² ∝ r³   →   T² / r³ = constant  (same for all bodies orbiting the SAME central mass)
```

### Listing 4 — Derivation of Kepler's third law (T² / r³ = 4π²/GM)
```text
START: gravity provides the centripetal force for a circular orbit
        G M m / r²  =  m v² / r

SUBSTITUTE the orbital speed as circumference / period:
        v = 2πr / T
        G M m / r²  =  m (2πr / T)² / r

EXPAND the square:
        G M m / r²  =  m · 4π²r² / T² / r
                    =  4π² m r / T²

CANCEL m, then rearrange:
        G M / r²  =  4π² r / T²
        G M T²    =  4π² r³
        ────────────────────────────
        T² / r³  =  4π² / (G M)        ← KEPLER'S THIRD LAW
        ────────────────────────────

   • the right-hand side has NO satellite terms → same constant for all satellites of M
   • the constant depends on the CENTRAL mass M only
   • Earth's constant ≠ Sun's constant (different M) — never mix them
```

### Listing 5 — Kepler's data (Tycho Brahe's observations; r³/T² is constant)
The data Kepler pulled his third law from in 1618. The last column, \(r^3/T^2\), is very nearly the same for every planet — the whole point.

| Planet  | Mean distance to Sun (AU) | Period (days) | r³/T² (10⁻⁶ AU³/day²) |
|---------|---------------------------|---------------|-----------------------|
| Mercury | 0.389                     | 87.77         | 7.64                  |
| Venus   | 0.724                     | 224.70        | 7.52                  |
| Earth   | 1.000                     | 365.25        | 7.50                  |
| Mars    | 1.524                     | 686.95        | 7.50                  |
| Jupiter | 5.20                      | 4332.62       | 7.49                  |
| Saturn  | 9.510                     | 10759.2       | 7.43                  |

The ratio holds constant to ~2% across the solar system — strong evidence for the heliocentric model. (Full story: case study on Kepler's third law from empirical data.)

### Listing 6 — Geostationary orbit: radius from Kepler's third law (worked)
```text
GOAL: find the orbital radius for which the period T = 1 day, so the satellite keeps
      pace with the Earth's rotation and appears fixed above one point on the equator.

Rearrange Kepler's third law for r³:
        T² / r³ = 4π² / (G M)   →   r³ = G M T² / (4π²)

Substitute  (T = 1 day = 86 400 s):
        G M   = 3.98 × 10¹⁴
        T²    = (86 400)² = 7.46 × 10⁹
        r³    = (3.98 × 10¹⁴)(7.46 × 10⁹) / (4π²)
              = 2.97 × 10²⁴ / 39.5
              = 7.52 × 10²²
        r     = (7.52 × 10²²)^(1/3) ≈ 4.22 × 10⁷ m   (≈ 42 200 km from Earth's CENTRE)

ALTITUDE above the surface:
        h = r − R = 4.22 × 10⁷ − 6.37 × 10⁶ ≈ 3.58 × 10⁷ m ≈ 35 800 km

Orbital speed there:  v = √(GM/r) = √(3.98 × 10¹⁴ / 4.22 × 10⁷) ≈ 3.07 × 10³ m s⁻¹
   → must be over the EQUATOR, moving with Earth's spin, to be geostationary.
```

### Listing 7 — Low Earth orbit vs geostationary orbit (comparison + uses)
| Feature | Low Earth orbit (LEO) | Geostationary orbit (GEO) |
|---------|-----------------------|---------------------------|
| Altitude | ~200–2 000 km (e.g. ISS ~400 km) | ~35 800 km (over the equator) |
| Orbital radius r | ~6.8 × 10⁶ m | ~4.22 × 10⁷ m |
| Orbital speed | ~7.7 km s⁻¹ (fast) | ~3.1 km s⁻¹ (slow) |
| Period | ~90 min | 24 h (matches Earth's spin) |
| Appears from ground | races across the sky | fixed over one point |
| Typical uses | imaging, spy/weather sensing, ISS, Hubble | communications, TV, weather, GPS timing |

"Higher is slower": GEO is ~6× the radius of LEO, so its speed is ~√6 ≈ 2.5× slower.

### Listing 8 — Data table (constants and orbits, quick reference)
| Quantity | Symbol | Value |
|----------|--------|-------|
| Universal gravitational constant | G | 6.67 × 10⁻¹¹ N m² kg⁻² |
| Mass of the Earth | M_E | 5.97 × 10²⁴ kg |
| Radius of the Earth | R_E | 6.37 × 10⁶ m |
| GM for the Earth | GM_E | 3.98 × 10¹⁴ m³ s⁻² |
| Mass of the Sun | M_S | 1.99 × 10³⁰ kg |
| Geostationary orbital radius | r_geo | ≈ 4.22 × 10⁷ m |
| Geostationary altitude | h_geo | ≈ 3.58 × 10⁷ m (≈ 35 800 km) |
| One day (period of GEO) | T | 86 400 s |
| Orbital velocity | v = √(GM/r) | — |
| Kepler's third law | T²/r³ = 4π²/GM | — |

### Listing 9 — Worked solutions to the closing exam questions
```text
Q3 — orbital speed at 600 km altitude. (3 marks)
   r = R + h = 6.37 × 10⁶ + 0.6 × 10⁶ = 6.97 × 10⁶ m   (add altitude to radius!)
   v = √(GM/r) = √( (6.67 × 10⁻¹¹)(5.97 × 10²⁴) / 6.97 × 10⁶ )
     = √( 3.98 × 10¹⁴ / 6.97 × 10⁶ ) = √( 5.71 × 10⁷ )
     ≈ 7.6 × 10³ m s⁻¹   (≈ 7.6 km s⁻¹)
   Marks: add h to R · substitute √(GM/r) · ≈ 7.6 × 10³ m s⁻¹.

Q4 — geostationary orbital radius and altitude (T = 1 day). (4 marks)
   r³ = G M T² / (4π²) = (3.98 × 10¹⁴)(86 400)² / (4π²)
      = (3.98 × 10¹⁴)(7.46 × 10⁹) / 39.5 = 7.52 × 10²²
   r  = (7.52 × 10²²)^(1/3) ≈ 4.22 × 10⁷ m  (≈ 42 200 km from centre)
   h  = r − R = 4.22 × 10⁷ − 6.37 × 10⁶ ≈ 3.58 × 10⁷ m ≈ 35 800 km
   Marks: rearrange for r³ · substitute T in seconds · cube root ≈ 4.22 × 10⁷ m ·
          subtract R for altitude ≈ 35 800 km.

Q5 — period ratio for r × 4 (same central mass). (3 marks)
   Kepler 3:  T² ∝ r³
   r → 4r  ⇒  r³ → 4³ = 64  ⇒  T² → 64  ⇒  T → √64 = 8
   → the outer moon's period is 8 × the inner moon's.
   Marks: T² ∝ r³ · cube the factor 4 → 64 · square-root → factor 8 (don't stop at 64).
```
