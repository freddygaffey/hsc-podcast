---
title: "Supplementary Materials — Relativistic Momentum, E = mc-squared, and the Cosmic Speed Limit"
module: M7
lesson: "15"
script: script.md
---

# Supplementary Materials

Key equations and worked numerical solutions for the relativity capstone. Nothing here is spoken in the audio. Symbols: p = momentum; m₀ = rest mass; m = relativistic mass; v = speed; c = speed of light = 3.0 × 10⁸ m s⁻¹ (c² = 9.0 × 10¹⁶ m² s⁻²); γ = Lorentz factor = 1 / √(1 − v²/c²); E = energy.

### Listing 1 — Relativistic momentum (equation and worked example)

Relativistic momentum:

$$
p = \gamma m_{0} v = \frac{m_{0} v}{\sqrt{1 - v^{2}/c^{2}}}
$$

- \(\gamma\) — Lorentz factor (\(\ge 1\)); \(m_{0}\) — rest mass; \(v\) — speed relative to observer
- Low speed (\(v \ll c\)): \(\gamma \to 1\), so \(p \to m_{0}v\) (recovers Newton's \(p = mv\))

WORKED: momentum of a proton at \(v = 0.6c\) (\(m_{0} = 1.67 \times 10^{-27}\ \mathrm{kg}\)):

$$
\sqrt{1 - v^{2}/c^{2}} = \sqrt{1 - 0.6^{2}} = \sqrt{0.64} = 0.8 \qquad (\text{so } \gamma = 1.25)
$$

$$
p = \frac{m_{0} v}{0.8} = \frac{(1.67 \times 10^{-27})(0.6 \times 3.0 \times 10^{8})}{0.8} = \frac{(1.67 \times 10^{-27})(1.8 \times 10^{8})}{0.8} = 3.76 \times 10^{-19}\ \mathrm{kg\,m\,s^{-1}}
$$

### Listing 2 — Why a mass cannot reach the speed of light

Relativistic mass:

$$
m = \gamma m_{0} = \frac{m_{0}}{\sqrt{1 - v^{2}/c^{2}}}
$$

As \(v \to c\):

$$
\frac{v^{2}}{c^{2}} \to 1 \quad\Rightarrow\quad \sqrt{1 - v^{2}/c^{2}} \to 0 \quad\Rightarrow\quad \gamma \to \infty
$$

- \(\Rightarrow m = \gamma m_{0} \to \infty\) (inertia grows without limit)
- \(\Rightarrow p = \gamma m_{0} v \to \infty\) (momentum grows without limit)

Consequence chain (the band-6 answer): \(\gamma \to \infty\) \(\Rightarrow\) mass & momentum \(\to \infty\) \(\Rightarrow\) energy to accelerate further \(\to \infty\) \(\Rightarrow\) reaching \(c\) needs INFINITE energy \(\Rightarrow\) impossible for any object with mass. Only MASSLESS particles (photons, \(m_{0} = 0\)) travel at exactly \(c\).

⚠ "Mass increase" = increased inertia/momentum measured from an EXTERNAL frame. In its own rest frame nothing changes; the object does not physically swell. Conversion factor in \(E = mc^{2}\) is \(c^{2}\) (NOT \(c\)) — never drop the square.

### Listing 3 — E = mc²: power output of the Sun

Mass–energy equivalence: \(E = mc^{2}\) (and \(\Delta E = \Delta m\, c^{2}\)).

The Sun loses mass via fusion at \(\Delta m / \Delta t = 4.4 \times 10^{9}\ \mathrm{kg}\) per second. Power \(=\) energy per second \(=\) (mass lost per second) \(\times c^{2}\):

$$
P = (4.4 \times 10^{9})(9.0 \times 10^{16}) = 4.0 \times 10^{26}\ \mathrm{W}
$$

(Answer is a power directly, in watts, because the mass loss was per second.)

### Listing 4 — E = mc²: annihilation and combustion (100% vs negligible)

**Electron–positron annihilation** (100% of mass \(\to\) energy). Each mass \(m = 9.11 \times 10^{-31}\ \mathrm{kg}\); both annihilate.

$$
\text{Total mass converted} = 2 \times 9.11 \times 10^{-31} = 1.82 \times 10^{-30}\ \mathrm{kg}
$$

$$
E = mc^{2} = (1.82 \times 10^{-30})(9.0 \times 10^{16}) = 1.64 \times 10^{-13}\ \mathrm{J}
$$

(\(\approx 1.022\ \mathrm{MeV}\) total \(= 2 \times 0.511\ \mathrm{MeV}\), the electron rest energy) \(\to\) physics behind the PET scan (M8: case_pet_scans_antimatter).

**Chemical combustion** (negligible fraction of mass \(\to\) energy). Burn 1 tonne of coal, release \(\Delta E \approx 20 \times 10^{9}\ \mathrm{J}\):

$$
\Delta m = \frac{\Delta E}{c^{2}} = \frac{20 \times 10^{9}}{9.0 \times 10^{16}} \approx 2.2 \times 10^{-7}\ \mathrm{kg}
$$

(~0.2 milligram — far too small to weigh; why mass seemed conserved in chemistry).

Same equation, very different efficiency: annihilation 100% \(>\) nuclear fusion (small but significant) \(>\) combustion (negligible).

### Listing 5 — Particle-accelerator evidence: Newton vs relativity

Give a proton \(\Delta E = 11\ \mathrm{GeV}\) of energy (\(1\ \mathrm{GeV} = 10^{9} \times 1.6 \times 10^{-19}\ \mathrm{J}\)):

$$
\Delta E = 11 \times 10^{9} \times 1.6 \times 10^{-19} = 1.76 \times 10^{-9}\ \mathrm{J}
$$

RELATIVITY — energy goes mostly into MASS:

$$
\Delta m = \frac{\Delta E}{c^{2}} = \frac{1.76 \times 10^{-9}}{9.0 \times 10^{16}} = 1.96 \times 10^{-26}\ \mathrm{kg}
$$

Proton rest mass \(= 1.67 \times 10^{-27}\ \mathrm{kg}\) \(\Rightarrow\) accelerated proton behaves as \(\sim 13\times\) its rest mass; speed stays below \(c\). ✓ observed

NEWTON — if the same 11 GeV were ordinary kinetic energy \(\tfrac{1}{2}mv^{2}\):

$$
v = \sqrt{\frac{2E}{m}} = \sqrt{\frac{2 \times 1.76 \times 10^{-9}}{1.67 \times 10^{-27}}} = 1.45 \times 10^{9}\ \mathrm{m\,s^{-1}}
$$

(\(\approx 4.8\times\) the speed of light — IMPOSSIBLE) ✗

Above \(\sim 0.1c\) Newton fails; particles obey the relativistic equations exactly. \(\to\) M8: case_particle_accelerators_quarks
