---
title: "Supplementary Materials — The Michelson-Morley Experiment"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Expected fringe shift on 90 degree rotation

The two perpendicular arms have slightly different round-trip times when the
apparatus moves through a stationary aether at speed v.

Parallel arm (along motion):

$$
t_{\parallel} = \frac{L}{c - v} + \frac{L}{c + v} = \frac{2 L c}{c^{2} - v^{2}} = \frac{2L/c}{1 - v^{2}/c^{2}}
$$

Perpendicular arm (across motion):

$$
t_{\perp} = \frac{2 L}{\sqrt{c^{2} - v^{2}}} = \frac{2L/c}{\sqrt{1 - v^{2}/c^{2}}}
$$

Time difference (small \(v/c\), binomial approximation):

$$
\Delta t = t_{\parallel} - t_{\perp} \approx \frac{L}{c}\,\frac{v^{2}}{c^{2}}
$$

Path difference:

$$
c\,\Delta t \approx \frac{L v^{2}}{c^{2}}
$$

Rotating 90 degrees swaps the arms, doubling the effect. Expected fringe shift:

$$
n = \frac{2 L v^{2}}{\lambda c^{2}}
$$

### Listing 2 — Plugging in the 1887 numbers

Values: \(L = 11\ \mathrm{m}\) (effective folded arm length), \(v = 3.0\times 10^{4}\ \mathrm{m/s}\) (Earth orbital speed, \({\sim}30\ \mathrm{km/s}\)), \(c = 3.0\times 10^{8}\ \mathrm{m/s}\) (speed of light), \(\lambda = 5.0\times 10^{-7}\ \mathrm{m}\) (\({\sim}500\ \mathrm{nm}\), yellow-green light).

$$
\begin{aligned}
n &= \frac{2 L v^{2}}{\lambda c^{2}} \\
&= \frac{(2)(11)(3.0\times 10^{4})^{2}}{(5.0\times 10^{-7})(3.0\times 10^{8})^{2}} \\
&= \frac{(2)(11)(9.0\times 10^{8})}{(5.0\times 10^{-7})(9.0\times 10^{16})} \\
&= \frac{1.98\times 10^{10}}{4.5\times 10^{10}} \\
&\approx 0.44\ \text{fringes}
\end{aligned}
$$

(the \({\sim}0.4\) fringe figure quoted in the paper)

### Listing 3 — The Lorentz factor and contraction

The FitzGerald-Lorentz contraction (1889 / 1892), later reinterpreted by
Einstein (1905). The same gamma factor runs through all of special relativity.

Lorentz factor:

$$
\gamma = \frac{1}{\sqrt{1 - v^{2}/c^{2}}}
$$

Length contraction (HSC formula):

$$
l = l_{0} \sqrt{1 - v^{2}/c^{2}} = \frac{l_{0}}{\gamma}
$$

Time dilation (HSC formula):

$$
t = \frac{t_{0}}{\sqrt{1 - v^{2}/c^{2}}} = t_{0}\,\gamma
$$

The contraction of the parallel arm by factor \(\sqrt{1 - v^{2}/c^{2}}\) exactly cancels the expected time difference in Listing 1, producing a null fringe shift.

### Listing 4 — Einstein's two postulates (1905)

**Principle of relativity:** All inertial frames of reference are equivalent; the laws of physics are identical in every inertial frame.

**Constancy of light speed:** The speed of light in a vacuum is the same for all observers, independent of the motion of the source or the observer:

$$
c = 299\,792\,458\ \mathrm{m/s}\ (\text{exact}) = 2.9979\times 10^{8}\ \mathrm{m/s}\ (\text{HSC value}) \approx 3\times 10^{8}\ \mathrm{m/s}\ (\text{approximation})
$$

**NESA wording (Light and special relativity):** "Outline Einstein's first and second postulates of special relativity." NESA does not fix which postulate is numbered first. Jacaranda lists (1) constant speed of light, (2) equivalent inertial frames; the teacher's slides reverse this order. In the exam, state BOTH postulates precisely; the numbering does not matter.

**Consequence (the key exam point).** The null result of Michelson-Morley is not a puzzle to be explained, but a direct prediction of the postulates.

- Constancy of \(c\): light has the same speed in both arms, so no time difference and no fringe shift.
- Equivalence of inertial frames: there is no aether rest frame, so it cannot matter which way the apparatus points \(\to\) rotating it produces no change in the interference pattern.

