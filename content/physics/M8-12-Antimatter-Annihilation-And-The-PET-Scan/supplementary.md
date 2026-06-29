---
title: "Supplementary Materials — Antimatter, Annihilation, and the PET Scan"
module: M8
lesson: "12"
script: script.md
---

# Supplementary Materials

Key equations, decay equations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference. The narration refers to each listing by label only.

### Listing 1 — Energy of an annihilation photon (worked example)

Find: energy of EACH gamma photon when an electron and positron annihilate at rest.

Reaction (two photons, opposite directions, \(\approx 180^{\circ}\) apart):

$$
e^{-} + e^{+} \to \gamma + \gamma
$$

Data:

- \(m_e = 9.11 \times 10^{-31}\ \mathrm{kg}\)
- \(c = 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\)
- \(1\ \mathrm{MeV} = 1.602 \times 10^{-13}\ \mathrm{J}\)

**Step 1 — Total energy released = rest energy of BOTH particles:**

$$
E_{\text{total}} = 2 m_e c^{2}
$$

$$
E_{\text{total}} = 2 \times (9.11 \times 10^{-31}) \times (3.0 \times 10^{8})^{2}
$$

$$
E_{\text{total}} = 2 \times (9.11 \times 10^{-31}) \times (9.0 \times 10^{16}) = 1.64 \times 10^{-13}\ \mathrm{J}
$$

**Step 2 — Two photons share it equally → each photon:**

$$
E_{\text{photon}} = \tfrac{1}{2} \times (1.64 \times 10^{-13}) = 8.2 \times 10^{-14}\ \mathrm{J}
$$

**Step 3 — Convert one photon to MeV:**

$$
E_{\text{photon}} = (8.2 \times 10^{-14}) \div (1.602 \times 10^{-13}) = 0.511\ \mathrm{MeV}
$$

Answer: each photon \(= 8.2 \times 10^{-14}\ \mathrm{J} = 0.511\ \mathrm{MeV}\); total released \(= 1.64 \times 10^{-13}\ \mathrm{J} = 1.022\ \mathrm{MeV} = 2 m_e c^{2}\).

### Listing 2 — Energy released in C-11 beta-plus decay (worked example)

Reaction (positron + neutrino emitted):

$$
{}^{11}_{6}\mathrm{C} \to {}^{11}_{5}\mathrm{B} + {}^{0}_{+1}e + \nu
$$

Atomic masses (u):

- \({}^{11}_{6}\mathrm{C} = 11.01143\)
- \({}^{11}_{5}\mathrm{B} = 11.00931\)
- electron / positron \(= 0.00055\) each

Conversion: \(1\ \mathrm{u} \equiv 931.5\ \mathrm{MeV}/c^{2}\) (multiply by 931.5 and STOP).

These are ATOMIC masses (include orbital electrons), so the electrons must be tracked explicitly. Neutrino mass is neglected.

Mass before (C-11 nucleus) = atomic mass − 6 electrons:

$$
= 11.01143 - (6 \times 0.00055) = 11.00813\ \mathrm{u}
$$

Mass after (B-11 nucleus + emitted positron), via electron bookkeeping:

$$
= [11.00931 - (4 \times 0.00055)] = 11.00711\ \mathrm{u}
$$

Mass lost \((\Delta m)\):

$$
\Delta m = 11.00813 - 11.00711 = 0.00102\ \mathrm{u}
$$

Energy released (multiply by 931.5; do NOT divide by \(c^{2}\) as well):

$$
E = 0.00102 \times 931.5 \approx 0.95\ \mathrm{MeV}
$$

Answer: \(\approx 0.95\ \mathrm{MeV}\), shared as kinetic energy of the positron and neutrino. (The emitted positron then annihilates \(\to\) two \(0.511\ \mathrm{MeV}\) photons: Listing 1.)

### Listing 3 — Key equations for this episode

Beta-plus decay (general):

$$
{}^{1}_{1}p \to {}^{1}_{0}n + {}^{0}_{+1}e + \nu
$$

- mass number \(A\) unchanged; atomic number \(Z\) falls by 1

Pair production:

$$
\gamma \to e^{-} + e^{+}
$$

- energy → mass, near a nucleus
- two PARTICLES made to conserve CHARGE
- threshold \(E_{\gamma} \ge 1.022\ \mathrm{MeV} = 2 m_e c^{2}\)

Annihilation:

$$
e^{-} + e^{+} \to \gamma + \gamma
$$

- mass → energy
- two PHOTONS made to conserve MOMENTUM (pair at rest, total \(p \approx 0\))
- \(E_{\text{total}} = 2 m_e c^{2} = 1.022\ \mathrm{MeV}\); each photon \(= m_e c^{2} = 0.511\ \mathrm{MeV}\)

Mass–energy equivalence: \(E = mc^{2}\). Mass→energy shortcut: \(1\ \mathrm{u} \equiv 931.5\ \mathrm{MeV}/c^{2}\).

### Listing 4 — Particle properties and key constants
| Quantity | Symbol | Value |
|----------|--------|-------|
| Electron / positron rest mass | m_e | 9.11 × 10⁻³¹ kg (= 0.000 55 u) |
| Electron rest energy | m_e c² | 0.511 MeV |
| Annihilation photon energy (each) | E_photon | 0.511 MeV |
| Total annihilation energy | 2 m_e c² | 1.022 MeV |
| Pair-production threshold | 2 m_e c² | 1.022 MeV |
| Electron charge | −e | −1.6 × 10⁻¹⁹ C |
| Positron charge | +e | +1.6 × 10⁻¹⁹ C |
| Speed of light | c | 3.0 × 10⁸ m s⁻¹ |
| Atomic mass unit | u | 1.661 × 10⁻²⁷ kg ≡ 931.5 MeV/c² |
| 1 MeV in joules | — | 1.602 × 10⁻¹³ J |

### Listing 5 — The PET imaging chain (the "TRACER" memory hook)
| Step | TRACER | What happens |
|------|--------|--------------|
| 1 | **T**racer injected | Short-lived β⁺ emitter (e.g. F-18 in FDG, a glucose analogue) injected into the patient |
| 2 | **R**eaches active tissue | FDG concentrates in metabolically active tissue (tumours, active brain) because it behaves like glucose |
| 3 | **A**nnihilation | Each positron travels a few mm, meets an electron, and annihilates → two 0.511 MeV γ photons, ≈180° apart |
| 4 | **C**oincidence detection | A surrounding ring of detectors registers the two photons simultaneously, on opposite sides |
| 5 | **E**stablish the line | The line joining the two detectors — the "line of response" — passes through the annihilation point |
| 6 | **R**econstruct | A computer combines millions of lines of response into a 3-D image of tracer concentration = metabolic map |

### Listing 6 — Production routes and named scientists
| Item | Detail |
|------|--------|
| Production route 1 — Beta-plus decay | Proton-rich nucleus: p → n + e⁺ + ν; e.g. ¹¹₆C → ¹¹₅B + e⁺ + ν, or ²²₁₁Na → ²²₁₀Ne + e⁺ + ν |
| Production route 2 — Pair production | High-energy γ near a nucleus: γ → e⁻ + e⁺ (threshold 1.022 MeV) |
| Predicted by | Paul Dirac (1928–1931), from negative-energy solutions of his relativistic quantum equation |
| Discovered by | Carl Anderson (1932–1933), cosmic-ray track curving opposite to an electron in a cloud chamber |
| Real PET isotopes | Fluorine-18 (≈110 min half-life), Carbon-11, Nitrogen-13, Oxygen-15 |
