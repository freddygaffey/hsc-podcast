---
title: "Supplementary Materials — Charge-to-Mass, the Elementary Charge, and the Plum Pudding Model"
module: M8
lesson: "02"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Stage 1: the velocity selector (find the speed)

Both \(E\) and \(B\) fields ON, forces opposed; beam adjusted until UNDEFLECTED. Undeflected \(\Rightarrow\) net force \(= 0\) \(\Rightarrow\) electric force \(=\) magnetic force:

$$
F_E = F_B
$$

$$
qE = qvB
$$

\(q\) cancels (appears on both sides):

$$
E = vB \qquad \Rightarrow \qquad v = \frac{E}{B}
$$

Key point: \(q\) cancels, so the selected speed \(v\) is INDEPENDENT of the charge AND the mass of the particle. (\(q\) cancels \(\ne\) \(q\) is zero.)

Symbols/units:

- \(F_E,\ F_B\) = force (\(\mathrm{N}\))
- \(q\) = charge (\(\mathrm{C}\))
- \(E\) = electric field strength (\(\mathrm{N\,C^{-1}} = \mathrm{V\,m^{-1}}\))
- \(v\) = speed (\(\mathrm{m\,s^{-1}}\))
- \(B\) = magnetic flux density (\(\mathrm{T}\), tesla)

### Listing 2 — Stage 2: magnetic-only circular motion (find q/m)

Electric field switched OFF; only \(B\) acts. Magnetic force is ALWAYS perpendicular to \(v\) \(\Rightarrow\) does no work \(\Rightarrow\) acts as the centripetal force \(\Rightarrow\) beam follows a circular arc. Setting magnetic force \(=\) centripetal force:

$$
qvB = \frac{m v^{2}}{r}
$$

Cancel one factor of \(v\) and rearrange for \(q/m\):

$$
qB = \frac{m v}{r} \qquad \Rightarrow \qquad \frac{q}{m} = \frac{v}{B r}
$$

Substitute \(v = E/B\) from Stage 1 to get the combined form:

$$
\frac{q}{m} = \frac{E/B}{B r} = \frac{E}{B^{2} r}
$$

Symbols/units:

- \(m\) = mass (\(\mathrm{kg}\))
- \(r\) = radius of circular path (\(\mathrm{m}\))
- \(q/m\) = charge-to-mass ratio (\(\mathrm{C\,kg^{-1}}\))

### Listing 3 — Worked example: Thomson's q/m for the electron

GIVEN (crossed-fields CRT): undeflected with \(E = 5.0 \times 10^{3}\ \mathrm{N\,C^{-1}}\), \(B = 2.0 \times 10^{-2}\ \mathrm{T}\); with \(E\) off, circular arc radius \(r = 7.1 \times 10^{-5}\ \mathrm{m}\).

STAGE 1 — speed (charge cancelled — speed independent of \(q\) and \(m\)):

$$
v = \frac{E}{B} = \frac{5.0 \times 10^{3}}{2.0 \times 10^{-2}} = 2.5 \times 10^{5}\ \mathrm{m\,s^{-1}}
$$

STAGE 2 — charge-to-mass ratio:

$$
\frac{q}{m} = \frac{v}{B r} = \frac{2.5 \times 10^{5}}{(2.0 \times 10^{-2})(7.1 \times 10^{-5})} = \frac{2.5 \times 10^{5}}{1.42 \times 10^{-6}} \approx 1.76 \times 10^{11}\ \mathrm{C\,kg^{-1}}
$$

INTERPRETATION: this is \(\sim 1800\times\) the \(q/m\) of a hydrogen ion \(\Rightarrow\) electron mass \(\approx 1/1800\) that of hydrogen \(\Rightarrow\) first sub-atomic particle \(\Rightarrow\) atom is divisible.

### Listing 4 — Magnetic force on an electron (supports Stage 2)

GIVEN:

- \(q = 1.6 \times 10^{-19}\ \mathrm{C}\)
- \(v = 2.5 \times 10^{4}\ \mathrm{m\,s^{-1}}\) (perpendicular to \(B\), so \(\sin\theta = \sin 90^\circ = 1\))
- \(B = 2.0 \times 10^{-2}\ \mathrm{T}\)

$$
F = qvB\sin\theta = (1.6 \times 10^{-19})(2.5 \times 10^{4})(2.0 \times 10^{-2})(1) = 8.0 \times 10^{-17}\ \mathrm{N}
$$

The force stays perpendicular to \(v\) \(\Rightarrow\) path is CIRCULAR, speed unchanged (magnetic force does no work; it changes direction, not speed).

