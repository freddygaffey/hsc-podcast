---
title: "Supplementary Materials — Evaluating the Wave Model: Diffraction, Interference and Polarisation as Evidence"
module: M7
lesson: "08"
script: script.md
---

# Supplementary Materials

Read-along reference for this episode: the full model extended-response answer, the worked
polarisation and interference numericals, and the key facts table. Nothing here is spoken in
the audio.

### Listing 1 — Model 7-mark answer: "Evaluate the evidence supporting the wave model of light"
```text
VERDICT (state up front):
  The classical wave model of light is strongly supported by three phenomena — diffraction,
  interference and polarisation — each of which Newton's rival particle (corpuscular) model
  cannot explain. However, it is ultimately shown incomplete by later quantum observations,
  so the evidence supports the wave model decisively for classical optics while exposing its limits.

SET THE CONTEST:
  Both Newton's particle model and Huygens's wave model explained reflection and refraction,
  so those phenomena do not decide between them. The models made OPPOSITE predictions for
  refraction into water: particle model → light speeds up; wave model → light slows down.
  In 1850 Foucault (and independently Fizeau, ~7 weeks later) measured light SLOWER in water
  → particle model refuted on refraction, wave model favoured.

PILLAR 1 — DIFFRACTION (observation + why particles fail):
  Light spreads around edges and through narrow gaps, producing fringes at a shadow's edge.
  Huygens's Principle: each point on a wavefront is a source of secondary wavelets that spread
  into the shadow region. WHEREAS Newton's particles travel in straight lines and have no
  mechanism to bend around a corner → diffraction is evidence light is a wave.

PILLAR 2 — INTERFERENCE (the decisive pillar):
  Young's double slit (1801–1803): two coherent beams give alternating bright and dark bands.
  Path difference = whole number of wavelengths → in phase → bright (constructive).
  Path difference = odd number of half-wavelengths → out of phase → dark (destructive).
  WHEREAS a particle model cannot produce the DARK bands: two streams of particles can only
  ADD to give more light, never cancel to give darkness. Light + light = darkness is decisive
  evidence for waves.

PILLAR 3 — POLARISATION (does two jobs):
  A filter restricts light to one plane; a crossed analyser (90°) extinguishes it (Malus: zero).
  (1) A particle stream has no plane of oscillation to filter → confirms light is a WAVE.
  (2) A longitudinal wave cannot be polarised → proves light is specifically TRANSVERSE,
      correcting Huygens (who thought light longitudinal). Hertz showed EM (radio) waves
      reflect, refract and polarise like light → light is an electromagnetic transverse wave.

JUDGEMENT + LIMIT (close):
  Evidence from Young, Fresnel, Foucault and Hertz OVERWHELMINGLY supports the wave model for
  classical light behaviour. HOWEVER it fails to explain black-body radiation (the ultraviolet
  catastrophe) and the photoelectric effect, both requiring discrete photons (quantum model).
  THEREFORE the wave model is strongly supported but NOT a complete description of light.

WHY IT SCORES: (1) states a verdict; (2) each pillar = observation + why particles fail (the
  contrast, not a list); (3) named historical evidence + the 1850 date; (4) gives the limitation
  that "evaluate" demands.
```

### Listing 2 — Worked numerical: the three-polariser puzzle

Setup: unpolarised light \(I_{0}\) \(\to\) polariser \(\to\) analyser at \(60°\) \(\to\) second analyser \(30°\) further (\(= 90°\) to the first filter, so first and last are CROSSED).

