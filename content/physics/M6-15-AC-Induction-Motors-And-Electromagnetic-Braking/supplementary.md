---
title: "Supplementary Materials — AC Induction Motors and Electromagnetic Braking"
module: M6
lesson: "15"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. These listings are the read-along reference; the audio is self-contained and never depends on them, though it speaks the key results in words.

### Listing 1 — Synchronous speed and slip (worked)

**The rotating field's speed (synchronous speed)**

The field rotates at the mains supply frequency. Australia: \(f = 50\ \mathrm{Hz}\).

$$
n_s = f = 50\ \mathrm{rev\,s^{-1}}
$$

In rpm:

$$
n_s = 50 \times 60 = 3000\ \mathrm{rpm} \quad \text{(single pole-pair)}
$$

(Use 50 Hz — that's Australia. 60 Hz is the US.)

**Slip — worked example**

- Synchronous (field) speed \(n_s = 3000\ \mathrm{rpm}\)
- Actual rotor speed (loaded) \(n_{\text{rotor}} = 2880\ \mathrm{rpm}\)

$$
\text{slip speed} = n_s - n_{\text{rotor}} = 3000 - 2880 = 120\ \mathrm{rpm}
$$

$$
\text{fractional slip} = \frac{n_s - n_{\text{rotor}}}{n_s} = \frac{120}{3000} = 0.04 = 4\%
$$

**Why slip is necessary**

At \(n_{\text{rotor}} = n_s\) exactly: relative speed \(= 0 \to \Delta\Phi/\Delta t = 0 \to\) induced EMF \(= 0 \to\) induced current \(= 0 \to\) force \(= 0 \to\) torque \(= 0\). The non-zero 120 rpm of slip is precisely what keeps the flux changing and the torque flowing. No slip \(\to\) no torque.

**Self-regulation**

More load \(\to\) rotor slows \(\to\) slip \(\uparrow \to \Delta\Phi/\Delta t \uparrow \to\) induced \(I \uparrow \to\) force \(F = BIL \uparrow \to\) torque \(\uparrow\) (rises to meet the load).

### Listing 2 — Faraday induction in one rotor bar (illustrative)

**Why slip produces an EMF — the core formula made quantitative**

**Given (one rotor loop):**

- Effective loop area \(A = 0.0030\ \mathrm{m^{2}}\)
- Stator field \(B = 0.40\ \mathrm{T}\)
- Field sweep changes flux from full (\(B\cdot A\)) to \(0\) in time \(\Delta t = 5.0 \times 10^{-3}\ \mathrm{s}\)
- Turns \(N = 1\)

**Flux**

$$
\Phi_{\text{initial}} = B A = 0.40 \times 0.0030 = 1.2 \times 10^{-3}\ \mathrm{Wb}
$$

$$
\Phi_{\text{final}} = 0\ \mathrm{Wb}
$$

$$
\Delta\Phi = \Phi_{\text{final}} - \Phi_{\text{initial}} = -1.2 \times 10^{-3}\ \mathrm{Wb} \quad (\text{magnitude } 1.2 \times 10^{-3}\ \mathrm{Wb})
$$

**Induced EMF (Faraday's law)**

$$
\varepsilon = -N \left(\frac{\Delta\Phi}{\Delta t}\right) = -(1) \times \frac{-1.2 \times 10^{-3}}{5.0 \times 10^{-3}} = 0.24\ \mathrm{V}
$$

**Interpretation**

\(\sim 0.24\ \mathrm{V}\) is induced in the bar each field sweep. The end rings short-circuit the thick, low-resistance bars, so this small EMF drives a LARGE current \(I\); that current in field \(B\) gives the force \(F = BIL\) that turns the rotor. Slip less (rotor catches up) \(\to \Delta t\) longer \(\to \Delta\Phi/\Delta t\) smaller \(\to\) EMF and torque fall. Faster slip \(\to\) more torque.

### Listing 3 — The torque chain (the examinable cause-and-effect order)

**AC induction motor — how induction makes torque** (write the links IN THIS ORDER for full marks):

1. Three-phase stator coils (\(120°\) apart, currents \(120°\) out of phase) \(\to\) resultant field of CONSTANT magnitude whose DIRECTION rotates at supply frequency = ROTATING FIELD.
2. Rotating field sweeps past stationary squirrel-cage bars \(\to\) RELATIVE MOTION between field and bars.
3. Relative motion \(\to\) magnetic flux through the rotor loops CHANGES with time.
4. FARADAY'S LAW: \(\varepsilon = -N\,(\Delta\Phi/\Delta t)\) \(\to\) changing flux induces an EMF; end rings close the loop \(\to\) large INDUCED (eddy) CURRENT in the bars.
5. MOTOR EFFECT: \(F = BIL\) \(\to\) each current-carrying bar in the stator field feels a FORCE.
6. LENZ'S LAW (= conservation of energy): induced current opposes the change (the relative motion) \(\to\) force drags the rotor IN THE DIRECTION OF FIELD ROTATION \(\to\) TORQUE.
7. SLIP: rotor must run slower than the field. At equal speed, no relative motion \(\to\) no torque. Slip is essential.

MEMORY HOOK: "Rotating Round, Faraday's Force, Lenz Follows" + the rotor must SLIP. Barer: "Faraday makes it, Lenz aims it."

### Listing 4 — Equations used in this episode (symbols and SI units)

**Magnetic flux**

$$
\Phi = B A \cos\theta
$$

- \(\Phi\) = magnetic flux (weber, \(\mathrm{Wb}\))
- \(B\) = magnetic flux density / field (tesla, \(\mathrm{T} = \mathrm{Wb\,m^{-2}}\))
- \(A\) = area (\(\mathrm{m^{2}}\))
- \(\theta\) = angle between \(B\) and the loop NORMAL (area vector)

**Faraday's law of induction**

$$
\varepsilon = -N \left(\frac{\Delta\Phi}{\Delta t}\right)
$$

- \(\varepsilon\) = induced EMF (volt, \(\mathrm{V}\))
- \(N\) = number of turns
- \(\Delta\Phi\) = change in flux \(= \Phi_{\text{final}} - \Phi_{\text{initial}}\) (\(\mathrm{Wb}\))
- \(\Delta t\) = time interval (\(\mathrm{s}\))
- The minus sign IS Lenz's law (EMF opposes the change).

**Motor effect** (force on each current-carrying bar)

$$
F = BIL \sin\theta \qquad (F = BIL \text{ when } \theta = 90°)
$$

- \(F\) = force (newton, \(\mathrm{N}\))
- \(I\) = induced current in the bar (ampere, \(\mathrm{A}\))
- \(L\) = length of bar in the field (metre, \(\mathrm{m}\))

**Electrical power consumed by the motor**

$$
P = VI
$$

\(P\) = power (watt, \(\mathrm{W}\)); \(V\) = terminal voltage (\(\mathrm{V}\)); \(I\) = stator current (\(\mathrm{A}\)).

**Resistive (Joule) heating** — where lost KE goes in braking

$$
P = I^{2} R \qquad (\mathrm{W},\ \mathrm{A},\ \text{ohm } \Omega)
$$

### Listing 5 — Electromagnetic braking (the cause-and-effect chain)

**How a force opposing motion is generated**

1. A conductor (disc / plate / rail) moves through a magnetic field \(\to\) RELATIVE MOTION between conductor and field.
2. Relative motion \(\to\) magnetic flux through the conductor CHANGES.
3. FARADAY'S LAW \(\to\) changing flux induces an EMF \(\to\) drives circulating EDDY CURRENTS in the bulk metal.
4. LENZ'S LAW (conservation of energy) \(\to\) eddy currents flow so as to OPPOSE the change \(\to\) they OPPOSE the motion \(\to\) RETARDING (braking) FORCE.
5. Kinetic energy \(\to\) HEAT (\(P = I^{2} R\)) in the conductor \(\to\) object slows.

**Key mark-earning feature**

Braking force \(\propto\) speed:

- fast \(\to\) flux changes fast \(\to\) big eddy currents \(\to\) big force
- slow \(\to\) small force

So the brake is strong at speed, fades as the object slows, and approaches rest ASYMPTOTICALLY. It cannot give a sudden complete stop on its own — a friction brake finishes the job.

CONTACTLESS, WEAR-FREE, SMOOTH. Uses: trains / trams, roller coasters, fairground rides, gym and exercise equipment.

### Listing 6 — Motor vs generator, and AC induction vs DC motor

**Energy transformation** (learn the exact wording):

- MOTOR: electrical energy \(\to\) rotational kinetic (mechanical)
- GENERATOR: mechanical kinetic energy \(\to\) electrical energy

Same device, opposite directions; both use the motor effect / electromagnetic induction. The exam tests the DIRECTION.

**AC induction motor vs DC motor** (use "whereas"):

- DC motor: current FED to the rotor via brushes + split-ring commutator (commutator reverses current each half-turn).
- AC induction motor: rotor current is INDUCED by the rotating field — NO brushes, NO commutator, NO slip rings on the rotor.
- \(\to\) Nothing rubs the rotor \(\to\) no wear, no sparking, low maintenance \(\to\) induction motor is more reliable; the most common motor made.

**Brushless DC motor** (cross-link): same induction-torque chain — torque from currents in the rotor produced WITHOUT brushes carrying rotor current (electronic commutation instead of mains three-phase).

### Listing 7 — Reference data
| Quantity | Symbol | Value / unit |
|---|---|---|
| Mains (supply) frequency, Australia | f | 50 Hz |
| Synchronous field speed (1 pole-pair) | n_s | 50 rev s^-1 = 3000 rpm |
| Magnetic flux | Φ | weber (Wb) |
| Magnetic flux density | B | tesla (T) = Wb m^-2 |
| Induced emf | ε | volt (V) |
| Induced current (in bars) | I | ampere (A) |
| Force per bar | F | newton (N) |
| Motor energy transform | — | electrical → rotational kinetic (mechanical) |
| Generator energy transform | — | mechanical kinetic → electrical |
