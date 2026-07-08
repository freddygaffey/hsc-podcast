---
title: "Supplementary Materials — Circular Motion in Practice, and Torque"
module: M5
lesson: "03"
script: script.md
---

# Supplementary Materials

The read-along reference for circular motion in practice and torque: the NET-to-the-centre method carried forward, the flat and banked corner, the conical pendulum, the vertical circle, why the centripetal force does no work, torque, and full worked solutions. Nothing here is spoken in the audio. Symbols: m = mass (kg); r = radius of the circular path (m); v = tangential speed (m s⁻¹); g = 9.8 m s⁻² (gravitational acceleration); N = normal force (N); T = tension (N); μ = coefficient of (static) friction; θ = angle (of bank, string, or applied force); F_c = centripetal force (N, toward the centre); τ = torque (N m); W = weight = mg (N).

### Listing 1 — NET-to-the-centre carried forward, and the flat corner
```text
THE METHOD (reused from M5-02) — "NET to the centre":
   1. Draw the free-body diagram: every REAL force as a labelled arrow.
      (Real forces = gravity, tension, normal force, friction. NEVER an
       "extra" centripetal-force arrow — centripetal force IS the net.)
   2. Resolve forces; find the NET component pointing TOWARD the centre.
   3. Set that net inward force = m v² / r   (= m ω² r).
   4. Solve for the unknown.

FLAT (level) CORNER — friction is the centripetal force:
   friction acts inward:        F_c = friction = m v² / r
   friction has a CEILING:      friction_max = μ m g
   MAX SAFE SPEED (set them equal):
        μ m g = m v² / r   →   v_max = √(μ g r)
   Above v_max: friction can't supply enough inward force →
        car runs along the TANGENT, slides off the OUTSIDE of the bend.
   (Independent of mass: m cancels.)
```

### Listing 2 — Banked track (frictionless design speed) + worked example
```text
SETUP: a car on a track banked at angle θ, NO friction.
Only two forces act: weight W = mg (down), and normal force N
(perpendicular to the tilted surface, so it leans inward by angle θ).

RESOLVE the tilted normal force into components:
   VERTICAL   (holds the car up):        N cos θ = m g
   HORIZONTAL (points to the centre):    N sin θ = m v² / r   ← this IS F_c

DIVIDE the horizontal equation by the vertical equation
(N cancels, m cancels):
        (N sin θ)/(N cos θ) = (m v²/r)/(m g)
        tan θ = v² / (r g)                ← DESIGN-SPEED relationship

   → v_design = √(r g tan θ)

BEHAVIOUR off the design speed (friction present in reality):
   too SLOW  → needs less F_c than bank gives → tends to slide DOWN/inward.
   too FAST  → needs more F_c than bank gives → tends to slide UP/outward.
   Steeper bank (larger θ) → larger v_design (velodrome ≈ 42°, road ≈ few°).

WORKED EXAMPLE: r = 50 m, θ = 30°  (tan 30° ≈ 0.577), g = 9.8.
   v² = r g tan θ = 50 × 9.8 × 0.577 ≈ 283
   v  = √283 ≈ 16.8 m s⁻¹   (≈ 60 km h⁻¹)
   NOTE: mass never appears — one banking angle works for all vehicles.
```

### Listing 3 — Conical pendulum (same physics as the banked track) + worked example
```text
SETUP: a ball on a string of length L swung so it traces a HORIZONTAL circle;
the string sweeps out a cone, making angle θ with the VERTICAL.
Two forces: weight W = mg (down), tension T (up along the string).

TRAP — the radius is NOT the string length:
        r = L sin θ     (horizontal distance from ball to the central axis)

RESOLVE the tension:
   VERTICAL   (balances gravity):        T cos θ = m g
   HORIZONTAL (points to the centre):    T sin θ = m v² / r   ← this IS F_c

DIVIDE → same form as the banked track:
        tan θ = v² / (r g)

WORKED EXAMPLE: m = 0.3 kg, L = 1.5 m, θ = 25° from vertical, g = 9.8.
   (cos 25° ≈ 0.906,  sin 25° ≈ 0.423)
   Tension (vertical balance):
        T = m g / cos θ = (0.3 × 9.8) / 0.906 = 2.94 / 0.906 ≈ 3.24 N
   Radius:
        r = L sin θ = 1.5 × 0.423 ≈ 0.634 m
   Speed (horizontal equation T sin θ = m v²/r):
        v² = (T sin θ × r) / m = (3.24 × 0.423 × 0.634) / 0.3 ≈ 2.90
        v  = √2.90 ≈ 1.70 m s⁻¹
   ANSWER: tension ≈ 3.24 N, speed ≈ 1.70 m s⁻¹.
```

### Listing 4 — Vertical circle: top vs bottom, and minimum speed at the top
```text
NOT uniform (speed changes with height) — but at every instant the NET
INWARD force = m v² / r. Only gravity and tension act.

AT THE TOP (both gravity and tension point DOWN = toward centre, they ADD):
        T + m g = m v² / r
        → T = m v²/r − m g

MINIMUM SPEED AT THE TOP (string just goes slack, T = 0):
        m g = m v²/r      (m cancels)
        → v_min = √(g r)
   Below v_min: gravity exceeds the required F_c → object leaves the circle,
   string slack, water spills.

AT THE BOTTOM (tension UP = toward centre; gravity DOWN = away from centre):
        T − m g = m v² / r
        → T = m v²/r + m g          ← LARGEST tension → string breaks here

WORKED EXAMPLE: m = 0.25 kg, r = 0.6 m, v_bottom = 5 m s⁻¹, g = 9.8.
   Minimum speed at top:
        v_min = √(g r) = √(9.8 × 0.6) = √5.88 ≈ 2.4 m s⁻¹
   Tension at the bottom:
        T = m v²/r + m g = (0.25 × 5² / 0.6) + (0.25 × 9.8)
          = (0.25 × 25 / 0.6) + 2.45 = (6.25 / 0.6) + 2.45
          ≈ 10.4 + 2.45 ≈ 12.9 N
```

