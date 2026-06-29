---
title: "Supplementary Materials — Diffraction and Interference: Why the Double-Slit Pattern Forms"
module: M7
lesson: "05"
script: script.md
---

# Supplementary Materials

Key equations, the worked double-slit example, the model extended-response answer, and the reference values for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Worked example: sodium light through a double slit

**Given:**

- \(\lambda = 589\ \mathrm{nm} = 589 \times 10^{-9}\ \mathrm{m}\) (sodium yellow, monochromatic)
- \(d = 0.100\ \mathrm{mm} = 1.0 \times 10^{-4}\ \mathrm{m}\) (slit separation)
- \(L = 1.50\ \mathrm{m}\) (slit-to-screen distance)

**Condition for a bright fringe (maximum)**

$$
d \sin\theta = m\lambda \qquad m = 0, 1, 2, 3, \ldots \quad (m = 0 \text{ is the central maximum})
$$

**(a) First-order maximum, \(m = 1\) — angle and screen distance**

$$
\sin\theta = \frac{m\lambda}{d} = \frac{1 \times 589 \times 10^{-9}}{1.0 \times 10^{-4}} = 5.89 \times 10^{-3}
$$

$$
\theta = \sin^{-1}(5.89 \times 10^{-3}) = 0.337°
$$

Screen distance (small angle, \(x = L\sin\theta\)):

$$
x_1 = L \sin\theta = 1.50 \times 5.89 \times 10^{-3} = 8.8 \times 10^{-3}\ \mathrm{m} = 8.8\ \mathrm{mm}
$$

**(b) Third-order maximum, \(m = 3\) — distance from centre**

Maxima are evenly spaced, so:

$$
x_3 = 3 \times x_1 = 3 \times 8.8\ \mathrm{mm} = 26.4\ \mathrm{mm}
$$

Check via \(x = m\lambda L/d\):

$$
x_3 = \frac{3 \times 589 \times 10^{-9} \times 1.50}{1.0 \times 10^{-4}} \approx 26.5\ \mathrm{mm} \quad \text{— rounding-consistent.}
$$

**Answers:** (a) \(\theta \approx 0.337°\), \(x_1 \approx 8.8\ \mathrm{mm}\); (b) \(x_3 \approx 26.4\ \mathrm{mm}\).

### Listing 2 — Symbols, meanings and SI units
| Symbol | Meaning | SI unit |
|--------|---------|---------|
| \(d\) | slit separation (centre-to-centre distance between the two slits) | metre (m) |
| \(\theta\) (theta) | angle from the central axis to the fringe | degree or radian (dimensionless) |
| \(m\) | order number of the fringe (\(m = 0\) is the central bright fringe) | none (integer) |
| \(\lambda\) (lambda) | wavelength of the light | metre (m); \(1\ \mathrm{nm} = 10^{-9}\ \mathrm{m}\) |
| \(x\) | distance on the screen from the central maximum to the \(m\)-th maximum | metre (m) |
| \(L\) | perpendicular distance from the slits to the screen | metre (m) |

### Listing 3 — The two interference conditions and the screen relation

**Constructive interference — bright fringe (maximum)**

Path difference = whole number of wavelengths:

$$
d \sin\theta = m\lambda \qquad m = 0, 1, 2, 3, \ldots
$$

\(\to\) waves arrive IN PHASE (crest meets crest) \(\to\) reinforce \(\to\) BRIGHT.

**Destructive interference — dark fringe (minimum)**

Path difference = half-integer number of wavelengths (\(\tfrac{1}{2}\lambda,\ 1\tfrac{1}{2}\lambda,\ 2\tfrac{1}{2}\lambda, \ldots\) i.e. a whole number minus a half):

$$
d \sin\theta = \left(m - \tfrac{1}{2}\right)\lambda \qquad m = 1, 2, 3, \ldots
$$

