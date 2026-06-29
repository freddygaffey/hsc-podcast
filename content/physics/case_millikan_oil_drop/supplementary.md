---
title: "Supplementary Materials — The Millikan Oil-Drop Experiment"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — The two governing equations of the balanced drop

**Stage 1 — Find the mass** (field OFF, drop falls at terminal velocity \(v_{g}\)). At terminal velocity, weight = drag (Stokes' law):

$$
\tfrac{4}{3}\pi r^{3} (\rho_{\text{oil}} - \rho_{\text{air}})\, g = 6\pi \eta r v_{g}
$$

Solve for the drop radius \(r\):

$$
r = \sqrt{\frac{9 \eta v_{g}}{2 g (\rho_{\text{oil}} - \rho_{\text{air}})}}
$$

Then the mass:

$$
m = \tfrac{4}{3}\pi r^{3} \rho_{\text{oil}}
$$

**Stage 2 — Find the charge** (field ON, forces balanced). The drop is in equilibrium either held stationary OR moving at constant (uniform) velocity. Either way the net force is zero. Weight force (down) is \(F_{g} = m g\); electric force (up) is \(F_{E} = E q\). For equilibrium:

$$
F_{g} = F_{E} \quad\Rightarrow\quad m g = E q
$$

Electric field from the plates:

$$
E = \frac{V}{d}
$$

Therefore the charge on the drop:

$$
q = \frac{m g}{E} = \frac{m g d}{V}
$$

### Listing 2 — Stokes' law small-drop correction (Millikan's refinement)

For very small drops (radius near the mean free path of air \({\sim}70\ \mathrm{nm}\)), plain Stokes' law overestimates the drag. Millikan corrected it:

$$
F_{\text{drag, corrected}} = 6\pi \eta r v \cdot \frac{1}{1 + \dfrac{b}{p r}}
$$

where:

- \(b\) = empirical constant \(= 7.88\times 10^{-3}\ \mathrm{Pa\,m}\)
- \(p\) = air pressure
- \(r\) = drop radius

This correction was Millikan's key methodological contribution beyond the basic balanced-drop idea.

### Listing 3 — Demonstrating quantisation of charge

Measure the charge \(q\) on many different drops, and on single drops before and after ionising them with X-rays. Every value satisfies:

$$
q = n e \qquad \text{where } n = 1, 2, 3, 4, \ldots \text{ (a whole number)}
$$

where \(e\) is the fundamental (elementary) charge = charge on one electron.

Key evidence:

- No drop ever carries a fractional multiple of \(e\)
- X-rays change a single drop's charge by exactly \(\pm e, \pm 2e, \ldots\)
- Conclusion: electric charge is QUANTISED

### Listing 4 — Key values and constants

| Quantity | Value |
|----------|-------|
| Millikan's 1913 published charge | 1.5924 x 10^-19 C |
| Modern fixed value (since 2019) | 1.602176634 x 10^-19 C |
| Discrepancy (cause: air viscosity) | ~0.6% |
| Plate separation d | ~16 mm = 0.016 m |
| Voltage across plates V | ~5000 V |
| Resulting field E = V/d | ~313 kV/m |
| Oil density rho_oil | 919.9 kg/m^3 |
| Air density rho_air | ~1.2 kg/m^3 |
| Air viscosity eta (~23 C) | 1.820 x 10^-5 kg/(m*s) |
| Typical drop radius | 1–3 micrometres |
| Typical drop mass | 10^-14 to 10^-13 kg |
| Drops in notebooks vs published | ~175 recorded, 58 published |
| Thomson's charge-to-mass ratio (measured) | ~1.8 x 10^11 C/kg |
| Thomson's charge-to-mass ratio (modern value) | 1.759 x 10^11 C/kg |
| Elementary (quantum of) charge e | 1.6 x 10^-19 C |
| Acceleration due to gravity g (used) | 9.8 m/s^2 |
| Nobel Prize in Physics | 1923 |

### Listing 5 — Worked example: charge on a suspended drop

A charged oil drop of mass \(6.8\times 10^{-15}\ \mathrm{kg}\) is held stationary between two plates 16 mm apart with 5000 V across them.

**Step 1 — Electric field between the plates:**

$$
E = \frac{V}{d} = \frac{5000}{0.016} = 3.125\times 10^{5}\ \mathrm{V/m}
$$

**Step 2 — At balance, electric force = weight:**

$$
\begin{aligned}
q E &= m g \\
q &= \frac{m g}{E} = \frac{6.8\times 10^{-15} \times 9.8}{3.125\times 10^{5}} \\
&= \frac{6.664\times 10^{-14}}{3.125\times 10^{5}} = 2.13\times 10^{-19}\ \mathrm{C}
\end{aligned}
$$

**Step 3 — Number of excess electrons:**

$$
n = \frac{q}{e} = \frac{2.13\times 10^{-19}}{1.6\times 10^{-19}} \approx 1.3 \to \text{rounds to 1 excess electron (within experimental error)}
$$

Note: real drops typically carried 5–30 electrons; the charge always came out as a whole-number multiple \(n\) of \(e\), never a fraction.

### Listing 6 — Consequences unlocked by knowing e

**1. Mass of the electron** (using Thomson's charge-to-mass ratio):

$$
m_{e} = \frac{e}{e/m} = \frac{e}{1.759\times 10^{11}} \approx 9.109\times 10^{-31}\ \mathrm{kg}
$$

**2. Avogadro constant** (from Faraday's constant \(F = N_{A} e\)):

$$
N_{A} = \frac{F}{e} \to \text{confirmed atomic theory, counts atoms per mole}
$$

**3. The electronvolt energy unit:**

$$
1\ \mathrm{eV} = 1.602\times 10^{-19}\ \mathrm{J}
$$
