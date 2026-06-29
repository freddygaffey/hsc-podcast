---
title: "Supplementary Materials — Muon Lifetime — Time Dilation Made Real"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — The classical (wrong) prediction: how far a muon should travel

Proper lifetime of the muon \(t_0 = 2.2\ \mu\mathrm{s} = 2.2\times10^{-6}\ \mathrm{s}\), and the absolute best case is travel at the speed of light \(c = 3\times10^{8}\ \mathrm{m/s}\).

Classical maximum distance:

$$
d = v\,t_0 = (3\times10^{8}\ \mathrm{m/s})(2.2\times10^{-6}\ \mathrm{s}) = 660\ \mathrm{m}
$$

A realistic muon at \(v = 0.98c\):

$$
d = (0.98\times3\times10^{8})(2.2\times10^{-6}) \approx 647\ \mathrm{m}
$$

The journey actually required is \(15{,}000\ \mathrm{m}\). Verdict: classical physics is short by a factor of \(\approx 22\).

### Listing 2 — Time dilation: the muon survives in OUR frame

Lorentz factor:

$$
\gamma = \frac{1}{\sqrt{1 - v^{2}/c^{2}}}
$$

The standard HSC narrative value is \(\gamma = 15\) (corresponds to \(v = 0.9978c\)).

Time dilation formula:

$$
t = \gamma\,t_0 = 15\times(2.2\times10^{-6}\ \mathrm{s}) = 33\times10^{-6}\ \mathrm{s} = 33\ \mu\mathrm{s}
$$

Distance now possible in Earth's frame:

$$
d = v\,t = (0.9978\times3\times10^{8}\ \mathrm{m/s})(33\times10^{-6}\ \mathrm{s}) \approx 9{,}880\ \mathrm{m} \approx 10\ \mathrm{km}
$$

This is enough to cross the atmosphere \(\to\) muons reach the ground.

### Listing 3 — Length contraction: the muon survives in ITS OWN frame

In the muon's frame, its clock is NORMAL: it lives only \(t_0 = 2.2\ \mu\mathrm{s}\). Instead, the atmosphere is contracted along the direction of motion.

Length contraction formula:

$$
L = \frac{L_0}{\gamma} \qquad\left(\text{equivalently } L = L_0\sqrt{1 - v^{2}/c^{2}}\right)
$$

