---
title: "Supplementary Materials — Lenz's Law: Conservation of Energy in Disguise"
module: M6
lesson: "11"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — Worked example: induced EMF (Faraday) and direction (Lenz)

Given — flat circular coil in a uniform field: number of turns \(N = 50\), radius \(r = 0.10\ \mathrm{m}\), plane \(\perp\) field \(\theta = 0°\) \(\to\) \(\cos\theta = 1\) (field along the normal), field falls \(B_1 = 0.40\ \mathrm{T} \to B_2 = 0\ \mathrm{T}\), time interval \(\Delta t = 0.20\ \mathrm{s}\).

**Step 1 — area of the coil:**

$$
A = \pi r^{2} = \pi (0.10)^{2} = \pi (0.01) = 3.14 \times 10^{-2}\ \mathrm{m^{2}}
$$

**Step 2 — flux per turn** (\(\Phi = B A \cos\theta\), \(\cos\theta = 1\)):

$$
\begin{aligned}
\Phi_1 &= B_1 A = 0.40 \times 3.14 \times 10^{-2} = 1.26 \times 10^{-2}\ \mathrm{Wb} \\
\Phi_2 &= B_2 A = 0 \times 3.14 \times 10^{-2} = 0\ \mathrm{Wb} \\
\Delta\Phi &= \Phi_2 - \Phi_1 = 0 - 1.26 \times 10^{-2} = -1.26 \times 10^{-2}\ \mathrm{Wb} \quad (\text{flux DECREASES})
\end{aligned}
$$

**Step 3 — Faraday's law** (magnitude — drop the minus sign):

$$
|\varepsilon| = N \left|\frac{\Delta\Phi}{\Delta t}\right| = 50 \times \frac{1.26 \times 10^{-2}}{0.20} = 50 \times (6.28 \times 10^{-2}) = 3.14\ \mathrm{V} \approx 3.1\ \mathrm{V}
$$

**Step 4 — Lenz's law (direction, part b).** Flux is decreasing \(\to\) induced current OPPOSES the decrease \(\to\) induced field points the SAME way as the original field \(\to\) current flows so as to reinforce the original field direction (right-hand grip rule: thumb along original field, fingers = current).

ANSWER: (a) \(|\varepsilon| \approx 3.1\ \mathrm{V}\); (b) current reinforces the original field direction (opposing the decrease).

NOTE — the minus sign in \(\varepsilon = -N(\Delta\Phi/\Delta t)\) carries DIRECTION only. Never substitute it into a magnitude calculation.

### Listing 2 — The conservation-of-energy argument (proof by contradiction)

**Lenz's law (marker-preferred wording):** An induced current always flows in the direction that creates a magnetic field OPPOSING THE CHANGE in flux that produced it. (Opposes the CHANGE — not the flux, not the magnet.)

**Why it must oppose — assume the opposite, then watch energy break:**

