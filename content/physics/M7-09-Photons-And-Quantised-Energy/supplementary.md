---
title: "Supplementary Materials — Photons: Light as a Particle with Quantised Energy"
module: M7
lesson: "09"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference. Constants used throughout: Planck's constant h = 6.63 × 10^-34 J s, speed of light c = 3.0 × 10^8 m s^-1, and 1 eV = 1.6 × 10^-19 J (all on the HSC Physics Data Sheet / Formulae Sheet except the eV conversion).

### Listing 1 — Photon energy: the three forms (E = hf, c = fλ, E = hc/λ)

Photon energy (Planck relation):

$$
E = h f
$$

- \(E\) — energy of ONE photon (J)
- \(h\) — Planck's constant \(= 6.63 \times 10^{-34}\ \mathrm{J\,s}\)
- \(f\) — frequency (\(\mathrm{Hz} = \mathrm{s^{-1}}\))

Wave relation (vacuum):

$$
c = f \lambda \qquad\to\qquad f = \frac{c}{\lambda}
$$

- \(c = 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\)
- \(\lambda\) — wavelength (m)

Combined form (substitute \(f = c/\lambda\) into \(E = hf\)):

$$
E = \frac{h c}{\lambda}
$$

Units: \((\mathrm{J\,s} \times \mathrm{m\,s^{-1}}) / \mathrm{m} = \mathrm{J}\) ✓

Proportionalities to memorise:

$$
E \propto f \qquad\text{(higher frequency} \to \text{higher-energy photon)}
$$

$$
E \propto \frac{1}{\lambda} \qquad\text{(shorter wavelength} \to \text{higher-energy photon)}
$$

"short wave, big punch". Convert nm \(\to\) m before substituting: \(1\ \mathrm{nm} = 1 \times 10^{-9}\ \mathrm{m}\).

### Listing 2 — The electron-volt (energy unit at this scale)

Definition — \(1\ \mathrm{eV}\) is the energy an electron gains across a potential difference of \(1\ \mathrm{V}\):

$$
1\ \mathrm{eV} = e \times V = (1.6 \times 10^{-19}\ \mathrm{C})(1\ \mathrm{V}) = 1.6 \times 10^{-19}\ \mathrm{J}
$$

Converting:

- joules \(\to\) eV: divide by \(1.6 \times 10^{-19}\)
- eV \(\to\) joules: multiply by \(1.6 \times 10^{-19}\)

Why use it: photon energies are \(\sim 10^{-19}\ \mathrm{J}\) — awkward in joules,
tidy in eV. Work functions (later episodes) are also quoted in eV.

### Listing 3 — Worked Example A: energy of a UV photon (λ = 3.00 × 10^-7 m)

Want \(E\), given \(\lambda\) \(\to\) use \(E = hc/\lambda\):

$$
E = \frac{(6.63 \times 10^{-34})(3.0 \times 10^{8})}{3.00 \times 10^{-7}}
$$

Numerator: \(6.63 \times 10^{-34} \times 3.0 \times 10^{8} = 1.989 \times 10^{-25}\).

$$
E = \frac{1.989 \times 10^{-25}}{3.00 \times 10^{-7}} = 6.63 \times 10^{-19}\ \mathrm{J}
$$

In eV:

$$
\frac{6.63 \times 10^{-19}}{1.6 \times 10^{-19}} \approx 4.1\ \mathrm{eV}
$$

Method (mark-earning structure): (1) write equation; (2) substitute with units; (3) evaluate; (4) convert to eV.

### Listing 4 — Worked Example B: λ = 425 nm → frequency and energy (J and eV)

Convert wavelength: \(425\ \mathrm{nm} = 4.25 \times 10^{-7}\ \mathrm{m}\).

Frequency:

$$
f = \frac{c}{\lambda} = \frac{3.0 \times 10^{8}}{4.25 \times 10^{-7}} = 7.06 \times 10^{14}\ \mathrm{Hz} \quad (\approx 7.1 \times 10^{14}\ \mathrm{Hz})
$$

Energy:

