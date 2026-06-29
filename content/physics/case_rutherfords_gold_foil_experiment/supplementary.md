---
title: "Supplementary Materials — Rutherford's Gold Foil Experiment"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — The Rutherford scattering formula

$$
\frac{d\sigma}{d\Omega} = \left(\frac{Z_1 Z_2 e^{2}}{4 E_k}\right)^{2} \csc^{4}\!\left(\frac{\theta}{2}\right)
$$

where:

- \(\dfrac{d\sigma}{d\Omega}\) = differential scattering cross-section (scattering probability per solid angle)
- \(Z_1\) = charge number of the alpha particle \(= 2\)
- \(Z_2\) = charge number of the target nucleus (gold \(\approx 79\))
- \(e\) = elementary charge \(= 1.602\times10^{-19}\ \mathrm{C}\)
- \(E_k\) = kinetic energy of the incoming alpha particle
- \(\theta\) = scattering angle (\(0^{\circ}\) = straight through, \(180^{\circ}\) = straight back)

Key behaviour:

- \(\csc^{4}(\theta/2)\) is very large for small \(\theta\) \(\to\) most particles barely deflect
- \(\csc^{4}(\theta/2)\) is small but NON-ZERO at large \(\theta\) \(\to\) rare large-angle backscatter

### Listing 2 — The four predictions confirmed by Geiger & Marsden (1912–1913)

The number of particles scattered at angle \(\theta\) is:

1. proportional to \(\csc^{4}(\theta/2)\) (the angular dependence)
2. proportional to foil thickness (linear in thickness)
3. proportional to \((\text{nuclear charge})^{2}\) (proportional to \(Z_2^{2}\))
4. inversely proportional to \(v^{4}\) (\(1/\text{particle velocity}\), fourth power)

All four were verified experimentally \(\to\) strong confirmation of the nuclear model.

### Listing 3 — Coulomb repulsion and the head-on "distance of closest approach"

At a head-on collision the alpha particle is momentarily stopped. All its kinetic energy has converted to electric potential energy:

$$
E_k = \frac{k (Z_1 e)(Z_2 e)}{r_{\min}}
$$

Rearranged for the distance of closest approach:

$$
r_{\min} = \frac{k Z_1 Z_2 e^{2}}{E_k}
$$

where:

- \(k\) = Coulomb constant \(= 8.99\times10^{9}\ \mathrm{N\,m^{2}\,C^{-2}}\)
- \(Z_1 = 2\) (alpha)
- \(Z_2 = 79\) (gold)
- \(E_k\) = alpha kinetic energy \(\approx 7.7\ \mathrm{MeV} = 7.7\times10^{6}\times1.602\times10^{-19}\ \mathrm{J}\)

This \(r_{\min}\) sets an UPPER LIMIT on the nuclear radius (\(\approx 3\times10^{-14}\ \mathrm{m}\) for gold, i.e. \(\approx 30\ \mathrm{fm}\); see the worked calculation in Listing 4), because the alpha clearly never penetrates inside the nucleus.

### Listing 4 — Worked example: distance of closest approach for an alpha on gold

GIVEN:

- \(Z_1 = 2\), \(Z_2 = 79\)
- \(e = 1.602\times10^{-19}\ \mathrm{C}\)
- \(k = 8.99\times10^{9}\ \mathrm{N\,m^{2}\,C^{-2}}\)
- \(E_k = 7.7\ \mathrm{MeV} = 7.7\times10^{6}\times1.602\times10^{-19}\ \mathrm{J} = 1.233\times10^{-12}\ \mathrm{J}\)

STEP 1 — numerator \(k Z_1 Z_2 e^{2}\):

$$
e^{2} = (1.602\times10^{-19})^{2} = 2.566\times10^{-38}\ \mathrm{C^{2}}
$$

$$
Z_1 Z_2 = 2\times79 = 158
$$

$$
k Z_1 Z_2 e^{2} = 8.99\times10^{9}\times158\times2.566\times10^{-38} = 3.645\times10^{-26}\ \mathrm{N\,m^{2}}
$$

STEP 2 — divide by \(E_k\):

$$
r_{\min} = \frac{3.645\times10^{-26}}{1.233\times10^{-12}} = 2.96\times10^{-14}\ \mathrm{m} \approx 3\times10^{-14}\ \mathrm{m}\ (\approx 30\ \text{femtometres})
$$

INTERPRETATION: the gold nucleus must be SMALLER than \(\approx 3\times10^{-14}\ \mathrm{m}\) (this \(r_{\min}\) is an UPPER LIMIT, not the true nuclear radius — the alpha never quite reaches the nuclear surface). Compare to the atomic radius \(\approx 1.44\times10^{-10}\ \mathrm{m}\). Even using the upper-limit \(r_{\min}\), the atom is \(\approx 5000\times\) larger than the nucleus; using the true nuclear radius the ratio is at least \(10{,}000{:}1\) \(\to\) atom is mostly empty space.

### Listing 5 — Key numbers from the experiment

| Quantity | Value |
|----------|-------|
| Gold foil thickness | ≈ 100 nm (≈ 0.000004 cm, ~1000 atoms thick) |
| Alpha particle charge | +2e |
| Alpha particle mass | ≈ 4 atomic mass units |
| Alpha particle energy (radium C) | ≈ 7.7 MeV |
| Alpha particle speed | ≈ 1.6 × 10^7 m/s (~5% of c) |
| Deflected > 90° (gold foil, Geiger–Marsden) | ≈ 1 in 8,000 |
| Fraction passing nearly straight through | > 99.9% |
| Nucleus holds fraction of atom's mass | ≈ 99.9% |
| Atomic radius (order of magnitude) | ≈ 1.44 × 10^-10 m |
| Nuclear radius (upper limit, Rutherford) | ≈ 10^-14 m (10 fm) |
| Gold nuclear charge (modern, Z) | 79 (Rutherford estimated ~100) |
| Atom : nucleus size ratio | ≥ 10,000 : 1 |

### Listing 6 — Plum pudding model vs nuclear model

| Feature | Thomson plum pudding (1904) | Rutherford nuclear (1911) |
|---------|-----------------------------|----------------------------|
| Positive charge | spread evenly through whole atom | concentrated in tiny central nucleus |
| Mass distribution | spread evenly through whole atom | almost all in the nucleus |
| Electrons | embedded throughout positive sphere | out in surrounding (mostly empty) space |
| Predicted large-angle scattering | effectively impossible | rare but expected (single close encounter) |
| Explains backscatter? | No | Yes |
| Known weakness | wrong charge distribution | orbiting electrons should radiate and collapse (fixed by Bohr, 1913) |
