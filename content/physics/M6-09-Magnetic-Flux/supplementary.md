---
title: "Supplementary Materials — Magnetic Flux: What It Actually Means"
module: M6
lesson: "09"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The flux equation and three worked angle cases

**The definition (HSC data sheet):**

$$
\Phi = B A \cos\theta
$$

- \(\Phi\) = magnetic flux (weber, \(\mathrm{Wb}\))
- \(B\) = magnetic field strength (tesla, \(\mathrm{T}\))
- \(A\) = area of the loop / surface (\(\mathrm{m^{2}}\))
- \(\theta\) = angle between \(B\) and the AREA VECTOR (the normal to the loop) — NOT the angle between \(B\) and the plane of the loop

Equivalent form: \(\Phi = B_\perp A\), where \(B_\perp = B \cos\theta\) (only the component of \(B\) perpendicular to the face threads the loop).

Flux density: \(B = \Phi / A\) \(\to\) field strength IS the flux per unit area. Units: \(1\ \mathrm{Wb} = 1\ \mathrm{T\cdot m^{2}} = 1\ \mathrm{V\cdot s}\); \(1\ \mathrm{T} = 1\ \mathrm{Wb\cdot m^{-2}}\).

Given (all three versions): radius \(r = 8.0\ \mathrm{cm} = 0.080\ \mathrm{m}\) (convert BEFORE squaring), field \(B = 0.20\ \mathrm{T}\), area

$$
A = \pi r^{2} = \pi (0.080)^{2} = \pi \times 0.0064 = 0.020106\ldots\ \mathrm{m^{2}} \quad (\text{keep full precision})
$$

**Version A — field straight through the loop (\(\theta = 0°\), \(\cos 0° = 1\)):**

$$
\Phi = B A \cos\theta = 0.20 \times 0.020106 \times 1 = 0.0040\ \mathrm{Wb} = 4.0 \times 10^{-3}\ \mathrm{Wb} = 4.0\ \mathrm{mWb} \quad \leftarrow \text{MAXIMUM flux}
$$

**Version B — field at \(60°\) to the area vector (\(\theta = 60°\), \(\cos 60° = 0.5\)):**

$$
\Phi = 0.20 \times 0.020106 \times 0.5 = 0.0020\ \mathrm{Wb} = 2.0 \times 10^{-3}\ \mathrm{Wb} = 2.0\ \mathrm{mWb} \quad \leftarrow \text{HALF of A}
$$

Note: \(B\) and \(A\) are unchanged. The flux halves purely because the loop is tilted — fewer field lines thread it.

**Version C — field lying in the plane of the loop (\(\theta = 90°\), \(\cos 90° = 0\)):**

$$
\Phi = 0.20 \times 0.020106 \times 0 = 0\ \mathrm{Wb} \quad \leftarrow \text{ZERO flux}
$$

No field lines pass through; they all skim across the face.

### Listing 2 — Flux vs angle (cos θ intuition), for max flux B·A = 4.0 mWb

| Angle θ (field to normal) | Orientation | cos θ | Flux Φ |
|---|---|---|---|
| 0° | field straight through loop face (plane ⊥ field) | 1.000 | 4.0 mWb (maximum) |
| 30° | tilted slightly | 0.866 | 3.5 mWb |
| 60° | tilted more | 0.500 | 2.0 mWb |
| 90° | field in plane of loop (plane ∥ field) | 0 | 0 mWb |

### Listing 3 — Rectangular loop flux (and the Faraday preview, NOT solved here)

Given: loop dimensions \(0.25\ \mathrm{m} \times 0.30\ \mathrm{m}\), field \(B = 0.66\ \mathrm{T}\), perpendicular to loop (\(\theta = 0°\)).

Area: \(A = \text{length} \times \text{width} = 0.25 \times 0.30 = 0.075\ \mathrm{m^{2}}\).

Flux (\(\theta = 0°\), \(\cos\theta = 1\)):

$$
\Phi = B A \cos\theta = 0.66 \times 0.075 \times 1 = 0.0495\ \mathrm{Wb} \approx 0.05\ \mathrm{Wb}
$$

PREVIEW ONLY — belongs to M6-10 (Faraday), do NOT solve in this episode: if this flux is removed over \(\Delta t = 2.0\ \mathrm{s}\) in an \(N = 1\) loop, Faraday's law \(\varepsilon = -N(\Delta\Phi / \Delta t)\) would give \(|\varepsilon| = 0.0495 / 2.0 \approx 0.025\ \mathrm{V}\). Today's job is only step one: finding the flux \(\Phi\).

### Listing 4 — Exam worked solution: circular coil, two orientations

Given: radius \(r = 0.10\ \mathrm{m}\), field \(B = 0.40\ \mathrm{T}\).

Area: \(A = \pi r^{2} = \pi (0.10)^{2} = \pi \times 0.010 = 0.031416\ \mathrm{m^{2}}\).

(i) AREA VECTOR PARALLEL TO FIELD (\(\theta = 0°\), \(\cos\theta = 1\)):

$$
\Phi = B A \cos\theta = 0.40 \times 0.031416 \times 1 = 0.01257\ \mathrm{Wb} \approx 0.013\ \mathrm{Wb} \approx 13\ \mathrm{mWb}
$$

(ii) AREA VECTOR AT \(60°\) TO FIELD (\(\theta = 60°\), \(\cos\theta = 0.5\)):

$$
\Phi = 0.40 \times 0.031416 \times 0.5 = 0.00628\ \mathrm{Wb} \approx 0.0063\ \mathrm{Wb} \approx 6.3\ \mathrm{mWb} \quad (\text{exactly half of (i)})
$$

MARK-EARNING POINTS:

- radius converted/kept in metres before squaring
- \(\theta\) measured from the AREA VECTOR (normal), so cos used correctly
- both answers quoted in webers (\(\mathrm{Wb}\)), not tesla
