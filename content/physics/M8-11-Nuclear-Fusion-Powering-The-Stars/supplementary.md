---
title: "Supplementary Materials — Nuclear Fusion: Powering the Stars"
module: M8
lesson: "11"
script: script.md
---

# Supplementary Materials

Key equations, derivations, worked numerical solutions, and reference data for this episode. Nothing here is spoken in the audio — it's the read-along reference for working you don't have time to write out at 4–5× speed.

### Listing 1 — Deuterium–tritium fusion: energy released (full working)

Reaction (conserve mass number \(A\) on top, atomic number \(Z\) on bottom):

$$
{}^{2}_{1}\mathrm{H} + {}^{3}_{1}\mathrm{H} \to {}^{4}_{2}\mathrm{He} + {}^{1}_{0}n + \text{energy}
$$

Check conservation:

- \(A\) (top):  \(2 + 3 = 5\)  and  \(4 + 1 = 5\)  ✓
- \(Z\) (bottom):  \(1 + 1 = 2\)  and  \(2 + 0 = 2\)  ✓

**Step 1 — Mass defect** \(\Delta m = (\Sigma\ \text{reactant masses}) - (\Sigma\ \text{product masses})\):

$$
\text{reactants:}\quad m({}^{2}\mathrm{H}) + m({}^{3}\mathrm{H}) = 2.014102 + 3.016050 = 5.030152\ \mathrm{u}
$$

$$
\text{products:}\quad m({}^{4}\mathrm{He}) + m(n) = 4.002603 + 1.008665 = 5.011268\ \mathrm{u}
$$

$$
\Delta m = 5.030152 - 5.011268 = 0.018884\ \mathrm{u} \quad (\approx 0.0188\ \mathrm{u})
$$

**Step 2 — Energy via the data-sheet shortcut** \(E\ (\mathrm{MeV}) = \Delta m\ (\mathrm{u}) \times 931.5\):

$$
E = 0.018884 \times 931.5 \approx 17.6\ \mathrm{MeV}
$$

(textbook value \(\approx 17.69\ \mathrm{MeV}\) using more precise intermediate masses)

⚠ TRAP: 931.5 already carries units \(\mathrm{MeV}/c^{2}\) — the \(c^{2}\) is built in. Multiply by 931.5 and STOP. Do NOT also divide by \(c^{2}\).

**Step 3 — Cross-check via** \(E = \Delta m\, c^{2}\) (the long route, in SI units):

$$
\Delta m = 0.018884\ \mathrm{u} \times 1.6605 \times 10^{-27}\ \mathrm{kg/u} \approx 3.136 \times 10^{-29}\ \mathrm{kg}
$$

$$
E = \Delta m\, c^{2} = (3.136 \times 10^{-29})(3.0 \times 10^{8})^{2} \approx 2.9 \times 10^{-12}\ \mathrm{J}
$$

$$
\text{Convert:}\quad 2.9 \times 10^{-12}\ \mathrm{J} \div 1.602 \times 10^{-13}\ \mathrm{J/MeV} \approx 17.6\ \mathrm{MeV} \quad \checkmark
$$

ANSWER: \(\approx 17.6\ \mathrm{MeV}\ (\approx 2.9 \times 10^{-12}\ \mathrm{J})\) released per D–T fusion event. The free neutron carries away most of this energy.

### Listing 2 — Masses and constants used
| Quantity | Value |
|----------|-------|
| Deuterium ²₁H | 2.014102 u |
| Tritium ³₁H | 3.016050 u |
| Helium-4 ⁴₂He | 4.002603 u |
| Neutron ¹₀n | 1.008665 u |
| Proton ¹₁H | 1.007276 u |
| Electron | 0.000549 u |
| Mass–energy conversion | 1 u ≡ 931.5 MeV/c² = 1.661 × 10⁻²⁷ kg |
| Speed of light | c = 3.0 × 10⁸ m s⁻¹ (c² ≈ 9.0 × 10¹⁶ m² s⁻²) |
| 1 MeV | 1.602 × 10⁻¹³ J |
| Iron-56 (curve peak) | ≈ 8.8 MeV/nucleon — most stable nucleus |

### Listing 3 — The proton–proton chain (stellar prototype, previewed; full treatment in M8-14)

