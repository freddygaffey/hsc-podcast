---
title: "Supplementary Materials — PET Scans — Antimatter in Medicine"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Energy released in positron-electron annihilation

Mass-energy equivalence:

$$
E = m c^{2}
$$

The rest mass energy of an electron is \(0.511\ \mathrm{MeV} = 511\ \mathrm{keV}\); the rest mass energy of a positron is \(0.511\ \mathrm{MeV} = 511\ \mathrm{keV}\) (identical mass, by Dirac symmetry).

Total energy released in one annihilation:

$$
E_{\text{total}} = 2\times0.511\ \mathrm{MeV} = 1.022\ \mathrm{MeV}
$$

This is shared equally between two photons:

$$
E_{\text{per photon}} = \frac{1.022\ \mathrm{MeV}}{2} = 0.511\ \mathrm{MeV} = 511\ \mathrm{keV}
$$

The precise value of each photon energy is \(510.99895\ \mathrm{keV}\).

In SI units (showing \(E = mc^{2}\) explicitly), the mass is the electron plus positron:

$$
m = 9.109\times10^{-31}\ \mathrm{kg} + 9.109\times10^{-31}\ \mathrm{kg} = 1.822\times10^{-30}\ \mathrm{kg}
$$

with \(c = 3.00\times10^{8}\ \mathrm{m/s}\):

$$
E = (1.822\times10^{-30})(3.00\times10^{8})^{2} = 1.64\times10^{-13}\ \mathrm{J} = 1.022\ \mathrm{MeV}
$$

(since \(1\ \mathrm{MeV} = 1.602\times10^{-13}\ \mathrm{J}\)).

### Listing 2 — Why two photons, back to back (conservation laws)

Annihilation reaction:

$$
e^{-}\ (\text{electron}) + e^{+}\ (\text{positron}) \to \gamma + \gamma
$$

CHARGE conservation: before, \((-e) + (+e) = 0\); after, \(0 + 0 = 0\) (photons are neutral) — OK.

ENERGY conservation:

$$
\text{total energy in} = 0.511 + 0.511 = 1.022\ \mathrm{MeV}, \qquad \text{total energy out} = 0.511 + 0.511 = 1.022\ \mathrm{MeV}
$$

so each photon must carry \(511\ \mathrm{keV}\).

MOMENTUM conservation: before, the \(e^{-}\) and \(e^{+}\) are (nearly) at rest, so total momentum \(\approx 0\); after, the total momentum must still be \(0\). One photon carries momentum \(p\) in some direction, so the second photon must carry momentum \(p\) in the EXACTLY opposite direction, so that \(p + (-p) = 0\). Therefore the two photons are emitted 180 degrees apart (back to back).

Note (non-collinearity): the electron has a small residual momentum, so in the lab frame the angle deviates from 180 degrees by \(\approx 0.25\) degrees. This is a fundamental limit on PET spatial resolution, NOT an engineering flaw.

### Listing 3 — The PET imaging chain (step by step)

1. FDG (fluorodeoxyglucose) injected into bloodstream. FDG = glucose with one OH group replaced by fluorine-18.
2. Cells take up FDG like glucose (via GLUT transporters). Tumour cells consume glucose fastest (Warburg effect) \(\to\) take up most FDG. FDG gets phosphorylated then TRAPPED inside the cell \(\to\) accumulates.
3. Fluorine-18 decays by beta-plus decay (mediated by the WEAK nuclear force): \(\mathrm{F}\text{-}18 \to \mathrm{O}\text{-}18 + e^{+}\ (\text{positron}) + \text{neutrino}\) (a proton turns into a neutron, emitting a positron). Underlying transformation: \(p \to n + e^{+} + \text{neutrino}\).
4. Positron travels only \(\approx 0.5\text{-}2.3\ \mathrm{mm}\) in tissue, then meets an electron.
5. Annihilation: \(e^{+} + e^{-} \to\) two \(511\ \mathrm{keV}\) gamma photons at \(\approx 180\) degrees.
6. Gamma photons (mean free path \(\approx 10\ \mathrm{cm}\) in tissue) escape the body. NOTE: the scanner detects the GAMMA RAYS, never the positrons.
7. A ring of detector crystals surrounds the patient. Two opposite detectors firing within a few nanoseconds = a "coincidence".
8. Each coincidence defines a LINE OF RESPONSE (LOR): the annihilation occurred somewhere on the straight line joining the two detectors.
9. Millions of LORs are collected. Where many lines intersect = where the FDG is concentrated. A computer reconstructs a 3D map of metabolism.

