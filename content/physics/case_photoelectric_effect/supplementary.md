---
title: "Supplementary Materials — The Photoelectric Effect — Birth of the Quantum"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Photon energy (Planck–Einstein relation)

$$
E = h f
$$

where:

- \(E\) = energy of one photon (joules, J)
- \(h\) = Planck's constant \(= 6.626\times10^{-34}\ \mathrm{J\,s}\)
- \(f\) = frequency of the light (hertz, Hz)

Using the wave relation \(c = f\lambda\), you can also write:

$$
E = \frac{h c}{\lambda}
$$

where \(c\) = speed of light \(= 3.0\times10^{8}\ \mathrm{m/s}\) and \(\lambda\) = wavelength (metres, m).

Handy shortcut in electron-volt units: \(h c = 1240\ \mathrm{eV\cdot nm}\), so

$$
E\ (\text{in eV}) = \frac{1240}{\lambda\ (\text{in nm})}
$$

### Listing 2 — Einstein's photoelectric equation

$$
K_{\max} = h f - W \qquad (\text{NESA / data-sheet form})
$$

where:

- \(K_{\max}\) = maximum kinetic energy of an ejected photoelectron (J)
- \(h f\) = energy delivered by one incident photon (J)
- \(W\) = work function of the metal (J) — the minimum energy to free an electron from the surface

NOTE ON SYMBOLS: NESA and the Jacaranda textbook write the work function as \(W\). The Greek letter \(\phi\) (phi) is the same quantity and appears in some references; use \(W\) in HSC answers. The textbook also writes the kinetic-energy term as \(E_{k,\max}\).

This equation IS the law of conservation of energy for a single photon–electron collision:

$$
\text{photon energy} = \text{escape cost} + \text{kinetic energy}, \qquad h f = W + K_{\max}
$$

Threshold (cut-off) frequency \(f_0\) — the photon just barely frees an electron, so \(K_{\max} = 0\):

$$
0 = h f_0 - W \qquad\Rightarrow\qquad f_0 = \frac{W}{h}
$$

Below \(f_0\): no emission, regardless of intensity. At or above \(f_0\): emission is immediate (no time delay).

The same energy equation describes THERMIONIC EMISSION, where the escape energy \(W\) is supplied by heating the metal rather than by a photon. NESA pairs the two in the same dot point.

### Listing 3 — Stopping voltage (how the energy is measured)

A reverse voltage \(V_s\) is applied to halt the fastest electrons. When the photocurrent just reaches zero:

$$
e V_s = K_{\max} = h f - W
$$

where \(e\) = elementary charge \(= 1.602\times10^{-19}\ \mathrm{C}\) and \(V_s\) = stopping voltage (volts, V).

Rearranged to show the straight-line graph Einstein predicted:

$$
V_s = \frac{h}{e}\,f - \frac{W}{e}
$$

Plot \(V_s\) on the y-axis against \(f\) on the x-axis:

- slope \(= h/e\) \(\to\) multiply by \(e\) to get Planck's constant \(h\)
- x-intercept \(= f_0\) (threshold frequency)
- y-intercept \(= -W/e\)

All metals give parallel lines (same slope), shifted by their \(W\).

NESA exam tip: a graph of \(K_{\max}\) (in joules or eV) versus \(f\) gives a slope equal to \(h\) DIRECTLY, an x-intercept of \(f_0\), and a y-intercept of \(-W\). This is the graph the question usually shows.

### Listing 4 — Key constants and conversions

| Quantity | Symbol | Value (NESA data sheet) |
|----------|--------|-------|
| Planck's constant | h | 6.626 x 10^-34 J s  (= 4.136 x 10^-15 eV s) |
| Speed of light | c | 3.00 x 10^8 m/s |
| Charge on electron | q_e | -1.602 x 10^-19 C |
| Energy conversion | — | 1 eV = 1.602 x 10^-19 J |
| Wien's displacement constant | b | 2.898 x 10^-3 m K |
| Useful product | h c | 1240 eV·nm (= 1.99 x 10^-25 J·m) |
| Millikan's measured h (1916) | h | 6.57 x 10^-34 J s (within ~0.5% of accepted value) |

(The NESA data sheet lists \(h\) as \(6.626\times10^{-34}\ \mathrm{J\,s}\). The Jacaranda textbook rounds this to \(6.63\times10^{-34}\ \mathrm{J\,s}\), which is what the worked example below uses; both are accepted in HSC answers.)

### Listing 5 — Work functions of common metals

| Metal | Work function W (eV) | Threshold f_0 (Hz) | Threshold λ (nm) |
|-------|---------------------|--------------------|------------------|
| Sodium (Na) | 2.46 | 5.9 x 10^14 | ~505 (green) |
| Aluminium (Al) | 4.08 | 9.9 x 10^14 | ~304 (UV) |
| Zinc (Zn) | 4.31 | 1.04 x 10^15 | ~288 (UV) |
| Copper (Cu) | 4.70 | 1.14 x 10^15 | ~264 (UV) |
| Silver (Ag) | 4.73 | 1.14 x 10^15 | ~262 (UV) |
| Platinum (Pt) | 6.35 | 1.54 x 10^15 | ~195 (UV) |

(Alkali metals like sodium have the lowest work functions — their outer electrons are loosely held — which is why early photocells used them, and why sodium and zinc are the metals named in the textbook experiments. Reactive metals such as sodium oxidise instantly in air, which is why Millikan cut a fresh surface in vacuum. Work-function values vary slightly with surface condition between sources, so they are not on the data sheet — you will always be given a value in a question.)

### Listing 6 — Wave model vs photon model (the four observations)

