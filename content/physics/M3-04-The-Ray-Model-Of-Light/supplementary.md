---
title: "Supplementary Materials — The Ray Model of Light: Reflection, Refraction and Total Internal Reflection"
module: M3
lesson: "04"
script: script.md
---

# Supplementary Materials

The read-along reference for ray optics: reflection, refraction (Snell's law), total internal reflection, dispersion and the inverse-square law. Nothing here is spoken in the audio. Symbols: n = refractive index; c = speed of light in vacuum; v = speed of light in the medium; i = angle of incidence; r = angle of refraction; iᶜ = critical angle; I = intensity; d/r = distance.

### Listing 1 — The ray model: reflection, mirrors, lenses, dispersion
```text
RAY MODEL: light travels in straight lines (rays). ALL angles measured from the NORMAL
   (the perpendicular to the surface), NOT from the surface.

REFLECTION:  angle of incidence = angle of reflection (from the normal).
   specular (smooth/mirror) → clear image ;  diffuse (rough) → scattered, no image.
   PLANE mirror image: upright, same size, as far BEHIND as object is in front, VIRTUAL.
   CURVED mirrors (concave/convex) → magnified or reduced images.

LENSES (refraction twice on curved surfaces):
   CONVEX / converging  — thick middle, bends rays IN to a focus (magnifier, camera, eye).
                          → magnified upright OR real inverted image (depends on distance).
   CONCAVE / diverging  — thin middle, spreads rays OUT → reduced upright image (myopia).

DISPERSION: n is slightly larger for SHORTER wavelengths (violet) than longer (red),
   so white light splits into a SPECTRUM through a prism (violet bends most, red least).
   Rainbow = dispersion + reflection inside raindrops. (→ EM spectrum, M7.)
```

### Listing 2 — Refractive index, bending rule, TIR, inverse-square
```text
REFRACTIVE INDEX:   n = c / v        (always > 1, since v < c in any medium)
   air ≈ 1.00 · water ≈ 1.33 · glass ≈ 1.5 · diamond ≈ 2.4
   higher n = "optically denser" = light travels SLOWER.

BENDING RULE:
   into a DENSER (higher-n) medium → slows → bends TOWARD the normal  (r < i)
   into a LESS dense (lower-n) medium → speeds up → bends AWAY from the normal (r > i)

TOTAL INTERNAL REFLECTION — needs BOTH:
   (1) light going from DENSER → LESS DENSE (high n → low n), AND
   (2) angle of incidence > CRITICAL ANGLE iᶜ.
   Critical angle (set refracted angle = 90°):  sin iᶜ = n₂ / n₁   ( = 1/n if medium 2 is air)
   Uses: OPTICAL FIBRES (internet/phone data, endoscopes); diamond sparkle (iᶜ ≈ 24°).

INVERSE-SQUARE LAW (light intensity from a point source):  I ∝ 1 / d²
   I₁ r₁² = I₂ r₂²    (double the distance → ¼ intensity; ×4 distance → 1/16).
```

### Listing 3 — Worked Snell's law, critical angle & intensity
```text
SNELL'S LAW:   n₁ sin i = n₂ sin r

(1) Air → glass: n₁ = 1, i = 30° (sin 30° = 0.5), n₂ = 1.5:
       1 × 0.5 = 1.5 × sin r  →  sin r = 0.5 / 1.5 = 0.33  →  r ≈ 19°
       (r < i: bent TOWARD the normal entering denser glass ✓)

(2) Air → water: n₁ = 1, i = 40° (sin 40° = 0.64), n₂ = 1.33:
       1 × 0.64 = 1.33 × sin r  →  sin r = 0.64 / 1.33 = 0.48  →  r ≈ 29°

(3) Critical angle, water (n = 1.33) → air:
       sin iᶜ = 1 / 1.33 = 0.75  →  iᶜ ≈ 49°
       below 49° → light refracts out; above 49° → TOTAL internal reflection.

(4) Inverse-square: 200 lux at 1 m. At 4 m:
       I₁ r₁² = I₂ r₂²  →  200 × 1² = I₂ × 4²  →  I₂ = 200 / 16 = 12.5 lux
       (×4 distance → 1/16 intensity — square the ratio!)
```
