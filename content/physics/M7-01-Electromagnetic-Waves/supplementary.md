---
title: "Supplementary Materials — Electromagnetic Waves: Production, Propagation, and the One Constant Speed"
module: M7
lesson: "01"
script: script.md
---

# Supplementary Materials

Key equations, the production-and-propagation chain, worked numerical solutions, and reference data for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Wave equation: frequency of 300 nm light (worked example)

$$
c = f \lambda \quad \text{(speed of an EM wave = frequency} \times \text{wavelength)}
$$

Want frequency, so rearrange:

$$
f = \frac{c}{\lambda}
$$

**Given:**

- \(\lambda = 3.00 \times 10^{-7}\ \mathrm{m}\) (300 nm, near-UV, just past the violet edge)
- \(c = 3.00 \times 10^{8}\ \mathrm{m\,s^{-1}}\) (speed of light in vacuum)

**Substitute:**

$$
f = \frac{3.00 \times 10^{8}}{3.00 \times 10^{-7}} = 1.00 \times 10^{15}\ \mathrm{Hz}
$$

**Photon-energy cross-check** (\(E = hf\), previews M7-09), with \(h = 6.63 \times 10^{-34}\ \mathrm{J\,s}\):

$$
E = (6.63 \times 10^{-34})(1.00 \times 10^{15}) = 6.63 \times 10^{-19}\ \mathrm{J} \quad \text{(energy of one such photon)}
$$

Point: a radio wave (low \(f\), long \(\lambda\)) and a gamma ray (high \(f\), short \(\lambda\)) both satisfy \(c = f\lambda\) with the SAME \(c\). Only \(f\) and \(\lambda\) trade off.

### Listing 2 — Band-6 model extended-response answer

Q: "Describe how electromagnetic waves are produced and propagated, and explain why all electromagnetic waves travel at the same speed in a vacuum. Relate your answer to Maxwell's electromagnetic theory." (6 marks)

**Production**

- An EM wave is produced by an ACCELERATING electric charge — e.g. electrons oscillating in a radio transmitter antenna, driven by an alternating current.
- A stationary charge \(\to\) only a static electric field (no wave).
- A charge at constant velocity (steady DC) \(\to\) only a steady magnetic field (no wave).
- ONLY an accelerating charge (velocity changing) radiates.

**Propagation** (the self-regenerating chain)

- The oscillating charge produces a CHANGING ELECTRIC FIELD.
- Ampère–Maxwell law: a changing electric field induces a changing magnetic field (at right angles to it).
- Faraday's law: that changing magnetic field induces a changing electric field.
- The two fields CONTINUOUSLY REGENERATE ONE ANOTHER and propagate outward.
- It is a TRANSVERSE wave: \(E \perp B\), and both \(\perp\) to the direction of travel.
- It is an oscillation of the FIELDS themselves \(\to\) needs NO MEDIUM; the luminiferous aether was never found and is unnecessary \(\to\) travels through vacuum.

**Constant speed (Maxwell)**

- \(v = \dfrac{1}{\sqrt{\mu_0 \varepsilon_0}}\): speed set only by the permittivity \(\varepsilon_0\) and permeability \(\mu_0\) of free space.
- These are FIXED constants of the vacuum \(\to\) regeneration rate fixed \(\to\) speed fixed.
- So EVERY EM wave travels at the same \(c \approx 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\) in a vacuum, regardless of frequency.
- Radio \(\to\) microwave \(\to\) infrared \(\to\) visible \(\to\) UV \(\to\) X-ray \(\to\) gamma differ only in frequency and wavelength, related by \(c = f\lambda\).

**Weak answer** (for contrast — scores almost nothing): "EM waves are made by electricity and travel through space." (No accelerating charge, no Faraday/Ampère–Maxwell coupling, no transverse geometry, no reason for constant speed.)

