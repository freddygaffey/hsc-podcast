---
title: "Supplementary Materials — Charged Particles in Electric Fields: The Conceptual Picture"
module: M6
lesson: "01"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it's the read-along reference.

### Listing 1 — Field strength of a uniform field (E = V/d), worked

Uniform field between parallel plates:

$$
E = \frac{V}{d}
$$

where:

- \(E\) = electric field strength (\(\mathrm{V\,m^{-1}}\), equivalently \(\mathrm{N\,C^{-1}}\))
- \(V\) = potential difference (volts, V)
- \(d\) = plate separation (metres, m)

Worked: \(V = 100\ \mathrm{V}\), \(d = 5.0\ \mathrm{cm} = 5.0\times10^{-2}\ \mathrm{m}\):

$$
E = \frac{100}{5.0\times10^{-2}} = 2000\ \mathrm{V\,m^{-1}}\ (= 2000\ \mathrm{N\,C^{-1}})
$$

Unit check: \(1\ \mathrm{V\,m^{-1}} = 1\ \mathrm{N\,C^{-1}}\) (the two units of \(E\) are identical). Direction: field points from the \(+\) plate to the \(-\) plate.

### Listing 2 — Direction conventions and key constants
| Quantity / rule | Value or statement |
|---|---|
| Field line direction | From the + plate to the − plate |
| Force on a + charge | Along E (toward the − plate) |
| Force on a − charge (electron) | Opposite to E (toward the + plate) |
| Field defined by | Force per unit charge on a small + test charge |
| Electron charge | −1.6 × 10^-19 C (magnitude 1.602 × 10^-19 C) |
| Proton charge | +1.60 × 10^-19 C |
| Electron mass | 9.1 × 10^-31 kg |
| Proton mass | 1.67 × 10^-27 kg |
| Proton / electron mass ratio | ≈ 1836 (electron's acceleration ~1836× larger, opposite sign) |
| Units of E | N C^-1 = V m^-1 (identical) |
| Unit of V | volt = J C^-1 |
| Units of W, K | joule (J) |
| Path: fired across the field | Parabola (projectile-motion structure) |
| Path: released from rest / along the field | Straight-line uniform acceleration |

### Listing 3 — From force and work to E = V/d and v = √(2qV/m)

Core relations:

$$
\begin{aligned}
\text{Force on a charge:} \quad & F = qE \\
\text{Newton's second law:} \quad & F = ma \;\Rightarrow\; a = \frac{F}{m} = \frac{qE}{m} \\
\text{Work through a p.d.:} \quad & W = qV \\
\text{Work as force} \times \text{distance:} \quad & W = qEd \quad (d = \text{distance moved along the field}) \\
\text{Kinetic energy:} \quad & K = \tfrac{1}{2}mv^{2}
\end{aligned}
$$

Show \(E = V/d\) falls out of the energy picture:

$$
qEd = qV \quad (\text{equate the two expressions for } W)
$$

$$
\text{cancel } q:\quad Ed = V \quad\Rightarrow\quad E = \frac{V}{d} \quad\checkmark\ (\text{matches Listing 1})
$$

Speed gained from rest through voltage \(V\): with \(W = qV\) and \(W = K = \tfrac{1}{2}mv^{2}\),

$$
qV = \tfrac{1}{2}mv^{2} \;\Rightarrow\; v^{2} = \frac{2qV}{m} \;\Rightarrow\; v = \sqrt{\frac{2qV}{m}}
$$

Unit notes: \(1\ \mathrm{V} = 1\ \mathrm{J\,C^{-1}}\) (a volt is joules per coulomb), so \(qV \to (\mathrm{C})(\mathrm{J\,C^{-1}}) = \mathrm{J}\) = energy \(\checkmark\).

### Listing 4 — Worked Example A: electron gun (energy → speed)

An electron, from rest, accelerated through \(V = 100\ \mathrm{V}\), with \(e = 1.6\times10^{-19}\ \mathrm{C}\) (magnitude of electron charge) and \(m_e = 9.1\times10^{-31}\ \mathrm{kg}\).

(a) Energy gained:

$$
W = qV = (1.6\times10^{-19})(100) = 1.6\times10^{-17}\ \mathrm{J}
$$

(b) This work becomes kinetic energy, \(W = \tfrac{1}{2}mv^{2}\):

$$
1.6\times10^{-17} = \tfrac{1}{2}(9.1\times10^{-31})v^{2}
$$

$$
v^{2} = \frac{2\times1.6\times10^{-17}}{9.1\times10^{-31}} = 3.516\times10^{13}
$$

$$
v = 5.9\times10^{6}\ \mathrm{m\,s^{-1}}
$$

Sanity check: \(\approx 5900\ \mathrm{km\,s^{-1}} \approx 2\%\) of \(c\) \(\to\) classical mechanics is fine. Context: cathode (\(-\), hot filament) emits electrons (thermionic emission); the field accelerates them to the anode (\(+\)); a hole forms the beam (cathode ray).

### Listing 5 — Worked Example B: proton fired sideways (parabolic trajectory)

Horizontal parallel plates, \(d = 5\ \mathrm{cm} = 0.05\ \mathrm{m}\), \(V = 2.56\ \mathrm{V}\), upper plate \(+\). Proton fired horizontally just below the top plate. Gravity ignored. \(m_p = 1.67\times10^{-27}\ \mathrm{kg}\), \(q_p = +1.60\times10^{-19}\ \mathrm{C}\).

(a) Field strength:

$$
E = \frac{V}{d} = \frac{2.56}{0.05} = 51.2\ \mathrm{V\,m^{-1}} \quad (\text{directed downward, } + \to -)
$$

(b) Force on proton (positive \(\Rightarrow\) force ALONG \(E\), i.e. downward):

$$
F = qE = (1.60\times10^{-19})(51.2) = 8.192\times10^{-18}\ \mathrm{N}
$$

$$
a = \frac{F}{m} = \frac{8.192\times10^{-18}}{1.67\times10^{-27}} = 4.9\times10^{9}\ \mathrm{m\,s^{-2}}\ (\text{down})
$$

(c) Time to cross the gap (vertical: \(u = 0\), \(s = \tfrac{1}{2}at^{2}\)):

$$
0.05 = \tfrac{1}{2}(4.9\times10^{9})t^{2}
$$

$$
t^{2} = \frac{0.10}{4.9\times10^{9}} = 2.04\times10^{-11}
$$

$$
t = 4.5\times10^{-6}\ \mathrm{s}\ (4.5\ \mu\mathrm{s})
$$

(d) Vertical velocity gained:

$$
v_{\text{vert}} = a t = (4.9\times10^{9})(4.5\times10^{-6}) = 2.2\times10^{4}\ \mathrm{m\,s^{-1}}\ (\text{downward})
$$

(e) Horizontal velocity: UNCHANGED throughout (no horizontal force) = the injection speed.

(f) Resultant = constant horizontal + growing vertical \(\to\) PARABOLA. Exit angle matches a gravitational projectile of the same horizontal speed.

Why ignore gravity here: the electric force \(\approx 8\times10^{-18}\ \mathrm{N}\); the weight \(= m_p g \approx 1.6\times10^{-26}\ \mathrm{N}\). The electric force is \(\approx 10^{8}\times\) larger \(\to\) gravity negligible (justified).
