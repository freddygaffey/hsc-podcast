---
title: "Supplementary Materials — Module Review: Advanced Mechanics"
module: M5
lesson: "99"
script: script.md
---

# Supplementary Materials

The read-along reference for the Module Five review: the four mnemonics and the master equation toolkit, the projectile "split then suvat" method worked in full, a "net to the centre" circular-motion example, the Newton's-cannon progression from projectile to orbit to escape with the orbital-speed and Kepler's-third-law derivations, the gravitational-energy and escape-velocity summary, and full worked solutions to the closing exam questions. Nothing here is spoken in the audio. Symbols: G = universal gravitational constant = 6.67 × 10⁻¹¹ N m² kg⁻²; M = mass of the central body (kg); m = mass of the small object (kg); r = distance from the CENTRE of the central body (m); R_E = radius of the Earth = 6.37 × 10⁶ m; g = 9.8 m s⁻²; v = speed (m s⁻¹); T = period (s); a_c = centripetal acceleration (m s⁻²); F_c = centripetal force (N); U = gravitational potential energy (J); E = total mechanical energy (J); v_esc = escape velocity. For the Earth GM = 3.98 × 10¹⁴ m³ s⁻² and M = 5.97 × 10²⁴ kg.

### Listing 1 — The four mnemonics, the master toolkit, and the six traps

```text
THE FOUR MNEMONICS (write all four in the first minute of the exam):
  1. SPLIT then SUVAT       → projectiles: resolve into horizontal (constant v)
                              and vertical (accel g); two 1-D problems, one clock.
  2. NET-to-the-CENTRE      → circular motion: centripetal force is the NET of the
                              REAL forces (gravity/tension/normal/friction) resolved
                              inward, set = m v²/r. Never a new force.
  3. HIGHER is SLOWER but   → orbits: raise r → v = √(GM/r) FALLS, but total energy
     BIGGER-ENERGY            E = −GMm/2r RISES toward zero.
  4. ZERO at INFINITY,      → gravitational energy: U = −GMm/r; a bound orbit has
     NEGATIVE everywhere      NEGATIVE total energy.
  (Kepler's laws order: "Every Astronomer Pauses" → Ellipse, Area, Period.)

MASTER TOOLKIT (all on the NSW data/formula sheet):
  Projectile:   horizontal:  x = u_x t         (u_x = u cosθ, constant)
                vertical:     v_y = u_y − g t,  Δy = u_y t − ½ g t²   (u_y = u sinθ)
  Circular:     v = 2πr/T ;  a_c = v²/r ;  F_c = m v²/r ;  τ = r F sinθ
  Gravitation:  F = G M m / r² ;  g = G M / r²   ("twice as far, a quarter the pull")
  Orbits:       v_orbit = √(GM/r) ;  T²/r³ = 4π²/GM
  Energy:       U = −GMm/r ;  K = +GMm/2r ;  E = −GMm/2r  (ratio K:U:E = +1:−2:−1)
                v_esc = √(2GM/r) = √2 · v_orbit   ("root two to break free")

THE ONE THREAD: it is all ONE force (gravity) or ONE method (resolve, set net to
  the centre) applied to motion that CURVES. Ask: (a) what is the net force and
  where does it point? (b) where is the energy going?

THE SIX TRAPS (most are one topic confused for another):
  1. Projectile acceleration is NEVER zero — not even at the top of the arc; only
     the vertical velocity is zero there, horizontal velocity is unchanged.
  2. No outward "centrifugal" force — the only real horizontal force is inward
     (centripetal). It is a REAL force in a new role, not an extra force.
  3. Centripetal force does NO WORK (perpendicular to motion) → circular-orbit
     speed and energy are constant.
  4. Two speeds differ by √2: v_orbit = √(GM/r), v_esc = √(2GM/r).
  5. r is from the CENTRE, not the surface → "altitude given, add the radius."
  6. U is ALWAYS negative and more negative lower down; positive U = dropped sign.
```

### Listing 2 — Projectile motion worked example (SPLIT then SUVAT)

```text
GIVEN: launch u = 30 m s⁻¹ at θ = 40° above horizontal, level ground, no air
       resistance, g = 9.8 m s⁻². Find time of flight, range, max height.

STEP 1 — SPLIT the launch velocity:
   u_x = u cosθ = 30 cos40° = 30 × 0.766 = 22.98 m s⁻¹   (constant all flight)
   u_y = u sinθ = 30 sin40° = 30 × 0.643 = 19.28 m s⁻¹   (gravity acts on this)

STEP 2 — THE CLOCK (vertical motion sets the time). Level ground → returns to
   launch height; time of flight:
   t = 2 u_y / g = 2(19.28) / 9.8 = 3.93 s

STEP 3 — HORIZONTAL uses the shared clock:
   Range R = u_x · t = 22.98 × 3.93 ≈ 90 m

STEP 4 — MAX HEIGHT (vertical, v_y = 0 at top):
   H = u_y² / (2g) = 19.28² / (2 × 9.8) = 371.8 / 19.6 ≈ 19 m

KEY: vertical gives the TIME, horizontal gives the RANGE, they meet only through t.
AT THE TOP: v_y = 0, v_x = 22.98 m s⁻¹ (unchanged), a = 9.8 m s⁻² down (never zero).
```

