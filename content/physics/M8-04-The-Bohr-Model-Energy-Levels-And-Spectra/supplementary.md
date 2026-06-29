---
title: "Supplementary Materials — The Bohr Model: Energy Levels, Spectra, and the Photon"
module: M8
lesson: "04"
script: script.md
---

# Supplementary Materials

Key equations, derivations, worked numerical solutions, and reference data for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Worked Example A: the H-alpha (red Balmer) line, longest visible wavelength

Rydberg equation, with \(R_H = 1.097 \times 10^{7}\ \mathrm{m^{-1}}\):

$$
\frac{1}{\lambda} = R_H \left( \frac{1}{n_f^{2}} - \frac{1}{n_i^{2}} \right)
$$

Longest \(\lambda\) \(\Rightarrow\) smallest energy gap \(\Rightarrow\) smallest transition. Visible (Balmer) series lands on \(n_f = 2\), so smallest gap is \(n_i = 3 \to n_f = 2\).

$$
\begin{aligned}
\frac{1}{\lambda} &= 1.097 \times 10^{7} \times \left( \frac{1}{2^{2}} - \frac{1}{3^{2}} \right) \\
&= 1.097 \times 10^{7} \times \left( \frac{1}{4} - \frac{1}{9} \right) \\
&= 1.097 \times 10^{7} \times (0.2500 - 0.1111) \\
&= 1.097 \times 10^{7} \times 0.1389 \\
&= 1.524 \times 10^{6}\ \mathrm{m^{-1}}
\end{aligned}
$$

$$
\lambda = \frac{1}{1.524 \times 10^{6}} = 6.56 \times 10^{-7}\ \mathrm{m} = 656\ \mathrm{nm}\quad (\text{red H-alpha line})
$$

Trap: \(R_H\) is in \(\mathrm{m^{-1}}\), so the equation returns \(1/\lambda\). Always take the reciprocal to get \(\lambda\). An answer \(\sim 10^{6}\) is \(1/\lambda\), NOT a wavelength.

### Listing 2 — Worked Example B: the n = 4 → n = 1 photon (energy, frequency, wavelength)

Level energies, with \(E_1 = -13.6\ \mathrm{eV}\):

$$
E_n = \frac{E_1}{n^{2}}
$$

(a)

$$
E_4 = \frac{-13.6}{4^{2}} = \frac{-13.6}{16} = -0.85\ \mathrm{eV}
$$

(b) Photon energy (take the MAGNITUDE — subtracting the wrong way gives a meaningless negative frequency):

$$
|E_i - E_f| = |(-0.85) - (-13.6)| = 12.75\ \mathrm{eV}
$$

Convert to joules:

$$
12.75 \times 1.602 \times 10^{-19} = 2.04 \times 10^{-18}\ \mathrm{J}
$$

(c) Frequency, from \(E = hf\):

$$
f = \frac{E}{h} = \frac{2.04 \times 10^{-18}}{6.63 \times 10^{-34}} = 3.08 \times 10^{15}\ \mathrm{Hz}
$$

(d) Wavelength, from \(c = f\lambda\):

$$
\lambda = \frac{c}{f} = \frac{3.0 \times 10^{8}}{3.08 \times 10^{15}} = 9.7 \times 10^{-8}\ \mathrm{m} \approx 97\ \mathrm{nm}
$$

Lands on \(n = 1\) \(\Rightarrow\) Lyman series \(\Rightarrow\) ultraviolet. Self-check agrees: 97 nm is UV.

### Listing 3 — Hydrogen energy levels (electron volts)
| Level n | Energy E_n (eV) | Notes                          |
|---------|-----------------|--------------------------------|
| 1       | −13.6           | ground state (most bound)      |
| 2       | −3.4            | first excited state            |
| 3       | −1.51           |                                |
| 4       | −0.85           |                                |
| 5       | −0.54           |                                |
| 6       | −0.38           |                                |
| ∞       | 0               | ionisation (electron free)     |

### Listing 4 — Exam Question 4 worked: n = 2 → n = 1 photon

Given: \(E_2 = -3.4\ \mathrm{eV}\), \(E_1 = -13.6\ \mathrm{eV}\).