Net result \((\approx 26.7\ \mathrm{MeV}\) per He-4\()\):

$$
4\,({}^{1}_{1}\mathrm{H}) \to {}^{4}_{2}\mathrm{He} + 2e^{+} + 2\nu + \text{energy}
$$

Step 1 (a proton \(\to\) neutron, \(\beta^{+}\); \(\approx 1.44\ \mathrm{MeV}\)):

$$
{}^{1}_{1}\mathrm{H} + {}^{1}_{1}\mathrm{H} \to {}^{2}_{1}\mathrm{H} + e^{+} + \nu
$$

Step 2 \((\approx 5.49\ \mathrm{MeV})\):

$$
{}^{2}_{1}\mathrm{H} + {}^{1}_{1}\mathrm{H} \to {}^{3}_{2}\mathrm{He} + \gamma
$$

Step 3 \((\approx 12.9\ \mathrm{MeV})\):

$$
{}^{3}_{2}\mathrm{He} + {}^{3}_{2}\mathrm{He} \to {}^{4}_{2}\mathrm{He} + 2\,({}^{1}_{1}\mathrm{H})
$$

Each step conserves mass number \(A\) and atomic number \(Z\). The positron \((e^{+})\) is antimatter — it later annihilates with an electron (M8-12).

### Listing 4 — Why helium-4 is so tightly bound (the "why H→He is so energetic" number)

$$
\Delta m = [2\,m({}^{1}\mathrm{H}) + 2\,m(n)] - m({}^{4}\mathrm{He}) \quad (\text{atomic masses; electron masses cancel})
$$

$$
= [2(1.007276) + 2(1.008665)] - 4.002603 = 4.032882 - 4.002603 = 0.030379\ \mathrm{u}
$$

Total binding energy:

$$
E_B = 0.030379 \times 931.5 \approx 28.3\ \mathrm{MeV}
$$

Binding energy per nucleon:

$$
E_B / A = 28.3 \div 4 \approx 7.07\ \mathrm{MeV/nucleon}
$$

(unusually high for such a light nucleus — close to the iron peak, which is why hydrogen \(\to\) helium fusion releases so much energy)

### Listing 5 — Energy per unit mass: the comparison (fusion > fission ≫ chemical)
| Process | Typical energy per event | Basis of "more energy per unit mass" |
|---------|--------------------------|--------------------------------------|
| Chemical (burn 1 C atom) | ≈ 10 eV | Rearranges electrons only — the floor |
| Fission (one U-235 split) | ≈ 200 MeV | ~20 million × a chemical event per atom |
| Fusion (one D–T event) | ≈ 17.6 MeV | Fewer nucleons, steepest part of the curve → most energy *per nucleon* |

Order PER UNIT MASS:  fusion \(>\) fission \(\gg\) chemical. Mnemonic: "Fusion Feeds the Cosmos" (Fusion \(\to\) Fission \(\to\) Chemical, descending).

Note the basis: per single EVENT, fission \((200\ \mathrm{MeV}) >\) fusion \((17.6\ \mathrm{MeV})\); but per UNIT MASS / per nucleon, fusion wins. Always state the basis.

### Listing 6 — Key terms, names and dates
| Item | What to know |
|------|--------------|
| Coulomb barrier | Long-range electrostatic repulsion between the two positive nuclei — the obstacle to fusion |
| Strong nuclear force | Short-range (~10⁻¹⁵ m) attraction that binds nucleons once close; overcomes Coulomb repulsion |
| Temperature requirement | High KE to beat the Coulomb barrier; Sun's core ≈ 15 million K; Earth reactors need 100s of millions K |
| Pressure/density requirement | Frequent enough collisions to sustain the reaction; in a star, supplied by gravity |
| Iron limit | Fusion releases energy only up to iron-56; beyond iron it consumes energy → iron is heaviest fusion product |
| Arthur Eddington (~1926) | Proposed fusion of hydrogen as the Sun's energy source |
| Mark Oliphant (1932) | Australian; first observed fusion in the lab (with Rutherford); discovered tritium and helium-3 |
| Hans Bethe (1938) | Worked out the proton–proton chain and CNO cycle; Nobel Prize |
| ITER | Magnetic-confinement tokamak; leading Earth-based fusion candidate; not yet net-positive sustained |
