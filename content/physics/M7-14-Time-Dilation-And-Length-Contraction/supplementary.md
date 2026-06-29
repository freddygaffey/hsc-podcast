---
title: "Supplementary Materials — Time Dilation and Length Contraction: The Consequences of Constant c"
module: M7
lesson: "14"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference. Constants used throughout: speed of light c = 3.0 × 10^8 m s^-1 (exact: 299 792 458 m s^-1). The time dilation and length contraction equations are on the HSC Physics Data Sheet / Formulae Sheet.

### Listing 1 — The Lorentz factor, time dilation and length contraction (the three equations)

Lorentz factor (gamma):

$$
\gamma = \frac{1}{\sqrt{1 - v^{2}/c^{2}}}
$$

- \(\gamma\) — Lorentz factor (dimensionless, no unit; ALWAYS \(\ge 1\))
- \(v\) — relative speed between the two frames (\(\mathrm{m\,s^{-1}}\))
- \(c\) — speed of light \(= 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\)

\(\gamma = 1\) only when \(v = 0\); \(\gamma \to \infty\) as \(v \to c\).

Time dilation:

$$
t = t_{0} \gamma \qquad \left(\text{equivalently } t = \frac{t_{0}}{\sqrt{1 - v^{2}/c^{2}}}\right)
$$

- \(t\) — dilated (measured) time — events at DIFFERENT places; the LONGER time (s)
- \(t_{0}\) — proper time — events at the SAME place (one clock present at both); the SHORTER time (s)

Length contraction:

$$
L = \frac{L_{0}}{\gamma} \qquad \left(\text{equivalently } L = L_{0}\sqrt{1 - v^{2}/c^{2}}\right)
$$

- \(L\) — contracted (measured) length, from a frame in which the object MOVES; the SHORTER length (m)
- \(L_{0}\) — proper length — measured in the object's REST frame; the LONGER length (m)
- Acts ONLY along the direction of motion. Perpendicular dimensions unchanged.

Getting \(v\) back from \(\gamma\) (often needed in muon problems):

$$
v = c\sqrt{1 - 1/\gamma^{2}}
$$

Sanity checks: \(\gamma \ge 1\), \(t \ge t_{0}\), \(L \le L_{0}\). Any violation = algebra error.

### Listing 2 — Worked Example: time dilation (James and Mabry, v = 0.5c)

Q: Mabry's clock shows 5 min elapse as she moves past James at \(0.5c\). How much time passes for James?

Step 1 — identify the proper time: the two events (clock reads 12.00, clock reads 12.05) are at the SAME place on Mabry's moving clock \(\to\) \(t_{0} = 5\ \mathrm{min}\) (the proper, shorter time).

Step 2 — compute \(\gamma\) at \(v = 0.5c\):

$$
\frac{v^{2}}{c^{2}} = (0.5)^{2} = 0.25, \qquad 1 - 0.25 = 0.75, \qquad \sqrt{0.75} = 0.8660
$$

$$
\gamma = \frac{1}{0.8660} = 1.155
$$

Step 3 — apply \(t = t_{0}\gamma\):

$$
t = 5 \times 1.155 = 5.775\ \mathrm{min} \quad (= 5\ \mathrm{min}\ 46.5\ \mathrm{s})
$$

Answer: 5.775 minutes pass for James — the moving clock runs slow.

### Listing 3 — Derivation: length contraction from the tipped light clock

Tip the light clock so its length \(L\) lies ALONG the direction of motion (speed \(v\)). Pulse goes back mirror \(\to\) front mirror \(\to\) back mirror.

Outbound (front mirror recedes, light must catch up):

$$
t_{AB} = \frac{L}{c - v}
$$

Return (back mirror advances to meet the light):

$$
t_{BA} = \frac{L}{c + v}
$$

Total time (external frame):

$$
t = \frac{L}{c - v} + \frac{L}{c + v} = \frac{2Lc}{c^{2} - v^{2}}
$$

Set this equal to the time-dilated tick, with rest-frame relation \(t_{0} = 2L_{0}/c\):

$$
t = \frac{t_{0}}{\sqrt{1 - v^{2}/c^{2}}} = \frac{2L_{0}/c}{\sqrt{1 - v^{2}/c^{2}}}
$$

Equate and solve for the measured length \(L\):

$$
\frac{2Lc}{c^{2} - v^{2}} = \frac{2L_{0}/c}{\sqrt{1 - v^{2}/c^{2}}} \quad\Rightarrow\quad L = L_{0}\sqrt{1 - v^{2}/c^{2}} = \frac{L_{0}}{\gamma}
$$

Result: \(L = L_{0}/\gamma\) — moving lengths contract along the motion only.

### Listing 4 — Worked Example: length contraction (spacecraft at v = 0.5c)

Q: A spacecraft passes Earth at \(0.5c\). By what percentage is it contracted?

Step 1 — \(\gamma\) at \(0.5c = 1.155\) (from Listing 2).

Step 2 — ratio of measured length to proper length:

$$
\frac{L}{L_{0}} = \frac{1}{\gamma} = \frac{1}{1.155} = 0.866
$$

Step 3 — interpret:

$$
\text{Measured length} = 86.6\%\ \text{of proper length}, \qquad \text{Contraction} = 100\% - 86.6\% = 13.4\%
$$

