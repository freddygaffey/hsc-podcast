---
title: "Supplementary Materials — Matter Waves: de Broglie, Electron Diffraction, and Standing Waves"
module: M8
lesson: "05"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference. Constants used throughout: Planck's constant \(h = 6.63 \times 10^{-34}\ \mathrm{J\cdot s}\); electron mass \(m_e = 9.1 \times 10^{-31}\ \mathrm{kg}\); elementary charge \(e = 1.6 \times 10^{-19}\ \mathrm{C}\); \(1\ \mathrm{eV} = 1.6 \times 10^{-19}\ \mathrm{J}\); speed of light \(c = 3.0 \times 10^{8}\ \mathrm{m\cdot s^{-1}}\).

### Listing 1 — Why a person never diffracts (de Broglie wavelength of an athlete)

de Broglie wavelength:

$$
\lambda = \frac{h}{p} = \frac{h}{mv}
$$

70 kg athlete sprinting at \(v = 10\ \mathrm{m/s}\):

$$
p = mv = (70)(10) = 700\ \mathrm{kg\cdot m\cdot s^{-1}}
$$

$$
\lambda = \frac{h}{p} = \frac{6.63 \times 10^{-34}}{700} = 9.5 \times 10^{-37}\ \mathrm{m}
$$

Conclusion: \(\sim 10^{-37}\ \mathrm{m}\) is far smaller than a proton (\(\sim 10^{-15}\ \mathrm{m}\)) and vastly smaller than any aperture, so diffraction is unobservable. The wave exists — it is just undetectably small.

(Contrast: a 60 g tennis ball at 30 m/s \(\to \lambda \approx 3.7 \times 10^{-34}\ \mathrm{m}\). Same conclusion.)

### Listing 2 — de Broglie wavelength of an electron (≈100 V, direct λ = h/mv)

Electron: \(m = 9.1 \times 10^{-31}\ \mathrm{kg}\), accelerated through \(\sim\)100 V \(\to v \approx 6.0 \times 10^{6}\ \mathrm{m/s}\).

$$
p = mv = (9.1 \times 10^{-31})(6.0 \times 10^{6}) = 5.5 \times 10^{-24}\ \mathrm{kg\cdot m\cdot s^{-1}}
$$

$$
\lambda = \frac{h}{p} = \frac{6.63 \times 10^{-34}}{5.5 \times 10^{-24}} = 1.2 \times 10^{-10}\ \mathrm{m}
$$

This is the same order of magnitude as the spacing between atoms in a crystal lattice (\(\sim 10^{-10}\ \mathrm{m} = 1\ \text{Å}\)), so a crystal acts as a ready-made diffraction grating for electrons.

Diffraction rule of thumb: noticeable diffraction when \(\lambda \gtrsim \tfrac{1}{10} \times\) aperture width.

### Listing 3 — The electron-diffraction evidence (key facts and figures)
| Experiment | Year | Method | Pattern observed | Result |
|------------|------|--------|------------------|--------|
| Davisson & Germer (USA) | 1927 | Beam of electrons reflected off a **single nickel crystal** (sample V = 54 V) in vacuum; intensity measured vs angle | Regular intensity **peaks** at specific angles | Wavelength from the diffraction angles **matched** \(\lambda = h/mv\) exactly |
| G. P. Thomson (England) | 1927 | Higher-energy electrons fired **through a thin polycrystalline metal foil** | Concentric **rings** (bullseye), analysed like X-ray diffraction | Wavelength again **matched** the de Broglie prediction |
| The Nobel irony | — | J. J. Thomson (Nobel **1897**) showed the electron is a **particle** (charge-to-mass ratio); his son G. P. Thomson (Nobel **1937**, with Davisson) showed it is a **wave** | — | "Father particle, son wave, both correct" — wave–particle duality |

### Listing 4 — The standing-wave condition for an allowed orbit

Picture the electron as a wave wrapped around a circular orbit of radius \(r\). For the wave to join smoothly onto itself (form a standing wave) and persist, the circumference must hold a WHOLE NUMBER of electron wavelengths:

$$
n \lambda = 2 \pi r \qquad n = 1, 2, 3, \dots\ (\text{positive integer})
$$

Equivalently:

$$
\lambda = \frac{2 \pi r}{n}
$$

If the circumference is NOT a whole number of wavelengths, the wave returns out of phase, interferes destructively with itself on each lap, and dies out — so that orbit is forbidden.

