---
title: "Supplementary Materials — The Electromagnetic Spectrum and Spectroscopy: Reading Light"
module: M7
lesson: "03"
script: script.md
---

# Supplementary Materials

Key equations, reference data, and worked solutions for this episode. These listings are the read-along reference; the audio is self-contained and never depends on them, though it speaks the key results in words.

### Listing 1 — Electron energy through an accelerating voltage (worked)

**Relationship**

$$
E_k = qV
$$

- \(E_k\) = kinetic energy gained (joule, \(\mathrm{J}\))
- \(q\) = charge (coulomb, \(\mathrm{C}\)); electron \(e = 1.6 \times 10^{-19}\ \mathrm{C}\)
- \(V\) = accelerating voltage (volt, \(\mathrm{V}\))

**Problem:** Calculate the energy of an electron accelerated through 100 kV (the order of voltage used in an X-ray tube).

**Step 1 — convert the voltage to base units**

$$
V = 100\ \mathrm{kV} = 100 \times 10^{3}\ \mathrm{V} = 1.0 \times 10^{5}\ \mathrm{V}
$$

**Step 2 — substitute**

$$
E_k = qV = (1.6 \times 10^{-19}\ \mathrm{C})(1.0 \times 10^{5}\ \mathrm{V})
$$

**Step 3 — evaluate**

$$
E_k = 1.6 \times 10^{-14}\ \mathrm{J} \quad (= 100\ \mathrm{keV})
$$

