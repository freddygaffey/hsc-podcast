---
title: "Supplementary Materials — Half-Life and the Mathematics of Decay"
module: M8
lesson: "08"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it's the read-along reference.

### Listing 1 — The decay law and the decay-constant / half-life relationship

Defining differential equation (conceptual root) — rate of decay \(\propto\) number of undecayed nuclei present:

$$
\frac{dN}{dt} = -\lambda N
$$

Integrates to the decay law (on the HSC data sheet):

$$
N_t = N_0\, e^{-\lambda t}
$$

- \(N_0\) = number of undecayed nuclei at \(t = 0\)
- \(N_t\) = number remaining at time \(t\)
- \(\lambda\) = decay constant (probability of decay per nucleus per unit time), unit \(\mathrm{s^{-1}}\)
- \(t\) = elapsed time (same time unit as \(\lambda\))
- \(e \approx 2.718\)

Activity follows the SAME exponential, since \(A = \lambda N\):

$$
R_t = R_0\, e^{-\lambda t}
$$

where \(R\) = activity, unit becquerel (\(\mathrm{Bq}\)) = 1 decay per second = \(1\ \mathrm{s^{-1}}\).

Derive \(\lambda = \ln 2 / t_{1/2}\) by asking "when is \(N = \tfrac{1}{2}N_0\)?":

$$
\begin{aligned}
\tfrac{1}{2}N_0 &= N_0\, e^{-\lambda t_{1/2}} \\
\tfrac{1}{2} &= e^{-\lambda t_{1/2}} \\
\ln\!\left(\tfrac{1}{2}\right) &= -\lambda t_{1/2} \\
-\ln 2 &= -\lambda t_{1/2}
\end{aligned}
$$

$$
\lambda = \frac{\ln 2}{t_{1/2}} \quad (\text{data sheet}), \qquad \text{equivalently} \qquad t_{1/2} = \frac{\ln 2}{\lambda} \approx \frac{0.693}{\lambda}
$$

with \(\ln 2 = 0.6931\).

Fraction-remaining shortcut (whole/simple numbers of half-lives only), \(n = t/t_{1/2}\) = number of half-lives:

$$
\frac{N_t}{N_0} = \left(\tfrac{1}{2}\right)^{t/t_{1/2}} = \left(\tfrac{1}{2}\right)^{n}
$$

### Listing 2 — Worked example: amount remaining (iodine-123 tracer)

Problem: 20 mg of iodine-123 (\(t_{1/2} = 13\ \mathrm{h}\)). How much remains after 24 h? 24 h is NOT a whole number of half-lives \(\to\) use \(N_t = N_0\, e^{-\lambda t}\).

Step 1 — find \(\lambda\) FIRST (the law needs \(\lambda\), not \(t_{1/2}\)); unit per HOUR, because \(t_{1/2}\) in hours:

$$
\lambda = \frac{\ln 2}{t_{1/2}} = \frac{0.6931}{13\ \mathrm{h}} = 0.0533\ \mathrm{h^{-1}}
$$

Step 2 — substitute into the decay law (keep \(t\) in hours to match \(\lambda\)):

$$
N_t = 20 \times e^{-0.0533 \times 24} = 20 \times e^{-1.279}
$$

Step 3 — evaluate:

$$
e^{-1.279} = 0.278 \qquad N_t = 20 \times 0.278 = 5.57\ \mathrm{mg}
$$

Step 4 — sanity check with the shortcut:

$$
n = \frac{24}{13} = 1.846\ \text{half-lives} \qquad \left(\tfrac{1}{2}\right)^{1.846} = 0.278 \ \to\ 20 \times 0.278 = 5.57\ \mathrm{mg}\ \checkmark\ (\text{textbook } 5.56\ \mathrm{mg})
$$

Answer: \(\approx 5.6\ \mathrm{mg}\) remains after 24 h.

Whole-number-of-half-lives versions (no calculator):

- After 26 h = 2 half-lives: \(20 \to 10 \to 5\ \mathrm{mg}\) (5 mg remains)
- Activity 8.0 MBq, \(t_{1/2} = 10.0\ \mathrm{min}\), reach 1.0 MBq: \(8 \to 4 \to 2 \to 1\) = 3 halvings = 30 min

### Listing 3 — Worked example: decay constant and half-life from a drop in activity

Problem: activity falls from 600 counts/min to 100 counts/min in 6 hours. Find the decay constant and the half-life.

Step 1 — activity follows the same exponential:

$$
100 = 600 \times e^{-\lambda \cdot 6}
$$

Step 2 — divide by 600:

$$
\frac{100}{600} = \frac{1}{6} = 0.1667 = e^{-6\lambda}
$$

Step 3 — take natural log of both sides:

$$
\ln(0.1667) = -1.7918 = -6\lambda
$$

Step 4 — solve for \(\lambda\) (PER HOUR — \(t\) was in hours):

