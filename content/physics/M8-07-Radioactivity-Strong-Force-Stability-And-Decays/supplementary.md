---
title: "Supplementary Materials — Radioactivity: The Strong Force, Nuclear Stability, and the Three Decays"
module: M8
lesson: "07"
script: script.md
---

# Supplementary Materials

Key equations, decay bookkeeping, worked numerical solutions, and reference data for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Alpha decay of uranium-238: balanced equation and energy released

Equation:

$$
{}^{238}_{92}\mathrm{U} \to {}^{234}_{90}\mathrm{Th} + {}^{4}_{2}\mathrm{He} + \text{energy}
$$

Conservation check:

- mass number \(A\): \(238 = 234 + 4\) ✓
- atomic number \(Z\): \(92 = 90 + 2\) ✓ (\(Z = 90\) is thorium)

Masses (atomic mass units, u):

- \(m\big({}^{238}_{92}\mathrm{U}\big) = 238.05079\ \mathrm{u}\)
- \(m\big({}^{234}_{90}\mathrm{Th}\big) = 234.04363\ \mathrm{u}\)
- \(m\big({}^{4}_{2}\mathrm{He}\big) = 4.00260\ \mathrm{u}\)

Mass of products:

$$
234.04363 + 4.00260 = 238.04623\ \mathrm{u}
$$

Mass defect (mass lost):

$$
\Delta m = 238.05079 - 238.04623 = 0.00456\ \mathrm{u}
$$

Energy released (using \(1\ \mathrm{u} \leftrightarrow 931.5\ \mathrm{MeV}\)):

$$
E = \Delta m \times 931.5 = 0.00456 \times 931.5 \approx 4.25\ \mathrm{MeV}
$$

(released as kinetic energy of the alpha particle and the recoiling Th nucleus)

Note: the quoted masses are ATOMIC masses (electrons included). In alpha decay the electron counts cancel, so no correction is needed.

### Listing 2 — Beta-minus decay energy: lead-210 → bismuth-210 (electron masses must be tracked)

Equation:

$$
{}^{210}_{82}\mathrm{Pb} \to {}^{210}_{83}\mathrm{Bi} + {}^{0}_{-1}e + \bar{\nu} + \text{energy}
$$

Atomic masses (u):

- \(m(\text{Pb-210, atomic}) = 209.98419\ \mathrm{u}\)
- \(m(\text{Bi-210, atomic}) = 209.98412\ \mathrm{u}\)
- \(m(\text{electron}) = 0.00055\ \mathrm{u}\)

Because these are ATOMIC masses, in beta decay the electron counts do NOT fully cancel (\(Z\) changes by 1), so track them:

$$
\text{Initial nuclear mass} = 209.98419 - 82(0.00055) = 209.93909\ \mathrm{u}
$$

$$
\begin{aligned}
\text{Final mass} &= [\text{Bi-210 nuclear mass}] + \text{emitted electron} \\
&= (209.98412 - 83 \times 0.00055) + 0.00055 \\
&= 209.98412 - 82 \times 0.00055 \\
&= 209.93902\ \mathrm{u}
\end{aligned}
$$

Mass lost:

$$
\Delta m = 209.93909 - 209.93902 = 0.00007\ \mathrm{u}
$$

Energy released:

$$
E = 0.00007 \times 931.5 \approx 0.065\ \mathrm{MeV}
$$

(antineutrino mass is negligible; energy is shared between the \(\beta^-\) and the \(\bar{\nu}\), which is why \(\beta\) particles emerge with a CONTINUOUS range of energies)

### Listing 3 — Exam Q2: alpha decay of radium-226

Radium-226 undergoes alpha decay. Alpha decay rule: \(A\) decreases by 4, \(Z\) decreases by 2.

$$
{}^{226}_{88}\mathrm{Ra} \to {}^{222}_{86}\mathrm{Rn} + {}^{4}_{2}\mathrm{He}
$$

Conservation check:

- mass number: \(226 = 222 + 4\) ✓
- charge (\(Z\)): \(88 = 86 + 2\) ✓ (\(Z = 86\) is radon)

Daughter nucleus: radon-222.

