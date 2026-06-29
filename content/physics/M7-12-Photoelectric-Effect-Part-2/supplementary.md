---
title: "Supplementary Materials — The Photoelectric Effect, Part 2: Einstein, K_max = hf - phi, and Real Applications"
module: M7
lesson: "12"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference. Symbols: K_max = maximum kinetic energy of a photoelectron; h = Planck's constant; f = frequency; φ (or W) = work function; f₀ = threshold frequency; V₀ = stopping voltage; e = electron charge; c = speed of light; λ = wavelength.

### Listing 1 — Full worked example: 425 nm light, stopping voltage 1.25 V (parts a–e)

Einstein equation: \(K_{\max} = hf - \phi\). Data sheet: \(h = 6.63 \times 10^{-34}\ \mathrm{J\,s}\), \(c = 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\), \(e = 1.6 \times 10^{-19}\ \mathrm{C}\), \(1\ \mathrm{eV} = 1.6 \times 10^{-19}\ \mathrm{J}\). Given: \(\lambda = 425\ \mathrm{nm} = 4.25 \times 10^{-7}\ \mathrm{m}\), \(V_{0} = 1.25\ \mathrm{V}\).

**(a)** Frequency:

$$
f = \frac{c}{\lambda} = \frac{3.0 \times 10^{8}}{4.25 \times 10^{-7}} = 7.06 \times 10^{14}\ \mathrm{Hz}
$$

**(b)** Photon energy:

$$
E = hf = (6.63 \times 10^{-34})(7.06 \times 10^{14}) = 4.68 \times 10^{-19}\ \mathrm{J}
$$

In eV: \(4.68 \times 10^{-19} \div 1.6 \times 10^{-19} = 2.92\ \mathrm{eV}\) (\(\approx 2.9\ \mathrm{eV}\)).

**(c)** \(K_{\max}\) — stopping voltage gives \(K_{\max}\) directly: \(K_{\max} = eV_{0}\). With \(V_{0} = 1.25\ \mathrm{V}\) \(\Rightarrow\) \(K_{\max} = 1.25\ \mathrm{eV}\). In joules:

$$
K_{\max} = 1.25 \times 1.6 \times 10^{-19} = 2.00 \times 10^{-19}\ \mathrm{J}
$$

**(d)** Work function: \(K_{\max} = hf - \phi \Rightarrow \phi = hf - K_{\max}\).

$$
\phi = 2.92 - 1.25 = 1.67\ \mathrm{eV}
$$

In joules: \(1.67 \times 1.6 \times 10^{-19} = 2.67 \times 10^{-19}\ \mathrm{J}\).

**(e)** Threshold \(f_{0}\) — at threshold \(K_{\max} = 0 \Rightarrow \phi = h f_{0} \Rightarrow f_{0} = \phi / h\):

$$
f_{0} = \frac{2.67 \times 10^{-19}}{6.63 \times 10^{-34}} = 4.03 \times 10^{14}\ \mathrm{Hz}
$$

Threshold wavelength:

$$
\lambda_{0} = \frac{c}{f_{0}} = \frac{3.0 \times 10^{8}}{4.03 \times 10^{14}} = 7.4 \times 10^{-7}\ \mathrm{m} = 740\ \mathrm{nm}
$$

### Listing 2 — Reading the graph: lithium photocell, two data points

\(K_{\max}\) vs \(f\) is a straight line, \(K_{\max} = hf - \phi\) (compare \(y = mx + c\)):

