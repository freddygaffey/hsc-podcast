---
title: "Supplementary Materials — Module Review: Waves and Thermodynamics"
module: M3
lesson: "99"
script: script.md
---

# Supplementary Materials

A consolidated reference for the whole Waves and Thermodynamics module, with worked integrated solutions. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The Module 3 toolkit (all six episodes)
```text
WAVE PROPERTIES (M3-01):  energy transferred, NOT matter. v = f λ ;  f = 1/T.
   transverse (⊥) vs longitudinal (∥) ; mechanical (needs medium) vs EM (vacuum, 3×10⁸ m s⁻¹).
   time graph → period/frequency ; position graph → wavelength.

WAVE BEHAVIOUR (M3-02):  reflection (∠i = ∠r) · refraction (speed change bends it) ·
   diffraction (spreads; most when gap ≈ λ) · SUPERPOSITION (add displacements).
   interference: in phase = constructive ; out of phase = destructive.
   standing wave = 2 opposite waves → fixed NODES (0) & ANTINODES (max); stores energy.
   resonance: driving f = natural f → energy transfer max, amplitude large.

SOUND (M3-03):  longitudinal pressure wave; needs a medium. pitch=f, loudness=amplitude/intensity.
   I ∝ 1/r². strings/open pipes λ₀ = 2L (all harmonics); closed pipe λ₀ = 4L (odd only).
   beats f_beat = |f₂−f₁|. Doppler: approach → higher observed f ; recede → lower (emitted f constant).

RAY MODEL OF LIGHT (M3-04):  angles from the NORMAL. n = c/v (>1). denser → bend toward normal.
   Snell: n₁ sin i = n₂ sin r. TIR: dense→less-dense AND i > iᶜ, where sin iᶜ = n₂/n₁.
   dispersion splits white light by wavelength. I ∝ 1/d²  (I₁r₁² = I₂r₂²).

TEMPERATURE & HEAT (M3-05):  temperature = AVERAGE particle KE ; heat = energy in TRANSIT (hot→cold).
   internal energy = TOTAL particle energy. K = °C + 273 ; absolute zero = 0 K = −273 °C.
   thermal equilibrium = equal T, no net flow.  ΔQ = m c ΔT.  (water c ≈ 4200)

HEAT TRANSFER & LATENT HEAT (M3-06):  conduction (collisions, solids) · convection (fluid rises/sinks) ·
   radiation (EM waves, NO medium — crosses vacuum).  Q/t = kAΔT/d.
   change of state: T constant (energy breaks bonds, not KE).  Q = m L.
   water L_fus ≈ 334 kJ kg⁻¹ ; L_vap ≈ 2260 kJ kg⁻¹.

FORWARD: → M7 (wave model of light, EM spectrum, dispersion, Doppler redshift, black-body radiation)
         → M8 (quantum origins) ;  BACK: → M2 (energy conserved & transformed underlies all of it).
```

### Listing 2 — Worked integrated solutions
```text
(Sound + graphs) particle cycle every 2 ms (T = 0.002 s), v = 340 m s⁻¹:
   f = 1/T = 1/0.002 = 500 Hz ;  λ = v/f = 340/500 = 0.68 m

(Pipe + wave eqn + beats) open pipe L = 0.68 m, v = 340:
   λ₀ = 2L = 1.36 m → f₀ = 340/1.36 = 250 Hz ; with a 254 Hz fork → f_beat = |254−250| = 4 /s

(Snell → speed) air→plastic, i = 50° (sin 0.77), r = 30° (sin 0.5):
   n₂ = (1 × 0.77)/0.5 = 1.54 ;  v = c/n = 3×10⁸ / 1.54 ≈ 1.95×10⁸ m s⁻¹

(Critical angle) glass n = 1.5 → air:  sin iᶜ = 1/1.5 = 0.67 → iᶜ ≈ 42° ; above 42° → TIR.

(Conduction) glass window k = 0.8, A = 2 m², ΔT = 15 K, d = 0.004 m:
   Q/t = kAΔT/d = (0.8 × 2 × 15)/0.004 = 24/0.004 = 6000 W

(Inverse square) 36 units at 2 m → at 6 m (×3): 36/3² = 36/9 = 4 units.

(Wave on string) f = 25 Hz, λ = 0.08 m:  v = fλ = 2 m s⁻¹ ; T = 1/f = 0.04 s ; TRANSVERSE.
```

### Listing 3 — Mnemonic / rule registry (M3)
| Topic | Hook |
|-------|------|
| Wave equation | v = f λ ; f = 1/T ("frequency and period are reciprocals") |
| Two classifications | transverse ⊥ / longitudinal ∥ ; mechanical needs medium / EM doesn't |
| Reading graphs | TIME axis → period & frequency ; POSITION axis → wavelength |
| Four behaviours | Reflection · Refraction · Diffraction · Superposition |
| Interference | in phase → constructive ; out of phase → destructive |
| Standing wave | 2 opposite waves; nodes (always out of phase, 0) / antinodes (always in phase, max); STORES energy |
| Resonance | driving f = natural f → big amplitude |
| Sound | pitch = frequency ; loudness = amplitude/intensity ; I ∝ 1/r² |
| Pipes | open/string λ₀ = 2L (all harmonics) ; closed λ₀ = 4L (odd only) |
| Beats / Doppler | f_beat = \|f₂−f₁\| ; approach = higher, recede = lower (observed, not emitted) |
| Refraction | denser (higher n) → bend TOWARD the normal ; n = c/v |
| TIR | dense→less-dense AND angle > critical ; sin iᶜ = n₂/n₁ |
| Heat vs temperature | temperature = average particle KE ; heat = energy in transit |
| Latent heat | "energy to bonds, not temperature" (T constant during change of state) |
| Heat transfer | conduction (solids) · convection (fluids rise/sink) · radiation (no medium, crosses vacuum) |

### Listing 4 — Which equation? (decision guide)
```text
WAVES:
   speed / frequency / wavelength?            → v = f λ   (and f = 1/T)
   refracted angle at a boundary?             → Snell:  n₁ sin i = n₂ sin r
   speed of light in a medium?                → n = c / v
   will it totally internally reflect?        → dense→less-dense AND i > iᶜ (sin iᶜ = n₂/n₁)
   intensity vs distance (sound or light)?    → I ∝ 1/r²

THERMAL — ask: is the TEMPERATURE changing, or the STATE?
   TEMPERATURE changing  → ΔQ = m c ΔT
   STATE changing (const T, melt/boil) → Q = m L   (L_fus to melt, L_vap to boil)
   COMBINED (e.g. ice → warm water → steam): sum the stages, m L for each phase change,
        m c ΔT for each temperature change.
   rate of CONDUCTION?    → Q/t = k A ΔT / d
   MIXING (insulated)?    → heat lost by hot = heat gained by cold (energy conserved)

GOLDEN RULE: identify what the question is CHANGING (a frequency, a temperature, a state,
   a direction) and the matching equation follows. When stuck, ask "where is the energy going?"
```
