---
title: "Supplementary Materials — Wave Behaviour: Reflection, Refraction, Diffraction and Superposition"
module: M3
lesson: "02"
script: script.md
---

# Supplementary Materials

The read-along reference for how waves behave at boundaries and when they meet. Nothing here is spoken in the audio. Symbols: v = speed; f = frequency; λ = wavelength; θ = angle from the normal.

### Listing 1 — The four wave behaviours
```text
REFLECTION   wave bounces back into its original medium at a boundary.
             LAW: angle of incidence = angle of reflection (both measured from the NORMAL).
             Fixed-end reflection INVERTS (crest → trough); free-end does NOT invert.

REFRACTION   wave changes DIRECTION on entering a new medium, CAUSED by a change in SPEED.
             At the boundary:   f stays SAME (set by source)
                                v changes  (set by medium)   ⇒  λ changes  (v = fλ)
             Slows down (denser) → bends TOWARD the normal; speeds up → bends AWAY.

DIFFRACTION  wave SPREADS through a gap / around an edge.
             MOST pronounced when gap size ≈ wavelength.
             gap ≫ λ → little spreading;  gap ≈ λ → large spreading.
             (Why you HEAR around corners — sound λ ~1 m ≈ doorway; light λ tiny → no spread.)

SUPERPOSITION  when waves overlap, resultant displacement = SUM of the individual
               displacements (with sign). After overlapping, waves pass through unchanged.
```

### Listing 2 — Worked superposition & path difference
```text
SUPERPOSITION (add displacements at a point):
   wave A gives +3 cm, wave B gives +2 cm  →  resultant = +5 cm   (constructive)
   wave A gives +3 cm, wave B gives −3 cm  →  resultant =  0 cm   (destructive, full cancel)
   wave A gives +3 cm, wave B gives −1 cm  →  resultant = +2 cm   (partial cancel)

PATH DIFFERENCE rule (two in-step sources, λ = wavelength):
   path difference = 0, 1λ, 2λ, 3λ …            → IN phase  → CONSTRUCTIVE (loud/bright)
   path difference = ½λ, 1½λ, 2½λ …             → OUT of phase → DESTRUCTIVE (quiet/dark)

   e.g. λ = 0.5 m, you are 4.0 m from source 1 and 3.0 m from source 2:
        path difference = 4.0 − 3.0 = 1.0 m = 2 × 0.5 m = 2λ (whole number) → CONSTRUCTIVE.
   e.g. same sources, points 4.25 m and 3.0 m:
        path difference = 1.25 m = 2.5 × 0.5 m = 2½λ (odd half-wavelengths) → DESTRUCTIVE.
```

### Listing 3 — Interference, phase & resonance
```text
INTERFERENCE (set by PHASE):
   CONSTRUCTIVE : waves IN phase (crest on crest) → displacements ADD → larger amplitude.
   DESTRUCTIVE  : waves OUT of phase (crest on trough) → displacements SUBTRACT → smaller/zero.

RESONANCE:
   natural frequency  = the frequency a system oscillates at on its own when disturbed
                        (set by its size, tension, mass, stiffness).
   resonance          = driving frequency EQUALS natural frequency
                        → energy transferred efficiently EVERY cycle → amplitude grows LARGE.
   off resonance      → energy transfer poor → amplitude stays small.
   Swing analogy: push in time with the natural rhythm → small pushes build a big swing.
   Small driving force can build a large amplitude AT resonance (energy accumulates).
```

### Listing 4 — Standing waves vs progressive waves
```text
STANDING (stationary) WAVE — how it forms:
   TWO identical waves (same f, same amplitude) travelling in OPPOSITE directions superpose
   (e.g. an incident wave + its reflection off a fixed end).
     NODE     : the two waves are ALWAYS out of phase → permanent CANCELLATION
                → zero displacement (a fixed point that never moves).
     ANTINODE : the two waves are ALWAYS in phase → permanent REINFORCEMENT
                → maximum-amplitude oscillation.
   Pattern looks STATIONARY (nodes & antinodes fixed in place).
   GEOMETRY: distance between adjacent nodes = ½λ of the original waves.
   On a fixed-length string only certain wavelengths "fit" (node at each end) →
   a discrete ladder: fundamental, then harmonics (→ pitch & timbre, see M3-03).

   ┌──────────────┬───────────────────────────┬───────────────────────────┐
   │              │ PROGRESSIVE (travelling)  │ STANDING (stationary)     │
   ├──────────────┼───────────────────────────┼───────────────────────────┤
   │ energy       │ TRANSPORTED along medium  │ STORED (stays put)        │
   │ pattern      │ moves through space       │ fixed nodes & antinodes   │
   │ amplitude    │ same for all particles    │ 0 at nodes, max at antinodes │
   └──────────────┴───────────────────────────┴───────────────────────────┘
```
