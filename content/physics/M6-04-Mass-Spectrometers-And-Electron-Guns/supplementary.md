---
title: "Supplementary Materials — Mass Spectrometers and Electron Guns: Fields Applied"
module: M6
lesson: "04"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference for the worked examples narrated in the script.

### Listing 1 — Electron gun: energy gained and exit speed (V = 100 V)

An electron starts from rest and is accelerated through \(V = 100\ \mathrm{V}\). Constants: \(m = 9.1 \times 10^{-31}\ \mathrm{kg}\), \(q = 1.6 \times 10^{-19}\ \mathrm{C}\).

(a) ENERGY GAINED — work done by the field becomes kinetic energy:

$$
W = qV = (1.6 \times 10^{-19})(100) = 1.6 \times 10^{-17}\ \mathrm{J} \quad (\text{this is also the KE gained})
$$

(b) EXIT SPEED — all the work becomes kinetic energy (starts from rest):

$$
qV = \tfrac{1}{2} m v^{2}
$$

$$
v = \sqrt{\frac{2W}{m}} = \sqrt{\frac{2 \times 1.6 \times 10^{-17}}{9.1 \times 10^{-31}}} = \sqrt{3.516 \times 10^{13}} = 5.9 \times 10^{6}\ \mathrm{m/s} \quad (\approx 2\%\ \text{of the speed of light})
$$

Equivalent single formula: \(v = \sqrt{2qV / m}\).

### Listing 2 — Magnetic deflection: radius of the electron's path

The \(5.9 \times 10^{6}\ \mathrm{m/s}\) electron enters a uniform magnetic field \(B = 6.0\ \mathrm{mT} = 6.0 \times 10^{-3}\ \mathrm{T}\), perpendicular to its velocity.

The magnetic force supplies the centripetal force:

$$
qvB = \frac{m v^{2}}{r} \quad\Rightarrow\quad r = \frac{m v}{q B}
$$

$$
r = \frac{9.1 \times 10^{-31} \times 5.9 \times 10^{6}}{1.6 \times 10^{-19} \times 6.0 \times 10^{-3}} = \frac{5.369 \times 10^{-24}}{9.6 \times 10^{-22}} = 5.6 \times 10^{-3}\ \mathrm{m} = 5.6\ \mathrm{mm}
$$

Note: the speed is UNCHANGED by the magnetic field (it does no work); the field only bends the path. Light particle \(\Rightarrow\) small radius.

### Listing 3 — Velocity selector: the pass-through condition

Crossed (perpendicular) E and B fields. Two forces on a moving ion, arranged to point in OPPOSITE directions:

- electric force \(F_E = qE\) (independent of speed)
- magnetic force \(F_B = qvB\) (increases with speed)

The ion passes straight through (zero net force) when the forces balance:

$$
F_E = F_B \quad\Rightarrow\quad qE = qvB
$$

\(q\) cancels from both sides:

$$
E = vB \quad\Rightarrow\quad v = \frac{E}{B}
$$

Only this ONE speed passes. Faster ions: \(F_B > F_E\), deflected one way. Slower ions: \(F_E > F_B\), deflected the other way — both are blocked.

Underlying law (full force in combined fields) — the Lorentz force:

$$
\vec{F} = q\vec{E} + q\,\vec{v} \times \vec{B}
$$

The selector sets the \(q\vec{E}\) term and the \(q\,\vec{v} \times \vec{B}\) term equal and opposite.

KEY POINT: \(v = E/B\) contains no \(m\) and no \(q\) — the selector sorts by SPEED, not by mass. It guarantees every ion exits at the same speed.

### Listing 4 — Full mass spectrometer: separating Ne-20 and Ne-22

Singly-ionised neon, \(q = 1.6 \times 10^{-19}\ \mathrm{C}\), accelerated through \(V = 1000\ \mathrm{V}\), through a velocity selector, then into \(B = 0.50\ \mathrm{T}\). Masses: Ne-20 \(m = 3.32 \times 10^{-26}\ \mathrm{kg}\); Ne-22 \(m = 3.65 \times 10^{-26}\ \mathrm{kg}\).

**Stage A — Accelerate:** speed after acceleration (use Ne-20):

$$
qV = \tfrac{1}{2} m v^{2}
$$

$$
v = \sqrt{\frac{2qV}{m}} = \sqrt{\frac{2 \times 1.6 \times 10^{-19} \times 1000}{3.32 \times 10^{-26}}} = \sqrt{9.64 \times 10^{9}} = 9.8 \times 10^{4}\ \mathrm{m/s}
$$

(the velocity selector then ensures BOTH isotopes travel at this \(v\))

**Stage D — Deflect:** radius \(r = m v / (q B)\).

Ne-20:

$$
r = \frac{3.32 \times 10^{-26} \times 9.8 \times 10^{4}}{1.6 \times 10^{-19} \times 0.50} = \frac{3.25 \times 10^{-21}}{8.0 \times 10^{-20}} = 0.041\ \mathrm{m} \approx 4.1\ \mathrm{cm}
$$

Ne-22 (same \(q\), same selected \(v\), same \(B\); only \(m\) is larger):

