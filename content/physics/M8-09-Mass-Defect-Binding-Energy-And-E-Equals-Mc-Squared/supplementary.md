---
title: "Supplementary Materials — Mass Defect, Binding Energy, and E = mc^2"
module: M8
lesson: "09"
script: script.md
---

# Supplementary Materials

Worked nuclear-energy calculations for this episode. Nothing here is spoken in the audio — it is the read-along reference. Symbols: \(u\) = atomic mass unit; \(\Delta m\) = mass defect; \(E_b\) = binding energy; \(A\) = mass number (number of nucleons); \(c\) = speed of light. Key conversion: \(1\ \mathrm{u} \leftrightarrow 931.5\ \mathrm{MeV}\) (the data sheet writes it as \(931.5\ \mathrm{MeV}/c^{2}\) — the \(c^{2}\) is already built into the factor, so multiply by 931.5 and STOP).

### Listing 1 — Binding energy of helium-4 (the canonical worked example)

Goal: total binding energy and binding energy per nucleon of helium-4 (2 p, 2 n).

**Step 1 — mass of the separate constituents (atomic-mass bookkeeping).** Use atomic masses and include 2 electrons; these cancel against the 2 electrons already inside the helium-4 ATOMIC mass, so the nuclear result is unaffected.

$$
2 \times (\text{proton} + \text{neutron} + \text{electron}) = 2 \times (1.007276 + 1.008665 + 0.000549)
$$

$$
= 2 \times 2.016490 = 4.032980\ \mathrm{u}
$$

(Equivalently: \(2 \times \text{H-1 atom} + 2 \times \text{neutron} = 2(1.007825) + 2(1.008665) = 4.032980\ \mathrm{u}\).)

**Step 2 — mass defect.** The helium-4 atomic mass is \(4.002603\ \mathrm{u}\):

$$
\Delta m = 4.032980 - 4.002603 = 0.030377\ \mathrm{u} \quad (\approx 0.0304\ \mathrm{u};\ \sim 0.75\%\ \text{of the nucleus})
$$

**Step 3 — total binding energy (fast way, via 931.5).**

$$
E_b = \Delta m \times 931.5 = 0.030377 \times 931.5 = 28.30\ \mathrm{MeV}
$$

⚠ DO NOT also divide by \(c^{2}\): the "per \(c^{2}\)" is already in the 931.5 factor.

Cross-check (long way, via kilograms and \(E = mc^{2}\)):

$$
\Delta m = 0.030377 \times 1.661 \times 10^{-27} = 5.046 \times 10^{-29}\ \mathrm{kg}
$$

$$
E_b = \Delta m\, c^{2} = (5.046 \times 10^{-29})(3.0 \times 10^{8})^{2} = 4.54 \times 10^{-12}\ \mathrm{J}
$$

$$
\text{In MeV:}\quad 4.54 \times 10^{-12} \div 1.602 \times 10^{-13} = 28.3\ \mathrm{MeV} \quad \checkmark\ (\text{agrees})
$$

**Step 4 — binding energy per nucleon.**

$$
E_b / A = 28.30 / 4 = 7.07\ \mathrm{MeV\ per\ nucleon}
$$

(Landmark value: helium-4 is unusually tightly bound for so light a nucleus.)

### Listing 2 — Masses and constants (data sheet / atomic-mass tables)
| Quantity | Symbol | Value |
|----------|--------|-------|
| Atomic mass unit | 1 u | 1.661 × 10⁻²⁷ kg ↔ 931.5 MeV/c² |
| Proton mass | m_p | 1.007276 u |
| Neutron mass | m_n | 1.008665 u |
| Electron mass | m_e | 0.000549 u |
| Hydrogen-1 (atom) | ¹H | 1.007825 u |
| Deuterium, H-2 (atom) | ²H | 2.014102 u |
| Tritium, H-3 (atom) | ³H | 3.016049 u |
| Helium-4 (atom) | ⁴He | 4.002603 u |
| Speed of light | c | 3.0 × 10⁸ m s⁻¹ (c² ≈ 9.0 × 10¹⁶) |
| MeV → joules | 1 MeV | 1.602 × 10⁻¹³ J |
| Iron-56 peak | — | ≈ 8.8 MeV per nucleon (most stable nucleus) |