### Listing 4 — Fluorine-18 half-life and decay

Beta-plus (positron) decay equation:

$$
{}^{18}_{9}\mathrm{F} \to {}^{18}_{8}\mathrm{O} + e^{+} + \text{neutrino}
$$

In beta-plus decay the WEAK nuclear force converts a proton into a neutron:

$$
{}^{1}_{1}p \to {}^{1}_{0}n + e^{+} + \text{neutrino}
$$

so the atomic number \(Z\) decreases by 1 (\(9 \to 8\)); the mass number \(A\) is unchanged (18). Note: beta-PLUS emits a neutrino; beta-MINUS emits an ANTI-neutrino.

Half-life of fluorine-18, \(t_{1/2} = 109.77\ \mathrm{min}\) (\(\approx 110\ \mathrm{min}\)).

Decay constant:

$$
\lambda = \frac{\ln 2}{t_{1/2}} = \frac{0.693}{110\ \mathrm{min}} = 0.0063\ \text{per min}
$$

Fraction remaining after \(n\) half-lives \(= \left(\tfrac{1}{2}\right)^{n}\):

| Half-lives passed | Time | Fraction remaining |
|---|---|---|
| 0 | 0 min | 100% |
| 1 | ~110 min | 50% |
| 2 | ~220 min (3.7 h) | 25% |
| 3 | ~330 min | 12.5% |
| 6 | ~660 min (11 h) | ~1.6% |

So it is long enough to ship from cyclotron and scan (uptake takes \(\approx 60\text{-}90\ \mathrm{min}\)), short enough that the patient is essentially non-radioactive next day. Compare carbon-11 (\(t_{1/2} \approx 20\ \mathrm{min}\)) \(\to\) too short to ship; F-18 chosen instead.

### Listing 5 — Key numbers and constants for this episode

| Quantity | Value |
|----------|-------|
| Electron / positron rest mass energy | 0.511 MeV (= 511 keV) each |
| Energy of each annihilation photon | 511 keV (510.99895 keV precisely) |
| Total energy per annihilation | 1.022 MeV |
| Angle between the two photons | 180 degrees (back to back) |
| Fluorine-18 half-life | 109.77 min (~110 min) |
| Positron range in tissue (F-18) | mean ~0.6 mm; max ~2.3 mm in water |
| Mean free path of 511 keV gamma in tissue | ~10 cm |
| Coincidence timing window | ~6-12 nanoseconds |
| PET spatial resolution | ~1-8 mm (scanner dependent) |
| Standard FDG dose | 185-370 MBq (5-10 millicuries) |
| Uptake time before scan | 60-90 min |
| Speed of light, c | 3.00 x 10^8 m/s |
| 1 MeV | 1.602 x 10^-13 J |

### Listing 6 — Timeline of the discovery and the application

| Year | Event |
|------|-------|
| 1928 | Dirac publishes The Quantum Theory of the Electron (Cambridge); negative-energy solutions appear |
| 1930 | Oppenheimer argues the "hole" must have the electron's mass, not be a proton |
| 1931 | Dirac explicitly predicts the "anti-electron" (positron) |
| 1932 | Anderson photographs the positron in a cloud chamber at Caltech (2 Aug); names it the positron |
| 1933 | Dirac shares Nobel Prize (with Schrodinger) |
| 1936 | Anderson shares Nobel Prize for the positron |
| 1953 | Brownell & Sweet (MGH) use positron emitters to locate brain tumours |
| 1974 | First ring PET scanner (Ter-Pogossian, Phelps, Hoffman, Washington Univ. St Louis) |
| 1976 | First human administration of [18F]FDG (Alavi, Univ. of Pennsylvania, Aug) |
| ~1980 | Discovery that tumours accumulate FDG -> PET becomes an oncology tool |
