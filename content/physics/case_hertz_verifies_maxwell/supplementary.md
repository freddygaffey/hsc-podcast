---
title: "Supplementary Materials — The Hertz Experiment — Proving Maxwell Right"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Maxwell's speed of an electromagnetic wave

$$
v = \frac{1}{\sqrt{\mu_{0}\,\epsilon_{0}}}
$$

where (values and units as given in Jacaranda Physics 12):

- \(\mu_{0}\) — permeability of free space \(= 4\pi\times 10^{-7}\ \mathrm{m\,kg\,C^{-2}}\)
- \(\epsilon_{0}\) — permittivity of free space \(= 8.854\times 10^{-12}\ \mathrm{C^{2}\,s^{2}\,kg^{-1}\,m^{-3}}\)

Substitute:

$$
\begin{aligned}
v &= \frac{1}{\sqrt{(4\pi\times 10^{-7}) \cdot (8.854\times 10^{-12})}} \\
&= \frac{1}{\sqrt{1.1126\times 10^{-17}}} \\
&= \frac{1}{3.3356\times 10^{-9}} \\
&= 2.998\times 10^{8}\ \mathrm{m/s} \quad \text{(rounded to } 3.0\times 10^{8}\ \mathrm{m/s}\text{)}
\end{aligned}
$$

The exact accepted value of \(c = 299\,792\,458\ \mathrm{m/s}\).

This matched the measured speed of light, leading Maxwell to conclude that light IS an electromagnetic wave, and that other (invisible) frequencies of EM wave must also exist.

With the less precise constants available in the 1860s, Maxwell's own figure came out near \({\sim}3.1\times 10^{8}\ \mathrm{m/s}\), within \({\sim}1\text{–}3\%\) of the best measured speed of light of the day (\({\sim}3.0\times 10^{8}\ \mathrm{m/s}\)) — close enough that he judged it could not be a coincidence.

### Listing 2 — The universal wave equation (how Hertz got the speed)

$$
v = f \lambda
$$

where:

- \(v\) — wave speed (m/s)
- \(f\) — frequency (Hz)
- \(\lambda\) — wavelength (m)

Hertz's method:

- \(\lambda\) \(\to\) measured directly from standing-wave node spacing
- \(f\) \(\to\) calculated from the oscillator's L–C resonant frequency
- \(v\) \(\to\) \(f \lambda \approx 3\times 10^{8}\ \mathrm{m/s}\) (the speed of light)

### Listing 3 — Standing wave from a reflector (node spacing)

A transmitted wave plus its reflection off a metal sheet superimpose to form a STANDING wave:

$$
\text{distance between adjacent nodes} = \frac{\lambda}{2}, \qquad \text{distance between adjacent antinodes} = \frac{\lambda}{2}
$$

Hertz measured node-to-node spacing of about 2 m:

$$
\frac{\lambda}{2} = 2\ \mathrm{m} \quad\Rightarrow\quad \lambda = 4\ \mathrm{m}
$$

Detector loop:

- at a NODE \(\to\) fields cancel \(\to\) spark vanishes
- at an ANTINODE \(\to\) fields add \(\to\) spark is brightest

### Listing 4 — Resonant frequency of the spark-gap oscillator

$$
f = \frac{1}{2\pi \sqrt{L C}}
$$

where:

- \(L\) — inductance of the 2 m copper dipole (set by its geometry)
- \(C\) — capacitance of the rods + zinc end-spheres

Hertz could NOT measure \(f\) directly with any instrument of the day. He CALCULATED it from \(L\) and \(C\), getting roughly 50–100 MHz (VHF band — similar to modern television frequencies).

Check: \(\lambda = c / f\). If \(f \sim 75\ \mathrm{MHz}\):

$$
\lambda = \frac{3\times 10^{8}}{75\times 10^{6}} = 4\ \mathrm{m}
$$

consistent with the measured standing-wave value.

### Listing 5 — Hertz's apparatus: key numbers

