---
title: "Supplementary Materials — The Motor Effect: Why a Wire Moves"
module: M6
lesson: "05"
script: script.md
---

# Supplementary Materials

Key equations, the mark-earning mechanism, worked numerical solutions, and reference data for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The "explain why" mechanism: weak vs strong answer

QUESTION (3–4 marks): "Use magnetic field interactions to explain WHY a current-carrying conductor experiences a force in a magnetic field."

**Weak answer (band 4 — scores almost nothing):** "A force acts because \(F = BIL\)." \(\to\) quotes a formula; describes no interaction; not an explanation.

**Strong answer (full marks):**

1. The current-carrying conductor produces its OWN magnetic field — concentric circles around the wire (right-hand grip rule).
2. This field is superimposed on the EXTERNAL uniform magnetic field.
3. On one side the two fields REINFORCE \(\to\) stronger combined field. On the other side they partially CANCEL \(\to\) weaker combined field.
4. The conductor experiences a NET FORCE directed FROM the region of stronger field TOWARD the region of weaker field.

**Key distinction:**

- \(F = BIL \sin\theta\) \(\to\) gives the MAGNITUDE (a calculation tool).
- Right-hand push rule \(\to\) gives the DIRECTION (a memory aid only).
- Two-field interaction \(\to\) is the EXPLANATION of WHY (the marks).
- NEVER answer "explain why" with the formula or the hand rule.

### Listing 2 — F = BIL sin θ: the three worked examples

$$
F = B I L \sin\theta
$$

- \(F\) = force on conductor (newton, \(\mathrm{N}\))
- \(B\) = external field strength (tesla, \(\mathrm{T} = \mathrm{N\,A^{-1}\,m^{-1}}\))
- \(I\) = current (ampere, \(\mathrm{A}\))
- \(L\) = length of conductor IN field (metre, \(\mathrm{m}\)) [textbook uses lowercase \(l\)]
- \(\theta\) = angle between WIRE and FIELD (NOT wire-to-force)
- \(\theta = 90°\) \(\to\) \(\sin\theta = 1\) \(\to\) MAXIMUM force (wire \(\perp\) field)
- \(\theta = 0°\) \(\to\) \(\sin\theta = 0\) \(\to\) ZERO force (wire \(\parallel\) field)

ALWAYS CONVERT TO SI FIRST: cm→m, mA→A, mT→T.

**Worked example A (all three angle cases).** Given: \(L = 8.0\ \mathrm{cm} = 8.0 \times 10^{-2}\ \mathrm{m}\), \(I = 30\ \mathrm{mA} = 3.0 \times 10^{-2}\ \mathrm{A}\), \(B = 0.25\ \mathrm{T}\).

(a) \(\theta = 90°\):

$$
F = 0.25 \times (3.0 \times 10^{-2}) \times (8.0 \times 10^{-2}) \times \sin 90° = 6.0 \times 10^{-4}\ \mathrm{N} \quad (\text{maximum force})
$$

(b) \(\theta = 30°\):

$$
F = 6.0 \times 10^{-4} \times \sin 30° = 6.0 \times 10^{-4} \times 0.5 = 3.0 \times 10^{-4}\ \mathrm{N} \quad (\text{halved})
$$

(c) \(\theta = 0°\) (parallel):

$$
F = 6.0 \times 10^{-4} \times \sin 0° = 6.0 \times 10^{-4} \times 0 = 0\ \mathrm{N} \quad (\text{no force})
$$

**Worked example B** ("maximum force" \(\Rightarrow \theta = 90°\), \(\sin\theta = 1\)). Given: \(L = 5\ \mathrm{cm} = 5 \times 10^{-2}\ \mathrm{m}\), \(B = 2 \times 10^{-4}\ \mathrm{T}\), \(I = 200\ \mathrm{mA} = 0.200\ \mathrm{A}\).

$$
F = B I L = (2 \times 10^{-4})(0.200)(5 \times 10^{-2}) = 2 \times 10^{-6}\ \mathrm{N} \quad (\text{perpendicular to both } I \text{ and } B)
$$

