---
title: "Supplementary Materials — The Great Comparison: Fields, Forces and Paths"
module: M6
lesson: "03"
script: script.md
---

# Supplementary Materials

Key equations, derivations, the four-scenario comparison, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The same electron through an electric field, then a magnetic field (worked example)

Constants: electron charge magnitude \(q = 1.6 \times 10^{-19}\ \mathrm{C}\), electron mass \(m = 9.1 \times 10^{-31}\ \mathrm{kg}\).

**Stage 1 — Electric field accelerates the electron (does work, changes speed).** An electron starts from rest, accelerated through \(V = 100\ \mathrm{V}\) (electron gun).

(a) Work done by the field = kinetic energy gained:

$$
W = qV = (1.6 \times 10^{-19})(100) = 1.6 \times 10^{-17}\ \mathrm{J}
$$

(b) Equate to kinetic energy and solve for speed:

$$
W = \tfrac{1}{2}mv^{2}
$$

$$
v = \sqrt{\frac{2W}{m}} = \sqrt{\frac{2(1.6 \times 10^{-17})}{9.1 \times 10^{-31}}} = 5.9 \times 10^{6}\ \mathrm{m\,s^{-1}} \quad (\approx 2\%\ \text{of the speed of light})
$$

The E-field DID work (\(1.6 \times 10^{-17}\ \mathrm{J}\)) and INCREASED the speed from 0.

**Stage 2 — That same electron enters a magnetic field (does no work, bends into a circle).** The electron (\(v = 5.9 \times 10^{6}\ \mathrm{m\,s^{-1}}\)) enters a uniform field \(B = 6.0\ \mathrm{mT} = 6.0 \times 10^{-3}\ \mathrm{T}\), perpendicular to its velocity.

$$
r = \frac{mv}{qB} = \frac{(9.1 \times 10^{-31})(5.9 \times 10^{6})}{(6.0 \times 10^{-3})(1.6 \times 10^{-19})} = 5.6 \times 10^{-3}\ \mathrm{m} = 5.6\ \mathrm{mm}
$$

The B-field does NO work — speed stays \(5.9 \times 10^{6}\ \mathrm{m\,s^{-1}}\) — but the perpendicular force bends it into a circle of radius \(5.6\ \mathrm{mm}\).

CONTRAST: same electron, two fields.

- Electric field \(\to\) did work, changed speed, parabola if launched across the field.
- Magnetic field \(\to\) no work, speed unchanged, circle.

### Listing 2 — The four scenarios compared by axis (the structure of a band-6 answer)
| Comparison axis | Uniform gravity (projectile) | Satellite orbit (radial gravity) | Uniform electric field | Uniform magnetic field |
|---|---|---|---|---|
| Force law | \(F = mg\) | \(F = \dfrac{GMm}{r^{2}}\) | \(F = qE\) | \(F = qvB \sin\theta\) |
| Force depends on | mass | mass and \(1/r^{2}\) | charge | charge AND speed |
| Acts on a stationary object? | Yes | Yes | Yes | No — motion required |
| Direction of force | along field (attractive, "down") | toward central body (attractive) | along field (+q) / opposite (−q): attract or repel | perpendicular to both v and B |
| Does the field do work? | Yes | No (circular) / Yes (elliptical) | Yes | No (F ⊥ v always) |
| Path projected across the field | parabola | circle / ellipse (orbit) | parabola | circle |

### Listing 3 — The key field equations, in symbols and units

**Gravitational (uniform / surface):**

$$
F = mg \qquad g = \frac{GM}{r^{2}}
$$

- \(F\) in \(\mathrm{N}\), \(m\) in \(\mathrm{kg}\), \(g\) in \(\mathrm{N\,kg^{-1}}\ (\equiv \mathrm{m\,s^{-2}})\)
- \(g = GM/r^{2}\) is the field strength, \(\mathrm{N\,kg^{-1}}\)

