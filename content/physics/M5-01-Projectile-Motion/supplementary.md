---
title: "Supplementary Materials — Projectile Motion"
module: M5
lesson: "01"
script: script.md
---

# Supplementary Materials

The read-along reference for projectile motion: the model and its assumptions, the SPLIT-then-SUVAT method, the suvat toolkit, and full worked solutions. Nothing here is spoken in the audio. Symbols: u = initial velocity; v = final velocity; a = acceleration; t = time; s = displacement; g = acceleration due to gravity ≈ 9.8 m s⁻² (downward); uₓ = horizontal component of launch velocity; u_y = vertical component of launch velocity; θ = launch angle above the horizontal; H = maximum height; T = time of flight; R = range.

### Listing 1 — The projectile model and the SPLIT-then-SUVAT method
```text
PROJECTILE = an object launched into the air, then moving under GRAVITY ALONE.
   (football, cricket ball, bullet, long-jumper, water jet, stunt car off a ramp)

MODEL ASSUMPTIONS (name these for marks):
   • NO air resistance.
   • Acceleration is CONSTANT = g ≈ 9.8 m s⁻², directed VERTICALLY DOWNWARD.
   • NO horizontal force  →  NO horizontal acceleration.

THE KEY IDEA — horizontal & vertical motion are INDEPENDENT:
   • HORIZONTAL: no force → velocity is CONSTANT for the whole flight (uₓ never changes).
   • VERTICAL:   free fall → constant acceleration g (u_y changes under gravity).
   • They share ONE thing only: the TIME (the same clock ticks for both).

METHOD — "SPLIT then SUVAT":
   1. SPLIT  — resolve into a constant-velocity HORIZONTAL part and a
              constant-acceleration VERTICAL part.
   2. SUVAT  — solve each part as its own 1-D suvat problem.
   BRIDGE   — the TIME links the two halves.
   USUAL ROUTE: use the VERTICAL motion to find the TIME, then feed t into the
                HORIZONTAL motion (R = uₓ t) to find the RANGE.

RESOLVING THE LAUNCH VELOCITY (angle θ from the horizontal):
   uₓ = u cos θ   (horizontal, adjacent to angle → cosine; stays CONSTANT)
   u_y = u sin θ  (vertical, opposite the angle → sine; CHANGES under g)
```

### Listing 2 — The SUVAT toolkit (constant acceleration, per axis)
```text
Apply ONLY to the vertical axis (a = g) — horizontally a = 0, so s = uₓ t.

   v = u + a t
   s = u t + ½ a t²
   v² = u² + 2 a s
   s = ½ (u + v) t

SIGN CONVENTION: pick "up = positive". Then a = −g for the vertical axis
   (gravity points down). Many level-ground shortcuts use magnitudes directly:

   time to top:      t_top = u_y / g          (v_y = 0 at the top)
   time of flight:   T = 2 u_y / g            (symmetric: time up = time down)
   maximum height:   H = u_y² / (2g)
   range (level):    R = uₓ T = uₓ · (2 u_y / g)

⚠ At the TOP of the arc, v_y = 0 but vₓ is UNCHANGED → the object is STILL MOVING.
⚠ These symmetry shortcuts assume LANDING HEIGHT = LAUNCH HEIGHT. If it lands
   higher/lower, solve the vertical quadratic s = u_y t − ½ g t² for t instead.
```

### Listing 3 — Worked Example 1: horizontal launch off a table (Galileo geometry)
```text
GIVEN: ball leaves a table horizontally. Height h = 1.25 m, launch speed = 3.0 m s⁻¹,
       g = 9.8 m s⁻². Find (a) time of flight, (b) range, (c) landing velocity.

SPLIT:  horizontal uₓ = 3.0 m s⁻¹ (constant);  vertical u_y = 0 (launched horizontally).

(a) VERTICAL gives the time (sets the clock):
        s = u_y t + ½ g t²   →   1.25 = 0 + ½ (9.8) t²
        t² = (2 × 1.25) / 9.8 = 0.2551
        t  = 0.505 s

(b) HORIZONTAL gives the range (coasts along that clock):
        R = uₓ t = 3.0 × 0.505 = 1.52 m

(c) LANDING VELOCITY (combine components at impact):
        v_y = g t = 9.8 × 0.505 = 4.95 m s⁻¹ (downward)
        vₓ = 3.0 m s⁻¹ (unchanged)
        speed = √(3.0² + 4.95²) = √33.5 = 5.79 m s⁻¹
        angle below horizontal = tan⁻¹(4.95 / 3.0) = 58.8°

NOTE: mass never appears (g is the same for every mass).
NOTE: double the launch speed → same t (vertical unchanged), DOUBLE the range.
      A ball DROPPED at the same instant lands at the SAME time (identical vertical motion).
```

