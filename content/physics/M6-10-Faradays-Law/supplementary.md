---
title: "Supplementary Materials — Faraday's Law: Why Change Is Everything"
module: M6
lesson: "10"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Worked example: rectangular loop entering a field

Given: loop dimensions \(0.25\ \mathrm{m} \times 0.30\ \mathrm{m}\), field strength \(B = 0.66\ \mathrm{T}\) (perpendicular to plane of loop), time to enter \(\Delta t = 2.0\ \mathrm{s}\), number of turns \(N = 1\).

**Step 1 — area of the loop:** \(A = 0.25 \times 0.30 = 0.075\ \mathrm{m^{2}}\).

**Step 2 — change in flux** (\(\Phi = B A \cos\theta\)). Field \(\perp\) plane \(\to\) \(\theta = 0\) \(\to\) \(\cos\theta = 1\) \(\to\) \(\Phi = B A\):

$$
\begin{aligned}
\Phi_{\text{initial}} &= 0 \quad (\text{loop outside the field, no flux through it}) \\
\Phi_{\text{final}} &= B A = 0.66 \times 0.075 = 0.0495\ \mathrm{Wb} \approx 0.05\ \mathrm{Wb} \\
\Delta\Phi &= \Phi_{\text{final}} - \Phi_{\text{initial}} = 0.0495 - 0 = 0.0495\ \mathrm{Wb} \approx 0.05\ \mathrm{Wb}
\end{aligned}
$$

**Step 3 — Faraday's law** \(\varepsilon = -N(\Delta\Phi / \Delta t)\):

$$
\varepsilon = -(1)\left(\frac{0.0495}{2.0}\right) = -0.0248\ \mathrm{V} \qquad |\varepsilon| \approx 0.025\ \mathrm{V} = 25\ \mathrm{mV}
$$

The minus sign = direction (opposes the increasing flux) = Lenz's law (M6-11). For a "magnitude" question, report the positive value: \(0.025\ \mathrm{V}\).

NUMBER-OF-TURNS VARIANT (same flux change, \(N = 200\)):

$$
\varepsilon = 200 \times 0.0248 \approx 5.0\ \mathrm{V}
$$

Same \(\Delta\Phi/\Delta t\), 200× the EMF — purely from more turns in series.

### Listing 2 — Worked example: squashed loop (changing the AREA, not the field)

Given: initial radius \(r_i = 15.0\ \mathrm{cm} = 0.150\ \mathrm{m}\) (convert cm → m BEFORE squaring), final radius \(r_f = 7.0\ \mathrm{cm} = 0.070\ \mathrm{m}\), field strength \(B = 0.30\ \mathrm{T}\) (constant, \(\perp\) to loop), time \(\Delta t = 0.13\ \mathrm{s}\), number of turns \(N = 1\).

Areas (\(A = \pi r^{2}\)):

$$
A_i = \pi (0.150)^{2} = 0.07069\ \mathrm{m^{2}} \qquad A_f = \pi (0.070)^{2} = 0.01539\ \mathrm{m^{2}}
$$

Flux (\(\Phi = B A\), since \(\theta = 0\)):

$$
\Phi_i = 0.30 \times 0.07069 = 0.02121\ \mathrm{Wb} \qquad \Phi_f = 0.30 \times 0.01539 = 0.004618\ \mathrm{Wb}
$$

Change in flux:

$$
\Delta\Phi = \Phi_f - \Phi_i = 0.004618 - 0.02121 = -0.01659\ \mathrm{Wb}
$$

(negative: flux decreased because the loop shrank).

Faraday's law \(\varepsilon = -N(\Delta\Phi / \Delta t)\):

$$
\varepsilon = -(1)\left(\frac{-0.01659}{0.13}\right) = +0.1276\ \mathrm{V} \qquad |\varepsilon| \approx 0.13\ \mathrm{V}
$$

KEY POINT: \(B\) never changed — only \(A\) did. Same Faraday machinery still gives an EMF. Constant field does NOT mean constant flux. (This is "lever A" of the BAT.)

