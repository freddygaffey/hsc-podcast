---
title: "Supplementary Materials — Maxwell's Prediction and Hertz's Proof: Calculating and Measuring c"
module: M7
lesson: "02"
script: script.md
---

# Supplementary Materials

Key equations, derivations, worked numerical solutions, and reference data for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Maxwell's speed of light, calculated from the two constants

$$
c = \frac{1}{\sqrt{\mu_0 \times \varepsilon_0}}
$$

- \(\mu_0\) (permeability of free space) \(= 4\pi \times 10^{-7} = 1.2566 \times 10^{-6}\) (\(\mathrm{m\,kg\,C^{-2}}\); std \(\mathrm{H\,m^{-1}}\) / \(\mathrm{T\,m\,A^{-1}}\))
- \(\varepsilon_0\) (permittivity of free space) \(= 8.854 \times 10^{-12}\) (\(\mathrm{C^{2}\,s^{2}\,kg^{-1}\,m^{-3}}\); std \(\mathrm{F\,m^{-1}}\))

**Step 1 — multiply the constants:**

$$
\mu_0 \times \varepsilon_0 = (1.2566 \times 10^{-6}) \times (8.854 \times 10^{-12}) = 1.1127 \times 10^{-17}\ \mathrm{s^{2}\,m^{-2}}
$$

**Step 2 — square root:**

$$
\sqrt{1.1127 \times 10^{-17}} = 3.336 \times 10^{-9}\ \mathrm{s\,m^{-1}}
$$

**Step 3 — reciprocal:**

$$
c = \frac{1}{3.336 \times 10^{-9}} = 2.998 \times 10^{8}\ \mathrm{m/s}
$$

Answer: \(c \approx 3.0 \times 10^{8}\ \mathrm{m/s}\) (exact accepted value \(299\,792\,458\ \mathrm{m/s}\)).

Key point for the discussion mark: \(\mu_0\) and \(\varepsilon_0\) are measured in electric and magnetic experiments INDEPENDENT of light, yet predict the measured speed of light \(\to\) light is an electromagnetic wave.

### Listing 2 — Measuring c in the lab (microwave standing-wave method), worked example

**Method** (required practical):

- transmitter \(\to\) metal reflector \(\to\) incident + reflected waves form a standing wave
- probe slid along the path locates nodes (minima) and antinodes (maxima)

Key relationship: adjacent NODES are \(\lambda/2\) apart \(\to \lambda = 2 \times (\text{node spacing})\). Speed: \(v = f \times \lambda\).

**Worked values:**

- \(f = 10.5\ \mathrm{GHz} = 1.05 \times 10^{10}\ \mathrm{Hz}\)
- node spacing \(= 14.3\ \mathrm{mm} = 14.3 \times 10^{-3}\ \mathrm{m}\)

**Step 1 — wavelength:**

$$
\lambda = 2 \times 14.3 \times 10^{-3} = 2.86 \times 10^{-2}\ \mathrm{m}
$$

**Step 2 — speed:**

$$
v = f \times \lambda = (1.05 \times 10^{10}) \times (2.86 \times 10^{-2}) = 3.00 \times 10^{8}\ \mathrm{m/s}
$$

**Step 3 — assess accuracy:**

$$
\%\ \text{error} = \frac{|3.00 \times 10^{8} - 2.998 \times 10^{8}|}{2.998 \times 10^{8}} \times 100 \approx 0.07\% \quad (\text{excellent})
$$

Dominant error: node-location uncertainty (nodes are broad, shallow minima) \(\to\) reduce by averaging over many node spacings. Other errors: transmitter frequency drift; stray reflections; probe-position reading error. Trap: forgetting the factor of 2 in \(\lambda = 2 \times (\text{node spacing})\) halves the computed speed.

### Listing 3 — Exam question 4, worked solution (microwave at 9.4 GHz)

Given: \(f = 9.4 \times 10^{9}\ \mathrm{Hz}\); adjacent node spacing \(= 16\ \mathrm{mm} = 16 \times 10^{-3}\ \mathrm{m}\).

$$
\lambda = 2 \times (\text{node spacing}) = 2 \times 16 \times 10^{-3} = 3.2 \times 10^{-2}\ \mathrm{m}
$$

$$
v = f \times \lambda = (9.4 \times 10^{9}) \times (3.2 \times 10^{-2}) = 3.0 \times 10^{8}\ \mathrm{m/s}
$$

Main error: node-location uncertainty (broad minima) \(\to\) average over many nodes.

### Listing 4 — Maxwell's four equations (qualitative, in story order)
| # | Name | What it states | Key constant |
|---|------|----------------|--------------|
| 1 | Gauss's law (electricity) | Electric charge produces an electric field; field lines start/end on charge | permittivity \(\varepsilon_0\) |
| 2 | Gauss's law (magnetism) | No magnetic monopoles; net magnetic flux through any closed surface = 0 | — |
| 3 | Faraday's law | A changing magnetic field induces an electric field | — |
| 4 | Ampère–Maxwell law | A current, or a changing electric field, induces a magnetic field | permeability \(\mu_0\) |

