---
title: "Supplementary Materials — Transformers: Why AC and How They Work"
module: M6
lesson: "14"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Why AC, not DC: the Faraday chain

**Faraday's law** (magnitude):

$$
\text{emf} = N \times \left(\frac{\Delta\phi}{\Delta t}\right)
$$

- \(\text{emf}\) = induced EMF, volts (\(\mathrm{V}\))
- \(N\) = number of turns (dimensionless)
- \(\Delta\phi\) = change in magnetic flux, weber (\(\mathrm{Wb}\))
- \(\Delta t\) = time interval, seconds (\(\mathrm{s}\))
- full law: \(\text{emf} = -N\,(\Delta\phi/\Delta t)\); minus sign \(=\) Lenz's law, opposition

**Magnetic flux:**

$$
\phi = B A \cos\theta
$$

- \(B\) = flux density, tesla (\(\mathrm{T} = \mathrm{Wb\,m^{-2}}\))
- \(A\) = area (\(\mathrm{m^{2}}\))
- \(\theta\) = angle to normal

DC input \(\to\) steady current \(\to\) constant flux \(\to \Delta\phi/\Delta t = 0 \to\) no induced emf \(\to\) NO sustained output (only a brief pulse at switch-on / switch-off, when \(\phi\) momentarily changes).

AC input \(\to\) reversing current \(\to\) continuously changing flux \(\to \Delta\phi/\Delta t \ne 0 \to\) continuous induced emf \(\to\) AC output, at the SAME frequency.

Conclusion: a transformer needs the continuously changing flux that ONLY AC supplies. Mark-earning step: state explicitly that constant flux gives \(\Delta\phi/\Delta t = 0\), so NO emf.

### Listing 2 — Worked example: electric-piano transformer (ideal)

**Given:**

- \(V_p = 240\ \mathrm{V}\) (primary voltage)
- \(V_s = 12.0\ \mathrm{V}\) (secondary voltage)
- \(N_s = 30\) turns (secondary turns)
- \(I_s = 500\ \mathrm{mA} = 0.500\ \mathrm{A}\) (convert mA \(\to\) A first)
- Treat as ideal.

**(a) Primary turns** — turns-ratio equation

$$
\frac{V_p}{V_s} = \frac{N_p}{N_s}
$$

$$
N_p = N_s \times \frac{V_p}{V_s} = 30 \times \frac{240}{12.0} = 30 \times 20 = 600\ \text{turns}
$$

(\(N_p > N_s \Rightarrow\) step-DOWN, consistent with \(240\ \mathrm{V} \to 12\ \mathrm{V}\))

**(b) Primary current** — conservation of energy

$$
V_p I_p = V_s I_s \quad\to\quad I_p = I_s \times \frac{N_s}{N_p}
$$

$$
I_p = 0.500 \times \frac{30}{600} = 0.500 \times \frac{1}{20} = 0.025\ \mathrm{A} = 25\ \mathrm{mA}
$$

Check (inverse trade-off): \(V\) down \(\times 20\) (\(240 \to 12\)); \(I\) up \(\times 20\) (\(25\ \mathrm{mA} \to 500\ \mathrm{mA}\)) ✓

**(c) Power output**

$$
P_s = V_s I_s = 12.0 \times 0.500 = 6.0\ \mathrm{W}
$$

Check power conserved:

$$
P_p = V_p I_p = 240 \times 0.025 = 6.0\ \mathrm{W} = P_s \ \checkmark
$$

### Listing 3 — Worked example: turns ratio from power (ideal)

**Given:**

- \(P_p = 10\ \mathrm{kW} = 10\,000\ \mathrm{W}\) (power supplied to transformer)
- \(V_p = 1.0\ \mathrm{kV} = 1000\ \mathrm{V}\) (primary voltage)
- \(I_s = 0.50\ \mathrm{A}\) (secondary current)
- Ideal \(\Rightarrow P_s = P_p = 10\,000\ \mathrm{W}\)

**Primary current**

$$
I_p = \frac{P_p}{V_p} = \frac{10\,000}{1000} = 10\ \mathrm{A}
$$

**Secondary voltage**

$$
V_s = \frac{P_s}{I_s} = \frac{10\,000}{0.50} = 20\,000\ \mathrm{V} = 20\ \mathrm{kV}
$$

**Turns ratio** \(=\) voltage ratio

$$
N_p : N_s = V_p : V_s = 1.0\ \mathrm{kV} : 20\ \mathrm{kV} = 1 : 20
$$

\(V_s > V_p \Rightarrow N_s > N_p \Rightarrow\) step-UP transformer.

