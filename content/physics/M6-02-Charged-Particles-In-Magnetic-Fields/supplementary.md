---
title: "Supplementary Materials — Charged Particles in Magnetic Fields: Circular Motion and the Cyclotron"
module: M6
lesson: "02"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference. Reference figures and constants follow the NSW HSC Physics data sheet.

### Listing 1 — Magnetic force on a moving charge

$$
F = q v_{\perp} B = q v B \sin\theta
$$

where:

- \(F\) = magnitude of the magnetic force (newtons, N)
- \(q\) = magnitude of the charge (coulombs, C)
- \(v\) = speed of the charge (metres per second, \(\mathrm{m\,s^{-1}}\))
- \(B\) = magnetic field strength (flux density) (teslas, T)
- \(\theta\) = angle between the velocity \(v\) and the field \(B\)
- \(v_{\perp}\) = component of velocity perpendicular to \(B = v \sin\theta\)

Cases:

- \(\theta = 90^{\circ}\) (\(v\) perpendicular to \(B\)): \(\sin\theta = 1 \to F = qvB\) (MAXIMUM)
- \(\theta = 0^{\circ}\) or \(180^{\circ}\) (\(v\) parallel to \(B\)): \(\sin\theta = 0 \to F = 0\) (no force)
- \(v = 0\) (charge at rest): \(F = 0\) (no force)

