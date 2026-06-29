---
title: "Supplementary Materials — LIGO: Listening to the Fabric of Spacetime"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Power radiated as gravitational waves (Peters quadrupole formula, 1964)

This is the rate at which a binary system loses energy to gravitational waves. It drives the runaway inspiral described in the script. The minus sign means energy is leaving the system.

$$
P = -\frac{32}{5}\,\frac{G^{4}}{c^{5}}\,\frac{m_{1}^{2} m_{2}^{2} (m_{1} + m_{2})}{r^{5}}
$$

where:

- \(P\) — power radiated as gravitational waves (W)
- \(G\) — gravitational constant \(= 6.67\times 10^{-11}\ \mathrm{N\,m^{2}\,kg^{-2}}\)
- \(c\) — speed of light \(= 3.00\times 10^{8}\ \mathrm{m\,s^{-1}}\)
- \(m_{1}\) — mass of first object (kg)
- \(m_{2}\) — mass of second object (kg)
- \(r\) — orbital separation between the two objects (m)

Key consequence (the runaway):

- energy radiated \(\to\) orbit shrinks (\(r\) decreases)
- \(r\) decreases \(\to\) orbital frequency increases (Kepler)
- frequency up \(\to\) \(r^{5}\) in denominator shrinks \(\to\) \(P\) increases sharply
- \(P\) increases \(\to\) orbit shrinks faster ... feedback loop \(\to\) merger

### Listing 2 — Chirp mass

The chirp mass is the single best-measured quantity from an inspiral signal. It controls how fast the frequency sweeps upward and is what the matched-filter templates lock onto.

$$
M_{c} = \frac{(m_{1} m_{2})^{3/5}}{(m_{1} + m_{2})^{1/5}}
$$

