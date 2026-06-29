---
title: "Supplementary Materials — Module Review: The Nature of Light, End to End"
module: M7
lesson: "99"
script: script.md
---

# Supplementary Materials

Key equations, full worked solutions, the extended-response skeletons, and the trap-reference tables for the Module 7 review. Nothing here is spoken in the audio — it is the read-along reference. Constants used throughout: speed of light c = 3.0 × 10^8 m s^-1; Planck constant h = 6.63 × 10^-34 J s; electron charge e = 1.6 × 10^-19 C (1 eV = 1.6 × 10^-19 J); Wien's constant b = 2.9 × 10^-3 m K.

### Listing 1 — Double-slit interference, worked example

Maxima: \(d \sin\theta = m\lambda\), so \(\sin\theta = m\lambda/d\) and \(x = L \sin\theta\).

Given: \(\lambda = 589\ \mathrm{nm} = 5.89 \times 10^{-7}\ \mathrm{m}\) (sodium light), \(d = 0.100\ \mathrm{mm} = 1.00 \times 10^{-4}\ \mathrm{m}\), \(L = 1.50\ \mathrm{m}\).

First-order maximum (\(m = 1\)):

$$
\sin\theta = \frac{(1)(5.89 \times 10^{-7})}{1.00 \times 10^{-4}} = 5.89 \times 10^{-3}
$$

$$
\theta = \sin^{-1}(5.89 \times 10^{-3}) = 0.337°
$$

$$
x_{1} = L \sin\theta = 1.50 \times 5.89 \times 10^{-3} = 8.8 \times 10^{-3}\ \mathrm{m} = 8.8\ \mathrm{mm}
$$

Third-order maximum (fringes evenly spaced):

$$
x_{3} = 3 \times x_{1} = 3 \times 8.8\ \mathrm{mm} = 26.4\ \mathrm{mm}
$$

### Listing 2 — Polarisation (Malus's law), worked example with the unpolarised-step trap

First (unpolarised) filter: \(I = \tfrac{1}{2}I_{0}\) (use \(\tfrac{1}{2}\), NOT Malus). Polariser \(\to\) analyser: \(I = I_{\max}\cos^{2}\theta\) (\(\theta =\) angle between axes).

Light: unpolarised, intensity \(I_{0}\). Polariser \(\to\) analyser at \(60°\) \(\to\) second analyser a further \(30°\) (\(90°\) total).

Step 1 — after polariser (unpolarised in):

$$
I_a = \tfrac{1}{2}I_{0} = 0.500\,I_{0} \quad (50\%)
$$

Step 2 — after analyser at \(60°\):

$$
I_b = I_a \cos^{2}(60°) = 0.500 \times (0.5)^{2} = 0.500 \times 0.25 = 0.125\,I_{0} \quad (12.5\%)
$$

Step 3 — after 2nd analyser, a further \(30°\):

$$
I_c = I_b \cos^{2}(30°) = 0.125 \times (0.866)^{2} = 0.125 \times 0.75 = 0.094\,I_{0} \quad (\approx 9.4\%)
$$

Crossed polarisers (polariser + analyser at \(90°\), nothing between):

$$
I = I_a \cos^{2}(90°) = I_a \times 0 = 0 \quad \text{(no light transmitted)}
$$

### Listing 3 — Photon energy, worked example

\(E = hf = hc/\lambda\).

UV photon, \(\lambda = 3.00 \times 10^{-7}\ \mathrm{m}\):

$$
E = \frac{(6.63 \times 10^{-34})(3.00 \times 10^{8})}{3.00 \times 10^{-7}} = \frac{1.989 \times 10^{-25}}{3.00 \times 10^{-7}} = 6.63 \times 10^{-19}\ \mathrm{J}
$$

Convert to electron-volts:

$$
E = \frac{6.63 \times 10^{-19}}{1.6 \times 10^{-19}} = 4.14\ \mathrm{eV}
$$

### Listing 4 — Wien's law, worked example

\(\lambda_{\max} = b/T \to T = b/\lambda_{\max}\) (\(b = 2.9 \times 10^{-3}\ \mathrm{m\,K}\)).

Dark-red hotplate, \(\lambda_{\max} = 4.0\ \mathrm{\mu m} = 4.0 \times 10^{-6}\ \mathrm{m}\):

$$
T = \frac{2.9 \times 10^{-3}}{4.0 \times 10^{-6}} = 725\ \mathrm{K}
$$

Direction check: longer \(\lambda_{\max}\) \(\to\) cooler body. Hotter = bluer (shorter \(\lambda_{\max}\)).

### Listing 5 — Photoelectric stopping voltage, worked example

\(E_{k,\max} = qV_{0} \to V_{0} = E_{k,\max}/q\) (\(q = e = 1.6 \times 10^{-19}\ \mathrm{C}\)).

Photoelectrons emitted with \(E_{k,\max} = 2.6 \times 10^{-19}\ \mathrm{J}\):