Direction: perpendicular to BOTH \(v\) and \(B\). Right-hand push (palm) rule — for a POSITIVE charge: fingers \(\to\) external field \(B\) (N to S); thumb \(\to\) velocity of positive charge (= conventional current); force \(\to\) straight out of the palm. For a NEGATIVE charge (e.g. an electron): reverse the result (or point the thumb opposite to the electron's velocity, or use the left hand).

### Listing 2 — Deriving r = mv/qB (equate magnetic force and centripetal force)

Newton's second law, magnetic force the only force:

$$
F_{\text{net}} = ma \quad\text{and}\quad F_{\text{magnetic}} = qvB \;\Rightarrow\; qvB = ma
$$

The acceleration is centripetal, \(a = v^{2}/r\):

$$
qvB = \frac{m v^{2}}{r}
$$

(THE KEY STEP: the magnetic force PROVIDES the centripetal force). Cancel one factor of \(v\) from both sides:

$$
qB = \frac{m v}{r}
$$

Rearrange for the radius:

$$
r = \frac{mv}{qB}
$$

Behaviour:

- \(r \propto m\) (heavier \(\to\) larger circle)
- \(r \propto v\) (faster \(\to\) larger circle)
- \(r \propto 1/q\) (more charge \(\to\) tighter circle)
- \(r \propto 1/B\) (stronger field \(\to\) tighter circle)

### Listing 3 — Worked Example A: radius of an electron's path

An electron at \(v = 5.9\times10^{6}\ \mathrm{m\,s^{-1}}\) enters \(B = 6.0\ \mathrm{mT}\) perpendicular to its motion. Find the radius \(r\).

Data: \(m = 9.1\times10^{-31}\ \mathrm{kg}\), \(q = 1.6\times10^{-19}\ \mathrm{C}\). Convert: \(6.0\ \mathrm{mT} = 6.0\times10^{-3}\ \mathrm{T}\) (millitesla-to-tesla conversion).

$$
r = \frac{mv}{qB} = \frac{9.1\times10^{-31}\times5.9\times10^{6}}{1.6\times10^{-19}\times6.0\times10^{-3}}
$$

$$
\text{numerator} = 5.369\times10^{-24}, \qquad \text{denominator} = 9.6\times10^{-22}
$$

$$
r = 5.6\times10^{-3}\ \mathrm{m} = 5.6\ \mathrm{mm}
$$

### Listing 4 — Worked Example B: force, then radius

Electrons at \(v = 1.2\times10^{6}\ \mathrm{m\,s^{-1}}\) enter \(B = 2.6\times10^{-3}\ \mathrm{T}\) at right angles (\(\theta = 90^{\circ}\)). Find (a) the force on each electron, (b) the radius of the path.

(a) \(\theta = 90^{\circ} \to \sin\theta = 1\), so \(F = qvB\):

$$
F = (1.6\times10^{-19})(1.2\times10^{6})(2.6\times10^{-3}) = 5.0\times10^{-16}\ \mathrm{N}
$$

(b)

$$
r = \frac{mv}{qB} = \frac{9.1\times10^{-31}\times1.2\times10^{6}}{1.6\times10^{-19}\times2.6\times10^{-3}}
$$

$$
\text{numerator} = 1.092\times10^{-24}, \qquad \text{denominator} = 4.16\times10^{-22}
$$

$$
r = 2.6\times10^{-3}\ \mathrm{m} = 2.6\ \mathrm{mm}
$$

### Listing 5 — Worked Example C: reverse problem, find the speed from the radius

Find the speed of an electron moving in an arc of radius \(r = 5.00\ \mathrm{mm}\) in a field \(B = 5.00\ \mathrm{mT}\).

Convert: \(r = 5.00\times10^{-3}\ \mathrm{m}\), \(B = 5.00\times10^{-3}\ \mathrm{T}\).

Rearrange \(r = mv/(qB)\) to \(v = rqB/m\):

$$
v = \frac{5.00\times10^{-3}\times1.6\times10^{-19}\times5.00\times10^{-3}}{9.1\times10^{-31}}
$$

$$
\text{numerator} = 4.0\times10^{-24}, \qquad \text{denominator} = 9.1\times10^{-31}
$$

$$
v \approx 4.4\times10^{6}\ \mathrm{m\,s^{-1}}
$$

### Listing 6 — Cyclotron period: why the speed cancels (extension / Module 8 link)

Period = circumference / speed:

$$
T = \frac{2\pi r}{v}
$$

Substitute \(r = mv/(qB)\):

$$
T = \frac{2\pi\,(mv/(qB))}{v} = \frac{2\pi m v}{qB v} = \frac{2\pi m}{qB}
$$

(the \(v\) cancels). The period \(T\) does NOT depend on \(v\) or \(r\) — only on \(m\), \(q\) and \(B\). (This is the cyclotron principle. NOTE: not an explicit M6 dot-point — the cyclotron is a Module 8 application; treat as insight, not a quoted M6 formula.)

Related forms:

$$
\text{cyclotron frequency}\quad f = \frac{1}{T} = \frac{qB}{2\pi m}
$$

$$
\text{angular frequency}\quad \omega = \frac{qB}{m}
$$

### Listing 7 — Worked Example D: proton period is independent of speed

Proton: \(m = 1.67\times10^{-27}\ \mathrm{kg}\), \(q = 1.6\times10^{-19}\ \mathrm{C}\), in \(B = 1.5\ \mathrm{T}\). Find the period of its circular motion.

$$
T = \frac{2\pi m}{qB} = \frac{2\pi\times1.67\times10^{-27}}{1.6\times10^{-19}\times1.5}
$$

$$
\text{numerator} = 1.049\times10^{-26}, \qquad \text{denominator} = 2.4\times10^{-19}
$$

$$
T \approx 4.4\times10^{-8}\ \mathrm{s}\quad (\approx 44\ \text{nanoseconds, independent of the proton's speed})
$$

### Listing 8 — Exam Question 4 worked solution: electron radius

Electron at \(v = 3.0\times10^{7}\ \mathrm{m\,s^{-1}}\) enters \(B = 0.20\ \mathrm{T}\) at right angles. Find \(r\).

$$
r = \frac{mv}{qB} = \frac{9.1\times10^{-31}\times3.0\times10^{7}}{1.6\times10^{-19}\times0.20}
$$

$$
\text{numerator} = 2.73\times10^{-23}, \qquad \text{denominator} = 3.2\times10^{-20}
$$

$$
r \approx 8.5\times10^{-4}\ \mathrm{m} \approx 0.85\ \mathrm{mm}
$$

### Listing 9 — Reference data: particle masses, charges, and relative radius
| Particle           | Mass (kg)        | Charge magnitude (C) | r relative to electron (same v, B) |
|--------------------|------------------|----------------------|------------------------------------|
| Electron (β⁻)      | 9.1 × 10⁻³¹      | 1.6 × 10⁻¹⁹ (−e)     | 1 (tightest curve)                 |
| Proton             | 1.67 × 10⁻²⁷     | 1.6 × 10⁻¹⁹ (+e)     | ≈ 1836                             |
| Alpha (⁴₂He nucleus) | 6.64 × 10⁻²⁷   | 3.2 × 10⁻¹⁹ (+2e)    | ≈ 3650                             |

### Listing 10 — Electric field vs magnetic field on a moving charge (contrast for M6-03)
| Property                  | Electric field (M6-01)              | Magnetic field (M6-02)                          |
|---------------------------|-------------------------------------|-------------------------------------------------|
| Force law                 | F = qE                              | F = qvB sin θ                                   |
| Acts on a stationary charge? | Yes                              | No — requires motion (v = 0 → F = 0)            |
| Force direction           | Along the field (sign-dependent)    | Perpendicular to BOTH v and B                   |
| Does the force do work?   | Yes — changes speed and KE          | No — speed and KE constant, direction only      |
| Trajectory (projected across field) | Parabola                  | Circle (helix if v has a component along B)     |
| Energy relation           | W = qV = ½mv²                       | W = 0 always                                    |
