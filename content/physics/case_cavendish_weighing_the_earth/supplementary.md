---
title: "Supplementary Materials — The Cavendish Experiment — Weighing the Earth"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — From the twisting wire to big G (the torsion-balance method)

**Set-up.** A horizontal rod of length \(L\) hangs from a thin wire at its midpoint. A small ball (mass \(m\)) sits at each end of the rod. A large ball (mass \(M\)) is brought close to each small ball. The centre-to-centre separation of a large/small pair is \(r\).

**Step 1 — Find the wire's stiffness (torsion constant, \(\kappa\)) by timing the swing.** The hanging rod is a torsional oscillator with period \(T\):

$$
T = 2\pi \sqrt{\frac{I}{\kappa}}
$$

The moment of inertia of two small balls on the rod (each at \(L/2\) from the axis):

$$
I = 2 m \left(\frac{L}{2}\right)^{2} = \frac{m L^{2}}{2}
$$

Rearrange the period equation for the torsion constant:

$$
\kappa = \frac{4\pi^{2} I}{T^{2}} = \frac{2\pi^{2} m L^{2}}{T^{2}}
$$

(Timing the oscillation gives \(\kappa\) WITHOUT applying any known force.)

**Step 2 — At rest, gravitational torque balances the wire's restoring torque.** The gravitational force on each small ball:

$$
F = \frac{G M m}{r^{2}}
$$

This force acts at each end of the rod (lever arm \(L/2\)), on both ends:

$$
\text{gravitational torque} = 2 F \left(\frac{L}{2}\right) = F L
$$

The restoring torque of the twisted wire (twist angle \(\theta\), in radians) is \(\kappa\,\theta\). At equilibrium the two are equal:

$$
F L = \kappa\,\theta
$$

**Step 3 — Solve for big G.** Substitute \(F = G M m / r^{2}\) and \(\kappa = 2\pi^{2} m L^{2} / T^{2}\):

$$
\frac{G M m}{r^{2}}\, L = \frac{2\pi^{2} m L^{2}}{T^{2}}\,\theta
$$

The small-ball mass \(m\) cancels. Rearranging:

$$
G = \frac{2\pi^{2} L\, r^{2}\, \theta}{M T^{2}}
$$

where:

- \(L\) — rod length
- \(r\) — centre-to-centre separation of a large/small ball pair
- \(\theta\) — equilibrium twist angle (radians)
- \(M\) — large-ball mass
- \(T\) — oscillation period of the balance

### Listing 2 — Worked example: weighing the Earth from big G

**Goal:** find the mass of the Earth once big G is known.

At the Earth's surface, the gravitational field strength is \(g\). The gravitational field strength of a planet (Newton's law with one unit mass) is:

$$
g = \frac{G M_{\text{Earth}}}{R_{\text{Earth}}^{2}}
$$

Note: \(g\ (\mathrm{N\,kg^{-1}})\) is numerically equal to the acceleration due to gravity \((\mathrm{m\,s^{-2}})\). Rearrange for the mass of the Earth:

$$
M_{\text{Earth}} = \frac{g\, R_{\text{Earth}}^{2}}{G}
$$

Substitute (modern values) \(g = 9.81\ \mathrm{N\,kg^{-1}}\), \(R_{\text{Earth}} = 6.371\times 10^{6}\ \mathrm{m}\), \(G = 6.674\times 10^{-11}\ \mathrm{m^{3}\,kg^{-1}\,s^{-2}}\):

$$
\begin{aligned}
M_{\text{Earth}} &= \frac{9.81 \cdot (6.371\times 10^{6})^{2}}{6.674\times 10^{-11}} \\
&= \frac{9.81 \cdot 4.059\times 10^{13}}{6.674\times 10^{-11}} \\
&= \frac{3.982\times 10^{14}}{6.674\times 10^{-11}} \\
&= 5.97\times 10^{24}\ \mathrm{kg}
\end{aligned}
$$

(Using the rounded HSC data-sheet values \(g = 9.8\ \mathrm{N\,kg^{-1}}\), \(R = 6.371\times 10^{6}\ \mathrm{m}\), \(G = 6.67\times 10^{-11}\), this gives \(M_{\text{Earth}} = 5.96\times 10^{24}\ \mathrm{kg}\), which the data sheet itself rounds to \(6.0\times 10^{24}\ \mathrm{kg}\).)

**Cross-check via density:**

$$
\begin{aligned}
\rho_{\text{Earth}} &= \frac{M_{\text{Earth}}}{\frac{4}{3}\pi R_{\text{Earth}}^{3}} \\
&= \frac{5.97\times 10^{24}}{\frac{4}{3}\pi (6.371\times 10^{6})^{3}} \\
&= 5.51\times 10^{3}\ \mathrm{kg\,m^{-3}} = 5.51\ \mathrm{g/cm^{3}}
\end{aligned}
$$

(i.e. \(\approx 5.5\) times the density of water — confirming a dense metallic core)

### Listing 3 — The apparatus (Cavendish, 1797–98)