$$
E = h f = (6.63 \times 10^{-34})(7.06 \times 10^{14}) = 4.68 \times 10^{-19}\ \mathrm{J}
$$

In eV:

$$
E = \frac{4.68 \times 10^{-19}}{1.6 \times 10^{-19}} = 2.92\ \mathrm{eV} \quad (\approx 2.9\ \mathrm{eV},\ \text{a blue-violet photon})
$$

Note: \(E = hf\) (via \(f\)) and \(E = hc/\lambda\) (direct) give the same answer.

### Listing 5 — Worked Example C: how many photons? (eye detection)

Q: eye detects \(E_{\text{total}} = 2.00 \times 10^{-17}\ \mathrm{J}\) of light at \(\lambda = 5.50 \times 10^{-7}\ \mathrm{m}\). How many photons is that?

Step 1 — energy of ONE photon:

$$
E_{\text{photon}} = \frac{hc}{\lambda} = \frac{(6.63 \times 10^{-34})(3.0 \times 10^{8})}{5.50 \times 10^{-7}} = \frac{1.989 \times 10^{-25}}{5.50 \times 10^{-7}} = 3.62 \times 10^{-19}\ \mathrm{J}
$$

Step 2 — number of photons:

$$
n = \frac{E_{\text{total}}}{E_{\text{photon}}} = \frac{2.00 \times 10^{-17}}{3.62 \times 10^{-19}} \approx 55\ \text{photons}
$$

Keep distinct:

- \(E_{\text{total}}\ (\mathrm{J}) \div E_{\text{photon}}\ (\mathrm{J}) \to n\) (pure number)
- \(P\ (\mathrm{W} = \mathrm{J\,s^{-1}}) \div E_{\text{photon}}\ (\mathrm{J}) \to N\) (photons per second)

### Listing 6 — Worked Example D: equal-power lasers, different colour

Q: red laser \(\lambda_{\text{red}} = 600\ \mathrm{nm}\), blue laser \(\lambda_{\text{blue}} = 450\ \mathrm{nm}\), SAME power \(P\). Compare their rate of emitting photons.

Energy per photon \(\propto 1/\lambda\), so:

$$
\frac{E_{\text{blue}}}{E_{\text{red}}} = \frac{\lambda_{\text{red}}}{\lambda_{\text{blue}}} = \frac{600}{450} = \frac{4}{3}
$$

(each blue photon carries \(\tfrac{4}{3}\) the energy of a red photon).

Photons per second at fixed power (\(N = P / E_{\text{photon}}\), so \(N \propto \lambda\)):

$$
\frac{N_{\text{red}}}{N_{\text{blue}}} = \frac{\lambda_{\text{red}}}{\lambda_{\text{blue}}} = \frac{600}{450} = \frac{4}{3} \approx 1.33
$$

Conclusion: the RED laser emits photons at the higher rate (\(\approx 1.33\times\) as many per second) because each red photon carries less energy, so more are needed to deliver the same power. Equal power \(\to\) redder light \(\to\) more photons per second.

### Listing 7 — Reference values and key terms
| Quantity / item | Value / detail |
|---|---|
| Planck's constant, h | 6.63 × 10^-34 J s |
| Speed of light, c | 3.0 × 10^8 m s^-1 |
| Electron charge, e | 1.6 × 10^-19 C |
| 1 electron-volt | 1 eV = 1.6 × 10^-19 J |
| Photon | discrete, indivisible quantum (packet) of light energy = hf |
| Quantisation | energy exchanged only in whole multiples of hf (all-or-nothing) |
| Frequency → | sets the ENERGY of each photon (E = hf) |
| Intensity → | sets the NUMBER of photons per second (not photon energy) |
| Power relation | P = N × hf  (power = photons per second × energy per photon) |
| Max Planck | 1900: introduced E = hf for black-body radiation; called it a "mathematical trick" |
| Albert Einstein | 1905: treated quanta as real photons; photoelectric effect; Nobel Prize 1921 |
| 1 nm | 1 × 10^-9 m (convert before using c = fλ) |