$$
\text{Photon energy} = |E_i - E_f| = |(-3.4) - (-13.6)| = 10.2\ \mathrm{eV}
$$

Convert:

$$
10.2 \times 1.602 \times 10^{-19} = 1.63 \times 10^{-18}\ \mathrm{J}
$$

Use \(E = hc/\lambda\) \(\to\) \(\lambda = hc/E\):

$$
\lambda = \frac{(6.63 \times 10^{-34})(3.0 \times 10^{8})}{1.63 \times 10^{-18}} = \frac{1.989 \times 10^{-25}}{1.63 \times 10^{-18}} = 1.22 \times 10^{-7}\ \mathrm{m} \approx 122\ \mathrm{nm}
$$

Lands on \(n = 1\) \(\Rightarrow\) Lyman series \(\Rightarrow\) ultraviolet.

### Listing 5 — Model extended-response answer (line emission spectrum of hydrogen)

"In the Bohr model the electron in a hydrogen atom can occupy only certain discrete stationary states, each with a fixed, quantised energy. When the atom is excited, the electron is raised to a higher stationary state. It then transitions back to a lower state, and in doing so the atom emits a single photon. By the law of conservation of energy, the photon's energy is exactly equal to the difference in energy between the two states — Planck's constant times the photon's frequency equals the higher energy minus the lower energy. Because the energy levels are discrete and unique to hydrogen, only photons of specific frequencies, and therefore specific wavelengths, can be emitted. These appear as a discrete set of bright lines — a line emission spectrum — rather than a continuous spectrum."

Weak (band-4) answer for contrast: "Electrons jump down and give off light." — states an observation with no mechanism, no quantisation, no conservation of energy: almost no marks.

### Listing 6 — Key equations and constants for transitions

Photon energy \(=\) Planck's constant \(\times\) frequency:

$$
E = hf
$$

Wave speed \(=\) frequency \(\times\) wavelength:

$$
c = f\lambda
$$

Photon energy \(= hc/\) wavelength:

$$
E = \frac{hc}{\lambda}
$$

Photon energy \(=\) magnitude of level difference:

$$
hf = E_i - E_f
$$

Rydberg equation (emission: \(n_f < n_i\)):

$$
\frac{1}{\lambda} = R_H \left( \frac{1}{n_f^{2}} - \frac{1}{n_i^{2}} \right)
$$

Hydrogen level energy, \(E_1 = -13.6\ \mathrm{eV}\):

$$
E_n = \frac{E_1}{n^{2}}
$$

Constants (HSC data sheet):

- \(h = 6.63 \times 10^{-34}\ \mathrm{J\cdot s}\) — Planck's constant
- \(c = 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\) — speed of light
- \(e = 1.602 \times 10^{-19}\ \mathrm{C}\) — elementary charge (\(= 1\ \mathrm{eV}\) in joules)
- \(1\ \mathrm{eV} = 1.602 \times 10^{-19}\ \mathrm{J}\) — electron-volt to joule conversion
- \(R_H = 1.097 \times 10^{7}\ \mathrm{m^{-1}}\) — Rydberg constant

### Listing 7 — Hydrogen spectral series ("Little Birds Pause")
| Series  | Falls to level | Region        | Mnemonic letter |
|---------|----------------|---------------|-----------------|
| Lyman   | n = 1          | ultraviolet   | Little (L)      |
| Balmer  | n = 2          | visible       | Birds (B)       |
| Paschen | n = 3          | infrared      | Pause (P)       |

### Listing 8 — Bohr model limitations ("Hydrogen Is My Sole Why")
| Letter | Limitation                                                              |
|--------|-------------------------------------------------------------------------|
| H      | Works for **H**ydrogen / one-electron systems only                      |
| I      | Cannot explain relative **I**ntensities of spectral lines               |
| M      | Cannot explain line splitting — fine structure and the **M**agnetic (Zeeman) effect |
| S      | Is a **S**ticky mixture of classical and quantum physics (inelegant)    |
| W      | Never explains **W**hy orbits are stable / non-radiating — only asserts it |
