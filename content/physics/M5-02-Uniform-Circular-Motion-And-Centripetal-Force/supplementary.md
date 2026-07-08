---
title: "Supplementary Materials — Uniform Circular Motion and Centripetal Force"
module: M5
lesson: "02"
script: script.md
---

# Supplementary Materials

The read-along reference for uniform circular motion: the key quantities (period, frequency, angular velocity), the centripetal acceleration and force equations, the NET-to-the-centre method, worked solutions, and the centripetal-versus-centrifugal distinction. Nothing here is spoken in the audio. Symbols: T = period (s); f = frequency (Hz); ω = angular velocity (rad s⁻¹); r = radius (m); v = orbital (tangential) speed (m s⁻¹); a_c = centripetal acceleration (m s⁻² toward the centre); F_c = centripetal force (N toward the centre); m = mass (kg); π ≈ 3.14.

### Listing 1 — Circular-motion quantities and their relationships
```text
UNIFORM CIRCULAR MOTION = moving in a circle at CONSTANT SPEED.
   • Speed is constant, but the DIRECTION of velocity changes continuously.
   • Velocity is always TANGENT to the circle (along the edge).
   • Therefore the velocity is CHANGING → there IS an acceleration (see Listing 2).

THE THREE QUANTITIES (name these for marks):
   PERIOD      T = time for one complete revolution        (seconds)
   FREQUENCY   f = number of revolutions per second        (hertz, Hz)
   ANGULAR VELOCITY  ω = angle swept per second            (radians per second)

RELATIONSHIPS:
   f = 1 / T          T = 1 / f              (frequency & period are reciprocals)
   ω = 2π / T = 2π f  (one revolution = 2π radians)

SPEED (tangential) — distance once around (circumference 2πr) per period:
   v = 2π r / T = 2π r f = ω r

KEY CONSEQUENCE of v = ω r:
   at the same ω, a point FURTHER from the centre (larger r) moves FASTER.
   (the rim of a disc outruns a point near the axle, though both turn together)

UNIT CONVERSION (revolutions per minute → SI):
   rev per min ÷ 60 = rev per second = f (Hz)   →   T = 1/f   →   ω = 2π f
```

### Listing 2 — Centripetal acceleration & force, and the NET-to-the-centre method
```text
CENTRIPETAL ACCELERATION (always directed TOWARD THE CENTRE, ⟂ to velocity):
   a_c = v² / r = ω² r
   • "centripetal" = centre-seeking.
   • perpendicular to velocity → changes DIRECTION of v, not its MAGNITUDE.
   • v² / r → double the speed ⇒ 4× the acceleration (square); tighter r ⇒ larger a_c.

CENTRIPETAL FORCE (Newton's 2nd law, F = ma, toward the centre):
   F_c = m v² / r = m ω² r

⚠ CENTRIPETAL FORCE IS NOT A NEW FORCE.
   It is the NAME for the NET of the REAL forces resolved toward the centre.
   Real forces = gravity, tension, normal force, friction.
   NEVER draw "centripetal force" as an extra arrow on a free-body diagram.

METHOD — "NET to the centre":
   1. Draw the free-body diagram: every REAL force as a labelled arrow.
   2. Find the NET force component pointing TOWARD the centre.
   3. Set that net inward force = m v² / r   (= m ω² r).
   4. Solve for the unknown (tension, friction, speed, radius…).

WHICH REAL FORCE PLAYS THE CENTRIPETAL ROLE:
   ball on a string (horizontal circle) → TENSION
   car on a flat corner                → sideways (static) FRICTION
   satellite / planet in orbit         → GRAVITY   (see M5-04, M5-05)
   charged particle in a magnetic field → the MAGNETIC FORCE (see M6)
```

### Listing 3 — Worked Example 1: ball on a string (horizontal circle)
```text
GIVEN: m = 0.5 kg, string length r = 1.0 m, period T = 2.0 s.
FIND:  (a) speed v, (b) centripetal acceleration a_c, (c) tension in the string.

(a) SPEED:
        v = 2π r / T = 2π (1.0) / 2.0 = π = 3.14 m s⁻¹

(b) CENTRIPETAL ACCELERATION (toward the centre):
        a_c = v² / r = (3.14)² / 1.0 = 9.87 / 1.0 ≈ 9.9 m s⁻²

(c) TENSION = the centripetal force (only horizontal force on the ball):
        T_string = F_c = m v² / r = m a_c = 0.5 × 9.9 ≈ 4.9 N  (inward, along the string)

NOTE: no "centripetal force" was invented — the REAL force (tension) was
      identified and set equal to m v² / r. This is "NET to the centre".
```