For GW150914, with \(m_{1} = 36\) solar masses and \(m_{2} = 29\) solar masses, \(M_{c} \approx 28.1\) solar masses (this naive value; LIGO's full source-frame fit gives \(M_{c} \approx 28.6\) solar masses).

Frequency of gravitational wave \(= 2 \times\) orbital frequency (so as the orbit speeds up, the detected pitch rises \(\to\) the "chirp").

### Listing 3 — Worked example: mass converted to gravitational-wave energy in GW150914

This applies Einstein's mass-energy equivalence (Module 7) to the "missing" three solar masses.

**Step 1 — Find the mass that disappeared:**

$$
\begin{aligned}
m_{\text{initial}} &= m_{1} + m_{2} = 36 + 29 = 65\ \text{solar masses} \\
m_{\text{final}} &= 62\ \text{solar masses} \\
m_{\text{lost}} &= 65 - 62 = 3\ \text{solar masses}
\end{aligned}
$$

**Step 2 — Convert solar masses to kilograms** (1 solar mass \(= 1.99\times 10^{30}\ \mathrm{kg}\)):

$$
m_{\text{lost}} = 3 \times 1.99\times 10^{30} = 5.97\times 10^{30}\ \mathrm{kg}
$$

**Step 3 — Apply \(E = m c^{2}\):**

$$
\begin{aligned}
E &= m_{\text{lost}}\, c^{2} \\
&= (5.97\times 10^{30}\ \mathrm{kg}) \times (3.00\times 10^{8}\ \mathrm{m\,s^{-1}})^{2} \\
&= (5.97\times 10^{30}) \times (9.00\times 10^{16}) \\
&= 5.4\times 10^{47}\ \mathrm{J}
\end{aligned}
$$

This energy was radiated almost entirely as gravitational waves in roughly 0.2 seconds, briefly outshining (in power) all the stars in the observable universe combined.

### Listing 4 — Strain and the size of the displacement LIGO measured

Strain is the fractional change in length. This is what puts the famous "about a thousandth the width of a proton" claim on a firm numerical footing.

Strain definition:

$$
h = \frac{\text{change in arm length}}{\text{arm length}} = \frac{\Delta L}{L}
$$

For GW150914, with \(h_{\text{peak}} = 1.0\times 10^{-21}\) (dimensionless) and \(L_{\text{arm}} = 4\ \mathrm{km} = 4\times 10^{3}\ \mathrm{m}\):

$$
\Delta L = h L = (1.0\times 10^{-21}) \times (4\times 10^{3}) = 4\times 10^{-18}\ \mathrm{m}
$$

Compare to a proton (diameter \({\sim}1.7\times 10^{-15}\ \mathrm{m}\); charge radius \({\sim}0.84\ \mathrm{fm}\)):

$$
\frac{\Delta L}{\text{proton diameter}} = \frac{4\times 10^{-18}}{1.7\times 10^{-15}} \approx 0.0024
$$

i.e. roughly \(1/400\) of a proton diameter for the GW150914 peak.

LIGO's headline "one thousandth the width of a proton" refers to its design displacement sensitivity (\({\sim}1\times 10^{-18}\ \mathrm{m}\), comparable to \(\Delta L\) above) measured against the proton's charge radius (\({\sim}8\times 10^{-16}\ \mathrm{m}\)):

$$
\frac{1\times 10^{-18}}{8\times 10^{-16}} \approx \frac{1}{800}, \quad \text{i.e. } {\sim}10^{-3}\ \text{of a proton.}
$$

Both statements describe the same order-of-magnitude feat: a length change roughly a thousandth the size of a proton.

### Listing 5 — Key numbers for GW150914 and GW170817

| Quantity | GW150914 (black holes) | GW170817 (neutron stars) |
|----------|------------------------|--------------------------|
| Date | 14 Sep 2015 | 17 Aug 2017 |
| Source objects | 36 + 29 solar masses | combined ~2.74 solar masses |
| Final object | 62 solar-mass black hole | neutron-star merger remnant |
| Energy radiated | ~3 solar masses (5.4 x 10^47 J) | smaller (lighter objects) |
| Signal duration in band | ~0.2 s | ~100 s |
| Frequency sweep | 35 Hz to 250 Hz (amplitude peaks at ~150 Hz, after ~8 cycles) | from ~24 Hz upward over ~100 s |
| Peak strain | 1.0 x 10^-21 | ~ order 10^-22 |
| Distance | ~1.3 billion ly (410 Mpc) | ~130 million ly (40 Mpc) |
| Signal-to-noise ratio | 24 | 32.4 |
| Detectors involved | 2 (Hanford, Livingston) | 3 (LIGO x2 + Virgo) |
| Light seen? | No (black holes) | Yes — gamma, optical, infrared |

### Listing 6 — LIGO detector specifications

| Specification | Value |
|---------------|-------|
| Arm length (each) | 4 km |
| Number of detectors (2015) | 2 (Hanford WA, Livingston LA) |
| Separation between sites | ~3,002 km |
| Light-travel time between sites | up to ~10 ms (6.9 ms for GW150914) |
| Laser input power | ~40 W |
| Circulating power in arm cavities | ~750 kW |
| Reflections per arm (Fabry-Perot) | ~300, giving ~1,200 km effective path |
| Test mass (mirror) | 40 kg fused silica |
| Mirror suspension | 4-stage quadruple pendulum |
| Displacement sensitivity | ~10^-18 m at GW frequencies |
| Typical ground/seismic motion | ~10^-7 m (about 10^11 x larger than signal) |

### Listing 7 — Module 5 gravity equations behind the inspiral

The runaway inspiral is the Module 5 physics of orbital energy in action.
Two orbiting masses sit in a negative-energy well; radiating energy away
makes the total energy MORE negative, which (from the equations below)
means a SMALLER orbital radius and a HIGHER orbital speed — the feedback
loop the script describes. These are the HSC syllabus equations.

Newton's law of universal gravitation (force between two masses):

$$
F = \frac{G m_{1} m_{2}}{r^{2}}
$$

Gravitational field strength:

$$
g = \frac{G M}{r^{2}}
$$

Orbital (circular) velocity of one mass about a much larger mass \(M\) (faster when \(r\) is smaller):

$$
v = \sqrt{\frac{G M}{r}}
$$

Gravitational potential energy (zero defined at infinity, always negative):

$$
U = -\frac{G M m}{r}
$$

Kinetic energy of a circular orbit:

$$
E_{k} = \frac{G M m}{2 r}
$$

Total mechanical (orbital) energy:

$$
E = U + E_{k} = -\frac{G M m}{2 r}
$$

\(\Rightarrow\) Radiating energy away (\(E\) becomes more negative) forces \(r\) to decrease and \(v\) to increase. This is exactly why a binary that loses energy to gravitational waves speeds up and spirals inward (see Listing 1).

Constants and values (from the data sheet / textbook):

- \(G = 6.674\times 10^{-11}\ \mathrm{N\,m^{2}\,kg^{-2}}\)
- \(c = 3.00\times 10^{8}\ \mathrm{m\,s^{-1}}\)
- 1 solar mass \(= 1.99\times 10^{30}\ \mathrm{kg}\)

### Listing 8 — Module 7 and Module 8 syllabus links

**Module 7 — mass-energy equivalence** (the "missing" 3 solar masses):

$$
E = m c^{2}
$$

Used in Listing 3. Same relationship the syllabus applies to energy production in the Sun and to particle-antiparticle annihilation.

**Module 8 — origin of the elements** (why GW170817 matters):

- Elements up to and including iron are synthesised inside stars; iron is the heaviest element a star can build, because beyond iron, fusion ABSORBS energy rather than releasing it (the "iron limit", set by the binding-energy-per-nucleon curve).
- Elements heavier than iron (gold, platinum, uranium) form by RAPID NEUTRON CAPTURE (the r-process), which needs an extremely neutron-rich, violent environment — confirmed by GW170817 to be a neutron-star merger (kilonova; strontium identified in the spectrum).
- Module 5 (gravity drives the inspiral) + Module 7 (\(E = m c^{2}\) powers the radiated energy and the kilonova) + Module 8 (stellar death, neutron stars, nucleosynthesis) all converge in this one event.