| Component | Specification |
|-----------|---------------|
| Transmitter rods | two copper rods, ~1 m each (2 m total dipole) |
| Spark gap (transmitter) | ~7.5 mm |
| End spheres (capacitive load) | zinc, ~30 cm diameter |
| Power source | Ruhmkorff induction coil, ~30 kV |
| Oscillation frequency | ~50-100 MHz (calculated, not measured) |
| Receiver | copper wire loop with adjustable micrometer gap |
| Receiver spark size | "scarcely a hundredth of a millimetre", ~10^-6 s |
| Reflector plate | zinc sheet, ~12 m from transmitter |
| Measured wavelength | ~4 m |
| Measured speed | ~3 x 10^8 m/s (the speed of light) |

### Listing 6 — Worked example: speed of an EM wave from standing waves

**Problem:** A spark-gap oscillator radiates waves at frequency \(f = 75\ \mathrm{MHz}\). A reflector produces standing waves; a detector loop finds the distance between adjacent nodes is 2.0 m. Find the wavelength and the wave speed.

**Step 1 — wavelength from node spacing:**

$$
\text{node spacing} = \frac{\lambda}{2} \quad\Rightarrow\quad 2.0 = \frac{\lambda}{2} \quad\Rightarrow\quad \lambda = 4.0\ \mathrm{m}
$$

**Step 2 — wave speed from \(v = f \lambda\):**

$$
f = 75\ \mathrm{MHz} = 75\times 10^{6}\ \mathrm{Hz}
$$

$$
v = f \lambda = (75\times 10^{6}) \cdot (4.0) = 3.0\times 10^{8}\ \mathrm{m/s}
$$

**Result:** \(v = 3.0\times 10^{8}\ \mathrm{m/s} \to\) the speed of light. This is how Hertz confirmed Maxwell's predicted speed.

### Listing 7 — The electromagnetic spectrum Maxwell's theory predicted

Maxwell's equations allow EM waves of ANY frequency. ALL travel at the same speed \(c = 3.0\times 10^{8}\ \mathrm{m/s}\) in a vacuum; they differ only in frequency \(f\) and wavelength \(\lambda\) (\(c = f \lambda\)).

Order from SHORTEST wavelength (highest \(f\), highest energy) to LONGEST wavelength (lowest \(f\), lowest energy):

$$
\text{gamma rays} \to \text{X-rays} \to \text{ultraviolet} \to \text{visible light} \to \text{infrared} \to \text{microwaves} \to \text{radio waves}
$$

In Maxwell's day (1860s) only VISIBLE LIGHT and INFRARED had been observed. The rest were predicted by the theory, then found later — Hertz's radio waves (1887) being the first deliberately produced.

| Property | Across the spectrum |
|----------|---------------------|
| Speed in vacuum | constant, \(c = 3.0\times 10^{8}\ \mathrm{m/s}\) (same for all) |
| Distinguishing quantities | frequency \(f\) and wavelength \(\lambda\) |
| Relation | \(c = f\lambda\) (so higher \(f\) means shorter \(\lambda\)) |
| Energy trend | shorter wavelength carries more energy per wave |
| Nature | transverse; E field perpendicular to B field, both perpendicular to direction of travel |

### Listing 8 — Syllabus checklist: where each dot-point is addressed (M7, Nature of light)

| NESA dot-point (Electromagnetic waves) | Covered in episode |
|----------------------------------------|--------------------|
| All EM radiation has constant speed c in a vacuum | Named EM spectrum; "the one speed, c, in a vacuum" |
| Explain how EM waves are produced and propagated | Accelerating/oscillating charge radiates; self-sustaining E and B fields regenerate each other |
| Maxwell: unification of electricity and magnetism | Maxwell's four equations unify the phenomena |
| Maxwell: prediction of electromagnetic waves | Displacement current term -> self-propagating wave |
| Maxwell: prediction of velocity | \(v = 1/\sqrt{\mu_{0}\epsilon_{0}}\) → matches speed of light |
| Historical prediction of c from permittivity and permeability | Listing 1; constants measured in "jars and coils" |
| Spark-gap oscillator and loop antenna verified the speed (Hertz) | Transmitter, receiver, standing-wave method, \(v = f\lambda\) |
| Reflection, refraction, diffraction, polarisation = same as light | Hertz reproduced every property of light |