Memory hook (this order): **G**auss's **G**lorious **F**ields **A**re **M**ine — Gauss(E), Gauss(M), Faraday, Ampère–Maxwell. Laws 3 + 4 are the self-propagating "leapfrog" that gives light.

### Listing 5 — Who did what: prediction vs verification (the marks-saving trap)
| Person | Date | Role | Did | Did NOT |
|--------|------|------|-----|---------|
| James Clerk Maxwell | 1864 (theory) | Theory / prediction | Unified E & M; predicted EM waves and their speed \(c = 1/\sqrt{\mu_0\varepsilon_0}\) | Did not measure c; did not detect EM waves (died 1879) |
| Heinrich Hertz | 1886–1888 (experiment) | Experiment / verification | Produced, detected & measured EM waves; showed reflection, refraction, polarisation; speed = c | Did not predict the waves |

Mnemonic: **Maxwell predicts, Hertz proves.** Theory → experiment.

### Listing 6 — Hertz's apparatus and the chain of reasoning

**Transmitter — spark-gap oscillator:** induction coil \(\to\) high oscillating voltage across gap between two spherical electrodes \(\to\) sparks = ACCELERATING charges \(\to\) radiate EM waves (links to M7-01 production).

**Receiver — loop antenna:** wire loop with a tiny gap, NO power source, placed metres away \(\to\) spark jumps its gap \(\to\) an EM wave crossed the room, induced a current (Faraday) \(\to\) first deliberate detection of EM waves (1886/87).

**Confirmed same nature as light:**

- Reflection (off metal sheet)
- Refraction (through pitch/wax prism)
- Polarisation (rotate loop: PARALLEL = max spark, PERPENDICULAR = no spark) \(\to\) transverse wave
- Speed measured via standing waves, \(v = f\lambda\) \(\to\) equals \(c\) (confirms Maxwell)

Result: same nature as light, lower frequency = radio waves. Unit "hertz" named for him. Forward irony (M7-11): UV from the spark gap caused the photoelectric effect — seed of the particle model of light, found at the bench that proved light is a wave.

### Listing 7 — c as a defined standard (since 1983) and the metre/second

**Speed of light (since 1983): DEFINED exactly**

$$
c = 299\,792\,458\ \mathrm{m/s} \quad \text{(no uncertainty — not measured)}
$$

**The second** (caesium-133 atomic clock): \(1\ \mathrm{s}\) = duration of \(9\,192\,631\,770\) oscillations of the Cs-133 transition.

**The metre** (defined FROM \(c\)): \(1\ \mathrm{m}\) = distance light travels in vacuum in \(\dfrac{1}{299\,792\,458}\ \mathrm{s}\).

Consequence (examinable): \(c\) cannot be "measured more accurately" — it is fixed by definition. Better experiments now refine the METRE, not \(c\).

### Listing 8 — Reference data: constants, values, dates
| Quantity | Symbol | Value | Notes |
|----------|--------|-------|-------|
| Speed of light (defined) | \(c\) | \(299\,792\,458\ \mathrm{m/s} \approx 3.0 \times 10^{8}\ \mathrm{m/s}\) | exact since 1983 |
| Permittivity of free space | \(\varepsilon_0\) | \(8.854 \times 10^{-12}\) | \(\mathrm{C^{2}\,s^{2}\,kg^{-1}\,m^{-3}}\) (std \(\mathrm{F\,m^{-1}}\)) — from electric experiments |
| Permeability of free space | \(\mu_0\) | \(4\pi \times 10^{-7} = 1.257 \times 10^{-6}\) | \(\mathrm{m\,kg\,C^{-2}}\) (std \(\mathrm{H\,m^{-1}}\), \(\mathrm{T\,m\,A^{-1}}\)) — from magnetic experiments |
| Caesium-133 second | — | \(9\,192\,631\,770\) oscillations | defines the second |
| Wave equation | \(c = f\lambda\) | — | \(f\) in Hz, \(\lambda\) in m, \(c\) in m/s |
| Node spacing | — | \(\lambda/2\) | adjacent nodes; \(\lambda = 2 \times \text{spacing}\) |
| Maxwell | — | 1831–1879 | predicted \(c\), 1864; died before Hertz |
| Hertz | — | 1857–1894 | produced/detected/measured EM waves, 1886–88 |
| Fizeau (1849) | — | 313 000 km/s | spinning toothed wheel |
| Foucault (1862) | — | 298 000 km/s | rotating mirror |
| Michelson (early 1900s) | — | \(2.99796 \times 10^{8}\ \mathrm{m/s}\) | rotating 8-sided mirror |