**(a)** After 1st filter (unpolarised \(\to\) use the \(\tfrac{1}{2}\) rule, NOT Malus's Law):

$$
I_a = \tfrac{1}{2} I_{0} \quad\to\quad \frac{I_a}{I_{0}} = 0.50 = 50\%
$$

**(b)** After \(60°\) analyser (now polarised \(\to\) Malus's Law, \(I = I_a \cos^{2}\theta\)):

$$
I_b = I_a \cos^{2}(60°) = (0.5\,I_{0})(0.5)^{2} = 0.5\,I_{0} \times 0.25 = 0.125\,I_{0} \quad\to\quad \frac{I_b}{I_{0}} = 12.5\%
$$

**(c)** After 2nd analyser, \(30°\) further (Malus again):

$$
I_c = I_b \cos^{2}(30°) = (0.125\,I_{0})(0.866)^{2} = 0.125\,I_{0} \times 0.75 = 0.0938\,I_{0} \quad\to\quad \frac{I_c}{I_{0}} \approx 9.4\%
$$

**(d)** Remove the MIDDLE filter (polariser + final analyser, crossed at \(90°\)):

$$
I_d = I_a \cos^{2}(90°) = 0.5\,I_{0} \times 0 = 0 \quad\to\quad \frac{I_d}{I_{0}} = 0\%
$$

Punchline: with the middle filter IN, ~9.4% gets through; REMOVE it and 0% gets through.
Resolution (classical): each filter re-projects the polarisation onto its own axis, so the
light reaching the last filter is only \(30°\) off (not \(90°\)). Classical component projection
reproduces these intensities exactly — but the behaviour is more naturally described by the
quantum model (each photon transmitted/absorbed with probability \(\cos^{2}\theta\)). A hint of the limit,
NOT a failure of the wave model.

Key cosine-squared values: \(\cos^{2}30° = 0.75\); \(\cos^{2}45° = 0.5\); \(\cos^{2}60° = 0.25\); \(\cos^{2}90° = 0\).
First filter on UNPOLARISED light \(\to\) \(\tfrac{1}{2}\) (averaged mean of \(\cos^{2}\theta\)); Malus's Law (\(\cos^{2}\theta\)) applies
only to already-POLARISED light hitting an analyser.

### Listing 3 — Worked numerical: double-slit interference (the evidence is measurable)

Given: \(d = 0.100\ \mathrm{mm} = 1.00 \times 10^{-4}\ \mathrm{m}\); \(L = 1.50\ \mathrm{m}\); \(\lambda = 589\ \mathrm{nm} = 589 \times 10^{-9}\ \mathrm{m}\).

Maxima condition (constructive interference):

$$
d \sin\theta = m \lambda
$$

**(a)** First-order maximum, \(m = 1\):

$$
\sin\theta = \frac{m\lambda}{d} = \frac{(1)(589 \times 10^{-9})}{1.00 \times 10^{-4}} = 5.89 \times 10^{-3}
$$

$$
\theta = \sin^{-1}(5.89 \times 10^{-3}) = 0.337°
$$

(tiny angle \(\to\) close slits, far screen). Position on screen:

$$
x = L \sin\theta = 1.50 \times \sin(0.337°) \approx 8.8 \times 10^{-3}\ \mathrm{m} = 8.8\ \mathrm{mm}
$$

**(b)** Third-order maximum, \(m = 3\) (fringes evenly spaced):

$$
x_{3} = 3 \times 8.8\ \mathrm{mm} = 26.4\ \mathrm{mm}
$$

Small-angle relation (alternative): \(\sin\theta \approx \tan\theta = x / L\), so \(x = \dfrac{m\lambda L}{d}\).

### Listing 4 — Key facts: the Newton-vs-Huygens contest and the three pillars
| Item | Detail (get this exact) |
|------|--------------------------|
| Newton's model | Particle / corpuscular model; "corpuscles"; dominant ~1670s–1700s |
| Huygens's model | Wave model; Huygens's Principle; WRONGLY thought light longitudinal |
| Don't decide the contest | Reflection and ordinary refraction (both models explain them) |
| Refraction prediction — particle | Light FASTER in water (medium attracts particles) |
| Refraction prediction — wave | Light SLOWER in water (wavefront slowed by denser medium) |
| The deciding measurement | Foucault (and Fizeau), 1850: light SLOWER in water → wave model wins |
| Three pillars (mnemonic: DIP) | Diffraction, Interference, Polarisation |
| Diffraction — why particles fail | Particles travel in straight lines; cannot bend round a corner |
| Interference — why particles fail | Particles can only add (bright); cannot cancel to make DARK bands |
| Polarisation — why decisive | No plane to filter → not particles; longitudinal can't polarise → TRANSVERSE |
| Definitive interference/diffraction | Thomas Young (~1801–1803); Augustin-Jean Fresnel (maths of diffraction) |
| EM-wave confirmation | Hertz: radio waves reflect, refract AND polarise like light |
| Coherent (precise) | Monochromatic (single λ) AND fixed/constant phase relationship |
| "Evaluate" demands | A stated VERDICT + the LIMITATION (criteria-based judgement) |
| The wave model's limit | Fails on black-body radiation (UV catastrophe) and the photoelectric effect → photons |
| Speed of light (vacuum) | c = 3.0 × 10⁸ m s⁻¹ (the contest is about v in water being LESS than c) |
