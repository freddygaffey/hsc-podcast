---
title: "Supplementary Materials — Black-Body Radiation, Wien's Law and the Ultraviolet Catastrophe"
module: M7
lesson: "10"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference. Symbols: λ_max = wavelength of peak intensity; T = absolute temperature (kelvin); b = Wien's displacement constant; h = Planck's constant; f = frequency; c = speed of light; E = energy of a quantum (photon).

### Listing 1 — Wien's displacement law (equation and definitions)

Wien's displacement law (a constant):

$$
\lambda_{\max} \times T = b
$$

Rearranged for each unknown:

$$
\lambda_{\max} = \frac{b}{T} \qquad\text{(find the peak wavelength from temperature)}
$$

$$
T = \frac{b}{\lambda_{\max}} \qquad\text{(find the temperature from the peak wavelength)}
$$

- \(\lambda_{\max}\) — wavelength of PEAK intensity (metres) — not the only wavelength emitted
- \(T\) — absolute temperature (KELVIN — always; °C \(+\ 273\) first)
- \(b\) — Wien's displacement constant \(= 2.9 \times 10^{-3}\ \mathrm{m \cdot K}\) (data sheet)

Direction: hotter \(T\) \(\to\) shorter \(\lambda_{\max}\) \(\to\) bluer ("hot and blue, short and true").
\(\lambda_{\max}\) and \(T\) are INVERSELY proportional: double \(T\) \(\Rightarrow\) halve \(\lambda_{\max}\).

### Listing 2 — Worked example: peak wavelength from temperature (the Sun, and a hot star)

**(a)** The Sun's surface, \(T = 5800\ \mathrm{K}\). Find the peak wavelength.

$$
\lambda_{\max} = \frac{b}{T} = \frac{2.9 \times 10^{-3}}{5800} = 5.0 \times 10^{-7}\ \mathrm{m} = 500\ \mathrm{nm}
$$

\(\to\) green-yellow, mid-visible (eyes peak here).

**(b)** Exam Q2: a star at \(T = 7250\ \mathrm{K}\). Find the peak wavelength.

$$
\lambda_{\max} = \frac{b}{T} = \frac{2.9 \times 10^{-3}}{7250} = 4.0 \times 10^{-7}\ \mathrm{m} = 400\ \mathrm{nm}
$$

\(\to\) blue-violet end of the visible spectrum (hot blue-white star).

Method markers reward: write the equation \(\to\) substitute with \(T\) in KELVIN
\(\to\) answer in metres \(\to\) convert to nm.

### Listing 3 — Worked example: temperature from peak wavelength (reading a star's colour)

Rearrange Wien's law for temperature: \(T = b / \lambda_{\max}\).

**(a)** Star peaks at \(\lambda_{\max} = 480\ \mathrm{nm} = 4.8 \times 10^{-7}\ \mathrm{m}\):

$$
T = \frac{2.9 \times 10^{-3}}{4.8 \times 10^{-7}} \approx 6.0 \times 10^{3}\ \mathrm{K} \quad (\sim 6000\ \mathrm{K},\ \text{Sun-like})
$$

**(b)** Blue star peaks at \(\lambda_{\max} = 290\ \mathrm{nm} = 2.9 \times 10^{-7}\ \mathrm{m}\):

$$
T = \frac{2.9 \times 10^{-3}}{2.9 \times 10^{-7}} = 1.0 \times 10^{4}\ \mathrm{K} \quad (\sim 10\,000\ \mathrm{K},\ \text{hot blue})
$$

**(c)** Red giant (e.g. Betelgeuse) peaks at \(\lambda_{\max} = 830\ \mathrm{nm} = 8.3 \times 10^{-7}\ \mathrm{m}\):

$$
T = \frac{2.9 \times 10^{-3}}{8.3 \times 10^{-7}} \approx 3.5 \times 10^{3}\ \mathrm{K} \quad (\sim 3500\ \mathrm{K},\ \text{cool red})
$$

This is the quantitative engine behind M7-04: blue stars hot, red stars cool.