| Component | Value |
|-----------|-------|
| Torsion rod (beam) length | 1.8 m (6 feet) |
| Small lead spheres (one each end) | 0.73 kg each, 51 mm (2 in) diameter |
| Large lead spheres (two) | 158 kg each, 300 mm (12 in) diameter |
| Centre-to-centre separation (large–small) | 0.225 m (8.85 in) |
| Housing case (mahogany) | ~1.98 m wide, sealed against air currents |
| Measured gravitational force per pair | ~1.7 x 10^-7 N (order of ~10^-7 N, a few hundred nN) |
| Oscillation period (initial wire) | ~15 minutes per full swing |
| Oscillation period (stiffened wire) | ~7.5 minutes per full swing |
| Number of trials | 17 |
| Read-out | telescopes through the shed wall; ropes/pulleys to move large spheres |

**Note on the force figure.** A naive point-mass calculation, \(F = G M m / r^{2}\), with \(M = 158\ \mathrm{kg}\), \(m = 0.73\ \mathrm{kg}\) and \(r = 0.225\ \mathrm{m}\) gives \(F \approx 1.5\times 10^{-7}\ \mathrm{N}\) (\(\approx 150\ \mathrm{nN}\)). The commonly quoted \(\approx 1.7\times 10^{-7}\ \mathrm{N}\) reflects the true geometry of the swinging rod and the fact that BOTH large spheres act on the beam at once. Either way the force is of order \(10^{-7}\ \mathrm{N}\) — roughly the weight of a grain of fine sand — which is the point of the story: an astonishingly tiny force.

### Listing 4 — Key results, then and now

| Quantity | Cavendish (1798) | Modern accepted |
|----------|------------------|-----------------|
| Density of Earth (published) | 5.480 g/cm^3 | — |
| Density of Earth (Baily's 1821 correction) | 5.448 g/cm^3 | 5.514 g/cm^3 |
| Accuracy vs modern | within ~1.2% | — |
| Big G (implied) | ~6.74 x 10^-11 | 6.67430(15) x 10^-11 |
| Mass of Earth (derived) | ~5.9 x 10^24 kg | 5.97 x 10^24 kg |

Note: Cavendish's paper was titled *Experiments to Determine the Density of the Earth*. It contains no value for big G and does not use the symbol G — that framing came later (C.V. Boys, 1889). The symbol G entered common use around 1873.

### Listing 5 — Why big G is the least-precisely-known constant

| Constant | Relative uncertainty (approx.) |
|----------|--------------------------------|
| Speed of light, c | exact (defined) |
| Planck's constant, h | exact (defined since 2019 SI) |
| Fine structure constant | ~0.15 parts per million |
| Gravitational constant, G | ~22 parts per million |

**Why G is so hard:**

- Gravity is by far the weakest fundamental force.
- There is NO way to shield against gravity (unlike electric/magnetic fields).
- Lab measurements are perturbed by the masses of walls, the experimenter, groundwater, distant terrain — none of which can be switched off.
- Since ~1990, high-precision experiments disagree with each other by far more than their stated error bars (up to ~0.05%), implying hidden systematic errors.
- Determining G to high precision remains an open problem in metrology.

### Listing 6 — The relevant HSC equations (Module 5)

Newton's law of universal gravitation (force between two masses):

$$
F = \frac{G M m}{r^{2}}
$$

- \(F\) is proportional to each mass; inverse-square in separation \(r\).
- \(r\) is measured centre-to-centre.

Gravitational field strength of a planet (force per unit mass):

$$
g = \frac{G M}{r^{2}}
$$

- Independent of the test mass placed in the field.
- Numerically, \(g\ (\mathrm{N\,kg^{-1}}) =\) acceleration due to gravity \((\mathrm{m\,s^{-2}})\).
- At the surface \(r = R\); at altitude \(h\) use \(r = R + h\):

$$
g = \frac{G M}{(R + h)^{2}}
$$

- A radial field approximates a UNIFORM field close to the surface (over a small region \(g\) is nearly constant in size and direction).

Mass of a planet from its surface field:

$$
M = \frac{g R^{2}}{G}
$$

**Official HSC data-sheet values (2019 onwards):**

- \(G = 6.67\times 10^{-11}\ \mathrm{N\,m^{2}\,kg^{-2}}\ (= \mathrm{m^{3}\,kg^{-1}\,s^{-2}})\)
- \(M_{\text{Earth}} = 6.0\times 10^{24}\ \mathrm{kg}\)
- \(R_{\text{Earth}} = 6.371\times 10^{6}\ \mathrm{m}\)
- \(g\) (surface) \(= 9.8\ \mathrm{m\,s^{-2}}\ (= 9.8\ \mathrm{N\,kg^{-1}})\)
- density of water \(= 1.00\times 10^{3}\ \mathrm{kg\,m^{-3}}\)

(The Jacaranda textbook quotes the more precise \(M_{\text{Earth}} = 5.97\times 10^{24}\ \mathrm{kg}\) and \(R_{\text{Earth}} = 6.37\times 10^{6}\ \mathrm{m}\); the data sheet rounds these for exam use.)
