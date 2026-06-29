---
title: "Supplementary Materials — J.J. Thomson and the Discovery of the Electron"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Crossed fields (the velocity selector)

When the electric and magnetic fields are adjusted so the beam passes
straight through (zero net deflection), the two forces are balanced.

The electric force equals the magnetic force:

$$
F_{E} = F_{B} \quad\Rightarrow\quad q E = q v B
$$

where \(q\) = particle charge, \(E\) = electric field, \(B\) = magnetic field, \(v\) = speed. The charge \(q\) cancels from both sides:

$$
E = v B
$$

Solve for the speed:

$$
v = \frac{E}{B}
$$

Note: the speed comes out independent of the charge AND the mass.
The velocity selector measures v using only the two field strengths
that the experimenter sets directly.

### Listing 2 — Charge-to-mass ratio (two routes)

Once the speed v is known from the crossed fields (Listing 1), the
charge-to-mass ratio follows. The textbook/syllabus route uses the
MAGNETIC field acting alone; an equivalent route uses the ELECTRIC
field acting alone. Either way the single quantity that drops out is
q/m. Neither q nor m can be found separately from this experiment.

Route A — magnetic field alone (the syllabus derivation).
Switch the electric field off. The magnetic force is always perpendicular
to the motion, so it cannot change the speed — it bends the beam into a
circular arc of radius r. The magnetic force supplies the centripetal force.

The magnetic force supplies the centripetal force:

$$
q v B = \frac{m v^{2}}{r}
$$

Cancel one \(v\) and rearrange for the charge-to-mass ratio:

$$
\frac{q}{m} = \frac{v}{B r}
$$

and since \(v = E / B\) from Listing 1 (same \(B\) if the field is unchanged):

$$
\frac{q}{m} = \frac{E}{B^{2} r}
$$

Route B — electric field alone (projectile-style deflection).
Switch the magnetic field off. The beam curves like a projectile while it
travels the plate length L, then drifts to the screen. Measure the
deflection y.

Electric force on particle:

$$
F = q E
$$

Acceleration while between plates:

$$
a = \frac{F}{m} = \frac{q E}{m}
$$

Time spent between plates (\(L\) = plate length, \(v\) from Listing 1):

$$
t = \frac{L}{v}
$$

Sideways deflection inside plates:

$$
y = \tfrac{1}{2} a t^{2} = \tfrac{1}{2}\,\frac{q E}{m}\left(\frac{L}{v}\right)^{2}
$$

Rearrange to isolate the charge-to-mass ratio:

$$
\frac{q}{m} = \frac{2 y v^{2}}{E L^{2}}
$$

Substitute \(v = E / B\) (from Listing 1) to write it using \(B\) instead of \(v\):

$$
\frac{q}{m} = \frac{2 y E}{B^{2} L^{2}}
$$

### Listing 3 — Force laws used above (HSC formula sheet)

- Electric force on a charge: \(F = q E\)
- Electric field between parallel plates: \(E = V / d\) (\(V\) = voltage, \(d\) = plate separation)
- Magnetic force on a moving charge: \(F = q v B\) (velocity perpendicular to \(B\))
- Magnetic force, general angle \(\theta\): \(F = q v B \sin\theta\)
- Centripetal force (circular motion): \(F = m v^{2} / r\)
- Charge in a \(B\) field (radius of arc): \(r = m v / (q B)\)
- Work done by an electric field: \(W = q V\)
- Kinetic energy gained from rest: \(q V = \tfrac{1}{2} m v^{2}\)

### Listing 4 — Key values

