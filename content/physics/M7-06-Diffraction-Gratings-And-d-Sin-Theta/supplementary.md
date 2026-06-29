---
title: "Supplementary Materials — Diffraction Gratings and d sin theta = m lambda: Solving Interference Problems"
module: M7
lesson: "06"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. These listings are the read-along reference; the audio is self-contained and never depends on them, though it speaks every key result in words.

### Listing 0 — The interference equations (reference)

**Maximum (bright fringe), condition for constructive interference:**

$$
d \sin\theta = m\lambda \qquad m = 0, 1, 2, 3 \ldots \quad \text{(on the HSC data sheet)}
$$

**Minimum (dark fringe), condition for destructive interference:**

$$
d \sin\theta = \left(m - \tfrac{1}{2}\right)\lambda \qquad m = 1, 2, 3 \ldots \quad \text{(not on data sheet)}
$$

**Symbols and SI units:**

- \(d\) = slit / grating-line separation, metres (\(\mathrm{m}\))
- \(\theta\) = angle from central (straight-through) direction, degrees or radians
- \(m\) = order of the maximum (integer), no unit
- \(\lambda\) = wavelength of the light, metres (\(\mathrm{m}\))

**Small-angle screen geometry** (small \(\theta\) only, a few degrees):

$$
\sin\theta \approx \tan\theta = \frac{x}{L} \quad\to\quad \frac{m\lambda}{d} = \frac{x}{L}
$$

- \(x\) = distance on screen from central maximum to the fringe (\(\mathrm{m}\))
- \(L\) = perpendicular distance from slits/grating to screen (\(\mathrm{m}\))

**Large angle** (\(\theta\) more than a few degrees): use \(d\sin\theta = m\lambda\) directly, then \(x = L\tan\theta\) (NOT \(x = L\sin\theta\)).

**Grating line-spacing from line density:**

$$
d = \frac{1}{N} \qquad N = \text{number of lines per METRE}
$$

lines per metre \(= (\text{lines per cm}) \times 100 \quad\to\quad d = \dfrac{1}{100 \times (\text{lines per cm})}\)

### Listing 1 — Double slit, worked example (sodium lamp)

**Given:**

- \(\lambda = 589\ \mathrm{nm} = 589 \times 10^{-9}\ \mathrm{m}\)
- \(d = 0.100\ \mathrm{mm} = 1.0 \times 10^{-4}\ \mathrm{m}\)
- \(L = 1.50\ \mathrm{m}\)

**(a) First-order maximum, \(m = 1\):**

$$
\sin\theta = \frac{m\lambda}{d} = \frac{1 \times 589 \times 10^{-9}}{1.0 \times 10^{-4}} = 5.89 \times 10^{-3}
$$

$$
\theta = \sin^{-1}(5.89 \times 10^{-3}) = 0.337° \quad \text{(small angle — approximation valid)}
$$

Distance on screen:

$$
x = L \sin\theta = 1.50 \times 5.89 \times 10^{-3} = 8.8 \times 10^{-3}\ \mathrm{m} = 8.8\ \mathrm{mm}
$$

**(b) Third-order maximum, \(m = 3\):**

Small angles \(\to\) maxima evenly spaced:

$$
x_3 = 3 \times x_1 = 3 \times 8.8\ \mathrm{mm} = 26.4\ \mathrm{mm} \approx 26\ \mathrm{mm}
$$

### Listing 2 — Diffraction grating, white-light dispersion (10 μm line spacing)

Given: \(d = 10\ \mathrm{\mu m} = 10 \times 10^{-6}\ \mathrm{m}\), \(m = 1\).

**Red, \(\lambda = 700\ \mathrm{nm} = 700 \times 10^{-9}\ \mathrm{m}\):**

$$
\sin\theta = \frac{m\lambda}{d} = \frac{700 \times 10^{-9}}{10 \times 10^{-6}} = 0.070
$$

$$
\theta_{\text{red}} = \sin^{-1}(0.070) = 4.0°
$$

**Blue, \(\lambda = 450\ \mathrm{nm} = 450 \times 10^{-9}\ \mathrm{m}\):**

$$
\sin\theta = \frac{m\lambda}{d} = \frac{450 \times 10^{-9}}{10 \times 10^{-6}} = 0.045
$$

$$
\theta_{\text{blue}} = \sin^{-1}(0.045) = 2.6°
$$

Conclusion: red (\(4.0°\)) is deflected MORE than blue (\(2.6°\)), so each order fans into a spectrum — blue/violet nearest the centre, red furthest out. This is the OPPOSITE order to a glass prism (where blue/violet bends most). "Grating Red Greatest."