### Listing 3 — Circular motion worked example (NET-to-the-centre)

```text
GIVEN: car m = 1200 kg, flat (unbanked) curve r = 50 m, speed v = 15 m s⁻¹.
       Identify the centripetal force and find its size.

NET-to-the-CENTRE — list the real forces:
   • weight (down)        )  vertical, cancel
   • normal force (up)    )
   • friction (horizontal) ← the ONLY force pointing toward the centre
   → FRICTION is the centripetal force (not a new force; a real force in that role)

CENTRIPETAL ACCELERATION and FORCE:
   a_c = v²/r = 15² / 50 = 225 / 50 = 4.5 m s⁻²  (directed at the centre)
   F_c = m v²/r = 1200 × 4.5 = 5400 N

CHECK (does the road grip?):  required friction coefficient μ = a_c/g = 4.5/9.8
   ≈ 0.46 → fine on dry road; on ice (μ small) the car slides straight on (inertia).

MISCONCEPTION: passengers "thrown outward" = inertia (Newton's 1st law), not a real
   outward force. The door pushes them INWARD to supply the centripetal force.
```

### Listing 4 — Newton's cannon: projectile → orbit → escape (derivations + speeds)

```text
NEWTON'S CANNON (one cannon, three regimes, set by launch speed alone):
   slow          → projectile, arcs to the ground (SPLIT then SUVAT)
   = v_orbit     → falls forever, ground curves away as fast as it falls → ORBIT
   = v_esc (=√2·v_orbit) → total energy 0 → ESCAPES to infinity, never returns

ORBITAL-SPEED DERIVATION (gravity IS the centripetal force):
   G M m / r²  =  m v² / r        ← NET-to-the-centre
   cancel m and one r:
   v² = G M / r
   ─────────────────────
   v_orbit = √( G M / r )
   ─────────────────────
   (satellite's mass cancels → all satellites at a given r have the same speed)

KEPLER'S THIRD LAW (from the same orbit):
   v = 2πr/T   AND   v = √(GM/r)
   → (2πr/T)² = GM/r
   → 4π²r²/T² = GM/r
   → T²  = 4π² r³ / (GM)
   ─────────────────────────
   T² / r³ = 4π² / (GM)      ← constant, fixed by the central mass alone
   ─────────────────────────

WORKED — satellite at r = 8.0 × 10⁶ m (Q4), GM = 3.98 × 10¹⁴:
   v = √(3.98×10¹⁴ / 8.0×10⁶) = √(4.98×10⁷) ≈ 7.05 × 10³ m s⁻¹  (≈ 7 km s⁻¹)
   T = 2πr / v = 2π(8.0×10⁶)/7.05×10³ = 5.03×10⁷ / 7.05×10³ ≈ 7.14 × 10³ s
     ≈ 119 min

SPEEDS AT THE EARTH'S SURFACE (r = R_E = 6.37 × 10⁶ m):
   v_orbit = √(GM/R_E) = √(3.98×10¹⁴ / 6.37×10⁶) = √(6.25×10⁷) ≈ 7.9 × 10³ m s⁻¹
   v_esc   = √2 · v_orbit ≈ 1.41 × 7.9 ≈ 1.12 × 10⁴ m s⁻¹  (11.2 km s⁻¹)
```

### Listing 5 — Gravitational energy & escape velocity (summary from M5-06)

```text
POTENTIAL ENERGY:  U = − G M m / r     ("zero at infinity, negative everywhere")
   zero at r = ∞; attractive gravity → must do +work to reach ∞ → U < 0 everywhere.
   reconciles with Year-11 mgh: for small hops near the surface ΔU ≈ m g h.

CIRCULAR-ORBIT ENERGIES (use v² = GM/r):
   K = ½ m v² = + G M m / (2r)
   U =         − G M m / r        = −2 × [GMm/2r]
   E = K + U = − G M m / (2r)     ← negative ⇒ BOUND
   RATIO  K : U : E = +1 : −2 : −1  (virial)

"HIGHER is SLOWER but BIGGER-ENERGY": bigger r → v = √(GM/r) FALLS, but
   E = −GMm/2r becomes LESS negative (RISES toward 0). Potential term (−2) beats
   kinetic term (+1) → to raise an orbit you must ADD energy though it ends slower.

ESCAPE VELOCITY (set total energy at the surface = 0):
   ½ m v_esc² + (−GMm/r) = 0  →  v_esc² = 2GM/r  →  v_esc = √(2GM/r)
   = √2 · v_orbit  ("root two to break free"); INDEPENDENT of the object's mass.

DATA TABLE (quick reference):
```