| Quantity | Value | Note |
|----------|-------|------|
| Electron charge-to-mass ratio (modern) | 1.76 x 10^11 C/kg | accepted e/m; textbook quotes 1.759 x 10^11 |
| Hydrogen-ion charge-to-mass ratio | ~9.6 x 10^7 C/kg | from electrolysis (~1 x 10^8) |
| Ratio of the two | ~1800 | Thomson's 1897 estimate was ~1000 |
| Elementary charge e | 1.602 x 10^-19 C | measured by Millikan, 1909 |
| Electron mass | 9.109 x 10^-31 kg | ~1/1836 of a proton |
| Proton mass | 1.673 x 10^-27 kg | for comparison |
| Hydrogen atom mass | 1.673 x 10^-27 kg | the lightest atom |
| Cathode ray speed (Thomson) | up to ~10^8 m/s | roughly 0.1c to 0.3c |

### Listing 5 — Worked example: finding speed, then charge-to-mass ratio

A cathode ray beam passes between plates 10 mm apart with 300 V across
them. A magnetic field of 1.00 x 10^-2 T is adjusted until the beam is
undeflected. Find the beam speed. Then, with B switched off, the beam
deflects 5.0 mm while crossing plates of length L = 50 mm. Find q/m.

**Step 1 — electric field between the plates:**

$$
E = \frac{V}{d} = \frac{300}{10\times 10^{-3}} = 3.0\times 10^{4}\ \mathrm{V/m}
$$

**Step 2 — speed from the balanced (crossed) fields** [Listing 1]:

$$
v = \frac{E}{B} = \frac{3.0\times 10^{4}}{1.00\times 10^{-2}} = 3.0\times 10^{6}\ \mathrm{m/s}
$$

**Step 3 — charge-to-mass ratio from the electric-only deflection** [Listing 2, Route B], with \(y = 5.0\times 10^{-3}\ \mathrm{m}\), \(L = 50\times 10^{-3}\ \mathrm{m}\):

$$
\begin{aligned}
\frac{q}{m} &= \frac{2 y v^{2}}{E L^{2}} \\
&= \frac{2 \times 5.0\times 10^{-3} \times (3.0\times 10^{6})^{2}}{3.0\times 10^{4} \times (50\times 10^{-3})^{2}} \\
&= \frac{2 \times 5.0\times 10^{-3} \times 9.0\times 10^{12}}{3.0\times 10^{4} \times 2.5\times 10^{-3}} \\
&= \frac{9.0\times 10^{10}}{75} \\
&= 1.2\times 10^{9}\ \mathrm{C/kg}
\end{aligned}
$$

(order-of-magnitude teaching figure for this simplified setup)

Interpretation: even a rough setup yields a q/m far larger than any
ion, which is the whole point — the particle's mass must be tiny. A
real Thomson-grade apparatus, measured carefully, returns the accepted
value of about 1.76 x 10^11 C/kg given in Listing 4.

### Listing 6 — Millikan's oil-drop experiment (the charge on the electron)

Thomson's experiment gives only the RATIO q/m. To split the charge and
the mass apart you need one of them measured on its own. Millikan (1909)
measured the charge q directly by suspending charged oil drops in a
uniform electric field between horizontal plates.

When a drop hangs stationary, the forces balance — electric force (up) equals weight (down):

$$
q E = m g
$$

Solve for the charge on the drop (\(E = V / d\) for parallel plates):

$$
q = \frac{m g}{E}
$$

Key result: q always came out as a whole-number multiple of one
smallest packet — the elementary charge e ≈ 1.6 x 10^-19 C. Charge is
quantised. (Millikan: Nobel Prize 1923.)

### Listing 7 — Putting it together: the mass of the electron

Combine Thomson's ratio with Millikan's charge to isolate the mass.

From Thomson: \(q/m = 1.76\times 10^{11}\ \mathrm{C/kg}\). From Millikan: \(q = e = 1.602\times 10^{-19}\ \mathrm{C}\).

$$
m = \frac{q}{q/m} = \frac{1.602\times 10^{-19}}{1.76\times 10^{11}} = 9.1\times 10^{-31}\ \mathrm{kg}
$$

This is the modern electron mass, about 1/1836 of a proton and about
1/1800 of the lightest atom (hydrogen) — the quantitative meaning of
"a particle nearly two thousand times lighter than the lightest atom."