- Gradient \(m = h\) (Planck's constant — same for ALL metals \(\to\) parallel lines)
- \(x\)-intercept \(= f_{0}\) (threshold frequency)
- \(y\)-intercept \(= -\phi\) (NEGATIVE work function; \(|y\text{-intercept}| = \phi\))

Two points on the line:

- Point 1: \(f = 4.52 \times 10^{14}\ \mathrm{Hz}\), \(K_{\max} = 0.45\ \mathrm{eV} = 7.20 \times 10^{-20}\ \mathrm{J}\)
- Point 2: \(f = 6.14 \times 10^{14}\ \mathrm{Hz}\), \(K_{\max} = 1.15\ \mathrm{eV} = 1.84 \times 10^{-19}\ \mathrm{J}\)

Planck's constant = gradient = rise / run:

$$
\text{rise} = 1.84 \times 10^{-19} - 7.20 \times 10^{-20} = 1.12 \times 10^{-19}\ \mathrm{J}
$$

$$
\text{run} = (6.14 - 4.52) \times 10^{14} = 1.62 \times 10^{14}\ \mathrm{Hz}
$$

$$
h = \frac{1.12 \times 10^{-19}}{1.62 \times 10^{14}} = 6.9 \times 10^{-34}\ \mathrm{J\,s} \quad (\approx \text{accepted value})
$$

Work function (use Point 1): \(\phi = hf - K_{\max}\):

$$
\phi = (6.9 \times 10^{-34})(4.52 \times 10^{14}) - 7.20 \times 10^{-20} = 3.12 \times 10^{-19} - 0.72 \times 10^{-19} \approx 2.4 \times 10^{-19}\ \mathrm{J} \quad (\approx 1.5\ \mathrm{eV})
$$

Threshold frequency: \(f_{0} = \phi / h\):

$$
f_{0} = \frac{2.4 \times 10^{-19}}{6.9 \times 10^{-34}} \approx 3.5 \times 10^{14}\ \mathrm{Hz} \quad (= x\text{-intercept})
$$

A metal with a LARGER work function \(\to\) parallel line (same gradient \(h\)), shifted RIGHT
(higher \(f_{0}\), more negative \(y\)-intercept). Lines never converge.

### Listing 3 — Exam Question 3 worked solution: 390 nm light, φ = 1.67 eV

\(K_{\max} = hc/\lambda - \phi\). Given: \(\lambda = 390\ \mathrm{nm} = 3.90 \times 10^{-7}\ \mathrm{m}\), \(\phi = 1.67\ \mathrm{eV}\). Use \(h\) in eV·s: \(h = 4.15 \times 10^{-15}\ \mathrm{eV\,s}\), \(c = 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\).

Photon energy:

$$
E = \frac{hc}{\lambda} = \frac{(4.15 \times 10^{-15})(3.0 \times 10^{8})}{3.90 \times 10^{-7}} = \frac{1.245 \times 10^{-6}}{3.90 \times 10^{-7}} = 3.19\ \mathrm{eV}
$$

Maximum kinetic energy:

$$
K_{\max} = E - \phi = 3.19 - 1.67 = 1.52\ \mathrm{eV} \quad (\approx 1.5\ \mathrm{eV})
$$

Stopping voltage: \(K_{\max} = eV_{0}\) \(\Rightarrow\) in eV, \(V_{0}\) (volts) \(= K_{\max}\) (eV) numerically:

$$
V_{0} = 1.5\ \mathrm{V}
$$

### Listing 4 — The four observations explained by Einstein's photon model (DENF)
| Observation | Wave-model prediction (wrong unless noted) | Einstein's photon explanation |
|-------------|---------------------------------------------|-------------------------------|
| **D** — No time **D**elay | Faint light needs time to accumulate energy → delay | One photon delivers all its energy (hf) in one collision → instant emission |
| **E** — **E**nergy from frequency | Energy comes from amplitude/intensity | K_max = hf − φ; higher f → more hf left after paying φ → higher K_max |
| **N** — **N**umber from intensity | Brighter → more electrons (✓ correct, wrong reason) | Intensity = photons per second → more 1-to-1 hits → more electrons (bigger photocurrent) |
| **F** — Threshold **F**requency f₀ | No threshold; any f works given time | If hf < φ a single photon can't free an electron, regardless of intensity → cut-off at f₀ = φ/h |

### Listing 5 — Key constants and values (NSW HSC data sheet)
| Quantity | Symbol | Value |
|----------|--------|-------|
| Planck's constant | h | 6.63 × 10⁻³⁴ J s  (= 4.14 × 10⁻¹⁵ eV s) |
| Speed of light | c | 3.0 × 10⁸ m s⁻¹ |
| Electron charge (magnitude) | e | 1.6 × 10⁻¹⁹ C |
| Electron-volt | 1 eV | 1.6 × 10⁻¹⁹ J |
| Electron rest mass | mₑ | 9.1 × 10⁻³¹ kg |
| Worked example work function (≈ calcium) | φ | 1.67 eV = 2.67 × 10⁻¹⁹ J |
| Worked example threshold frequency | f₀ | 4.03 × 10¹⁴ Hz (λ₀ ≈ 740 nm) |

### Listing 6 — Photoelectric vs thermionic emission; key people

- **Photoelectric emission** — electrons freed by LIGHT (single photon, one collision)
- **Thermionic emission** — electrons freed by HEAT (thermal energy in the metal)
- \(\to\) SAME barrier to overcome: the work function \(\phi\)
- \(\to\) DIFFERENT energy source: photon vs thermal
- \(\to\) BOTH analysed with the same work-function / energy-conservation logic

People & dates (get these right):

- Hertz 1887 — first observed the effect at a spark gap
- J.J. Thomson 1899 — showed UV ejects electrons (= cathode-ray particles)
- Lenard 1902 — quantified: higher \(f\) \(\to\) higher electron energy; intensity \(\to\) number
- Planck 1900 — introduced \(E = hf\) (quantisation) for black-body radiation; thought it a "trick"
- Einstein 1905 — photon ("light quantum") explanation \(\to\) Nobel Prize 1921 (for THIS, not relativity)
- Millikan 1915–16 — measured \(V_{0}\) vs \(f\), gradient \(= h\); confirmed Einstein "reluctantly"
- "Photon" — term coined 1926 (Gilbert Lewis)

### Listing 7 — Applications of the photoelectric effect (secondary-source investigation)
| Application | How the photoelectric effect is used |
|-------------|--------------------------------------|
| **Photovoltaic (solar) cell** (named in syllabus) | Photons above threshold free electrons inside a semiconductor (internal photoelectric effect, across a band gap); freed electrons drive a current → sunlight to electricity. *Caveat: electrons are freed inside the material, not ejected into the air.* |
| **Photomultiplier tube** (strong "one other") | A faint photon ejects one electron from a photocathode (photoelectric effect); cascaded plates amplify it ~10⁶× → single-photon detection (astronomy, medical scintillation detectors, radiation counters) |
| Light meters / camera exposure | Incident light frees electrons → current proportional to brightness |
| Digital image sensors (CCD/CMOS) | Photons free electrons per pixel → charge read out as an image |
| Automatic doors / light switches | Light beam frees electrons; breaking the beam changes the current → triggers the switch |
| Night-vision devices | Photocathode releases electrons that are amplified to brighten a dim image |