### Listing 5 — Why the centripetal force does NO work
```text
WORK: only the component of force ALONG the motion does work.
   W_done = F × d × cos(angle between force and displacement)

CENTRIPETAL FORCE is toward the CENTRE (along the radius);
VELOCITY (displacement) is along the TANGENT.
   → they are always PERPENDICULAR (90° apart), cos 90° = 0.
   → the centripetal force does ZERO work, everywhere on the path.

CONSEQUENCE:
   no work → no energy transfer → kinetic energy constant → SPEED constant.
   This is why uniform circular motion stays uniform (e.g. a satellite in a
   circular orbit keeps constant speed with no engine — see M5-05).

VERTICAL CIRCLE nuance:
   the centripetal force STILL does no work (still ⟂ to motion).
   The speed changes because the ALONG-TRACK component of GRAVITY does work
   (negative going up, positive coming down) — KE ↔ GPE, the M2 work–energy
   trade. The centripetal part never changes the speed.
```

### Listing 6 — Torque: the turning effect of a force
```text
TORQUE  τ = r F sin θ        (units: newton metres, N m)  — a VECTOR
   r  = distance from the pivot to where the force is applied (m)
   F  = applied force (N)
   θ  = angle between the arm r and the force F

THREE WAYS TO INCREASE TORQUE — mnemonic "REACH, FORCE, SQUARE-ON":
   REACH     larger r  (longer spanner)
   FORCE     larger F  (push harder)
   SQUARE-ON larger θ toward 90°  (sin θ max = 1 at θ = 90°)
   → sin 0° = 0: a force ALONG the arm produces NO turning at all.

TWO EQUIVALENT READINGS of r F sin θ (use whichever the data gives):
   (a) (F sin θ) × r  = perpendicular component of force × full arm
   (b) F × (r sin θ)  = full force × perpendicular distance to line of force
                        (r sin θ is the "lever arm" / "moment arm")

WORKED EXAMPLE: F = 80 N applied at r = 0.3 m, θ = 60° (sin 60° ≈ 0.866).
   τ = r F sin θ = 0.3 × 80 × 0.866 ≈ 20.8 N m
   Check via reading (a): F sin θ = 80 × 0.866 = 69.3 N; × 0.3 = 20.8 N m ✓
   Maximum for same F (θ = 90°): τ = 0.3 × 80 × 1 = 24 N m.
```

### Listing 7 — Key results (quick reference)
| Scenario | What provides the centripetal force | Key equation |
|----------|-------------------------------------|--------------|
| Flat corner | sideways static friction (inward) | v_max = √(μ g r) |
| Banked track (no friction) | horizontal component of normal force | tan θ = v² / (r g) → v = √(r g tan θ) |
| Conical pendulum | horizontal component of tension | tan θ = v² / (r g); r = L sin θ |
| Vertical circle — top | tension + weight (both inward) | T + mg = m v²/r; v_min = √(g r) |
| Vertical circle — bottom | tension − weight (net inward) | T − mg = m v²/r → T = m v²/r + mg |
| Work by centripetal force | — | zero (force ⟂ motion) ⇒ speed constant |
| Torque | — | τ = r F sin θ (N m); max at θ = 90° |

### Listing 8 — Worked solutions to the closing exam questions
```text
Q3 — banked bend: m = 1200 kg, r = 40 m, θ = 20° (tan 20° = 0.364), g = 9.8. (3 marks)
   tan θ = v²/(r g)  →  v² = r g tan θ = 40 × 9.8 × 0.364
   v² = 392 × 0.364 ≈ 143  →  v = √143 ≈ 12 m s⁻¹
   Mass cancels → same design speed for any vehicle.
   Marks: tan θ = v²/(r g) · substitution/rearrangement · ≈ 12 m s⁻¹ (mass cancels).

Q4 — vertical circle: m = 0.25 kg, r = 0.6 m, v_bottom = 5 m s⁻¹, g = 9.8. (4 marks)
   (a) Minimum speed at top (T = 0, gravity alone is F_c):
        v_min = √(g r) = √(9.8 × 0.6) = √5.88 ≈ 2.4 m s⁻¹
   (b) Tension at the bottom:
        T = m v²/r + m g = (0.25 × 25 / 0.6) + (0.25 × 9.8)
          = 10.42 + 2.45 ≈ 12.9 N
   Marks: v_min = √(g r) · ≈ 2.4 m s⁻¹ · T = m v²/r + mg · ≈ 12.9 N.

Q5 — spanner: F = 80 N, r = 0.3 m, θ = 60° (sin 60° = 0.866). (3 marks)
   τ = r F sin θ = 0.3 × 80 × 0.866 ≈ 20.8 N m
   Max torque for same F at θ = 90° (sin 90° = 1): τ = 0.3 × 80 = 24 N m.
   Marks: τ = r F sin θ substitution · ≈ 20.8 N m · 90° maximises (sin 90° = 1).
```