$$
\lambda = \frac{1.7918}{6} = 0.299\ \mathrm{h^{-1}}
$$

Step 5 — convert to half-life:

$$
t_{1/2} = \frac{\ln 2}{\lambda} = \frac{0.6931}{0.299} = 2.32\ \mathrm{h}
$$

Answer: \(\lambda \approx 0.30\ \mathrm{h^{-1}}\) (\(= 8.3 \times 10^{-5}\ \mathrm{s^{-1}}\)), \(t_{1/2} \approx 2.32\ \mathrm{h}\).

UNIT TRAP: \(\lambda\) here is per HOUR, not \(\mathrm{s^{-1}}\). A "per second" label would give a sub-second half-life, contradicting a source still active after 6 hours. Always keep \(\lambda\) and \(t\) in the same time unit.

### Listing 4 — Worked example: closing exam question 4 (activity 800 → 200 Bq in 12 h)

Problem: activity falls from 800 Bq to 200 Bq in 12 hours. Find the decay constant and the half-life.

$$
\begin{aligned}
200 &= 800 \times e^{-\lambda \cdot 12} \\
\frac{200}{800} = \frac{1}{4} &= e^{-12\lambda} \\
\ln\!\left(\tfrac{1}{4}\right) = -1.386 &= -12\lambda \\
\lambda = \frac{1.386}{12} &= 0.116\ \mathrm{h^{-1}} \quad (\text{per hour} - t \text{ in hours}) \\
t_{1/2} = \frac{\ln 2}{\lambda} = \frac{0.6931}{0.116} &= 6.0\ \mathrm{h}
\end{aligned}
$$

Check: \(800 \to 400 \to 200\) is 2 halvings; \(12\ \mathrm{h} / 6\ \mathrm{h} = 2\) half-lives. ✓

Answer: \(\lambda \approx 0.116\ \mathrm{h^{-1}}\), \(t_{1/2} = 6.0\ \mathrm{h}\).

### Listing 5 — Half-life and use of selected radioisotopes
| Radioisotope    | Half-life          | Emission (key)      | Typical use                                  |
|-----------------|--------------------|---------------------|----------------------------------------------|
| Technetium-99m  | ~6 hours           | gamma               | Most common medical diagnostic tracer        |
| Iodine-123      | 13 hours           | gamma               | Thyroid diagnostic tracer                    |
| Iodine-131      | 8.0 days           | beta + gamma        | Thyroid diagnosis and treatment              |
| Thallium-201    | ~73 days           | gamma (via EC)      | Imaging damaged heart tissue                 |
| Iridium-192     | 74 days            | gamma + beta        | Industrial: locating weaknesses/leaks in pipes |
| Cobalt-60       | 5.3 years          | gamma               | Long-lived gamma source / radiotherapy       |
| Sodium-24       | 15 hours           | beta + gamma        | Decay-graph example (100 g → 50 g at 15 h)   |
| Carbon-14       | 5730 years         | beta                | Radiocarbon dating                           |
| Americium-241   | 432 years          | alpha               | Smoke detectors                              |
| Uranium-238     | 4.5 × 10⁹ years    | alpha               | Very long half-life (≈ age of the Earth)     |
| Polonium-218    | 1.5 × 10⁻⁴ s       | alpha               | Very short half-life                         |

### Listing 6 — Diagnostic-tracer suitability: "GET OUT, GET CLEARED"

Match the PROPERTY to the PURPOSE (the marking key).

**GET OUT** — radiation type = GAMMA

- Penetrating \(\to\) escapes the body to reach an external detector (gamma camera) \(\to\) image
- Weakly ionising \(\to\) minimal damage to healthy tissue as it passes out

Contrast: ALPHA is unsuitable — barely penetrating (absorbed inside, not detectable externally) AND strongly ionising (high, damaging internal dose).

**GET CLEARED** — half-life trade-off

- Long enough \(\to\) administer, distribute to target organ, complete the scan
- Short enough \(\to\) decays/clears quickly afterwards \(\to\) patient's total dose minimised

Too long \(\to\) over-irradiates patient; too short \(\to\) decays before scan completed.

Industry flips the half-life: a permanent gauge / pipe-leak source needs a LONGER half-life (e.g. iridium-192 \(\sim\)74 d, cobalt-60 \(\sim\)5 yr) so it stays useful — same principle, opposite pull.

### Listing 7 — Scientists' contributions to radio-medicine
| Scientist            | Year / contribution                                                                 |
|----------------------|-------------------------------------------------------------------------------------|
| Henri Becquerel      | 1896 — discovered radioactivity (uranium salt fogged a wrapped photographic plate); SI unit of activity (becquerel) named after him |
| Marie & Pierre Curie | Isolated and identified new radioactive elements (polonium, radium); coined "radioactivity"; pioneered its study and medical use, opening the path to radiotherapy and diagnostic imaging |