$$
V_{0} = \frac{2.6 \times 10^{-19}}{1.6 \times 10^{-19}} = 1.6\ \mathrm{V}
$$

The stopping voltage is just the maximum kinetic energy expressed in volts.

### Listing 6 — Time dilation, worked example

\(\gamma = 1/\sqrt{1 - v^{2}/c^{2}}\), \(t = \gamma t_{0}\).

Clock moving at \(v = 0.5c\) shows \(t_{0} = 5\ \mathrm{min}\) (proper time, on the moving clock):

$$
\gamma = \frac{1}{\sqrt{1 - 0.5^{2}}} = \frac{1}{\sqrt{0.75}} = 1.155
$$

$$
t = \gamma t_{0} = 1.155 \times 5 = 5.775\ \mathrm{min} \approx 5\ \mathrm{min}\ 46.5\ \mathrm{s} \quad \text{(stationary observer's elapsed time)}
$$

\(t_{0}\) (proper time) is the smaller value; the moving clock runs slow, so the observed interval \(t\) is larger.

### Listing 7 — Muon evidence (time dilation), worked example

\(\gamma = t/t_{0}\), \(v = c\sqrt{1 - 1/\gamma^{2}}\), half-life in Earth frame \(= \gamma t_{0}\).

Muon proper half-life \(t_{0} = 1.56\ \mathrm{\mu s}\). Earth frame: journey takes \(t = 6.5\ \mathrm{\mu s}\) while muons "age" \(t_{0}\)-equiv \(= 0.7\ \mathrm{\mu s}\).

Lorentz factor:

$$
\gamma = \frac{6.5}{0.7} = 9.29
$$

Speed from \(\gamma\):

$$
v = c\sqrt{1 - 1/9.29^{2}} = c\sqrt{1 - 0.0116} = 0.994c
$$

Muon half-life as measured from Earth:

$$
t = \gamma t_{0} = 9.29 \times 1.56 \times 10^{-6} = 1.4 \times 10^{-5}\ \mathrm{s} = 14\ \mathrm{\mu s}
$$

The stretched half-life is why far more muons reach the ground than their \(1.56\ \mathrm{\mu s}\) proper half-life would allow.

### Listing 8 — Extended-response skeleton: "justify that light is both wave and particle"

Q: Light shows both wave and particle behaviour. Using specific evidence, justify.

WAVE evidence:

- Diffraction — light spreads through gaps \(\approx\) wavelength; particles cannot bend around corners.
- Interference (Young's double slit): \(d \sin\theta = m\lambda\).
  - bright: path difference \(= m\lambda\) (constructive)
  - dark: path difference \(= (m - \tfrac{1}{2})\lambda\) (destructive)
  - a particle stream cannot cancel to darkness \(\to\) wave evidence.
- Polarisation (Malus: \(I = I_{\max}\cos^{2}\theta\)) only occurs for TRANSVERSE waves \(\to\) proves light is a transverse wave.

PARTICLE (photon) evidence — photoelectric effect:

- no time delay
- threshold frequency \(f_{0}\) exists
- \(E_{k,\max}\) depends on FREQUENCY, not intensity: \(E_{k,\max} = hf - W\)
- wave model explains only intensity\(\to\)number; photon model (1 photon \(\to\) 1 electron) explains all four.

CONCLUSION: same light is BOTH wave and particle \(\to\) wave–particle duality.

Weak (band-4): "It diffracts so it's a wave, and the photoelectric effect makes it a particle." — no specific evidence, no equations, no reasoning \(\to\) almost no marks.

### Listing 9 — Reading the photoelectric graph (E_k,max vs frequency)

Plot \(E_{k,\max}\) (\(y\)-axis) against \(f\) (\(x\)-axis) from \(E_{k,\max} = hf - W\):

- gradient \(= h\) (Planck's constant — SAME for every metal, so all metals' lines are PARALLEL)
- \(x\)-intercept \(= f_{0}\) (threshold frequency, where \(E_{k,\max} = 0\))
- \(y\)-intercept \(= -W\) (NEGATIVE of the work function)

At threshold: \(W = h f_{0}\).

Common errors:

- reading the gradient as \(W\) (it is \(h\))
- reading the \(y\)-intercept as \(+W\) or as \(f_{0}\) (it is \(-W\))
- confusing \(f_{0}\) (a frequency, Hz) with \(W\) (an energy, J or eV)

### Listing 10 — The "proper" distinctions, directions, and module traps
| Pair / rule | Get it right |
|-------------|--------------|
| Malus's law | \(I = I_{\max}\cos^{2}\theta\) (cosine **squared**); \(\theta =\) angle **between the two filter axes** |
| First filter on unpolarised light | \(I = \tfrac{1}{2}I_{0}\) (use one half, **not** Malus) |
| Threshold frequency vs work function | \(f_{0}\) is a frequency (Hz); \(W\) is an energy (J/eV); linked by \(W = hf_{0}\) |
| Intensity vs frequency | intensity = number of photons (more electrons); only frequency raises \(E_{k,\max}\) |
| Photoelectric graph | gradient \(= h\); \(x\)-intercept \(= f_{0}\); \(y\)-intercept \(= -W\) (negative) |
| Black body vs discharge tube | black body = **continuous** spectrum; discharge tube = **emission lines** |
| Wien direction | hotter \(\to\) shorter \(\lambda_{\max}\) (bluer); cooler \(\to\) longer \(\lambda_{\max}\) |
| Stellar lines: shift vs broadening | Doppler **shift** = radial velocity; **broadening** = rotation/density |
| Proper time t₀ | measured where the two events occur at the **same place** (clock's own frame); time **dilates** (\(t = \gamma t_{0}\), larger) |
| Proper length l₀ | measured in the object's **rest frame**; length **contracts** (\(l = l_{0}/\gamma\), smaller), only **along the direction of motion** |
| Lorentz factor | \(\gamma \ge 1\) **always**; if you get \(\gamma < 1\) the working is wrong |
| Mass cannot reach c | as \(v \to c\), \(\gamma \to \infty\) so required energy \(\to \infty\); never "infinitely fast", say "needs infinite energy" |
| EM waves & medium | EM waves need **no medium**; aether never detected (Michelson–Morley null result) |
| Source of EM waves | **accelerating/oscillating** charges radiate; steady DC current does **not** |

### Listing 11 — Diffraction grating, first-order angle, worked example

\(d = 1/(\text{lines per metre})\), \(d \sin\theta = m\lambda\).

Grating: 600 lines per mm.

$$
600\ \text{lines/mm} = 6.00 \times 10^{5}\ \text{lines/m}
$$

$$
d = \frac{1}{6.00 \times 10^{5}} = 1.67 \times 10^{-6}\ \mathrm{m}
$$

Light: \(\lambda = 650\ \mathrm{nm} = 6.50 \times 10^{-7}\ \mathrm{m}\), first order (\(m = 1\)):

$$
\sin\theta = \frac{m\lambda}{d} = \frac{6.50 \times 10^{-7}}{1.67 \times 10^{-6}} = 0.389
$$

$$
\theta = \sin^{-1}(0.389) = 22.9°
$$

Mark-earning steps: convert lines/mm \(\to\) spacing in metres; substitute; take \(\sin^{-1}\).

### Listing 12 — Length contraction (spacecraft), worked example

\(\gamma = 1/\sqrt{1 - v^{2}/c^{2}}\), \(l = l_{0}/\gamma = l_{0}\sqrt{1 - v^{2}/c^{2}}\).

Spacecraft: \(v = 0.80c\), proper length \(l_{0} = 100\ \mathrm{m}\).

Lorentz factor:

$$
\gamma = \frac{1}{\sqrt{1 - 0.8^{2}}} = \frac{1}{\sqrt{0.36}} = \frac{1}{0.6} = 1.667
$$

Contracted length (Earth observer):

$$
l = \frac{l_{0}}{\gamma} = \frac{100}{1.667} = 60\ \mathrm{m}
$$

Proper length \(= 100\ \mathrm{m}\) (measured in the spacecraft's own rest frame). Earth observer measures the contracted 60 m.

### Listing 13 — Module 7 reference data and mnemonics
| Quantity / list | Value or hook |
|-----------------|---------------|
| Speed of light c | 3.0 × 10^8 m s^-1 (exact 299 792 458 m s^-1) |
| Planck constant h | 6.63 × 10^-34 J s |
| Electron charge e | 1.6 × 10^-19 C (= 1 eV in joules) |
| Wien's constant b | 2.9 × 10^-3 m K |
| Permittivity ε₀ | 8.854 × 10^-12 F m^-1 |
| Permeability μ₀ | 4π × 10^-7 ≈ 1.257 × 10^-6 T m A^-1 |
| Electron rest mass | 9.11 × 10^-31 kg |
| Proton rest mass | 1.67 × 10^-27 kg |
| EM spectrum (rising frequency) | Radio, Microwave, Infrared, Visible, Ultraviolet, X-ray, Gamma → "Raging Martians Invaded Venus Using X-ray Guns" |
| Three spectrum types | Continuous, Emission, Absorption → "CEA": hot Coal, Excited gas, cool Atmosphere |
| Four stellar properties | Temperature, Composition, Velocity, Rotation → "The Cosmos Verifies Relativity" |
| Three wave-model pillars | Diffraction, Interference, Polarisation → "Don't Ignore Photons" |
| Four photoelectric observations | Number, Threshold, Energy, No-delay → "Newton's Theory Explodes Now" |
| Evidence → model map | diffraction/interference/polarisation → wave; black-body curve + photoelectric → quantum (photon); Michelson–Morley null + muons + atomic clocks → relativity |