### Listing 4 — Worked Example 2: car rounding a flat corner (friction)
```text
GIVEN: m = 1000 kg, radius r = 25 m, constant speed v = 15 m s⁻¹.
FIND:  centripetal force required, and what provides it.

CENTRIPETAL ACCELERATION:
        a_c = v² / r = 15² / 25 = 225 / 25 = 9 m s⁻²

CENTRIPETAL FORCE required (inward):
        F_c = m v² / r = 1000 × 9 = 9000 N

PROVIDED BY: sideways STATIC FRICTION between tyres and road, acting toward
        the centre of the curve. On a FLAT road, friction is the ONLY inward force.

IF FRICTION IS INSUFFICIENT (wet/icy road, or too fast):
        friction cannot supply 9000 N → car cannot turn tightly enough →
        it continues along the TANGENT and slides off the OUTSIDE of the bend.

MAX SAFE SPEED (friction limit F_max = μ m g):  set μ m g = m v² / r
        → v_max = √(μ g r).   (banking the track raises this — see M5-03.)
```

### Listing 5 — Centripetal vs centrifugal, and the "fly-off" fact
```text
CENTRIPETAL FORCE (real):
   • directed TOWARD the centre.
   • the NET of real forces (tension / friction / gravity / normal).
   • what actually bends the straight-line path into a circle.

CENTRIFUGAL FORCE (fictitious):
   • the "outward" force people THINK they feel.
   • NOT a real force — an apparent effect of viewing motion from a
     ROTATING (accelerating, non-inertial) frame.
   • DO NOT put it on a free-body diagram in HSC analysis.

WHY YOU "FEEL FLUNG OUTWARD" (e.g. against a car door):
   • your INERTIA (Newton's 1st law) keeps you moving in a straight line;
   • the door pushes you INWARD (centripetal) to make you turn with the car;
   • you feel that inward push as pressure — there is NO outward force on you.

WHEN THE INWARD FORCE IS REMOVED (string cut / hammer released):
   • no net force → Newton's 1st law → straight line along the TANGENT,
     in the direction of motion at that instant. NOT radially outward.
```

### Listing 6 — Key facts and standard results (quick reference)
| Quantity | Formula | Notes |
|----------|---------|-------|
| Frequency | f = 1 / T | revolutions per second (Hz) |
| Angular velocity | ω = 2π / T = 2π f | radians per second |
| Tangential speed | v = 2π r / T = ω r | further out = faster (same ω) |
| Centripetal acceleration | a_c = v² / r = ω² r | toward centre, ⟂ to v |
| Centripetal force | F_c = m v² / r = m ω² r | net of real forces, inward |
| Direction of a_c and F_c | toward the centre | never outward |
| Path if inward force removed | straight line along tangent | Newton's 1st law |
| Work done by centripetal force | zero | force ⟂ displacement (see M5-03) |

### Listing 7 — Worked solutions to the closing exam questions
```text
Q3 — flat corner: m = 1200 kg, r = 50 m, v = 20 m s⁻¹. (3 marks)
   a_c = v² / r = 20² / 50 = 400 / 50 = 8 m s⁻²
   F_c = m a_c = 1200 × 8 = 9600 N  (inward)
   Provided by: sideways static FRICTION toward the centre.
   Marks: correct F = m v²/r substitution · 9600 N · friction (inward) named.

Q4 — ball on string: m = 0.2 kg, r = 0.8 m, 3 rev per second, π = 3.14. (4 marks)
   f = 3 Hz  →  T = 1/3 = 0.333 s
   v = 2π r / T = 2π r f = 2 × 3.14 × 0.8 × 3 ≈ 15.1 m s⁻¹
   T_string = F_c = m v² / r = 0.2 × (15.1)² / 0.8
            = 0.2 × 228 / 0.8 ≈ 57 N  (inward)
   Marks: T from f · v from 2πr/T · F = m v²/r · tension = F_c.

Q5 — "centrifugal force pushes passenger outward": ASSESS. (3 marks)
   NOT accurate. Centrifugal force is FICTITIOUS (a rotating-frame effect).
   Real cause: passenger's INERTIA (1st law) → tends to go straight; the door
   pushes INWARD (centripetal) to turn them with the car; felt as pressure.
   No outward force acts. Marks: fictitious force · inertia/1st law · door = inward centripetal.
```
