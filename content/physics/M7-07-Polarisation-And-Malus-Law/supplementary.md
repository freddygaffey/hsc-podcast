---
title: "Supplementary Materials — Polarisation and Malus's Law: The Plane of the Electric Field"
module: M7
lesson: "07"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. These listings are the read-along reference; the audio is self-contained and never depends on them, though it speaks the key results in words.

### Listing 1 — The two equations and the benchmark cosine-squared values

**Two filters, two rules**

**First filter (the POLARISER)**, acting on UNPOLARISED light:

$$
I = \tfrac{1}{2} I_0
$$

- \(I\) = intensity of emerging polarised light (\(\mathrm{W\,m^{-2}}\))
- \(I_0\) = intensity of incident unpolarised light (\(\mathrm{W\,m^{-2}}\))

\(\to\) Always one HALF. Independent of the filter's orientation. No angle, no cosine in this step.

**Second filter (the ANALYSER)**, acting on ALREADY-POLARISED light:

$$
I = I_{\max} \cos^{2}\theta \qquad \leftarrow \text{Malus's law (syllabus form)}
$$

- \(I\) = transmitted intensity (\(\mathrm{W\,m^{-2}}\))
- \(I_{\max}\) = polarised intensity arriving at analyser (\(\mathrm{W\,m^{-2}}\)) (value at \(\theta = 0°\))
- \(\theta\) = angle between the analyser's transmission axis and the plane of polarisation of the incident light (degrees)

**Why the square** (the key conceptual point):

$$
E = E_0 \cos\theta \quad \text{(resolving the vector)}, \qquad I \propto E^{2}
$$

$$
\Rightarrow I = I_{\max} \cos^{2}\theta \quad \text{(the cosine gets squared with the amplitude)}
$$

Mnemonic: "Malus loves to square."

**Benchmark values** (memorise — use to sanity-check answers):

- \(\theta = 0° \to \cos^{2}0° = 1 \to\) ALL transmitted
- \(\theta = 30° \to \cos^{2}30° = 0.75 \to\) three-quarters transmitted
- \(\theta = 45° \to \cos^{2}45° = 0.5 \to\) HALF transmitted
- \(\theta = 60° \to \cos^{2}60° = 0.25 \to\) one-quarter transmitted
- \(\theta = 90° \to \cos^{2}90° = 0 \to\) NONE transmitted (crossed filters)

### Listing 2 — Worked example: three filters in series (forward direction)

**Setup:** unpolarised light \(I_0 \to\) polariser \(\to\) analyser (\(60°\) to polariser) \(\to\) second analyser (\(30°\) to first analyser). Find the intensity after each stage as a % of \(I_0\).

**(a) After the POLARISER** (unpolarised \(\to\) polarised, the \(\tfrac{1}{2}\) step):

$$
I_a = \tfrac{1}{2} I_0, \qquad \frac{I_a}{I_0} = 0.5 = 50\%
$$

**(b) After the FIRST ANALYSER, \(60°\) to the polariser** (Malus's law):

$$
I_b = I_a \cos^{2}(60°) = 0.5\, I_0 \times (0.5)^{2} = 0.5\, I_0 \times 0.25 = 0.125\, I_0
$$

$$
\frac{I_b}{I_0} = 12.5\%
$$

**(c) After the SECOND ANALYSER, \(30°\) to the FIRST analyser** (Malus's law):

Use \(\theta = 30°\) — the angle between ADJACENT filters, NOT \(90°\) back to the polariser.

$$
I_c = I_b \cos^{2}(30°) = 0.125\, I_0 \times (0.8660)^{2} = 0.125\, I_0 \times 0.75 = 0.0938\, I_0
$$

$$
\frac{I_c}{I_0} \approx 9.4\%
$$

\(\to\) Light DOES emerge, even though the first and last filters are crossed at \(90°\). The middle filter re-projects the polarisation onto a new plane (three-polariser result).

**(d) REMOVE the middle analyser** (polariser + final analyser only, crossed at \(90°\)):

$$
I_d = I_a \cos^{2}(90°) = 0.5\, I_0 \times 0 = 0, \qquad \frac{I_d}{I_0} = 0\%
$$

\(\to\) With the middle filter gone, total extinction. The middle filter was the whole story.

### Listing 3 — Reverse problem: finding the angle (square-root FIRST)

**Problem:** Polarised light \(I_{\max}\) passes through one analyser; the transmitted intensity is \(\tfrac{1}{8} I_{\max}\). Find the angle \(\theta\).

$$
I = I_{\max} \cos^{2}\theta
$$

$$
\tfrac{1}{8} I_{\max} = I_{\max} \cos^{2}\theta
$$

$$
\cos^{2}\theta = 0.125 \qquad \leftarrow \text{divide (} I_{\max} \text{ cancels)}
$$

$$
\cos\theta = \sqrt{0.125} = 0.3536 \qquad \leftarrow \text{SQUARE-ROOT FIRST (do NOT inverse-cos 0.125)}
$$

$$
\theta = \cos^{-1}(0.3536) = 69.3° \approx 69°
$$

METHOD: divide \(\to\) root \(\to\) inverse-cosine. ("Malus makes you root.") TRAP: skipping the root and taking \(\cos^{-1}(0.125)\) gives \(\approx 82.8°\) — WRONG.

### Listing 4 — Exam Question 3, worked (polariser + analyser at 30°)

Unpolarised light \(I_0 \to\) polariser \(\to\) analyser at \(30°\). Find final \(I\) as % of \(I_0\).

After polariser (\(\tfrac{1}{2}\) step):

$$
I_1 = \tfrac{1}{2} I_0
$$

Through analyser (Malus):

$$
I_2 = I_1 \cos^{2}(30°) = \tfrac{1}{2} I_0 \times 0.75 = 0.375\, I_0 = \tfrac{3}{8} I_0
$$

$$
\frac{I_2}{I_0} = 37.5\%
$$

Marks: (1) \(\tfrac{1}{2}\) for the first filter; (2) \(\cos^{2}\theta\) (not \(\cos\theta\)) for the analyser; (3) correct final value 37.5 %.

### Listing 5 — Exam Question 5, worked (find θ given I = ¼ I_max)

Plane-polarised light \(\to\) analyser; transmitted intensity \(= \tfrac{1}{4}\) of incident polarised intensity. Find \(\theta\).

$$
\tfrac{1}{4} I_{\max} = I_{\max} \cos^{2}\theta
$$

$$
\cos^{2}\theta = 0.25
$$

$$
\cos\theta = \sqrt{0.25} = 0.5 \qquad \leftarrow \text{square-root FIRST}
$$

$$
\theta = \cos^{-1}(0.5) = 60°
$$

**Why a bare cosine fails:** Intensity \(\propto\) amplitude\(^{2}\); the analyser passes a field component \(\propto \cos\theta\), so intensity \(\propto \cos^{2}\theta\). Using a bare cosine you'd solve \(\cos\theta = 0.25 \to \theta \approx 75.5°\), which is WRONG (it ignores intensity \(\propto\) amplitude\(^{2}\)).

### Listing 6 — Key terms, names and contexts to get right
| Item | What to say in the exam |
|------|--------------------------|
| Plane of polarisation | Defined by the **electric field** (not the magnetic field) |
| Unpolarised light | Electric field oscillates in **all** planes perpendicular to propagation |
| Plane / linearly polarised | Electric field oscillates in **one** plane (synonyms) |
| Polariser | First filter: unpolarised → polarised, intensity → \(\tfrac{1}{2} I_0\) |
| Analyser | Second filter on polarised light: obeys \(I = I_{\max}\cos^{2}\theta\) |
| Transmission axis | The single direction a filter lets the field component through |
| Why transverse | Only **transverse** waves can be polarised; longitudinal (e.g. sound) cannot |
| Huygens | Proposed light was **longitudinal** — corrected by polarisation |
| Malus | Étienne-Louis Malus; the cosine-**squared** law bears his name |
| Hertz | Polarised radio waves by **rotating the receiver loop** (same physics) |
| Sunglasses | **Vertical** transmission axis blocks horizontally-polarised glare off water |
| Three pillars (wave model) | **D**iffraction, **I**nterference, **P**olarisation — "DIP"; P is the transverse clincher |
| Intensity unit | watts per square metre (\(\mathrm{W\,m^{-2}}\)); angle in degrees |