Chain to quantisation: only discrete \(\lambda\) allowed \(\to\) only discrete \(p\) allowed (\(p = h/\lambda\)) \(\to\) only discrete \(E\) allowed (quantised energy levels = Bohr's stationary states).

Guitar-string analogy (only certain harmonics "stand" on a string of length \(l\)):

$$
\lambda_n = \frac{2 l}{n}
$$

### Listing 5 — Structure of the full-mark "de Broglie fixes Bohr" extended response

STRONG ANSWER must contain, in order:

1. **The limitation:** Bohr POSTULATED that only certain orbits/energy levels are allowed but gave NO MECHANISM for why (Rutherford's criticism: "how does the electron know which orbit to occupy?").
2. **The de Broglie relation:** the electron has a wavelength \(\lambda = h/(mv)\) and behaves as a wave.
3. **The standing-wave condition:** for the electron-wave to persist around the orbit it must join smoothly onto itself \(\to\) a standing wave \(\to\) circumference = whole number of wavelengths, \(n \lambda = 2 \pi r\).
4. **Why other orbits die:** if the condition is not met, the wave interferes destructively with itself and dies out \(\to\) that orbit is forbidden.
5. **The payoff:** only standing-wave orbits survive \(\to\) discrete \(\lambda\) \(\to\) discrete \(p\) \(\to\) discrete (quantised) ENERGY LEVELS = exactly Bohr's stationary states. De Broglie SUPPLIED THE MISSING MECHANISM (like harmonics on a string).

WEAK ANSWER (band 4, \(\sim\)1 mark): "Electrons are waves because de Broglie said so." — asserts duality with no reason, never states the standing-wave condition, never connects to WHY orbits are quantised. The marks live in steps 3–5.

### Listing 6 — Schrödinger, Born, and Heisenberg (the modern model)

Schrödinger (1925–26): a WAVE EQUATION whose solutions are wave functions \(\psi\). Born: \(|\psi|^{2}\) gives the PROBABILITY of finding the electron at a location.

Bohr's definite circular ORBIT \(\to\) 3-D probability cloud called an ORBITAL:

- orbit (with a "t") = Bohr's definite path
- orbital (with "-al") = Schrödinger's fuzzy probability cloud ← marking trap

Schrödinger's model is FULLY quantum (no classical orbit bolted on):

- ✔ handles multi-electron atoms
- ✔ predicts relative line intensities (both of which Bohr could not)

Heisenberg uncertainty principle (late 1926):

$$
\Delta x \cdot \Delta p \ge \frac{h}{4\pi}
$$

CONSTANT TRAP: uncertainty uses \(h/(4\pi)\). Bohr's angular-momentum quantisation used \(h/(2\pi)\) — DIFFERENT result, do not swap.

Meaning: you cannot know position and momentum together, so a definite "orbit" must give way to "probability." (Schrödinger later showed his wave mechanics and Heisenberg's matrix mechanics are the same theory.)

### Listing 7 — Worked example: de Broglie wavelength of an electron accelerated through 600 V

Q: An electron is accelerated through a potential difference of 600 V. Find its de Broglie wavelength. (\(m = 9.1 \times 10^{-31}\ \mathrm{kg}\), \(e = 1.6 \times 10^{-19}\ \mathrm{C}\))

Step 1 — Kinetic energy gained = work done by the field:

$$
E_k = qV = (1.6 \times 10^{-19})(600) = 9.6 \times 10^{-17}\ \mathrm{J}
$$

Step 2 — Momentum from kinetic energy (\(E_k = p^{2}/2m \to p = \sqrt{2 m E_k}\)):

$$
p = \sqrt{2 \times 9.1 \times 10^{-31} \times 9.6 \times 10^{-17}} = \sqrt{1.747 \times 10^{-46}} = 1.32 \times 10^{-23}\ \mathrm{kg\cdot m\cdot s^{-1}}
$$

Step 3 — de Broglie wavelength:

$$
\lambda = \frac{h}{p} = \frac{6.63 \times 10^{-34}}{1.32 \times 10^{-23}} = 5.0 \times 10^{-11}\ \mathrm{m}
$$

Answer: \(\lambda \approx 5.0 \times 10^{-11}\ \mathrm{m}\) — comparable to the X-ray wavelength (\(7.1 \times 10^{-11}\ \mathrm{m}\)) used in foil experiments, which is why these electrons diffract off crystals just as X-rays do.

Combined form:

$$
\lambda = \frac{h}{\sqrt{2 m q V}}
$$

⚠ TYPO WARNING: some textbooks print the electron mass as \(9.1 \times 10^{-34}\ \mathrm{kg}\) here. That is wrong — use \(9.1 \times 10^{-31}\ \mathrm{kg}\). Only \(10^{-31}\) gives \(5.0 \times 10^{-11}\ \mathrm{m}\).

### Listing 8 — Reference data and key dates
| Quantity / fact | Value / detail |
|-----------------|----------------|
| Planck's constant h | 6.63 × 10⁻³⁴ J·s (= 4.15 × 10⁻¹⁵ eV·s) |
| Electron mass mₑ | 9.1 × 10⁻³¹ kg (data sheet 9.109 × 10⁻³¹ kg) |
| Electron charge e | 1.6 × 10⁻¹⁹ C |
| 1 eV | 1.6 × 10⁻¹⁹ J |
| Proton/neutron mass | ≈ 1.67 × 10⁻²⁷ kg (≈ 1800 × electron mass) |
| Crystal atomic spacing | ~10⁻¹⁰ m (= 1 Å) |
| Davisson–Germer voltage | V = 54 V (nickel crystal) |
| Louis de Broglie | matter-wave hypothesis 1923 (PhD thesis); atom standing-wave picture 1924 |
| Davisson & Germer | electron diffraction off nickel, 1927 |
| G. P. Thomson | electron diffraction through foil, 1927; Nobel 1937 |
| J. J. Thomson | electron as particle (q/m); Nobel 1897 |
| Erwin Schrödinger | wave equation / wave mechanics, 1925–26 |
| Max Born | probability interpretation of \|ψ\|² |
| Werner Heisenberg | uncertainty principle, late 1926 |
| Atomic-model order | Dalton → Thomson → Rutherford → Bohr → Schrödinger ("Dotty Tom Ran Bohr's Schedule") |