\(\to\) waves arrive EXACTLY OUT OF PHASE (crest meets trough) \(\to\) cancel \(\to\) DARK.

**Small-angle screen relation** (the practical workhorse)

For small \(\theta\), \(\sin\theta \approx \tan\theta\):

$$
\sin\theta \approx \frac{m\lambda}{d} \approx \frac{x}{L} \quad\to\quad x = \frac{m\lambda L}{d}
$$

MEMORY HOOK: "Whole is bright, half is dark." NOTE ON SYMBOLS: the data sheet uses \(m\) and \(d\sin\theta = m\lambda\). Some textbooks write the order as \(n\) and minima as \((n - 0.5)\lambda\) — identical physics. Use the data-sheet symbol \(m\) in the exam.

### Listing 4 — Model extended-response (5 marks)

Q: Explain, in terms of interference, the formation of the bright and dark bands in a double-slit pattern, and account for why small slit gaps are used.

**Model answer**

- When monochromatic light passes through the two narrow, closely spaced slits, each slit DIFFRACTS the light — spreads it out — because the slit width is comparable to light's very small wavelength.
- By HUYGENS'S PRINCIPLE each slit acts as a source of secondary wavelets; because both are lit by the same wavefront the two sources are COHERENT (same wavelength, constant phase relationship).
- The two diffracted waves overlap on the screen and SUPERPOSE.
- The pattern depends on the PATH DIFFERENCE — the difference in distance the light travels from each slit to a point on the screen.
- Where the path difference is a WHOLE NUMBER of wavelengths, the waves arrive IN PHASE, crest reinforces crest \(\to\) CONSTRUCTIVE interference \(\to\) BRIGHT band.
- Where the path difference is a WHOLE NUMBER PLUS A HALF, the waves arrive EXACTLY OUT OF PHASE, crest meets trough \(\to\) DESTRUCTIVE interference \(\to\) DARK band.
- Small slit gaps are essential because diffraction (and hence the overlap that allows interference) is only significant when the gap is of the same order as the wavelength of light, which is only a few hundred nanometres. A large gap \(\to\) negligible spreading \(\to\) no overlap \(\to\) no pattern.
- The appearance of DARK bands — where light added to light gives darkness — cannot be explained by a particle model and is therefore strong evidence for the WAVE MODEL of light.

### Listing 5 — Key terms, names and reference values
| Item | Value / meaning |
|------|-----------------|
| Christiaan Huygens | Proposed Huygens's Principle: every point on a wavefront acts as a source of secondary circular wavelets; the new wavefront is their envelope. (Thought light was longitudinal — wrong.) |
| Thomas Young (1773–1829) | Performed the double-slit experiment (~1801); definitive quantitative evidence of light interference. |
| Monochromatic | Single wavelength (one pure colour). |
| Coherent | Same wavelength AND constant phase relationship. |
| Incoherent | Random phase relationship (e.g. two separate lamps) → no stable pattern. |
| Constructive interference | In phase → reinforcement → bright maximum. |
| Destructive interference | Exactly out of phase → cancellation → dark minimum (energy redistributed, not destroyed). |
| Path difference | Difference in path lengths from the two slits to a screen point. |
| Order number \(m\) | \(m = 0\) central maximum, \(m = 1\) first-order, \(m = 2\) second-order, … |
| Visible wavelength range | ≈ 400 nm (violet) to 700 nm (red). |
| Sodium-lamp wavelength | 589 nm (yellow). |
| Speed of light \(c\) | \(3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\) (data sheet); \(c = f\lambda\). |
| White light through slits | Central maximum stays white (zero path difference for all \(\lambda\)); outer fringes smear into coloured spectra. |
| Unit conversions | \(1\ \mathrm{nm} = 10^{-9}\ \mathrm{m}\); \(1\ \mathrm{mm} = 10^{-3}\ \mathrm{m}\); \(1\ \mathrm{\mu m} = 10^{-6}\ \mathrm{m}\). |
