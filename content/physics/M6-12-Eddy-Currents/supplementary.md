---
title: "Supplementary Materials — Eddy Currents: Lenz's Law in Bulk Conductors"
module: M6
lesson: "12"
script: script.md
---

# Supplementary Materials

Key equations, the worked braking example, the model extended-response answer, and the help-versus-harm reference table for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Electromagnetic braking, worked numerical example
PROBLEM — roller-coaster car: \(m = 600\ \mathrm{kg}\), enters braking section at \(v_i = 25\ \mathrm{m\,s^{-1}}\), leaves at \(v_f = 5.0\ \mathrm{m\,s^{-1}}\), braking distance \(d = 30\ \mathrm{m}\). Find: (a) KE removed (b) where it goes (c) average braking force.

(a) KINETIC ENERGY REMOVED (\(K = \tfrac{1}{2} m v^{2}\)):

$$
\begin{aligned}
K_i &= \tfrac{1}{2} \times 600 \times (25)^{2} = \tfrac{1}{2} \times 600 \times 625 = 187\,500\ \mathrm{J} \\
K_f &= \tfrac{1}{2} \times 600 \times (5.0)^{2} = \tfrac{1}{2} \times 600 \times 25 = 7\,500\ \mathrm{J} \\
\Delta K &= K_i - K_f = 187\,500 - 7\,500 = 180\,000\ \mathrm{J} = 1.8 \times 10^{5}\ \mathrm{J}\ (180\ \mathrm{kJ})
\end{aligned}
$$

(b) ENERGY PATHWAY (irreversible): kinetic energy \(\to\) electrical energy of eddy currents \(\to\) thermal energy. Dissipated by resistive (Joule) heating in the conductor: \(P = I^{2} R\) \(\Rightarrow\) ~180 kJ of heat is generated in the rail / fin.

(c) AVERAGE BRAKING FORCE (\(W = F d = \Delta K\)):

$$
F = \frac{\Delta K}{d} = \frac{180\,000}{30} = 6\,000\ \mathrm{N} = 6.0 \times 10^{3}\ \mathrm{N}
$$

directed OPPOSITE to the car's motion.

NOTE: \(6000\ \mathrm{N}\) is an AVERAGE. The instantaneous force is largest at \(25\ \mathrm{m\,s^{-1}}\) (largest \(\Delta\Phi/\Delta t\) \(\to\) largest eddy current \(\to\) largest \(F\)) and falls as \(v\) falls. Because \(F \to 0\) as \(v \to 0\), eddy brakes cannot deliver the final stop alone.

### Listing 2 — Model extended-response answer (6 marks): "Explain how electromagnetic braking works, with reference to eddy currents and Lenz's law."
When a solid metal conductor (train wheel, disc or fin) moves through an external magnetic field, the magnetic flux through the region of metal inside the field changes. By Faraday's law of electromagnetic induction, this changing flux induces an EMF in the metal: \(\varepsilon = -N(\Delta\Phi / \Delta t)\).

Because the conductor is a solid bulk material rather than a wire, the induced EMF drives circulating closed loops of current within the body of the metal. These are EDDY CURRENTS.

By Lenz's law, the eddy currents flow in the direction that creates a magnetic field opposing the change in flux that produced them. As a consequence, the side of each eddy-current loop lying inside the external field is a current-carrying conductor in a magnetic field and therefore experiences a force (\(F = BIL\)). The right-hand push rule shows this force always acts OPPOSITE to the direction of motion — a braking (retarding) force.

This opposing direction is required by conservation of energy: if the induced force aided the motion, the conductor would gain kinetic energy while also generating electrical energy — creating energy from nothing. Instead, the braking force does negative work, removing kinetic energy, which is transferred to the eddy currents and then dissipated as thermal energy through resistive heating (\(P = I^{2}R\)) as the electrons collide with the metal lattice. The process is irreversible and always heats the metal.

Because the induced EMF — and hence the eddy current and braking force — all increase with the rate of change of flux, the braking force INCREASES WITH SPEED. Electromagnetic braking is therefore strongest at high speed and weakens as the object slows, giving smooth, wear-free, contactless braking — but the force falls to zero as the object stops, so it cannot by itself bring the object fully to rest.