$$
r = \frac{3.65 \times 10^{-26} \times 9.8 \times 10^{4}}{8.0 \times 10^{-20}} = 0.045\ \mathrm{m} \approx 4.5\ \mathrm{cm}
$$

RESULT: Ne-22 lands ~4 mm further out than Ne-20. Same \(q\), same \(v\), same \(B\) \(\Rightarrow\) \(r \propto m\) \(\Rightarrow\) separation is by MASS alone. Detector POSITION identifies the isotope; NUMBER of hits gives abundance.

**Caveat — which model applies:**

- WITH a velocity selector (all ions same \(v = E/B\)): \(r \propto m\)
- WITHOUT a selector (all ions same \(qV\), so \(v\) depends on \(m\)): \(v = \sqrt{2qV/m} \Rightarrow r = \sqrt{2mV/q}/B \Rightarrow r \propto \sqrt{m/q}\)

The standard HSC velocity-selector spectrometer uses \(r \propto m\).

### Listing 5 — Exam question 2 worked (electron through 200 V)

Electron from rest through \(V = 200\ \mathrm{V}\). Find the final speed. \(m = 9.1 \times 10^{-31}\ \mathrm{kg}\), \(q = 1.6 \times 10^{-19}\ \mathrm{C}\).

$$
qV = \tfrac{1}{2} m v^{2}
$$

$$
v = \sqrt{\frac{2qV}{m}} = \sqrt{\frac{2 \times 1.6 \times 10^{-19} \times 200}{9.1 \times 10^{-31}}} = \sqrt{\frac{6.4 \times 10^{-17}}{9.1 \times 10^{-31}}} = \sqrt{7.03 \times 10^{13}} = 8.4 \times 10^{6}\ \mathrm{m/s}
$$

Check: doubling \(V\) (\(100\ \mathrm{V} \to 200\ \mathrm{V}\)) multiplies \(v\) by \(\sqrt{2}\), since \(v \propto \sqrt{V}\). \(5.9 \times 10^{6} \times \sqrt{2} \approx 8.4 \times 10^{6}\ \mathrm{m/s}\). ✓

### Listing 6 — Equations used in this episode (HSC formula sheet)

- uniform field strength (parallel plates): \(E = \dfrac{V}{d}\)
- electric force on a charge: \(F = qE\)
- Newton's second law (gun acceleration): \(F = ma\)
- work done by the field: \(W = qV\) (also \(W = qEd\))
- kinetic energy: \(K = \tfrac{1}{2} m v^{2}\)
- energy balance (accelerated from rest): \(qV = \tfrac{1}{2} m v^{2} \Rightarrow v = \sqrt{2qV/m}\)
- magnetic force on a moving charge: \(F = qvB = qvB \sin\theta\) (max at \(\theta = 90°\))
- velocity-selector pass speed: \(v = \dfrac{E}{B}\) (from \(qE = qvB\))
- magnetic force = centripetal force: \(qvB = \dfrac{m v^{2}}{r}\)
- radius of circular path: \(r = \dfrac{m v}{q B} \Rightarrow m = \dfrac{r q B}{v}\)
- Lorentz force (combined fields): \(\vec{F} = q\vec{E} + q\,\vec{v} \times \vec{B}\)

### Listing 7 — Key constants and particle data

| Quantity | Symbol | Value | Note |
|----------|--------|-------|------|
| Elementary charge | e | 1.6 × 10^-19 C | electron charge = −e; use magnitude in qV and r |
| Electron mass | m_e | 9.1 × 10^-31 kg | ~1/1836 of a proton |
| Proton mass | m_p | 1.67 × 10^-27 kg | ~1836× the electron → much larger radius |
| Alpha particle charge | — | +3.2 × 10^-19 C (= +2e) | doubly ionised helium nucleus |
| Alpha particle mass | — | ≈ 6.64 × 10^-27 kg | ≈ 4 × proton mass |
| Neon-20 mass | — | 3.32 × 10^-26 kg | lighter isotope, tighter radius |
| Neon-22 mass | — | 3.65 × 10^-26 kg | heavier isotope, wider radius |
| Reference: 100 V electron gun exit speed | — | 5.9 × 10^6 m/s | ≈ 2% of c |
| Reference: that electron in 6.0 mT | r | 5.6 mm | from r = mv/(qB) |

### Listing 8 — Field roles and the three-stage (ASD) summary

**The one-line spine**

- Electric field \(\to\) changes SPEED / energy; DOES work.
- Magnetic field \(\to\) changes DIRECTION only; does NO work (speed constant).

**Electron gun (one field).** Thermionic emission \(\to\) E field accelerates \(\to\) \(qV = \tfrac{1}{2}mv^{2}\). Function: a beam of electrons at a known, tunable speed (set by \(V\)).

**Mass spectrometer — mnemonic "ASD" (Accelerate, Select, Deflect):**

- **A** — Accelerate (electric field): \(qV = \tfrac{1}{2}mv^{2}\) (gives the ions speed)
- **S** — Select (crossed E and B): \(v = E/B\) (one speed passes; not mass)
- **D** — Deflect (magnetic field): \(r = \dfrac{m v}{q B}\) (\(r \propto m\): heavier = wider)

Readout: detector POSITION = mass; NUMBER of hits = isotopic abundance.