1. ASSUME the induced current REINFORCES the change. (N-pole approaches coil \(\to\) coil's near face becomes a S-pole that ATTRACTS the magnet, instead of a N-pole that repels it.)
2. Attractive force \(\to\) magnet ACCELERATES toward the coil.
3. Faster magnet \(\to\) greater rate of change of flux (\(\Delta\Phi/\Delta t \uparrow\)).
4. Faraday's law \(\to\) larger induced EMF and current.
5. Larger current \(\to\) stronger coil field \(\to\) stronger attraction.
6. Stronger force \(\to\) magnet accelerates MORE \(\to\) loop runs away.
7. Both KE (magnet) and electrical energy (coil) grow with NO external energy input.
8. = a PERPETUAL MOTION MACHINE \(\to\) violates conservation of energy \(\to\) IMPOSSIBLE.
9. CONCLUSION: the induced current must OPPOSE the change. \(\to\) This is Lenz's law.

**Where the energy really comes from (the positive side).** Coil opposes the magnet's motion (repels on approach, attracts on withdrawal), so an external agent must do mechanical WORK to move it.

$$
\text{Work (mechanical)} \to \text{electrical energy (induced current)} \to \text{heat } (P = I^{2}R)
$$

"Work, Watts, Warmth." Every joule of induced electrical energy is paid for by mechanical work. Energy is conserved at every stage.

**The three "same law" applications (preview):**

- Magnet falling through a tube/solenoid \(\to\) opposing force, falls slowly [M6-12]
- Conductor plate moving into a field \(\to\) braking force (EM braking) [M6-12, M6-15]
- Spinning motor rotor \(\to\) back-EMF opposing the supply [M6-08]

### Listing 3 — Worked example: combined Faraday + Lenz (200-turn coil)

Given: number of turns \(N = 200\), coil area \(A = 2 \times 10^{-3}\ \mathrm{m^{2}}\), plane \(\perp\) field \(\theta = 0°\) \(\to\) \(\cos\theta = 1\), field falls \(B_1 = 0.5\ \mathrm{T} \to B_2 = 0.1\ \mathrm{T}\), time interval \(\Delta t = 0.10\ \mathrm{s}\).

Flux per turn (\(\Phi = B A \cos\theta\)):

$$
\begin{aligned}
\Phi_1 &= 0.5 \times 2 \times 10^{-3} = 1.0 \times 10^{-3}\ \mathrm{Wb} \\
\Phi_2 &= 0.1 \times 2 \times 10^{-3} = 0.2 \times 10^{-3}\ \mathrm{Wb} \\
|\Delta\Phi| &= (1.0 - 0.2) \times 10^{-3} = 0.8 \times 10^{-3}\ \mathrm{Wb}
\end{aligned}
$$

Faraday's law (magnitude):

$$
|\varepsilon| = N \left|\frac{\Delta\Phi}{\Delta t}\right| = 200 \times \frac{0.8 \times 10^{-3}}{0.10} = 200 \times (8 \times 10^{-3}) = 1.6\ \mathrm{V}
$$

Lenz's law (direction): flux is DECREASING \(\to\) induced current opposes the decrease \(\to\) induced field points the SAME way as the original field (it acts to maintain/replace the disappearing flux).

ANSWER: \(|\varepsilon| = 1.6\ \mathrm{V}\); current flows to reinforce the original field direction.

### Listing 4 — Finding the induced-current direction (the 3-step procedure)

**"Change, Oppose, Grip"**

1. **Change:** how is the flux through the loop changing? Increasing or decreasing, and in which direction does it point?
2. **Oppose:** which way must the INDUCED field point to oppose that change?
   - Flux increasing \(\to\) induced field points OPPOSITE to the external field (fight the increase).
   - Flux decreasing \(\to\) induced field points the SAME way as the original field (replace the lost flux).
3. **Grip:** right-hand GRIP (curl) rule for a coil. Thumb \(\to\) direction of the required induced field inside the coil. Curled fingers \(\to\) direction of the induced (conventional) current.

**Worked direction cases:**

- N-pole APPROACHING coil: flux into coil increasing \(\to\) near face must be a N-pole to repel \(\to\) current ANTICLOCKWISE (viewed from magnet).
- N-pole WITHDRAWING: flux decreasing \(\to\) near face becomes a S-pole to attract \(\to\) current reverses to CLOCKWISE.
- Ring pulled OUT of into-page field: into-page flux decreasing \(\to\) induced current CLOCKWISE to maintain into-page flux; current STOPS once the ring fully exits the field.

WARNING — use the right-hand GRIP rule (field→current for a coil), NOT the flat-hand/palm rule (force on a moving charge). Different rule.

### Listing 5 — Key terms, symbols and units for this episode

| Quantity / item | Symbol | Unit | Note |
|-----------------|--------|------|------|
| Induced EMF | ε (epsilon) | volt (V) | a voltage, NOT a force |
| Number of turns | N | (dimensionless) | integer |
| Magnetic flux | Φ (phi) | weber (Wb) | 1 Wb = 1 T·m² = 1 V·s |
| Magnetic field strength | B | tesla (T) | flux density |
| Loop area | A | square metre (m²) | |
| Angle in flux | θ (theta) | degrees / radians | between B and the NORMAL, not the plane |
| Time interval | Δt | second (s) | |
| Faraday's law (with Lenz sign) | ε = −N(ΔΦ/Δt) | V | minus sign = Lenz (direction only) |
| Flux | Φ = B A cos θ | Wb | max at θ = 0°, zero at θ = 90° |
| Resistive heating | P = I²R | watt (W) | energy destination |
| Lenz (person) | — | — | H. F. Lenz, 1804–1864, German |