MARKING TARGETS HIT: defines eddy currents in a bulk conductor; Faraday's law as the origin; Lenz's law for direction; motor-effect force opposing motion; conservation-of-energy justification; KE \(\to\) heat dissipation; speed-dependence.

### Listing 3 — Where eddy currents help vs harm
| Context | Eddy currents are… | Mechanism / outcome | Engineering response |
|---|---|---|---|
| Train / tram / coaster brakes | Useful | Force opposes motion; smooth, contactless, wear-free; stronger at high speed | Exploit — switch the electromagnet on |
| Induction cooktop | Useful | AC field induces eddy currents in the pot → I²R heats the pot directly (~80% eff. vs ~43% gas) | Exploit; ceramic surface stays comparatively cool |
| Induction furnace | Useful | Eddy currents melt and stir the metal charge | Exploit |
| Metal detector / induction switch | Useful | Eddy currents load the coil, shift the oscillator frequency (up to ~22 MHz) → relay trips | Exploit |
| Moving-disc electricity meter | Useful | Disc braked in proportion to power drawn → measures energy use | Exploit |
| Transformer iron core | Harmful | Alternating flux induces eddy currents → heat loss, lower efficiency | Laminate the core (thin insulated sheets along flux); or use a ferrite |
| Motor / generator core | Harmful | Same eddy-current heating in rotor / stator cores | Laminate the core |

### Listing 4 — Core equations for this episode (words, symbols, SI units)
**Faraday's law (origin of the eddy current).** "Induced EMF = −(number of turns) × (rate of change of magnetic flux)":

$$
\varepsilon = -N \frac{\Delta\Phi}{\Delta t}
$$

- \(\varepsilon\) — induced EMF, volts (\(\mathrm{V}\))
- \(N\) — number of turns (dimensionless; \(N = 1\) for a single bulk loop)
- \(\Delta\Phi\) — change in magnetic flux, webers (\(\mathrm{Wb}\))
- \(\Delta t\) — change in time, seconds (\(\mathrm{s}\))
- The minus sign is Lenz's law: the induced effect opposes the change.

**Magnetic flux.** "Flux = field strength × area × cosine of angle to the normal":

$$
\Phi = B A \cos\theta
$$

- \(\Phi\) — magnetic flux, webers (\(\mathrm{Wb}\))
- \(B\) — magnetic flux density / field strength, teslas (\(\mathrm{T}\))
- \(A\) — area, square metres (\(\mathrm{m^{2}}\))
- \(\theta\) — angle between \(B\) and the normal (area vector) to the loop

**Motor-effect force on the eddy current (why it brakes).** "Force = field × current × length in field × sine of angle":

$$
F = B I L \sin\theta \qquad (= B I L \text{ when current} \perp \text{field})
$$

- \(F\) — force, newtons (\(\mathrm{N}\))
- \(B\) — field strength, teslas (\(\mathrm{T}\))
- \(I\) — current, amperes (\(\mathrm{A}\))
- \(L\) — length of conductor in the field, metres (\(\mathrm{m}\))

**Resistive (Joule) heating — where the energy ends up.** "Power dissipated = current squared × resistance":

$$
P = I^{2} R
$$

- \(P\) — power dissipated, watts (\(\mathrm{W}\))
- \(I\) — current, amperes (\(\mathrm{A}\))
- \(R\) — resistance, ohms (\(\Omega\))

**Energy bookkeeping (braking).** Work by braking force = loss in kinetic energy = heat generated:

$$
W = F d \qquad \Delta KE = \tfrac{1}{2} m v_i^{2} - \tfrac{1}{2} m v_f^{2}
$$

\(W\) work, joules (\(\mathrm{J}\)); \(F\) force, \(\mathrm{N}\); \(d\) distance, \(\mathrm{m}\); \(m\) mass, \(\mathrm{kg}\); \(v\) speed, \(\mathrm{m\,s^{-1}}\).