### Listing 4 — Black-body curves at different temperatures (peak shift)
| Object | Temperature T (K) | Peak wavelength λ_max = b/T | Region / colour |
|--------|-------------------|-----------------------------|-----------------|
| Human skin | 305 (32 °C) | 9.5 × 10⁻⁶ m (≈ 9500 nm) | Infrared (invisible; thermal cameras) |
| Dull-red hotplate | 725 | 4.0 × 10⁻⁶ m (≈ 4000 nm) | Infrared, edge of red |
| Incandescent filament | 3000 | 9.7 × 10⁻⁷ m (≈ 970 nm) | Near-IR / red — yellow-white glow |
| Cool red star | 3500 | 8.3 × 10⁻⁷ m (≈ 830 nm) | Red |
| The Sun | 5800 | 5.0 × 10⁻⁷ m (≈ 500 nm) | Green-yellow (mid-visible) |
| Sun-like star | 6000 | 4.8 × 10⁻⁷ m (≈ 480 nm) | Blue-green |
| Hot blue star | 10 000 | 2.9 × 10⁻⁷ m (≈ 290 nm) | Ultraviolet / blue |

As T rises: the WHOLE curve rises (brighter at every wavelength) AND the peak moves to SHORTER wavelength.

### Listing 5 — Classical prediction vs experiment (the ultraviolet catastrophe)
```text
                Intensity
                  |
                  |\               ← CLASSICAL (Rayleigh–Jeans): rises without limit
                  | \                as λ → 0  ⇒  → INFINITY in the ultraviolet
                  |  \               (the "ultraviolet catastrophe")
                  |   \
                  |  _ \___
                  | /      ‾‾‾----___      ← EXPERIMENT (and Planck): rises to a
                  |/                 ‾‾---    PEAK, then falls back toward zero
                  +----------------------------→ Wavelength λ
                 short (UV)                long (IR)

Agreement at LONG wavelengths; total disagreement at SHORT wavelengths.
Classical curve → infinity  ⇒  impossible (violates conservation of energy)
                            ⇒  contradicts the measured peak-and-fall curve.
```

| Feature | Classical (Rayleigh–Jeans) | Experiment / Planck |
|---------|----------------------------|---------------------|
| Long wavelengths | Matches experiment | Matches classical |
| Short wavelengths | Intensity → ∞ (catastrophe) | Rises to a peak, then falls |
| Total emitted energy | Infinite (impossible) | Finite |
| Verdict | Fails — violates conservation of energy | Correct |

### Listing 6 — Planck's resolution (step-by-step logic)

1. Classical assumption: oscillating charges in the walls emit/absorb energy CONTINUOUSLY — any amount, however small. \(\Rightarrow\) predicts intensity rising without limit at short \(\lambda\) (the catastrophe).

2. Planck's hypothesis (1900): energy is exchanged only in DISCRETE QUANTA, each of size

$$
E = h f \qquad (h = 6.63 \times 10^{-34}\ \mathrm{J\,s},\ f = \text{frequency})
$$

   Energy comes in whole packets of \(hf\) — nothing in between.

3. Short wavelength = HIGH frequency \(f\) \(\Rightarrow\) LARGE quantum \(hf\) required.

4. At a given temperature the particles have a limited energy budget (the distribution of kinetic energies). Large quanta are only RARELY available \(\Rightarrow\) high-frequency (short-\(\lambda\)) emission is SUPPRESSED, not infinite.

5. Result: the predicted curve rises, PEAKS, and FALLS — matching experiment. The ultraviolet catastrophe is removed.

6. Planck believed this was only a "mathematical trick." Einstein (1905) took the quantum as a real, physical photon (next: photoelectric effect, M7-11/12). The SAME constant \(h\) reappears as the gradient of the photoelectric graph.

### Listing 7 — Key constants and values (NSW HSC data sheet)
| Quantity | Symbol | Value |
|----------|--------|-------|
| Wien's displacement constant | b | 2.9 × 10⁻³ m·K |
| Planck's constant | h | 6.63 × 10⁻³⁴ J s |
| Speed of light | c | 3.0 × 10⁸ m s⁻¹ |
| Quantum (photon) energy | E = hf | energy of one quantum, in joules |
| Celsius → kelvin | T(K) | T(°C) + 273 |