**Gravitational (orbital / radial):**

$$
F_g = \frac{GMm}{r^{2}} \qquad v = \sqrt{\frac{GM}{r}} \qquad F_c = \frac{mv^{2}}{r} \qquad a_c = \frac{v^{2}}{r}
$$

- \(F_g\) — attractive, toward central body; \(r\) = centre-to-centre (\(\mathrm{m}\))
- \(v\) — orbital speed (derived: \(F_g = F_c\))
- \(F_c,\ a_c\) — centripetal force / acceleration

**Electric (uniform field, parallel plates):**

$$
E = \frac{V}{d} \qquad F = qE \qquad a = \frac{qE}{m} \qquad W = qV = qEd \qquad K = \tfrac{1}{2}mv^{2}
$$

- \(E\) — field strength, \(\mathrm{N\,C^{-1}}\ (\equiv \mathrm{V\,m^{-1}})\)
- \(F\) — electric force, \(q\) in \(\mathrm{C}\)
- \(a\) — constant acceleration (from \(F = ma\))
- \(W\) — work done on charge as it moves ALONG the field, \(\mathrm{J}\)
- \(K\) — kinetic energy gained, \(\mathrm{J}\)
- Projectile components: across field \(x = v_x t\); along field \(y = \tfrac{1}{2}at^{2}\), \(v_y = at\) (the parabola)

**Magnetic:**

$$
F = qvB \sin\theta
$$

- \(\theta\) = angle between \(v\) and \(B\); max at \(90°\), zero if \(v \parallel B\) or \(v = 0\)
- \(B\) in tesla (\(\mathrm{T}\))
- magnetic force does ZERO work (\(F \perp v\) at all times)

### Listing 4 — Derivations of orbital speed and magnetic radius (equate to the centripetal force)

**Orbital speed — equate gravitational force to the centripetal force:**

$$
\begin{aligned}
\frac{GMm}{r^{2}} &= \frac{mv^{2}}{r} \\
\frac{GM}{r} &= v^{2} \\
v &= \sqrt{\frac{GM}{r}}
\end{aligned}
$$

Larger orbital radius \(r\) \(\Rightarrow\) lower orbital speed and longer period.

**Magnetic radius — equate magnetic force to the centripetal force:**

$$
\begin{aligned}
qvB &= \frac{mv^{2}}{r} \\
qB &= \frac{mv}{r} \\
r &= \frac{mv}{qB}
\end{aligned}
$$

- Larger mass \(m\) or speed \(v\) \(\Rightarrow\) larger radius (heavier isotope, bigger arc).
- Larger charge \(q\) or field \(B\) \(\Rightarrow\) smaller radius (tighter curve).

**The unifying point:** In every scenario the stated force is the NET force, so \(F = ma\) applies to all four. The differences are entirely in (i) the force law and (ii) the direction of the force relative to \(v\):

- force fixed in direction \(\to\) parabola, field does work
- force \(\perp\) to velocity \(\to\) circle, field does no work

### Listing 5 — Reference values and constants
| Quantity | Value |
|---|---|
| Electron charge magnitude | 1.6 × 10^-19 C |
| Electron mass | 9.1 × 10^-31 kg |
| Proton mass | 1.67 × 10^-27 kg (≈ 1836 × electron) |
| Proton charge magnitude | 1.6 × 10^-19 C |
| Speed after 100 V acceleration (electron) | 5.9 × 10^6 m s^-1 |
| E-field for 100 V across 5.0 cm plates | \(E = V/d = 2000\ \mathrm{V\,m^{-1}}\) |
| Universal gravitational constant G | 6.67 × 10^-11 N m² kg^-2 |
| g at Earth's surface | 9.8 N kg^-1 (≡ m s^-2) |
| Orbital speed, ~250 km altitude LEO | ≈ 7.75 × 10^3 m s^-1 (~27 900 km h^-1) |
