---
title: "Supplementary Materials — Reading the Stars: Spectra, Temperature, Composition, and Redshift"
module: M8
lesson: "13"
script: script.md
---

# Supplementary Materials

Key equations, the worked Hubble calculation, and reference tables for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Hubble's law and the age of the universe, worked example

Hubble's law (in words): recession velocity = Hubble's constant × distance.

$$
v = H d \quad \to \quad H = \frac{v}{d} \quad (\text{gradient of the } v\text{–}d \text{ graph})
$$

Age (constant-expansion model):

$$
t = \frac{1}{H}
$$

Given (Hubble's 1929 data):

- \(d = 2 \times 10^{6}\ \mathrm{pc}\)
- \(v \approx 1100\ \mathrm{km\,s^{-1}}\)

**Step 1 — convert distance to km** \((1\ \mathrm{pc} = 3.09 \times 10^{13}\ \mathrm{km})\):

$$
d = (2 \times 10^{6}\ \mathrm{pc})(3.09 \times 10^{13}\ \mathrm{km/pc}) = 6.2 \times 10^{19}\ \mathrm{km}
$$

**Step 2 — Hubble's constant** \(H = v / d\):

$$
H = 1100\ \mathrm{km\,s^{-1}} \div 6.2 \times 10^{19}\ \mathrm{km}
$$

$$
H = 1.77 \times 10^{-17}\ \mathrm{s^{-1}} \quad (\text{km cancel} \to \text{units are } \mathrm{s^{-1}}, \text{ an inverse time})
$$

$$
H \approx 1.8 \times 10^{-17}\ \mathrm{s^{-1}}
$$

**Step 3 — age** \(t = 1 / H\):

$$
t = \frac{1}{1.77 \times 10^{-17}\ \mathrm{s^{-1}}} = 5.64 \times 10^{16}\ \mathrm{s}
$$

**Step 4 — convert seconds to years** \((1\ \mathrm{yr} \approx 3.156 \times 10^{7}\ \mathrm{s})\):

$$
t = 5.64 \times 10^{16}\ \mathrm{s} \div 3.156 \times 10^{7}\ \mathrm{s/yr} \approx 1.8 \times 10^{9}\ \mathrm{yr}
$$

Result: \(H \approx 1.8 \times 10^{-17}\ \mathrm{s^{-1}}\); age \(\approx 1.8 \times 10^{9}\ \mathrm{yr} \approx 2\ \text{billion yr}\) (1 s.f.).

Evaluation: this is too young — younger than the ~4.6-billion-year-old Earth. Baade's 1950s Cepheid recalibration (Pop I vs Pop II) roughly halved \(H\), doubling the age. Modern value of the age of the universe \(\approx 13.8\) billion yr.

### Listing 2 — Constants and unit conversions used
| Quantity | Value |
|----------|-------|
| 1 parsec (pc) | 3.09 × 10^16 m = 3.09 × 10^13 km |
| 1 year | ≈ 3.156 × 10^7 s |
| Speed of light, c | 3.0 × 10^8 m s^-1 |
| Hubble's constant (this worked example) | ≈ 1.8 × 10^-17 s^-1 |
| Age of universe (Hubble's 1929 estimate) | ≈ 2 × 10^9 yr |
| Age of universe (modern value) | ≈ 13.8 × 10^9 yr |
| Cosmic microwave background temperature | ≈ 2.7 K (≈ −270 °C) |

### Listing 3 — Spectral classification (OBAFGKM, hottest to coolest)
| Class | Surface temp (K) | Colour | Key spectral features |
|-------|------------------|--------|------------------------|
| O | 28 000 – 50 000 | Blue | Ionised helium lines; strong UV |
| B | 10 000 – 28 000 | Blue | Neutral helium lines |
| A | 7 500 – 10 000 | Blue-white | Strong hydrogen lines; ionised metal lines |
| F | 6 000 – 7 500 | White | Strong metal lines; weak hydrogen |
| G | 5 000 – 6 000 | Yellow | Ionised calcium; metal lines (the Sun = G2) |
| K | 3 500 – 5 000 | Orange | Neutral metals dominate; molecular lines |
| M | 2 500 – 3 500 | Red | Molecular lines dominate; strong neutral metals |

Mnemonic: "Oh Be A Fine Girl, Kiss Me" → O B A F G K M. Order is by SURFACE TEMPERATURE (hottest → coolest), not alphabetical, not by abundance. "Metal" in astronomy = any element other than H or He. The Sun is class G2 (yellow, ~5500 K).

### Listing 4 — The three types of spectrum (Kirchhoff) and their sources
| Spectrum | Produced by | Celestial source |
|----------|-------------|------------------|
| Continuous (black-body) | hot, dense solid / liquid / high-pressure gas | star's dense interior; galaxies |
| Emission (bright lines) | hot, low-density (rarefied) glowing gas | emission nebulae; quasars; neon signs |
| Absorption (dark lines) | continuous source seen through a cooler gas in front | atmospheres (outer layers) of stars |

Why a star shows ABSORPTION (cause-and-effect chain the marker wants):

1. Hot, dense interior → continuous black-body spectrum.
2. Light passes outward through the cooler, less-dense atmosphere.
3. Atoms in that atmosphere absorb their characteristic wavelengths.
4. Result: continuous spectrum crossed by dark absorption lines.

Trap: "hot gas → emission" is WRONG for a star — a hot LOW-DENSITY gas gives emission; a hot DENSE body gives a continuous spectrum.

### Listing 5 — The three readings of a stellar spectrum ("Tall Cats Vanish")
| Reading | Spectral feature used | Rule |
|---------|-----------------------|------|
| Temperature | shape of the continuous (black-body) background | shorter-wavelength (bluer) peak ⇒ hotter; redder ⇒ cooler |
| Composition | identity (wavelengths) of the absorption lines | match dark lines to laboratory element "fingerprints" |
| Velocity | shift of the absorption lines (Doppler) | redshift ⇒ receding; blueshift ⇒ approaching; size of shift ⇒ radial speed |

Hook: "Tall Cats Vanish" = Temperature, Composition, Velocity. Mechanism map (the #1 anti-trap): SHAPE → temperature, IDENTITY → composition, SHIFT → velocity. Doppler gives RADIAL velocity only (along the line of sight); purely tangential motion produces no shift.

### Listing 6 — Redshift as evidence for an expanding universe (weak vs strong answer)

Question: "How does the redshift of galaxies provide evidence the universe is expanding?"

**WEAK answer (≈ 1 mark):** "Redshift means the galaxies are moving away from us." — states only motion; motion alone is not expansion.

**STRONG answer (full marks) adds:**

1. Distant galaxies' absorption-line spectra are redshifted ⇒ receding.
2. Hubble (1929): redshift INCREASES WITH DISTANCE — recession velocity is PROPORTIONAL to distance (Hubble's law, \(v = H d\)).
3. Velocity \(\propto\) distance is exactly what UNIFORM EXPANSION OF SPACE predicts (the balloon/raisin-loaf analogy) — space itself stretches and carries galaxies apart, stretching the light's wavelength en route (cosmological redshift). NOT motion through static space; no centre.
4. Run the expansion backwards ⇒ a hot, dense beginning (Big Bang); the cosmic microwave background (~2.7 K) is the partner evidence.