### Listing 4 — Worked example: step-down, find Vs and Ip (exam Q3)

**Given:**

- \(N_p = 8000\) turns, \(N_s = 200\) turns
- \(V_p = 240\ \mathrm{V}\) (AC), \(I_s = 3\ \mathrm{A}\), ideal

**Secondary voltage** — turns ratio

$$
\frac{V_p}{V_s} = \frac{N_p}{N_s}
$$

$$
V_s = V_p \times \frac{N_s}{N_p} = 240 \times \frac{200}{8000} = 240 \times \frac{1}{40} = 6\ \mathrm{V}
$$

(step-down: \(240\ \mathrm{V} \to 6\ \mathrm{V}\))

**Primary current** — conservation of energy

$$
V_p I_p = V_s I_s
$$

$$
I_p = \frac{V_s I_s}{V_p} = \frac{6 \times 3}{240} = \frac{18}{240} = 0.075\ \mathrm{A} = 75\ \mathrm{mA}
$$

Check: \(V\) down \(\times 40\) (\(240 \to 6\)); \(I\) up \(\times 40\) (\(75\ \mathrm{mA} \to 3\ \mathrm{A}\)) ✓

### Listing 5 — The transformer equations and quantities
| Relationship | Equation (words) | Holds for |
|---|---|---|
| Faraday's law | \(\text{emf} = N \times (\Delta\phi/\Delta t)\) — induced emf = turns × rate of change of flux | always (the working principle) |
| Turns / voltage ratio | \(V_p / V_s = N_p / N_s\) — voltage ratio = turns ratio | always (ideal core assumed) |
| Current ratio (inverse) | \(I_s / I_p = N_p / N_s\) — current goes the opposite way to voltage | ideal transformer |
| Power conservation | \(V_p I_p = V_s I_s\) — power out = power in | IDEAL only (real: \(V_p I_p > V_s I_s\)) |
| Power | \(P = V I\), watts | always |
| Line loss (grid context) | \(P_{\text{loss}} = I^{2} R\) — step \(V\) up \(\to I\) down \(\to\) loss falls as \(I^{2}\) | transmission lines |

### Listing 6 — Step-up vs step-down at a glance
| Feature | Step-up | Step-down |
|---|---|---|
| Secondary turns Ns vs Np | Ns > Np (more on secondary) | Ns < Np (fewer on secondary) |
| Output voltage Vs vs Vp | Vs > Vp (voltage raised) | Vs < Vp (voltage lowered) |
| Output current Is vs Ip | Is < Ip (current lowered) | Is > Ip (current raised) |
| Frequency | unchanged (= input) | unchanged (= input) |
| Grid use | generator → transmission line | transmission line → homes |

### Listing 7 — Real-transformer losses: "real transformers FRET"
| Loss (FRET) | Mechanism | Reduced by |
|---|---|---|
| **F** — incomplete Flux linkage | Some primary flux leaks through the air instead of threading the secondary, so the secondary links less flux. | Wind coils tightly together on a closed/continuous (toroidal or rectangular) soft-iron core. |
| **R** — Resistive heating (copper / \(I^{2}R\) loss) | Copper windings have resistance; current dissipates power as heat at rate \(I^{2}R\). | Use thicker, lower-resistance (high-conductivity) wire. |
| **E** — Eddy currents (in the IRON CORE) | Changing flux induces circulating currents in the conducting core (Faraday + Lenz); they heat the core via \(I^{2}R\). | Laminate the core (thin insulated iron layers cutting the loops); or use ferrites (poor electrical conductors). |

### Listing 8 — Trap table: pair each loss with the RIGHT fix

**Correct pairings** (do not scramble these):

- incomplete flux linkage \(\to\) closed, tightly-wound core
- eddy currents (in core) \(\to\) laminated core / ferrites
- resistive coil heating \(\to\) thicker, lower-resistance wire

**Common errors to avoid:**

- ✗ "lamination reduces resistive heating in the coils" (no — lamination = core, eddy currents)
- ✗ "thicker wire reduces eddy currents" (no — thicker wire = coil resistance)
- ✗ "eddy currents flow in the copper coils" (no — they are induced in the IRON core)
- ✗ "a transformer changes the frequency" (no — only voltage/current change)
- ✗ "\(V_p I_p = V_s I_s\) for a real transformer" (no — that is the IDEAL model; real: \(V_p I_p > V_s I_s\))
- ✗ "DC gives literally zero output ever" (imprecise — no SUSTAINED output; brief pulse at switch-on/off)