Answer: contracted to 86.6% of proper length (a 13.4% contraction).
Note: at \(0.1c\) the contraction is \(< 1\%\) — significant effects only beyond \(\sim 0.1c\).

### Listing 5 — Worked Example: the muon evidence, both frames (Rossi–Hall)

Data: muon proper half-life \(t_{0} = 1.56\ \mathrm{\mu s}\) (measured at rest in the lab). Journey takes \(6.5\ \mathrm{\mu s}\) by Earth clocks; muons decay as though only \(0.7\ \mathrm{\mu s}\) passed.

**(a)** Proper time for the half-life \(=\) the half-life in the muon's own rest frame \(= 1.56\ \mathrm{\mu s}\).

**(b)** Lorentz factor from the two journey times:

$$
\gamma = \frac{t}{t_{0}} = \frac{6.5}{0.7} = 9.29
$$

**(c)** Speed of the muons (from \(\gamma\)):

$$
v = c\sqrt{1 - 1/\gamma^{2}} = c\sqrt{1 - 1/9.29^{2}} = c\sqrt{1 - 0.0116} = 0.994c
$$

**(d)** Half-life measured from Earth's frame (dilated):

$$
t = t_{0}\gamma = (1.56 \times 10^{-6})(9.29) = 1.45 \times 10^{-5}\ \mathrm{s} \approx 14\ \mathrm{\mu s}
$$

Both-frames narrative (full-mark answer):

- Earth frame: muon clock is TIME-DILATED \(\to\) half-life stretched \(1.56\ \mathrm{\mu s} \to \sim 14\ \mathrm{\mu s}\), long enough to cross the atmosphere before decaying.
- Muon frame: half-life is the normal \(1.56\ \mathrm{\mu s}\), but the atmosphere is LENGTH-CONTRACTED \(\to\) short journey, completed before decay.
- One result: far more muons reach the surface than classical physics predicts.

### Listing 6 — Worked Example: spaceship at v = 0.8c (exam Question 2)

Q: Ship passes Earth at \(0.8c\). One year passes on the ship. Time on Earth?

Step 1 — \(\gamma\) at \(0.8c\):

$$
\frac{v^{2}}{c^{2}} = (0.8)^{2} = 0.64, \qquad 1 - 0.64 = 0.36, \qquad \sqrt{0.36} = 0.6
$$

$$
\gamma = \frac{1}{0.6} = 1.67
$$

Step 2 — identify proper time: 1 year on the ship; the ship's clock is present at both events \(\to\) \(t_{0} = 1\ \mathrm{yr}\).

Step 3 — apply \(t = t_{0}\gamma\):

$$
t = 1 \times 1.67 = 1.67\ \text{years on Earth}
$$

Answer: 1.67 years pass on Earth per ship-year.

### Listing 7 — Worked Example: contracted rod at v = 0.6c (exam Question 5)

Q: A 1.00 m rod (rest length) moves at \(0.6c\) along its length. Measured length? Does its perpendicular width change?

Step 1 — \(\gamma\) at \(0.6c\):

$$
\frac{v^{2}}{c^{2}} = (0.6)^{2} = 0.36, \qquad 1 - 0.36 = 0.64, \qquad \sqrt{0.64} = 0.8
$$

$$
\gamma = \frac{1}{0.8} = 1.25
$$

Step 2 — proper length \(L_{0} = 1.00\ \mathrm{m}\) (rest-frame length).

Step 3 — apply \(L = L_{0}/\gamma\):

$$
L = \frac{1.00}{1.25} = 0.80\ \mathrm{m}
$$

Answer: measured length \(= 0.80\ \mathrm{m}\). Perpendicular width: UNCHANGED — contraction acts only along the motion.

### Listing 8 — Key values, constants and evidence (reference data)
| Item | Correct value / form |
|------|----------------------|
| Speed of light c | 3.0 × 10^8 m s^-1 (exact: 299 792 458 m s^-1) |
| Lorentz factor γ | \(1 / \sqrt{1 - v^{2}/c^{2}}\); dimensionless; always \(\ge 1\) |
| γ at 0.5c | 1.155 |
| γ at 0.6c | 1.25 |
| γ at 0.8c | 1.67 |
| γ at 0.994c | 9.29 (Rossi–Hall muons) |
| Proper time t₀ | events at the SAME place (clock's rest frame); the shorter time |
| Proper length L₀ | object's REST frame; the longer length |
| Muon proper half-life (Jacaranda) | 1.56 μs = 1.56 × 10^-6 s |
| Muon mean lifetime (alternative model) | 2.2 μs — do NOT mix with the 1.56 μs half-life |
| Rossi–Hall experiment | Bruno Rossi & David Hall, 1941; muon flux drops far less than classical prediction |
| Hafele–Keating experiment | 1971; caesium atomic clocks on airliners (east, west, ground) matched predictions |
| Atomic-clock basis | caesium-133; 1 second = 9 192 631 770 oscillations |
| GPS correction | without relativity, timing drifts > 30 μs/day → km-scale navigation errors |
| Hendrik Lorentz | 1853–1928; "Lorentz factor", "Lorentz contraction" |
| Fitzgerald–Lorentz proposal | Fitzgerald (1889) & Lorentz (1892): a PHYSICAL contraction to save the aether; Einstein needs no force, no aether |
| Einstein's relativity paper | 1905 (special relativity) |
| Metre (modern definition) | distance light travels in vacuum in 1/299 792 458 s |
