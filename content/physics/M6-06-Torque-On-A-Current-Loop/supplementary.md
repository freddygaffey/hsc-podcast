---
title: "Supplementary Materials — Torque on a Current Loop: Why the Motor Spins"
module: M6
lesson: "06"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Torque on a coil, worked example (τ = nBIA cos θ)

$$
\tau = nBIA \cos\theta
$$

where \(\theta\) = angle between the field \(B\) and the PLANE of the coil.

Given: \(n = 50\) turns, \(A = 0.080\ \mathrm{m} \times 0.050\ \mathrm{m} = 4.0 \times 10^{-3}\ \mathrm{m^{2}}\) (convert cm → m BEFORE substituting), \(I = 2.0\ \mathrm{A}\), \(B = 0.25\ \mathrm{T}\).

(a) Plane PARALLEL to field \(\to\) \(\theta = 0°\), \(\cos 0° = 1\) (maximum torque):

$$
\tau = 50 \times 0.25 \times 2.0 \times (4.0 \times 10^{-3}) \times 1 = 0.10\ \mathrm{N\,m} \quad (\text{maximum torque})
$$

(b) Plane at \(60°\) to field \(\to\) \(\cos 60° = 0.50\):

$$
\tau = 0.10 \times 0.50 = 0.050\ \mathrm{N\,m} \quad (\text{half the maximum})
$$

(c) Plane PERPENDICULAR to field \(\to\) \(\theta = 90°\), \(\cos 90° = 0\):

$$
\tau = 0\ \mathrm{N\,m}
$$

Reason (earns the understanding mark): the forces are STILL \(B I L\) (not zero); the torque is zero because they act along the axis \(\to\) perpendicular distance = 0.

Unit note: torque is in newton metres (\(\mathrm{N\,m}\)), NEVER joules — even though \(\mathrm{N\,m}\) and \(\mathrm{J}\) are dimensionally identical.

### Listing 2 — First-principles cross-check (τ = Fd, the couple)

Force on ONE active side (length \(L = 0.080\ \mathrm{m}\)), perpendicular to \(B\) (\(\sin 90° = 1\)):

$$
F = BIL = 0.25 \times 2.0 \times 0.080 = 0.040\ \mathrm{N} \quad (\text{per turn})
$$

The two active sides form a COUPLE. At the plane-parallel position the lever arm = full coil width = \(0.050\ \mathrm{m}\).

Torque from the couple, one turn:

$$
\tau_{\text{1 turn}} = F \times \text{width} = 0.040 \times 0.050 = 2.0 \times 10^{-3}\ \mathrm{N\,m}
$$

For all \(n = 50\) turns:

$$
\tau = 50 \times 2.0 \times 10^{-3} = 0.10\ \mathrm{N\,m} \quad \checkmark\ (\text{matches Listing 1 part a})
$$

Insight: \(nBIA\) is just (force on a side) \(\times\) (coil width) \(\times\) (number of turns).

### Listing 3 — Torque vs coil orientation (reference)
| Position of coil | Angle θ (field-to-plane) | cos θ | Torque | Why |
|---|---|---|---|---|
| Plane PARALLEL to field | 0° | 1 | MAXIMUM = nBIA | Forces act at full perpendicular distance from axis |
| Plane at 60° to field | 60° | 0.5 | half of max | Lever arm reduced |
| Plane PERPENDICULAR to field (normal ∥ B) | 90° | 0 | ZERO | Forces act along/through the axis — no turning effect |

### Listing 4 — Exam question 3 worked solution (maximum torque)

Given: \(n = 100\), \(A = 2.0 \times 10^{-3}\ \mathrm{m^{2}}\), \(I = 1.5\ \mathrm{A}\), \(B = 0.4\ \mathrm{T}\). Maximum torque \(\to\) plane parallel to field \(\to\) \(\theta = 0°\), \(\cos 0° = 1\).

$$
\tau = nBIA = 100 \times 0.4 \times 1.5 \times (2.0 \times 10^{-3}) = 0.12\ \mathrm{N\,m}
$$

### Listing 5 — The cos-vs-sin convention (the #1 mark-loser)

SAME PHYSICS, two conventions for the angle \(\theta\) — always check which the question gives:

**Textbook / Surfing Physics convention (used in this episode):** \(\theta\) = angle between the field and the PLANE of the coil.

$$
\tau = nBIA \cos\theta \qquad (\text{maximum torque when plane} \parallel \text{field, } \theta = 0°)
$$

**NESA formula-sheet convention:** \(\theta\) = angle between the field and the NORMAL (area vector) of the coil.

$$
\tau = nBIA \sin\theta \qquad (\text{maximum torque when normal} \perp \text{field})
$$

Why both are correct: plane-angle + normal-angle = \(90°\) (the two angles are complements), so \(\cos(\text{plane-angle}) = \sin(\text{normal-angle})\) \(\Rightarrow\) both formulae trace the identical curve.

Rule: read which angle the diagram/wording defines, THEN choose cos or sin. Do NOT blindly copy "cos" onto a normal-angle question, or "sin" onto a plane-angle one.

### Listing 6 — Underlying motor-effect force (F = BIL sin θ) and reference values

$$
F = BIL \sin\theta \qquad (\text{force on one straight current-carrying side})
$$

- \(F\) = force (\(\mathrm{N}\))
- \(B\) = magnetic field strength / flux density (\(\mathrm{T}\))
- \(I\) = current (\(\mathrm{A}\))
- \(L\) = length of conductor in the field (\(\mathrm{m}\))
- \(\theta\) = angle between current direction and \(B\) (\(F\) max at \(90°\), zero at \(0°\))

For the active sides of a coil: \(\theta = 90°\), \(\sin\theta = 1\), so \(F = BIL\).

Reference worked force example (Jacaranda Sample Problem 1): \(L = 8.0 \times 10^{-2}\ \mathrm{m}\), \(I = 3.0 \times 10^{-2}\ \mathrm{A}\), \(B = 0.25\ \mathrm{T}\).

$$
\begin{aligned}
\text{(a) } \theta = 90°\ (\sin = 1): &\quad F = 3.0\times10^{-2} \times 8.0\times10^{-2} \times 0.25 \times 1 = 6.0 \times 10^{-4}\ \mathrm{N} \\
\text{(b) } \theta = 30°\ (\sin = 0.5): &\quad F = 6.0\times10^{-4} \times 0.5 = 3.0 \times 10^{-4}\ \mathrm{N} \\
\text{(c) } \theta = 0°\ (\sin = 0): &\quad F = 0\ \mathrm{N}
\end{aligned}
$$

General torque definition (slide 171 example):

$$
\tau = rF \sin\theta = 2\ \mathrm{m} \times 5\ \mathrm{N} \times \sin 90° = 10\ \mathrm{N\,m}
$$