### Listing 4 — Worked Example 2: launch at an angle (max height, time of flight, range)
```text
GIVEN: launched from ground level at u = 20 m s⁻¹, θ = 30° above horizontal, g = 9.8.

RESOLVE:
   uₓ = 20 cos 30° = 20 × 0.866 = 17.3 m s⁻¹  (constant)
   u_y = 20 sin 30° = 20 × 0.5   = 10.0 m s⁻¹  (upward, changes under g)

TIME TO TOP (v_y = 0):
   t_top = u_y / g = 10.0 / 9.8 = 1.02 s

TIME OF FLIGHT (symmetry, up = down):
   T = 2 t_top = 2.04 s

MAXIMUM HEIGHT (v² = u² − 2gs with v_y = 0 at top):
   H = u_y² / (2g) = 10.0² / (2 × 9.8) = 100 / 19.6 = 5.10 m

RANGE (constant horizontal velocity × total time):
   R = uₓ T = 17.3 × 2.04 = 35.3 m

SEQUENCE TO MEMORISE: resolve → vertical gives times & height → horizontal + total time gives range.
```

### Listing 5 — Why the path is a PARABOLA (eliminating time)
```text
Horizontal (constant velocity):     x = uₓ t          →   t = x / uₓ
Vertical (constant acceleration):   y = u_y t − ½ g t²

Substitute t = x / uₓ into the vertical equation:

   y = u_y (x / uₓ) − ½ g (x / uₓ)²
   y = (u_y / uₓ) x − ( g / (2 uₓ²) ) x²

y depends on x². A relationship of the form  y = (constant)x − (constant)x²
is a PARABOLA. Hence every projectile (no air resistance) follows a PARABOLIC path.
Use the word "parabolic" in exam answers — not "curved" or "arced".
```

### Listing 6 — Launch angle & range: 45° is furthest, complements match
```text
On LEVEL ground, for a FIXED launch speed:

   • RANGE is MAXIMUM at θ = 45°  (best trade-off between hang-time and horizontal speed).
   • COMPLEMENTARY angles give EQUAL ranges:
        θ and (90° − θ) → same R.
        e.g. 15° & 75°  ·  30° & 60°  ·  40° & 50°.
     The higher angle → tall, slow, long-hanging arc; the lower angle → flat, fast path;
     the horizontal distances come out identical.

MNEMONIC: "45 for furthest, and complements match."

WHY (level ground): R = (u² sin 2θ) / g.
   sin 2θ is maximised at 2θ = 90° → θ = 45°.
   sin 2θ = sin(180° − 2θ) → θ and (90° − θ) give the same R.
```

### Listing 7 — Worked solutions to the closing exam questions
```text
Q2 — horizontal launch: u = 8 m s⁻¹, h = 20 m, g = 9.8. (3 marks)
   VERTICAL (u_y = 0):  20 = ½ (9.8) t²  →  t² = 40 / 9.8 = 4.08  →  t = 2.02 s
   HORIZONTAL:          R = uₓ t = 8 × 2.02 = 16.2 m
   Marks: u_y = 0 · time from vertical · R = constant uₓ × t.

Q3 — complementary angles: 50 m s⁻¹ at 60° vs 30°. (2 marks)
   RANGES ARE EQUAL. 60° + 30° = 90° (complementary), so same R for the same speed
   on level ground. (See Listing 6.)  Marks: "equal" + complementary-angle reason.

Q4 — full angled projectile: u = 25 m s⁻¹, θ = 53°, g = 10, sin53 = 0.8, cos53 = 0.6. (5 marks)
   RESOLVE:  uₓ = 25 × 0.6 = 15 m s⁻¹ (constant)
             u_y = 25 × 0.8 = 20 m s⁻¹ (up)
   MAX HEIGHT:  H = u_y² / (2g) = 20² / (2×10) = 400 / 20 = 20 m
   TIME OF FLIGHT:  t_top = u_y / g = 20 / 10 = 2 s  →  T = 2 × 2 = 4 s
   RANGE:  R = uₓ T = 15 × 4 = 60 m
   Marks: resolve · H from vertical (v_y = 0) · T = 2 t_top · R = uₓ T.
   Mass never enters — g is independent of mass.
```

### Listing 8 — Key facts and standard results (quick reference)
| Quantity | Formula (level ground) | Notes |
|----------|------------------------|-------|
| Horizontal velocity | uₓ = u cos θ | constant for whole flight |
| Vertical velocity (launch) | u_y = u sin θ | changes under gravity |
| Horizontal displacement | x = uₓ t | no acceleration term |
| Vertical displacement | y = u_y t − ½ g t² | free-fall term |
| Time to maximum height | t_top = u_y / g | v_y = 0 at the top |
| Time of flight | T = 2 u_y / g | symmetric flight only |
| Maximum height | H = u_y² / (2g) | from v² = u² − 2gs |
| Range | R = uₓ T = (u² sin 2θ)/g | max at θ = 45° |
| Acceleration | a = g ≈ 9.8 m s⁻² down | independent of mass |