### Listing 3 — The three tiers of charge motion (what radiates)
| Charge motion | Field produced | Radiates an EM wave? |
|---------------|----------------|----------------------|
| Stationary charge | Static (unchanging) electric field | No |
| Constant velocity (steady DC current) | Steady (unchanging) magnetic field | No |
| Accelerating / oscillating charge (AC) | Changing electric AND magnetic fields | Yes |

### Listing 4 — The propagation loop and key equations (in words and symbols)

**The self-propagating loop** (memory hook: FAME)

- changing \(E\) field \(\xrightarrow{\text{Ampère–Maxwell}}\) changing \(B\) field
- changing \(B\) field \(\xrightarrow{\text{Faraday's law}}\) changing \(E\) field
- … repeats, regenerating itself, forever, with no medium.
- FAME = Faraday\(\to\)Electric, Ampère–Maxwell\(\to\)Magnetic.

**Wave-speed relation**

$$
c = f \lambda
$$

\(c\) = speed in vacuum (\(\mathrm{m\,s^{-1}}\)); \(f\) = frequency (\(\mathrm{Hz}\)); \(\lambda\) = wavelength (\(\mathrm{m}\)). \(c\) fixed \(\Rightarrow f\) and \(\lambda\) inversely related (higher \(f \Rightarrow\) shorter \(\lambda\)).

**Maxwell's speed prediction** (number is owned by M7-02)

$$
v = \frac{1}{\sqrt{\mu_0 \varepsilon_0}}
$$

\(\mu_0\) = permeability of free space (how readily a \(B\) field forms in vacuum); \(\varepsilon_0\) = permittivity of free space (how readily an \(E\) field forms in vacuum). Both are fixed vacuum constants \(\Rightarrow v\) is a fixed constant of the vacuum.

**Photon-energy preview** (owned by M7-09; flag only)

$$
E = hf = \frac{hc}{\lambda}
$$

Higher \(f \Rightarrow\) higher-energy photon \(\Rightarrow\) ionising (UV, X-ray, gamma).

**Refractive index** (why light slows in a medium, NOT a change in \(c\))

$$
n = \frac{c}{v_{\text{medium}}}
$$

(light at \(c\) in vacuum; slowed in glass/water by absorption and re-emission delay)

### Listing 5 — Reference data: constants and the EM spectrum
| Quantity | Symbol | Value |
|----------|--------|-------|
| Speed of light in vacuum | \(c\) | \(3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\) (exact: \(299\,792\,458\ \mathrm{m\,s^{-1}}\)) |
| Permittivity of free space | \(\varepsilon_0\) | \(8.854 \times 10^{-12}\ \mathrm{F\,m^{-1}}\) |
| Permeability of free space | \(\mu_0\) | \(4\pi \times 10^{-7} \approx 1.257 \times 10^{-6}\ \mathrm{T\,m\,A^{-1}}\) |
| Planck's constant (preview) | \(h\) | \(6.63 \times 10^{-34}\ \mathrm{J\,s}\) |
| Power-line AC frequency (radiates EM waves) | \(f\) | 50–60 Hz |
| Maxwell predicts (theory) | — | 1864 |
| Hertz verifies (experiment) | — | 1887 |

### Listing 6 — EM spectrum order (mnemonic) and ionising power
| Region | Order | Frequency / energy | Ionising? |
|--------|-------|--------------------|-----------|
| Radio | 1 (longest λ) | lowest | No |
| Microwave | 2 | low | No |
| Infrared | 3 | low | No |
| Visible | 4 | medium | No |
| Ultraviolet | 5 | high | Yes |
| X-ray | 6 | higher | Yes |
| Gamma | 7 (shortest λ) | highest | Yes |

Mnemonic (increasing frequency): **R**aging **M**artians **I**nvaded **V**enus **U**sing **X**-ray **G**uns — Radio, Microwave, Infrared, Visible, Ultraviolet, X-ray, Gamma.
