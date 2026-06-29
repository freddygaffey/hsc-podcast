---
title: "Supplementary Materials — Sound Waves, Resonance and Standing Waves"
module: M3
lesson: "03"
script: script.md
---

# Supplementary Materials

The read-along reference for sound as a longitudinal wave: pitch and loudness, standing waves in strings and pipes, beats and the Doppler effect. Nothing here is spoken in the audio. Symbols: v = speed of sound; f = frequency; λ = wavelength; L = length; I = intensity; r = distance.

### Listing 1 — Sound as a longitudinal wave (and the Doppler effect)
```text
SOUND = a LONGITUDINAL MECHANICAL wave: vibrating source pushes the medium into
   COMPRESSIONS (high pressure) and RAREFACTIONS (low pressure) that travel outward.
   Particles oscillate back & forth PARALLEL to travel (they do not travel with the wave).
   Two equivalent descriptions: particle DISPLACEMENT  &  PRESSURE variation
   (a quarter-cycle out of step: displacement = 0 where pressure swing is greatest).
   NEEDS A MEDIUM → no sound in a vacuum.

SPEED set by the MEDIUM (denser/stiffer = faster):
   air ≈ 340 m s⁻¹   |   water ≈ 1500 m s⁻¹   |   steel ≈ 5000 m s⁻¹

DOPPLER EFFECT — observed frequency shifts with RELATIVE motion (emitted f is constant):
   source APPROACHES → wavefronts COMPRESSED → λ shorter → observed f HIGHER (higher pitch)
   source RECEDES    → wavefronts STRETCHED  → λ longer  → observed f LOWER  (lower pitch)
   f ′ = f × (v + v_observer) / (v − v_source)
   (Returns for LIGHT in M7: redshift of receding stars.)
```

### Listing 2 — Pitch, loudness and the inverse-square law
```text
PITCH      ↔ FREQUENCY   (high f = high pitch).  Double f = up one octave.
LOUDNESS   ↔ AMPLITUDE / INTENSITY (I = power per unit area).
   → same note (same f) can be loud or soft (different amplitude). Keep them separate.

INTENSITY vs DISTANCE — INVERSE-SQUARE LAW:
   a point source spreads power over a sphere of area ∝ r²  ⇒   I ∝ 1 / r²
   double r → I ÷ 4 ;  triple r → I ÷ 9.

   e.g. I = 80 units at r = 3 m. At r = 9 m (×3 distance): I = 80 / 3² = 80/9 ≈ 8.9 units.
   e.g. 2 m → 6 m (×3 distance): intensity → 1/9 of original.
   (TRAP: ×3 distance is NOT ÷3 intensity — it is ÷9.)
```

### Listing 3 — Standing waves in strings and pipes
```text
GENERAL: reflections at the ends superpose → standing wave. Boundary fixes node/antinode
   positions → only certain wavelengths "fit" → a discrete ladder of allowed frequencies.
   FUNDAMENTAL (1st harmonic) = lowest frequency = the dominant PITCH.
   Higher harmonics = whole-number multiples of the fundamental.

STRING fixed at BOTH ends:   NODE at each end.
   fundamental: L = ½λ  →  λ₀ = 2L.   Produces ALL harmonics.
   Pitch raised by: shorter L, higher tension, lower mass per unit length.

PIPE OPEN at both ends:      ANTINODE at each end.
   fundamental: λ₀ = 2L.     Produces ALL harmonics (1, 2, 3, 4 …).

PIPE CLOSED at one end:      NODE at closed end, ANTINODE at open end.
   fundamental: λ₀ = 4L.     Produces ONLY ODD harmonics (1, 3, 5 …).
   ⇒ a closed pipe sounds an OCTAVE LOWER than an open pipe of the same length.

TIMBRE: a real note = fundamental + a blend of harmonics. The blend (which harmonics,
   how strong) is what makes a flute vs a violin on the same note sound different.
```

### Listing 4 — Worked pipe frequencies & beats
```text
CLOSED pipe, L = 0.2 m, v = 340 m s⁻¹:
   λ₀ = 4L = 4 × 0.2 = 0.8 m
   f₀ = v / λ₀ = 340 / 0.8 = 425 Hz
   harmonics: 425, 1275, 2125 Hz … (odd multiples only: ×1, ×3, ×5)

OPEN pipe, L = 0.34 m, v = 340 m s⁻¹:
   λ₀ = 2L = 0.68 m
   f₀ = v / λ₀ = 340 / 0.68 = 500 Hz
   harmonics: 500, 1000, 1500, 2000 Hz … (all multiples)

BEATS — two close frequencies superpose, loudness pulses at:
   f_beat = | f₂ − f₁ |
   e.g. 260 Hz & 256 Hz → 4 beats per second.
   e.g. 503 Hz & 500 Hz → 3 beats per second.
   Tuning: beats SLOW as the frequencies converge; STOP when equal (in tune).
   A reference 330 Hz with 4 beats/s ⇒ the other string is 326 Hz OR 334 Hz.
```