### Listing 3 — Diffraction grating, find the spot spacing (the reciprocal + small-angle traps)

Given: 3000 lines per cm, \(\lambda = 530\ \mathrm{nm} = 530 \times 10^{-9}\ \mathrm{m}\), \(L = 1.25\ \mathrm{m}\).

**(a) Line spacing \(d\)** — convert to lines per metre FIRST, then reciprocate:

$$
3000\ \mathrm{lines/cm} \times 100 = 300\,000\ \mathrm{lines/m}
$$

$$
d = \frac{1}{300\,000} = 3.33 \times 10^{-6}\ \mathrm{m} \quad (3.33\ \mathrm{\mu m})
$$

Trap: forgetting \(\times 100 \to 100\times\) error; using 3000 directly \(\to\) wrong.

**(b) First-order angle, \(m = 1\):**

$$
\sin\theta = \frac{m\lambda}{d} = \frac{530 \times 10^{-9}}{3.33 \times 10^{-6}} = 0.159
$$

$$
\theta = \sin^{-1}(0.159) = 9.15° \quad \leftarrow \text{NOT a small angle}
$$

**(c) Distance on screen** — angle is large, so use \(x = L\tan\theta\):

$$
x = L \tan\theta = 1.25 \times \tan(9.15°) = 1.25 \times 0.1611 = 0.201\ \mathrm{m} \approx 20\ \mathrm{cm}
$$

Compare small-angle (invalid here): \(x = L\sin\theta = 1.25 \times 0.159 = 0.199\ \mathrm{m}\). The two already differ at \(9°\) and diverge further as \(\theta\) grows — flag it.

### Listing 4 — Grating line-spacing quick reference (d = 1/N)
| Lines per cm | Lines per metre (× 100) | \(d = 1/N\) (m)        |
|--------------|-------------------------|----------------------|
| 3 000        | 300 000                 | \(3.33 \times 10^{-6}\) (3.33 μm)|
| 4 000        | 400 000                 | \(2.50 \times 10^{-6}\) (2.50 μm)|
| 5 000        | 500 000                 | \(2.00 \times 10^{-6}\) (2.00 μm)|
| 10 000       | 1 000 000               | \(1.00 \times 10^{-6}\) (1.00 μm)|

### Listing 5 — Exam-question worked answers (Q2 and Q3 from the script)

**Q2 — Double slit, second-order angle:** \(\lambda = 600\ \mathrm{nm} = 600 \times 10^{-9}\ \mathrm{m}\), \(d = 2 \times 10^{-5}\ \mathrm{m}\), \(m = 2\).

$$
\sin\theta = \frac{m\lambda}{d} = \frac{2 \times 600 \times 10^{-9}}{2 \times 10^{-5}} = \frac{1.2 \times 10^{-6}}{2 \times 10^{-5}} = 0.06
$$

$$
\theta = \sin^{-1}(0.06) = 3.4°
$$

**Q3 — Grating, 4000 lines/cm, red 650 nm, first order:**

$$
4000\ \mathrm{lines/cm} \times 100 = 400\,000\ \mathrm{lines/m}
$$

$$
d = \frac{1}{400\,000} = 2.5 \times 10^{-6}\ \mathrm{m}
$$

$$
\sin\theta = \frac{m\lambda}{d} = \frac{650 \times 10^{-9}}{2.5 \times 10^{-6}} = 0.26
$$

$$
\theta = \sin^{-1}(0.26) = 15.1°
$$

Judgement: \(15°\) is NOT small \(\to\) small-angle approximation invalid; use \(d\sin\theta = m\lambda\) directly and \(x = L\tan\theta\) for any screen distance.

### Listing 6 — Reference data and visible-spectrum values
| Quantity                         | Value / range                          |
|----------------------------------|----------------------------------------|
| Speed of light, \(c\)            | \(3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\) (data sheet)           |
| Visible spectrum                 | ≈ 400 nm (violet) to 700 nm (red)      |
| 1 nanometre (nm)                 | \(1 \times 10^{-9}\ \mathrm{m}\)                             |
| 1 micrometre (μm)                | \(1 \times 10^{-6}\ \mathrm{m}\)                             |
| 1 millimetre (mm)                | \(1 \times 10^{-3}\ \mathrm{m}\)                             |
| Central maximum                  | \(m = 0\) (white in white light)           |
| Dispersion order (grating)       | blue/violet nearest centre → red furthest |
| Dispersion order (prism, contrast)| red least deviated → blue/violet most |