| Quantity | Symbol / formula | Value / note |
|----------|------------------|--------------|
| Universal gravitational constant | G | 6.67 × 10⁻¹¹ N m² kg⁻² |
| Mass of the Earth | M_E | 5.97 × 10²⁴ kg |
| Radius of the Earth | R_E | 6.37 × 10⁶ m |
| GM for the Earth | GM_E | 3.98 × 10¹⁴ m³ s⁻² |
| Surface gravity | g | 9.8 m s⁻² (= GM/R_E²) |
| Orbital velocity | v_orbit = √(GM/r) | falls as r grows |
| Escape velocity | v_esc = √(2GM/r) | = √2 × v_orbit ≈ 11.2 km s⁻¹ (surface) |
| Total orbital energy | E = −GMm/2r | negative ⇒ bound |
| Energy ratio (circular orbit) | K : U : E | +1 : −2 : −1 |
| Kepler's third law | T²/r³ = 4π²/GM | constant for one central mass |

### Listing 6 — Worked solutions to the closing exam questions

```text
Q1 — thrown-horizontally vs dropped ball. (2 marks)
   Both land at the SAME time. Horizontal and vertical motion are INDEPENDENT, so
   the thrown ball's horizontal velocity does not affect its vertical motion. Both
   start with v_y = 0 and fall through the same height with the same g → same time.
   Marks: motions independent · both have identical vertical motion so land together.

Q2 — projectile u = 25 m s⁻¹ at 35°, level ground, g = 9.8. (3 marks)
   u_y = 25 sin35° = 25 × 0.574 = 14.3 m s⁻¹
   u_x = 25 cos35° = 25 × 0.819 = 20.5 m s⁻¹
   t   = 2 u_y / g = 2(14.3)/9.8 = 2.92 s
   R   = u_x · t = 20.5 × 2.92 ≈ 60 m
   Marks: resolve components · time from vertical · range = u_x·t.
   Trap: don't use the full 25 m s⁻¹ in the range — only the horizontal component.

Q3 — car m = 1000 kg, flat track r = 40 m, v = 20 m s⁻¹. (3 marks)
   Vertical forces (weight, normal) cancel → FRICTION is the only inward force →
   friction is the centripetal force.
   F_c = m v²/r = 1000 × 20² / 40 = 1000 × 400/40 = 1000 × 10 = 10 000 N
   Marks: friction named as centripetal force · F_c = mv²/r · 10 000 N.

Q4 — satellite r = 8.0 × 10⁶ m, GM = 3.98 × 10¹⁴. (4 marks)
   v = √(GM/r) = √(3.98×10¹⁴ / 8.0×10⁶) = √(4.98×10⁷) ≈ 7.05 × 10³ m s⁻¹ (≈ 7 km s⁻¹)
   T = 2πr/v = 2π(8.0×10⁶)/7.05×10³ = 5.03×10⁷/7.05×10³ ≈ 7.14 × 10³ s (≈ 119 min)
   Marks: v = √(GM/r) · ≈ 7 km s⁻¹ · T = 2πr/v · ≈ 7.1×10³ s.
   Trap: r is already from the centre (add nothing); circumference is 2πr, not 2r.

Q5 — Newton's cannon: projectile → orbit → escape. (6 marks, extended response)
   • Low speed: projectile, parabolic arc, lands short (SPLIT then SUVAT); faster →
     longer, flatter arc.
   • At v_orbit = √(GM/R_E) ≈ 7.9 km s⁻¹: the surface curves away as fast as the ball
     falls → it never lands → stable circular ORBIT. Gravity is the centripetal force
     (NET-to-the-centre); perpendicular to motion → does no work → no thrust needed.
   • At v_esc = √2 · v_orbit ≈ 11.2 km s⁻¹: total energy reaches 0 → unbound → coasts
     to infinity, never returns; no thrust needed (gravity conservative, launch gave
     all the energy). "Root two to break free."
   Marks: parabola at low speed · transition to orbit as surface curves away · gravity
   = centripetal force doing no work · v_orbit ≈ 7.9 km s⁻¹ · v_esc ≈ 11.2 km s⁻¹ = √2·v_orbit
   · no thrust because gravity supplies force and launch supplies energy.
```