### Listing 5 — Expected vs observed: the key comparison

| Quantity | Value |
|----------|-------|
| Expected fringe shift (aether prediction) | ~0.40 fringe |
| Smallest detectable shift (instrument sensitivity) | ~0.01 fringe |
| Observed shift (maximum) | < 0.02 fringe |
| Observed shift (typical / average) | far less than 0.01 fringe |
| Paper's stated limit | certainly < 1/20th, probably < 1/40th of expected |
| Implied upper limit on Earth–aether relative speed | < ~5 km/s (one-sixth of orbital speed) |

### Listing 6 — Timeline of key events and people

| Year | Event |
|------|-------|
| 1865 | Maxwell's equations imply light is an electromagnetic wave at speed c |
| 1881 | Michelson's first interferometer trial at Potsdam — null, but low sensitivity, with a calculation error |
| 1884 | Michelson and Morley meet after Lord Kelvin's Baltimore lectures |
| 1886 | Case Main building fire forces relocation to Adelbert Hall basement |
| 1887 | Michelson–Morley experiment (July); paper published November, Am. J. Sci. vol. 34, pp. 333–345 |
| 1889 | FitzGerald proposes length contraction (letter in Science) |
| 1892–1904 | Lorentz develops the contraction and the Lorentz transformations |
| 1905 | Einstein's "On the Electrodynamics of Moving Bodies" — special relativity, no aether |
| 1907 | Michelson awarded the Nobel Prize in Physics (first American science laureate) |
| 2015 | LIGO (a Michelson interferometer, 4 km arms) detects gravitational waves |

### Listing 7 — The HSC special-relativity formulas (where the gamma factor leads)

The same Lorentz factor that "saves" the null result in Listing 3 runs
through every quantitative formula NESA examines in this focus area.

Lorentz factor:

$$
\gamma = \frac{1}{\sqrt{1 - v^{2}/c^{2}}}
$$

Time dilation:

$$
t = \frac{t_{0}}{\sqrt{1 - v^{2}/c^{2}}} = t_{0}\,\gamma
$$

where \(t_{0}\) = proper time (measured in the frame where the two events occur at the same place).

Length contraction:

$$
l = l_{0} \sqrt{1 - v^{2}/c^{2}} = \frac{l_{0}}{\gamma}
$$

where \(l_{0}\) = proper length (measured in the object's own rest frame). Contraction acts ONLY along the direction of motion.

Relativistic momentum:

$$
p_{v} = \frac{m_{0} v}{\sqrt{1 - v^{2}/c^{2}}} = \gamma\, m_{0} v
$$

As \(v \to c\), \(\gamma \to \infty\), so \(p \to \infty\): an object with mass can never reach the speed of light.

Mass-energy equivalence (the famous consequence):

$$
E = m c^{2}
$$

### Listing 8 — Evidence supporting special relativity (NESA dot point)

NESA: "Analyse the evidence supporting the theory of relativity,
including the muon lifetime and atomic clocks moving at different
velocities." Michelson–Morley is the historical anchor; these are
the direct confirmations.

| Evidence | What it shows | Key numbers (Jacaranda / slides) |
|----------|---------------|----------------------------------|
| Michelson–Morley (1887) | No detectable aether wind; c is the same in all directions | Expected ~0.4 fringe; observed < 1/20, probably < 1/40 of that |
| Cosmic-origin muons (Rossi–Hall, 1941) | Time dilation lets fast muons reach the ground before decaying | Lab half-life 1.56 µs; gamma ≈ 9.3 at v ≈ 0.994c (mean lifetime quoted as 2.2 µs in the slides) |
| Atomic clocks (Hafele–Keating, 1971) | Moving clocks run slow; effect direction matches Earth's rotation | East-going clock ΔtE ≈ −59 ns; west-going clock ΔtW ≈ +273 ns |
| Particle accelerators | Relativistic momentum / mass increase; transition rates dilate | Confirmed to v ≈ c/3 measurements (2014) |
| GPS satellites | Daily proof time dilation is real | Without relativistic correction GPS drifts by > 30 µs/day |
| Modern laser/cavity Michelson–Morley | Isotropy of c | Confirmed to better than 1 part in 10^17 |