This is the comparison NESA exam questions return to again and again. Note that the wave model only succeeds on observation 3 — be precise.

| Observation | Wave model predicts | Photon model predicts |
|-------------|--------------------|-----------------------|
| 1. No time delay, even at very low intensity | A delay while faint light slowly builds up enough energy — FAILS | One photon delivers all its energy in a single collision; emission is instant — CORRECT |
| 2. Threshold frequency f_0, independent of intensity | No threshold; any colour should work if bright enough or given time — FAILS | If h f < W no single photon can free an electron, however many arrive — CORRECT |
| 3. Brighter light → more electrons (same energy each) | More intense light = more energy per electron — PARTLY RIGHT on number, WRONG on energy | Intensity = photons per second, so more photons = more electrons — CORRECT |
| 4. Electron K_max depends on frequency, not intensity | Bigger amplitude should mean more energetic electrons — FAILS | Each photon's energy is h f, so K_max rises linearly with f — CORRECT |

### Listing 7 — Timeline of the key discoveries

| Year | Who | What |
|------|-----|------|
| 1887 | Heinrich Hertz | First observes the effect: UV light makes the detector spark jump more easily |
| 1888 | Wilhelm Hallwachs | Negatively charged zinc plate discharges under UV; positively charged plate does not |
| 1897 | J. J. Thomson | Discovers the electron (in cathode rays) |
| 1899 | J. J. Thomson | Shows the ejected particles are electrons, freed by radiation not by a field |
| 1900 | Max Planck | Quantises energy (E = h f) to solve black body radiation / the ultraviolet catastrophe |
| 1902 | Philipp Lenard | Measures the four key behaviours; finds the energy of emitted electrons depends on frequency, not intensity, and there is a cut-off frequency |
| 1905 | Albert Einstein | Proposes the light quantum (photon); writes K_max = h f − W; the paper he called "very revolutionary" |
| 1916 | Robert Millikan | After ~10 years trying to disprove it, confirms the equation and measures h to ~0.5% |
| 1921 | Nobel Prize | Awarded to Einstein "for his discovery of the law of the photoelectric effect" (not relativity) |
| 1923 | Arthur Compton | X-ray scattering (Compton effect) shows photons carry momentum — final proof |
| 1926 | Gilbert Lewis | Coins the word "photon" |

### Listing 8 — Worked example (HSC-style)

PROBLEM: Light of wavelength \(425\ \mathrm{nm}\) strikes a clean metal surface. The stopping voltage needed to halt the fastest photoelectrons is measured to be \(1.25\ \mathrm{V}\).

- (a) Find the photon energy in joules and in eV.
- (b) Find the work function of the metal in eV and J.
- (c) Find the threshold frequency \(f_0\) and the longest wavelength that will still eject an electron.
- (d) Light of wavelength \(390\ \mathrm{nm}\) now strikes the same metal. Find the new stopping voltage.

SOLUTION

(a) Photon energy:

$$
f = \frac{c}{\lambda} = \frac{3.0\times10^{8}}{4.25\times10^{-7}} = 7.06\times10^{14}\ \mathrm{Hz}
$$

$$
E = h f = (6.63\times10^{-34})(7.06\times10^{14}) = 4.68\times10^{-19}\ \mathrm{J}
$$

$$
\text{In eV:} \quad E = \frac{4.68\times10^{-19}}{1.6\times10^{-19}} = 2.92\ \mathrm{eV}
$$

(b) Work function — the stopping voltage gives \(K_{\max}\) directly:

$$
K_{\max} = e V_s = 1.25\ \mathrm{eV}\ (= 2.00\times10^{-19}\ \mathrm{J})
$$

Rearrange Einstein's equation, \(W = h f - K_{\max}\):

$$
W = 2.92\ \mathrm{eV} - 1.25\ \mathrm{eV} = 1.67\ \mathrm{eV} = 1.67\times1.6\times10^{-19} = 2.67\times10^{-19}\ \mathrm{J}
$$

(c) Threshold frequency and wavelength:

$$
f_0 = \frac{W}{h} = \frac{2.67\times10^{-19}}{6.63\times10^{-34}} = 4.03\times10^{14}\ \mathrm{Hz}
$$

$$
\lambda_{\max} = \frac{c}{f_0} = \frac{3.0\times10^{8}}{4.03\times10^{14}} = 7.4\times10^{-7}\ \mathrm{m} = 740\ \mathrm{nm}
$$

(d) New stopping voltage at \(390\ \mathrm{nm}\) — work in eV using \(h c = 1240\ \mathrm{eV\cdot nm}\):

$$
\text{photon energy} = \frac{1240}{390} = 3.18\ \mathrm{eV}
$$

$$
K_{\max} = h f - W = 3.18 - 1.67 = 1.51\ \mathrm{eV}
$$

Since \(e V_s = K_{\max}\), the stopping voltage \(V_s = 1.51\ \mathrm{V}\) (\(\approx 1.5\ \mathrm{V}\)). Shorter wavelength \(\to\) higher frequency \(\to\) larger \(K_{\max}\) \(\to\) larger stopping voltage, as expected.

ANSWERS

- (a) \(4.68\times10^{-19}\ \mathrm{J} = 2.92\ \mathrm{eV}\)
- (b) \(W = 1.67\ \mathrm{eV} = 2.67\times10^{-19}\ \mathrm{J}\)
- (c) \(f_0 = 4.03\times10^{14}\ \mathrm{Hz}\); \(\lambda_{\max} = 740\ \mathrm{nm}\)
- (d) \(V_s \approx 1.5\ \mathrm{V}\)