Since \(F \propto I\) and \(F \propto B\): doubling \(I\) OR \(B\) doubles the force.

**Worked example C (rearrange for B).** Given: \(L = 10\ \mathrm{cm} = 0.10\ \mathrm{m}\), \(I = 15\ \mathrm{A}\), \(F = 3.5\ \mathrm{N}\) (max \(\Rightarrow \theta = 90°\)).

$$
F = B I L \quad\to\quad B = \frac{F}{I L} = \frac{3.5}{15 \times 0.10} = \frac{3.5}{1.5} = 2.3\ \mathrm{T} \quad (2.33\ \mathrm{T})
$$

### Listing 3 — Exam Question 3, full worked solution

Q: \(L = 12\ \mathrm{cm}\), \(I = 0.5\ \mathrm{A}\), \(\theta = 40°\) to a field \(B = 0.8\ \mathrm{T}\). Find \(F\).

Convert: \(L = 12\ \mathrm{cm} = 0.12\ \mathrm{m}\) (\(I\) and \(B\) already SI). \(\sin 40° \approx 0.643\).

$$
\begin{aligned}
F &= B I L \sin\theta = 0.8 \times 0.5 \times 0.12 \times \sin 40° \\
&= (0.8 \times 0.5 \times 0.12) \times 0.643 = 0.048 \times 0.643 \\
&\approx 0.031\ \mathrm{N} \approx 3.1 \times 10^{-2}\ \mathrm{N}
\end{aligned}
$$

Marks: (1) correct equation (2) substitution with SI units (3) answer in N.

### Listing 4 — The four factors that change the force (F ∝ B I L sin θ)
| Change | Effect on F | Relationship | Reason (in terms of moving charges) |
|--------|-------------|--------------|--------------------------------------|
| Increase current I | increases | F ∝ I | more charges flow per second → more individual charge-forces summed |
| Increase length L in field | increases | F ∝ L | more current-carrying charges lie inside the field region |
| Increase field strength B | increases | F ∝ B | larger force on each moving charge |
| Increase angle θ (0°→90°) | increases as sin θ | F ∝ sin θ | larger perpendicular velocity component; max at 90°, zero at 0° |

### Listing 5 — Direction rules and conventions (do not mix them up)
| Tool / symbol | What it finds / means | How |
|---------------|------------------------|-----|
| Right-hand GRIP rule | direction of the wire's OWN circular field | thumb = conventional current, curled fingers = field direction |
| Right-hand PUSH (palm) rule | direction of the FORCE on the conductor | fingers = field B (N→S), thumb = current I, palm pushes = force F |
| Conventional current | direction positive charge would move | OPPOSITE to electron drift — reverse electron-flow before applying rules |
| Dot (·) in a circle | field / current OUT of the page | arrow-tip flying toward you |
| Cross (×) in a circle | field / current INTO the page | arrow-tail (fletching) flying away |
| Force direction | always ⊥ to BOTH I and B | perpendicular to the plane containing I and B |

### Listing 6 — Reference data and key terms
| Item | Value / definition |
|------|--------------------|
| Motor effect (definition) | the force experienced by a current-carrying conductor in an external magnetic field |
| Discovery (textbook) | attributed to Michael Faraday, 1821 |
| Tesla (unit of B) | 1 T = 1 N A^-1 m^-1 |
| Force equation | F = BIL sin θ (data sheet) |
| Max force | θ = 90° (wire ⊥ field), sin θ = 1, F = BIL |
| Zero force | θ = 0° or 180° (wire ∥ field), sin θ = 0 |
| Electron charge magnitude | 1.6 × 10^-19 C |
| Electron mass | 9.1 × 10^-31 kg |
| Permeability of free space μ₀ | 4π × 10^-7 N A^-2 (parallel-wire context only — background) |
| k = μ₀ / 2π | 2.0 × 10^-7 N A^-2 (parallel-wire context only — background) |