**Physics link** (why this sits in the spectrum episode): These high-energy electrons slam into a metal target and decelerate sharply. An accelerating/decelerating charge radiates EM waves; this violent deceleration emits at the high-frequency, high-energy end of the spectrum \(\to\) X-rays. High \(V \to\) high-energy electrons \(\to\) high-frequency radiation. (Same idea as Röntgen's discharge tube, 1895.)

### Listing 2 — The electromagnetic spectrum in order (low → high frequency)
| Region | Wavelength (longest → shortest) | Frequency / photon energy | Ionising? | Typical source / use |
|---|---|---|---|---|
| Radio | longest | lowest | No | broadcast, comms (Hertz's waves, 1887) |
| Microwave | ↓ | ↓ | No | radar, mobile phones, ovens |
| Infrared | ↓ | ↓ | No | radiant heat (fire, hot road) |
| Visible | ~400–700 nm | middle | No | the band the eye detects |
| Ultraviolet | ↓ | ↑ | **Yes** | sunburn / skin damage |
| X-ray | ↓ | ↑ | **Yes** | medical imaging (Röntgen) |
| Gamma | shortest | highest | **Yes** | nuclear processes |

**Mnemonic (low \(\to\) high frequency):** Radio Microwave Infrared Visible Ultraviolet X-ray Gamma \(\to\) "Raging Martians Invaded Venus Using X-ray Guns".

**Along the spectrum, radio \(\to\) gamma:**

- frequency \(\uparrow\) increases
- photon energy \(\uparrow\) increases (\(E = hf\), previewed; taught in M7-09)
- ionising power \(\uparrow\) increases
- WAVELENGTH \(\downarrow\) decreases (because \(c = f\lambda\) is fixed)

TRAP: gamma has the SHORTEST wavelength, NOT the longest. IONISING = top three only: Ultraviolet, X-ray, Gamma ("U-X-G"). "Non-ionising" \(\ne\) "safe": high-intensity IR/microwave still burns.

### Listing 3 — The visible spectrum and dispersing devices

**Visible light** (long \(\lambda \to\) short \(\lambda\)): Red Orange Yellow Green Blue Indigo Violet \(\to\) "ROY G BIV" (Newton, *Opticks*, 1704).

- Red \(\approx 700\ \mathrm{nm}\) (longest \(\lambda\), lowest energy)
- Violet \(\approx 400\ \mathrm{nm}\) (shortest \(\lambda\), highest energy)
- \(1\ \mathrm{nm} = 10^{-9}\ \mathrm{m}\); \(1\ \text{Å} = 10^{-10}\ \mathrm{m}\)

**Wave equation** (links frequency and wavelength)

$$
c = f \lambda
$$

- \(c\) = speed of light in vacuum \(= 3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\)
- \(f\) = frequency (\(\mathrm{Hz}\)); \(\lambda\) = wavelength (\(\mathrm{m}\))

Rearranged: \(f = c/\lambda\) \(\to\) shorter \(\lambda\) means higher \(f\) means higher photon energy.

**Photon energy** (previewed, not derived here — M7-09)

$$
E = hf
$$

with \(h\) = Planck constant \(= 6.63 \times 10^{-34}\ \mathrm{J\,s}\); \(1\ \mathrm{eV} = 1.6 \times 10^{-19}\ \mathrm{J}\).

**Dispersing devices** (both spread white light into a spectrum):

- PRISM — mechanism: REFRACTION. Different \(\lambda\) bend by different amounts. VIOLET bends MOST, red least.
- GRATING — mechanism: DIFFRACTION (full geometry in M7-06). RED diffracts MOST, violet least.
- TRAP: the colour order REVERSES between prism and grating.

### Listing 4 — The three spectra: causes, appearance, and the comparison answer

**Kirchhoff & Bunsen (1859) — the three types of spectrum**

1. **Continuous spectrum** — SOURCE: hot, DENSE glowing solid / liquid / dense gas (a black body, e.g. tungsten filament \(\sim 3000\ \mathrm{K}\)). APPEARANCE: unbroken band — ALL wavelengths present. CAUSE: electrons are not confined to discrete atomic levels; they move relatively freely and emit a continuous range of frequencies.

2. **Emission spectrum** — SOURCE: hot, LOW-DENSITY (rarefied) gas — a discharge tube. APPEARANCE: BRIGHT coloured lines on a DARK background. CAUSE: discharge excites electrons to higher levels; they fall back (de-excite) and emit photons of specific energies \(\to\) specific wavelengths \(\to\) bright lines.

3. **Absorption spectrum** — SOURCE: continuous source seen THROUGH a COOLER gas in front. APPEARANCE: DARK lines on a CONTINUOUS (rainbow) background. CAUSE: cool gas absorbs photons at its characteristic wavelengths (electrons jump up) and re-emits them in ALL directions \(\to\) those \(\lambda\) depleted along line of sight \(\to\) dark gaps. (Sun's = Fraunhofer lines.)

**Source \(\to\) spectrum hook**

- dense + hot = CONTINUOUS
- thin + hot = EMISSION
- cool gas in front of a continuous source = ABSORPTION

**The top-band link** (write this for "compare" questions): For ONE element, the DARK absorption lines fall at EXACTLY the same wavelengths as the BRIGHT emission lines — because BOTH arise from the SAME electron energy-level transitions in that element's atoms. (Emission = electron falls; absorption = electron rises; SAME energy gap \(\to\) SAME \(\lambda\).)

**Model extended response (6–7 marks)**

"Compare the emission and absorption spectra of a given element, and explain how spectra are used to identify the elements present in a gas."

- Emission: bright lines on dark; hot low-density gas; excited electrons fall to lower levels emitting photons of specific \(\lambda\).
- Absorption (in contrast): dark lines on a continuous background; continuous source through a cooler gas; gas absorbs at characteristic \(\lambda\) and re-emits in all directions, depleting those \(\lambda\).
- LINK: the dark absorption lines occur at exactly the same wavelengths as the bright emission lines — same energy-level transitions.
- IDENTIFY: every element has a UNIQUE set of lines, and every atom of an element gives the SAME set; match observed lines to known laboratory spectra \(\to\) identifies the element — even in a distant star (helium found in the Sun, 1868, before Earth, 1895).

### Listing 5 — Spectroscopy timeline and key names
| Year | Person | Contribution |
|---|---|---|
| 1704 | Isaac Newton | Disperses sunlight into ROYGBIV with a prism (*Opticks*) |
| 1802 | William Wollaston | Builds early spectroscope; first sees dark solar lines |
| 1814 | Joseph von Fraunhofer | Maps ~576 dark solar lines → **Fraunhofer lines** |
| 1859 | Kirchhoff & Bunsen | State the three laws of spectra; lines = element fingerprints |
| 1868 | Norman Lockyer | Predicts **helium** from an unexplained solar line (*helios* = Sun) |
| 1895 | Wilhelm Röntgen | Discovers X-rays from a discharge tube |
| 1895 | William Ramsay | Isolates helium on Earth, confirming Lockyer (27 years later) |

### Listing 6 — Constants and reference values
| Quantity | Symbol | Value |
|---|---|---|
| Speed of light (vacuum) | \(c\) | \(3.0 \times 10^{8}\ \mathrm{m\,s^{-1}}\) (exactly \(299\,792\,458\ \mathrm{m\,s^{-1}}\)) |
| Planck constant | \(h\) | \(6.63 \times 10^{-34}\ \mathrm{J\,s}\) |
| Electron charge | \(e\) | \(1.6 \times 10^{-19}\ \mathrm{C}\) |
| Electron-volt | \(1\ \mathrm{eV}\) | \(1.6 \times 10^{-19}\ \mathrm{J}\) |
| Visible range | \(\lambda\) | ~400 nm (violet) to ~700 nm (red) |
| Ångström | \(1\ \text{Å}\) | \(10^{-10}\ \mathrm{m}\) |
| Incandescent tungsten filament | T | ~3000 K (high melting point) |
| Absolute zero | 0 K | −273.15 °C (quote stellar temps in kelvin) |