### Listing 4 — Exam Q5: beta-minus decay of carbon-14

Carbon-14 undergoes beta-minus decay. Beta-minus rule: \(A\) unchanged, \(Z\) increases by 1.

$$
{}^{14}_{6}\mathrm{C} \to {}^{14}_{7}\mathrm{N} + {}^{0}_{-1}e + \bar{\nu}
$$

Underlying nucleon change (a down quark \(\to\) up quark, via the weak force / W boson):

$$
{}^{1}_{0}n \to {}^{1}_{1}p + {}^{0}_{-1}e + \bar{\nu}
$$

Conservation check:

- mass number: \(14 = 14 + 0\) ✓
- charge (\(Z\)): \(6 = 7 + (-1)\) ✓ (\(Z = 7\) is nitrogen)
- lepton number: \(0 = 0 + (+1) + (-1)\) ✓ (electron \(+1\), antineutrino \(-1\) \(\to\) this forces the \(\bar{\nu}\))
- mass-energy: small \(\Delta m\) released as kinetic energy of the \(\beta^-\) and \(\bar{\nu}\)

Daughter nucleus: nitrogen-14. (This is the decay used in radiocarbon dating.)

### Listing 5 — The four decay-bookkeeping rules ("alpha eats four and two, beta swaps a charge, gamma changes nothing")
| Decay | Change in A | Change in Z | What is emitted | Underlying nucleon change |
|-------|-------------|-------------|-----------------|---------------------------|
| Alpha (α) | −4 | −2 | helium-4 nucleus (⁴₂He) | — |
| Beta-minus (β⁻) | 0 | +1 | electron + antineutrino | neutron → proton (down→up quark) |
| Beta-plus (β⁺) | 0 | −1 | positron + neutrino | proton → neutron (up→down quark) |
| Gamma (γ) | 0 | 0 | high-energy photon | excited nucleus de-excites (no transmutation) |

### Listing 6 — Comparing the three radiations ("bouncer, punter, ghost")
| Property | Alpha (α) | Beta-minus (β⁻) | Gamma (γ) |
|----------|-----------|-----------------|-----------|
| Composition | helium-4 nucleus (2 p + 2 n) | fast electron (from nucleus) | high-energy photon (EM radiation) |
| Symbol | ⁴₂He | ⁰₋₁e | γ |
| Charge | +2 | −1 | 0 |
| Relative mass | ~4 u (massive) | ~1/1836 u (tiny) | 0 (massless) |
| Ionising power | very high | moderate | very low |
| Penetration | very low (paper / few cm air / dead skin) | moderate (~1 cm aluminium / ~1 m air) | very high (cm of lead / m of concrete) |
| Speed | ~5–7% of c (≈2×10⁷ m/s) | range, up to ~99% of c | c (it is light) |
| Deflection in B-field | curves (positive) | curves opposite, more sharply (negative) | not deflected (neutral) |

Inverse relationship: ionising power α > β > γ; penetration γ > β > α.

### Listing 7 — Key values, constants, names and dates
| Quantity / fact | Value or detail |
|-----------------|-----------------|
| Strong nuclear force range | ~10⁻¹⁵ m (≈1 femtometre); nearest-neighbour; repulsive at very short range |
| Mass–energy conversion | 1 u ↔ 931.5 MeV/c² |
| Atomic mass unit | 1 u = 1.6605 × 10⁻²⁷ kg |
| Speed of light | c = 3.0 × 10⁸ m/s |
| Mass–energy equivalence | \(E = \Delta m \cdot c^{2}\); mass number \(A = Z + N\) |
| Proton / neutron / electron mass | 1.007276 u / 1.008665 u / 0.00055 u |
| Stability cutoff | beyond Z ≈ 83 (bismuth) no neutron excess gives stability |
| Quark content | proton = uud, neutron = udd; β⁻: down→up, β⁺: up→down |
| Weak-force carriers | W boson (and Z boson) |
| Neutrino predicted | Wolfgang Pauli, 1930; named by Enrico Fermi; detected 1956 |
| U-238 α decay energy | ≈ 4.25 MeV |
