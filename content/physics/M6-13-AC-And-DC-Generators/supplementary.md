---
title: "Supplementary Materials — AC and DC Generators: How Rotation Becomes Current"
module: M6
lesson: "13"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Worked Example A: peak EMF of a rotating generator coil

**Given:**

- \(N\) (turns) \(= 200\)
- \(A\) (area) \(= 0.075\ \mathrm{m^{2}}\)
- \(B\) (field) \(= 0.66\ \mathrm{T}\)
- \(f\) (rotation) \(= 50\ \mathrm{rev/s} = 50\ \mathrm{Hz}\)

**(a) Angular frequency**

$$
\omega = 2\pi f = 2 \times \pi \times 50 = 314.2\ \mathrm{rad\,s^{-1}} \quad (= 100\pi\ \mathrm{rad\,s^{-1}})
$$

**(b) Peak EMF** (peak of the sinusoid; derived from Faraday's law applied to \(\Phi = BA\cos\omega t\)):

$$
\varepsilon_{\max} = N B A \omega = 200 \times 0.66 \times 0.075 \times 314.2 = 9.9 \times 314.2 \approx 3110\ \mathrm{V} \quad (\approx 3.1 \times 10^{3}\ \mathrm{V})
$$

Instantaneous EMF:

$$
\varepsilon = 3110 \sin(314.2\, t)\ \mathrm{V}
$$

**(c) Output**

- Slip rings (AC generator): full sine wave, \(+3110\ \mathrm{V}\) to \(-3110\ \mathrm{V}\), one complete cycle per revolution \(\to 50\ \mathrm{Hz}\) (mains frequency).
- Split-ring commutator (DC generator): negative halves flipped positive, \(0 \to +3110\ \mathrm{V} \to 0 \to +3110\ \mathrm{V} \to 0\); two positive humps per revolution. Unidirectional, NOT flat, never negative.

NOTE: \(\varepsilon_{\max} = NBA\omega\) is NOT on the HSC formula sheet (only \(\varepsilon = -N\,\Delta\Phi/\Delta t\) is). Use it as "the peak value the sinusoid reaches", derived from Faraday's law.

### Listing 2 — Worked Example B: bare Faraday's-law calculation (formula-sheet only)

**Given:**

- Loop dimensions \(= 0.25\ \mathrm{m} \times 0.30\ \mathrm{m}\) (single turn, \(N = 1\))
- \(B = 0.66\ \mathrm{T}\) (perpendicular to loop)
- Flux change \(= 0 \to\) full flux over \(\Delta t = 2.0\ \mathrm{s}\)

**Step 1 — Area**

$$
A = 0.25 \times 0.30 = 0.075\ \mathrm{m^{2}}
$$

**Step 2 — Flux values**

$$
\Phi_{\text{initial}} = 0
$$

$$
\Phi_{\text{final}} = B A = 0.66 \times 0.075 = 0.0495\ \mathrm{Wb}
$$

$$
\Delta\Phi = 0.0495 - 0 = 0.0495\ \mathrm{Wb}
$$

**Step 3 — Faraday's law (magnitude)**

$$
\varepsilon = N \times \frac{\Delta\Phi}{\Delta t} = 1 \times \frac{0.0495}{2.0} = 0.0248\ \mathrm{V} \approx 0.025\ \mathrm{V} \quad (24.75\ \mathrm{mV})
$$

This is the AVERAGE EMF over the sweep. Scale by \(N\) for a multi-turn coil. (Contrast with Listing 1, where \(NBA\omega\) gives the PEAK of a sinusoid.)

### Listing 3 — Model 6-mark extended-response answer

QUESTION: "Explain the variations in current produced by an AC generator compared with a DC generator, with reference to their structure and function." (6 marks)

**Model answer**

Both an AC and a DC generator consist of a coil (the rotor) forced to rotate in the
magnetic field of stationary stator magnets. As the coil rotates, the angle between
the field and the coil changes, so the magnetic flux threading the coil continuously
changes \((\Phi = BA\cos\theta)\). By Faraday's law \((\varepsilon = -N\,\Delta\Phi/\Delta t)\), this changing flux induces an
EMF, and hence a current, in the coil. Because the EMF is proportional to the RATE OF
CHANGE of flux, it varies sinusoidally: the EMF is maximum when the coil plane is
parallel to the field (flux instantaneously zero but changing fastest) and zero when
the coil plane is perpendicular to the field (flux maximum but momentarily not
changing). This sinusoidal EMF is generated identically in both generators.

The only structural difference is how the rotating coil connects to the external
circuit. In an AC generator, two continuous SLIP RINGS keep each coil end permanently
connected to the same terminal. The external connection never reverses, so the output
follows the coil's EMF exactly: a true alternating current that reverses direction each
half-revolution, tracing a full sine wave from positive maximum to negative maximum.

In a DC generator, a SPLIT-RING COMMUTATOR (two insulated half-rings) replaces the slip
rings. The stationary brushes swap which half-ring they contact every half-revolution —
precisely as the coil's EMF passes through zero — reversing the external connection.
This keeps the current in the external circuit flowing in ONE direction only. The output
is therefore a pulsating direct current: each negative half-cycle of the sine wave is
flipped positive, so the current rises from zero to maximum and back to zero twice per
revolution, but never reverses. It is unidirectional but NOT a steady, flat DC.

In summary: identical mechanism (Faraday's law on a rotating coil) and identical
sinusoidal internal EMF; slip rings give a full alternating sinusoidal output, while
the split-ring commutator rectifies it into a pulsating unidirectional output.

### Listing 4 — Equations used in this episode (in symbols)

**Magnetic flux:**

$$
\Phi = B A \cos\theta
$$

- \(\theta\) = angle between \(B\) and the coil's AREA VECTOR (normal), NOT the plane.
- \(\Phi\) max when coil plane \(\perp B\) (\(\theta = 0\), \(\cos 0 = 1\))
- \(\Phi = 0\) when coil plane \(\parallel B\) (\(\theta = 90°\), \(\cos 90° = 0\))

**Faraday's law of induction** (formula sheet):

$$
\varepsilon = -N \left(\frac{\Delta\Phi}{\Delta t}\right)
$$

The minus sign \(=\) Lenz's law (direction); drop it for magnitude.

**Sinusoidal generator output:**

$$
\varepsilon = \varepsilon_{\max} \sin(\omega t)
$$

$$
\omega = 2\pi f \quad \text{(angular frequency, } \mathrm{rad\,s^{-1}}\text{)}
$$

**Peak EMF of a rotating coil** (derived, NOT on formula sheet):

$$
\varepsilon_{\max} = N B A \omega
$$

\(\varepsilon_{\max} \propto N,\ \propto B,\ \propto A,\ \propto \omega\). Doubling rotation speed doubles BOTH the peak EMF and the frequency.

**SI units**

- \(\Phi\) : weber (\(\mathrm{Wb}\))
- \(B\) : tesla (\(\mathrm{T} = \mathrm{Wb\,m^{-2}}\))
- \(A\) : \(\mathrm{m^{2}}\)
- \(\varepsilon\) : volt (\(\mathrm{V}\))
- \(\omega\) : \(\mathrm{rad\,s^{-1}}\)
- \(f\) : hertz (\(\mathrm{Hz}\))
- \(t\) : second (\(\mathrm{s}\))
- \(N\) : dimensionless

### Listing 5 — AC generator vs DC generator: the comparison
| Feature | AC generator | DC generator |
|---------|--------------|--------------|
| Connector | Two continuous slip rings | One split-ring commutator (two half-segments) |
| Connection to external circuit | Never reverses | Swaps every half-revolution (at zero-EMF instant) |
| Internal coil EMF | Sinusoidal (ε_max sin ωt) | Sinusoidal — identical to AC |
| External output | Full sine wave: + max to − max | Pulsating DC: rectified sine, all positive |
| Peaks per revolution | One positive + one negative | Two positive humps |
| Goes negative? | Yes | No (unidirectional) |
| Flat / steady? | No | No (single-coil); smoother with many coils |
| Energy transformation | Mechanical → electrical | Mechanical → electrical |

### Listing 6 — Components of generators / motors (shared memory hook)
| Component | Role | DC machine | AC machine |
|-----------|------|------------|------------|
| Rotor coil | Rotating coil where EMF is induced | yes | yes |
| Field magnets (stator) | Supply the magnetic field B | yes | yes |
| Brushes | Stationary graphite contacts; transfer current to terminals | yes | yes |
| Connector | Couple rotating coil to fixed terminals | Split-ring **C**ommutator | Slip rings |

### Listing 7 — Memory hook and trap-busters

**Memory hook** (shared with the DC motor lesson, M6-07):

- Rotor coil, Field magnets, Brushes, Commutator \(\to\) "R F B C"
- For an AC machine, swap the split-ring COMMUTATOR for SLIP RINGS.
- Commutator \(=\) DC.   Slip rings \(=\) AC.

**Trap-busters**

- Slip rings are CONTINUOUS rings \(\to\) AC.  Split ring is SPLIT \(\to\) DC.
- The commutator reverses the CONNECTION, not the EMF in the coil.
- DC generator output is PULSATING, not flat. Two humps per revolution.
- Max flux \(\leftrightarrow\) zero EMF.  Zero flux \(\leftrightarrow\) max EMF. (EMF \(\propto\) rate of change of flux.)
- Same mechanism in both — only the connector differs.