With \(L_0 = 15{,}000\ \mathrm{m}\) (proper length of atmosphere, Earth's frame) and \(\gamma = 15\):

$$
L = \frac{15{,}000}{15} = 1{,}000\ \mathrm{m}
$$

Time to cross, in the muon's frame:

$$
t = \frac{L}{v} = \frac{1000}{0.9978\times3\times10^{8}} \approx 3.3\times10^{-6}\ \mathrm{s} = 3.3\ \mu\mathrm{s}
$$

This is only \(\approx 1.5\) proper lifetimes, so a sizeable fraction of muons survive. Both frames agree on the outcome: the muon reaches the ground.

### Listing 4 — The Frisch-Smith experiment (Mount Washington, 1962-63)

| Quantity | Value |
|----------|-------|
| Summit altitude (Mount Washington) | 1,917 m |
| Muon speed selected | ~0.995c |
| Lorentz factor gamma at this speed | ~10 |
| Transit time, summit to Cambridge (Earth frame) | 6.34 us (~3 lifetimes) |
| Count rate at summit | 565 +/- 10 per hour |
| Predicted survivors WITHOUT time dilation | ~27 per hour |
| Predicted survivors WITH time dilation | ~400 per hour |
| Measured count at sea level | 409 +/- 9 per hour |
| Time dilation factor measured | 8.8 +/- 0.8 |
| Time dilation factor predicted | ~8.4 |

The survival count follows exponential decay:

$$
N = N_0\,e^{-t / (\gamma\,t_0)}
$$

WITH time dilation (\(\gamma\,t_0 = 8.8\times2.2\ \mu\mathrm{s} = 19.4\ \mu\mathrm{s}\)):

$$
N = 565\,e^{-6.34/19.4} = 565\,e^{-0.327} \approx 407\ \text{per hour} \quad(\text{matches } 409\ \text{measured})
$$

WITHOUT time dilation (\(\gamma = 1\), \(\gamma\,t_0 = 2.2\ \mu\mathrm{s}\)):

$$
N = 565\,e^{-6.34/2.2} = 565\,e^{-2.88} \approx 32\ \text{per hour} \quad(\text{matches } \approx 27\ \text{predicted})
$$

### Listing 5 — The Hafele-Keating experiment (1971): two effects, both real

| Effect | Eastward (ns) | Westward (ns) |
|--------|---------------|---------------|
| Gravitational, general relativity (altitude) | +144 | +179 |
| Kinematic, special relativity (motion) | -184 | +96 |
| Total predicted | -40 +/- 23 | +275 +/- 21 |
| Total measured | -59 +/- 10 | +273 +/- 7 |

Sign convention: positive = flying clock GAINS time vs ground clock.

- Eastward: plane speed ADDS to Earth's rotation \(\to\) faster vs Earth's centre \(\to\) SR slowing dominates \(\to\) clock loses time (net \(-59\ \mathrm{ns}\)).
- Westward: plane speed OPPOSES Earth's rotation \(\to\) slower vs Earth's centre \(\to\) less SR slowing, GR speed-up wins \(\to\) clock gains time (net \(+273\ \mathrm{ns}\)).

The westward result agreed with prediction to within \(\approx 0.1\) standard deviations.

### Listing 6 — GPS: relativity built into daily technology

Satellite orbital altitude \(\approx 20{,}200\ \mathrm{km}\); satellite speed \(\approx 3.87\ \mathrm{km/s}\).

- Special relativity (motion): clocks run SLOW by \(-7.2\ \mu\mathrm{s/day}\)
- General relativity (gravity): clocks run FAST by \(+45.8\ \mu\mathrm{s/day}\)
- Net effect: clocks run FAST by \(\approx +38.4\ \mu\mathrm{s/day}\)

Position error if uncorrected — light travels \(\approx 0.30\ \mathrm{m}\) per nanosecond:

$$
38.4\ \mu\mathrm{s} = 38{,}400\ \mathrm{ns}, \qquad \text{error} \approx 38{,}400\times0.30\ \mathrm{m} \approx 11{,}500\ \mathrm{m} \approx 10\ \mathrm{km}\ \text{per day (and growing)}
$$

Engineering fix (pre-compensation before launch): the target clock frequency is \(10.23\ \mathrm{MHz}\), but the ground frequency is pre-set to \(10.22999999543\ \mathrm{MHz}\) (set slightly slow so it ticks correctly once sped up in orbit).

### Listing 7 — Key constants and quick-reference values

| Quantity | Symbol | Value |
|----------|--------|-------|
| Speed of light | c | 3.00 x 10^8 m/s (exactly 299 792 458 m/s) |
| Muon proper MEAN lifetime | t0 | 2.197 us (~2.2 us) |
| Muon proper HALF-LIFE | t_half | ~1.56 us (value used in Jacaranda textbook) |
| Muon rest mass | — | 105.7 MeV/c^2 (~207 x electron mass) |
| Muon production altitude | — | ~15 km (range 10-20 km) |
| Muon flux at sea level | — | ~10,000 per square metre per minute |
| Time dilation formula | \(t = t_0 / \sqrt{1 - v^{2}/c^{2}}\) | \(t = \gamma\,t_0\) |
| Length contraction formula | \(L = L_0\sqrt{1 - v^{2}/c^{2}}\) | \(L = L_0/\gamma\) |
| Lorentz factor | \(\gamma\) | \(1/\sqrt{1 - v^{2}/c^{2}}\) |

NOTE on lifetime vs half-life (exam-relevant): the mean (average) lifetime of the muon is \(2.197\ \mu\mathrm{s}\) (\(\approx 2.2\ \mu\mathrm{s}\)) — this script uses that value. The half-life is the mean lifetime times \(\ln 2\):

$$
t_{1/2} = t_0\,\ln 2 = 2.197\ \mu\mathrm{s}\times0.693 = 1.52\ \mu\mathrm{s}\ (\approx 1.56\ \mu\mathrm{s})
$$

The Jacaranda textbook quotes the half-life of \(1.56\ \mu\mathrm{s}\) in the Rossi-Hall worked example. Both are correct; they describe the same exponential decay measured two ways.

Syllabus formulas (NESA, Nature of light):

$$
\text{time dilation:} \quad t = \frac{t_0}{\sqrt{1 - v^{2}/c^{2}}}
$$

$$
\text{length contraction:} \quad l = l_0\sqrt{1 - v^{2}/c^{2}}
$$

$$
\text{relativistic momentum:} \quad p = \frac{m_0 v}{\sqrt{1 - v^{2}/c^{2}}}
$$

$$
\text{mass-energy:} \quad E = mc^{2}
$$

### Listing 8 — The Rossi-Hall experiment (Colorado, 1940-41): textbook worked figures

| Quantity | Value |
|----------|-------|
| Muon proper half-life (rest frame) | 1.56 us |
| Transit time between detectors (Earth frame) | ~6.5 us |
| Decay time experienced by muons (muon frame) | ~0.7 us |
| Lorentz factor from \(\gamma = t/t_0\) | \(6.5/0.7 \approx 9.3\) |
| Muon speed from gamma | \(v = c\sqrt{1 - 1/\gamma^{2}} \approx 0.994c\) |
| Half-life measured in Earth frame | \(t = \gamma\,t_0 = 1.56\ \mu\mathrm{s}\times9.3 \approx 14.5\ \mu\mathrm{s}\) |

Two-frame interpretation (same outcome, both frames agree muons survive):

- EARTH frame: the muons' clocks run slow, so their half-life dilates from \(1.56\ \mu\mathrm{s}\) out to \(\approx 14.5\ \mu\mathrm{s}\) \(\to\) many survive the \(\approx 6.5\ \mu\mathrm{s}\) trip.
- MUON frame: the muons' clocks are normal (only \(\approx 0.7\ \mu\mathrm{s}\) elapses), but the mountain/atmosphere is LENGTH-CONTRACTED to a small hill, so the contracted distance is crossed within a normal lifetime.

This is the syllabus' quantitative muon-lifetime example, and it shows time dilation (Earth frame) and length contraction (muon frame) are two descriptions of one physical result.