### Listing 3 — Faraday's law: the relationships, terms and units

**Faraday's law of electromagnetic induction:**

$$
\varepsilon = -N \frac{\Delta\Phi}{\Delta t}
$$

- \(\varepsilon\) = induced EMF (electromotive force) (volt, \(\mathrm{V}\))
- \(N\) = number of turns in the coil (a pure count, no units)
- \(\Delta\Phi\) = change in magnetic flux = \(\Phi_{\text{final}} - \Phi_{\text{initial}}\) (weber, \(\mathrm{Wb}\))
- \(\Delta t\) = time interval over which flux changes (second, \(\mathrm{s}\))
- minus sign = direction; the EMF opposes the change (Lenz's law, M6-11)

EMF depends on the RATE OF CHANGE of flux, not the flux itself. \(\Delta\Phi/\Delta t = 0\) \(\Rightarrow\) \(\varepsilon = 0\) (steady flux, however strong, induces nothing).

**Magnetic flux (the quantity that changes):**

$$
\Phi = B A \cos\theta
$$

- \(\Phi\) = magnetic flux (weber, \(\mathrm{Wb}\); \(1\ \mathrm{Wb} = 1\ \mathrm{T\cdot m^{2}} = 1\ \mathrm{V\cdot s}\))
- \(B\) = magnetic field strength (tesla, \(\mathrm{T}\); \(1\ \mathrm{T} = 1\ \mathrm{Wb\cdot m^{-2}}\))
- \(A\) = area of the loop (\(\mathrm{m^{2}}\))
- \(\theta\) = angle between \(B\) and the area vector (normal) of the loop; \(\theta = 0° \to \cos\theta = 1\) → maximum flux (field straight through); \(\theta = 90° \to \cos\theta = 0\) → zero flux (field lies in the plane)

**Three ways to change the flux — "swing the BAT":**

- \(B\): change the field strength (move a magnet; switch an electromagnet)
- \(A\): change the area in the field (slide a rod on rails; loop enters field)
- \(\theta\): change the angle (rotate the coil — this is a generator)

All three change \(\Phi\), so all three induce an EMF by the same law.

**Motional EMF — straight conductor moving \(\perp\) to a field:**

$$
\varepsilon = B L v \qquad \left(\text{derivable from Faraday: } \frac{\Delta\Phi}{\Delta t} = \frac{B \cdot (L \cdot v \cdot \Delta t)}{\Delta t} = B L v\right)
$$

\(B\) = field strength (\(\mathrm{T}\)), \(L\) = length in field (\(\mathrm{m}\)), \(v\) = speed (\(\mathrm{m\cdot s^{-1}}\)). Microscopic origin: each free charge feels force \(F = q v B\), which separates charge to the ends of the rod \(\to\) potential difference (EMF). (\(F = q v B\) is the same moving-charge force from M6-02.)

**Worked exam item — square loop, rising field (script Q4).** Side \(0.20\ \mathrm{m}\) \(\to\) \(A = 0.20^{2} = 0.04\ \mathrm{m^{2}}\). Field \(\perp\) plane: \(0 \to 0.50\ \mathrm{T}\) in \(0.10\ \mathrm{s}\).

$$
\Phi_i = 0, \quad \Phi_f = 0.50 \times 0.04 = 0.02\ \mathrm{Wb}, \quad \Delta\Phi = 0.02\ \mathrm{Wb}
$$

$$
\varepsilon = N \frac{\Delta\Phi}{\Delta t} = 1 \times \frac{0.02}{0.10} = 0.2\ \mathrm{V}
$$

### Listing 4 — Induction in the three named systems (the mechanism, in order)

**Solenoid + moving magnet (lever B: change field strength).** Magnet approaches \(\to\) field through coil \(\uparrow\) \(\to\) flux \(\Phi \uparrow\) \(\to\) Faraday: EMF induced in each turn \(\to\) series \(\to\) total = \(N \times\) (EMF/turn) \(\to\) current flows IF the coil is a closed circuit. Magnet held still \(\to\) \(\Phi\) constant \(\to\) \(\Delta\Phi/\Delta t = 0\) \(\to\) EMF = 0 (key exam point).

**Straight conductor moving through a field (lever A: change area).** Rod cuts field lines \(\to\) area of its circuit inside the field changes \(\to\) \(\Delta\Phi\).

- Macroscopic: rate of cutting field lines sets the EMF (\(\varepsilon = B L v\)).
- Microscopic: \(F = q v B\) pushes + and − charges to opposite ends \(\to\) charge separation \(\to\) potential difference (EMF) across the rod \(\to\) the rod acts as a source of EMF.

**Metal plate moving through a field (eddy currents — preview M6-12).** No wire loops, but changing flux through the bulk still induces an EMF \(\to\) drives circulating currents (EDDY CURRENTS) through the solid metal \(\to\) by Lenz's law they oppose the motion (braking force). TRAP: "no loop, so no induction" is WRONG — bulk metal induces too.

**Why more turns \(\to\) more EMF.** Every turn encloses the same changing flux \(\to\) same EMF per turn. Turns are in series \(\to\) EMFs add \(\to\) \(N\) turns give \(N \times\) the single-turn EMF.

### Listing 5 — Extended response: weak vs strong answer

QUESTION: "Explain why an EMF is induced when a magnet is moved into a solenoid."

**Weak answer (Band 4 — loses marks):** "Moving the magnet into the coil causes a current to flow." Faults: collapses the chain; treats the magnet as directly making current; conflates EMF with current; names no law.

**Strong answer (full marks) — the three-step chain:**

1. As the magnet moves in, the field through the coil increases, so the magnetic flux through the coil increases.
2. By Faraday's law, this change in flux induces an EMF equal to the number of turns times the rate of change of flux (faster magnet or more turns \(\to\) larger EMF).
3. This induced EMF drives an induced current around the coil — but ONLY if the coil forms a complete circuit. (Open circuit: EMF still present, no current flows.)

MEMORY HOOK: "Flux, EMF, Current, if Closed." Flux changes \(\to\) EMF appears \(\to\) current flows (only with a closed loop).

KEEP DISTINCT: EMF (a voltage; exists with or without a circuit) vs CURRENT (needs a complete conducting loop).

### Listing 6 — Reference data and common traps

| Item | Value / statement |
|------|-------------------|
| EMF (electromotive force) | symbol ε; unit volt (V); it is a voltage, NOT a force — the name is a misnomer |
| Magnetic flux | symbol Φ; unit weber (Wb); 1 Wb = 1 T·m² = 1 V·s |
| Magnetic field strength (flux density) | symbol B; unit tesla (T) = Wb·m⁻²; "flux density" means B, NOT flux Φ |
| Number of turns | symbol N (or n); a pure count, dimensionless |
| Δ (delta) | "change in" = final value − initial value |
| Electron charge magnitude | 1.6 × 10⁻¹⁹ C (for the q v B mechanism, if needed) |
| Michael Faraday | discovered electromagnetic induction, August 1831 (iron-ring + moving-magnet experiments) |
| Trap 1 | A strong but CONSTANT field induces nothing — only changing flux induces |
| Trap 2 | "Magnet makes current" collapses the chain — state flux → EMF → current (if closed) |
| Trap 3 | EMF ≠ current — open circuit still has an EMF, just no current |
| Trap 4 | Flux Φ ≠ field strength B — different symbols and units (Wb vs T) |
| Trap 5 | θ is measured from the NORMAL; max flux at θ = 0, zero flux at θ = 90° (use cos θ) |
| Trap 6 | Don't drop N — number of turns is itself an examinable factor |
| Trap 7 | Convert cm → m BEFORE squaring for area; mixing units gives errors of 10ⁿ |
| Trap 8 | The minus sign is direction only (Lenz) — for magnitude, report the positive value |
| Trap 9 | A metal plate with no wires can still be induced in (eddy currents) |