### Listing 3 — Deuterium–tritium fusion (≈ 17.6 MeV)

Reaction:

$$
{}^{2}\mathrm{H}\ (\text{deuterium}) + {}^{3}\mathrm{H}\ (\text{tritium}) \to {}^{4}\mathrm{He} + n + \text{energy}
$$

(Electrons balance: \(1 + 1\) on the left, \(2 + 0\) on the right — atomic masses work directly.)

Mass of reactants:

$$
{}^{2}\mathrm{H} + {}^{3}\mathrm{H} = 2.014102 + 3.016049 = 5.030151\ \mathrm{u}
$$

Mass of products:

$$
{}^{4}\mathrm{He} + n = 4.002603 + 1.008665 = 5.011268\ \mathrm{u}
$$

Mass lost:

$$
\Delta m = 5.030151 - 5.011268 = 0.018883\ \mathrm{u} \quad (\approx 0.0189\ \mathrm{u})
$$

Energy released:

$$
E = \Delta m \times 931.5 = 0.018883 \times 931.5 \approx 17.6\ \mathrm{MeV}\ \text{per reaction}
$$

Consistent with the curve: \({}^{4}\mathrm{He}\) sits high on the binding-energy-per-nucleon curve, so forming it from lighter nuclei releases energy. (Per unit mass, fusion beats fission.)

### Listing 4 — Uranium-236 fission, two methods agree (≈ 160 MeV)

Reaction:

$$
{}^{236}\mathrm{U} \to {}^{148}\mathrm{La} + {}^{85}\mathrm{Br} + 3n + \text{energy}
$$

(Check: \(A = 148 + 85 + 3 = 236\ \checkmark\);  \(Z = 57 + 35 = 92\ \checkmark\))

**Method A — binding-energy method** \(\left(E_{\text{released}} = \Sigma\,\mathrm{BE}(\text{products}) - \mathrm{BE}(\text{reactant})\right)\):

- \(\mathrm{BE}(\text{U-236}) = 1790.415\ \mathrm{MeV}\)
- \(\mathrm{BE}(\text{La-148}) = 1213.125\ \mathrm{MeV}\)
- \(\mathrm{BE}(\text{Br-85}) = 737.291\ \mathrm{MeV}\)

$$
\Sigma\,\mathrm{BE}(\text{fragments}) = 1213.125 + 737.291 = 1950.416\ \mathrm{MeV}
$$

$$
E_{\text{released}} = 1950.416 - 1790.415 = 160.0\ \mathrm{MeV}
$$

**Method B — mass-difference method** \(\left(E_{\text{released}} = \Delta m\, c^{2}\right)\):

- \(\text{Mass}(\text{U-236}) = 3.919629 \times 10^{-25}\ \mathrm{kg}\)
- \(\text{Mass}(\text{La-148}) = 2.456472 \times 10^{-25}\ \mathrm{kg}\)
- \(\text{Mass}(\text{Br-85}) = 1.410057 \times 10^{-25}\ \mathrm{kg}\)
- \(\text{Mass}(n) = 1.674924 \times 10^{-27}\ \mathrm{kg}\)

$$
\Sigma\,\text{mass}(\text{products}) = 2.456472 \times 10^{-25} + 1.410057 \times 10^{-25} + 3(1.674924 \times 10^{-27}) = 3.916777 \times 10^{-25}\ \mathrm{kg}
$$

$$
\Delta m = 3.919629 \times 10^{-25} - 3.916777 \times 10^{-25} = 2.852 \times 10^{-28}\ \mathrm{kg}
$$

$$
E = \Delta m\, c^{2} = (2.852 \times 10^{-28})(2.998 \times 10^{8})^{2} = 2.563 \times 10^{-11}\ \mathrm{J}
$$

$$
= 2.563 \times 10^{-11} \div 1.602 \times 10^{-13} = 160.0\ \mathrm{MeV}
$$

BOTH METHODS \(\approx 160\ \mathrm{MeV}\) (agree to within rounding) — more binding energy in the products is the same physics as less mass in the products. A uranium fission releases \(\sim 10\times\) the energy of one D-T fusion (far more nucleons), but far less per unit mass.