### Listing 5 — Worked example: Millikan oil drop (charge + electron count)

GIVEN:

- drop mass \(m = 6.8 \times 10^{-6}\ \mathrm{g}\)
- plate separation \(d = 3.5\ \mathrm{mm} = 3.5 \times 10^{-3}\ \mathrm{m}\)
- plate voltage \(V = 110\ \mathrm{V}\)
- \(g = 9.8\ \mathrm{m\,s^{-2}}\), \(\ e = 1.6 \times 10^{-19}\ \mathrm{C}\)

(a) FIELD STRENGTH:

$$
E = \frac{V}{d} = \frac{110}{3.5 \times 10^{-3}} \approx 3.1 \times 10^{4}\ \mathrm{V\,m^{-1}}\quad (3.143 \times 10^{4})
$$

(b) CHARGE (suspended \(\Rightarrow qE = mg\)); convert mass: \(6.8 \times 10^{-6}\ \mathrm{g} = 6.8 \times 10^{-9}\ \mathrm{kg}\) (grams \(\to\) kg!):

$$
q = \frac{mg}{E} = \frac{(6.8 \times 10^{-9})(9.8)}{3.143 \times 10^{4}} = \frac{6.664 \times 10^{-8}}{3.143 \times 10^{4}} \approx 2.1 \times 10^{-12}\ \mathrm{C}
$$

(c) NUMBER OF EXCESS ELECTRONS (\(q = n e\)):

$$
n = \frac{q}{e} = \frac{2.1 \times 10^{-12}}{1.6 \times 10^{-19}} \approx 1.3 \times 10^{7}\ \text{electrons}
$$

(whole number \(\Rightarrow\) charge is quantised)

### Listing 6 — Combining Thomson and Millikan to get the electron mass

Thomson gives the RATIO: \(q/m = 1.76 \times 10^{11}\ \mathrm{C\,kg^{-1}}\). Millikan gives the CHARGE: \(e = 1.6 \times 10^{-19}\ \mathrm{C}\). Electron mass \(=\) charge \(\div\) (charge-to-mass ratio):

$$
m = \frac{e}{q/m} = \frac{1.6 \times 10^{-19}}{1.76 \times 10^{11}} \approx 9.1 \times 10^{-31}\ \mathrm{kg}
$$

Neither experiment alone gives the mass; together they do. Trap: Thomson = ratio only; Millikan = charge only.

### Listing 7 — Key values, constants and milestones
| Quantity / item | Value / fact |
|---|---|
| Electron charge-to-mass ratio (q/m) | 1.76 × 10¹¹ C kg⁻¹ (precise 1.759 × 10¹¹; ≈ 1.8 × 10¹¹) |
| Elementary charge (e) | 1.6 × 10⁻¹⁹ C (precise 1.602 × 10⁻¹⁹ C) |
| Electron mass | 9.1 × 10⁻³¹ kg |
| Proton / hydrogen-ion mass | 1.67 × 10⁻²⁷ kg |
| Mass ratio electron : hydrogen | electron ≈ 1/1800 of hydrogen (modern ≈ 1/1837) |
| Gravitational acceleration (g) | 9.8 m s⁻² (Millikan equilibrium) |
| J.J. Thomson | measured q/m in 1897; discovered the electron; plum pudding model ~1904 |
| Robert A. Millikan | oil-drop experiment ~1909 (refined ~1913); Nobel Prize 1923 |
| Velocity-selector condition | undeflected \(\Rightarrow qE = qvB \Rightarrow v = E/B\) (charge cancels) |
| Centripetal condition | \(qvB = mv^{2}/r \Rightarrow q/m = v/(Br) \Rightarrow q/m = E/(B^{2}r)\) |

### Listing 8 — Memory hooks
```text
WHO FOUND WHAT (the #1 lost mark):
    Thomson  → The ratio (q/m).      "Thomson Tangled them."
    Millikan → the Magnitude (e).    "Millikan Measured one."
    Mass of electron = combine both.

ORDER OF THE ATOMIC MODELS (P-N-L-W):
    Plum pudding  (Thomson)      ← we are here
    Nucleus       (Rutherford, gold foil)
    Levels        (Bohr energy levels)
    Waves         (Schrödinger / matter waves)
    Image: a plum pudding cracked open to a hard nucleus,
    organised into neat levels, dissolving into a blur of waves.

EVALUATE STRUCTURE (plum pudding):
    Strengths (electrons in, neutral atom, divisible atom)
    → Limitation (positive distribution untested)
    → Judgement (reasonable for the time; overturned by gold foil).
    Use contrast words: "but", "whereas", "in contrast".
```
