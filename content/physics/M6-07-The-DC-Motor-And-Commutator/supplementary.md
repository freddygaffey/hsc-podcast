---
title: "Supplementary Materials — The DC Motor: Components, Function, and the Commutator's Role"
module: M6
lesson: "07"
script: script.md
---

# Supplementary Materials

Key equations, the marked-up model answer, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it's the read-along reference.

### Listing 1 — Model answer: "Explain the role of the split-ring commutator" (3–4 marks), broken into scoring points
Q: Explain the role of the split-ring commutator in a simple DC motor. (3–4 marks)

**Weak answer (~1 mark):** "The commutator reverses the current." \(\to\) States what it does, but no WHEN, no WHY, no link to torque/rotation.

**Strong answer (full marks), mark by mark:**

- **[Set-up: torque]** The rotor coil carries current in a magnetic field, so the motor effect produces a force on the two coil sides perpendicular to the field (\(F = nBIL\)). These opposite forces on opposite sides of the axis form a couple \(\to\) a torque (\(\tau = nBIA \cos\theta\)) that rotates the coil.
- **[The problem]** As the coil rotates toward the position where its plane is perpendicular to \(B\) — the zero-torque position — torque falls to zero; the coil's momentum carries it PAST this point. The forces have NOT changed direction, so the torque would now push the coil BACK \(\to\) the coil would OSCILLATE about the zero-torque position, not rotate.
- **[The mechanism]** The split-ring commutator is a metal ring split into two insulated halves, each connected to one end of the coil, rotating with the coil while stationary brushes maintain contact. Just as the coil passes the zero-torque position, the insulating gap aligns with the brushes (circuit briefly broken); as rotation continues, each brush contacts the OPPOSITE segment \(\to\) current direction through the coil reverses.
- **[The result]** Reversing the current reverses the force on each side, so the torque keeps acting in the SAME rotational direction. \(\to\) Reverses current every half-turn at the zero-torque point, converting oscillation into CONTINUOUS one-way rotation.

RULE: every time you write "reverses the current", attach the WHEN (every half-turn, at the zero-torque position) and the WHY (so torque keeps acting one way \(\to\) continuous rotation).

### Listing 2 — Worked example: torque on a coil (magnitude)
Given: \(n = 15\) turns, \(B = 7.6\ \mathrm{mT} = 7.6 \times 10^{-3}\ \mathrm{T}\), \(I = 15\ \mathrm{mA} = 1.5 \times 10^{-2}\ \mathrm{A}\), coil = \(8.0\ \mathrm{cm} \times 12.0\ \mathrm{cm}\), \(\theta = 30°\) (angle between the COIL PLANE and \(B\) \(\to\) use \(\cos\theta\)).

Area: \(A = 0.080\ \mathrm{m} \times 0.120\ \mathrm{m} = 9.6 \times 10^{-3}\ \mathrm{m^{2}}\).

$$
\tau = n B I A \cos\theta
$$

Substitute and step through:

$$
\begin{aligned}
15 \times (7.6 \times 10^{-3}) &= 0.114 \\
0.114 \times (1.5 \times 10^{-2}) &= 1.71 \times 10^{-3} \\
(1.71 \times 10^{-3}) \times (9.6 \times 10^{-3}) &= 1.6416 \times 10^{-5} \\
\times \cos 30°\ (= 0.8660) &= 1.422 \times 10^{-5}
\end{aligned}
$$

$$
\tau \approx 1.4 \times 10^{-5}\ \mathrm{N\,m}
$$

### Listing 3 — Right-hand push (palm) rule, and the rotation direction
**Right-hand push (palm) rule — convention used here:**

- Fingers \(\to\) magnetic field \(B\) (from N pole to S pole)
- Thumb \(\to\) conventional current direction (flow of positive charge)
- Palm \(\to\) pushes in the direction of the FORCE on that conductor

Procedure for rotation direction:

1. Pick ONE identified side of the coil.
2. Note the current direction in that side and the field direction (N→S).
3. Apply the push rule \(\to\) read the force direction on that side.
4. That force, offset from the axis, gives the rotation sense.

For the Listing 2 coil: applying the push rule to the LEFT-HAND side \(\to\) force rotates it ANTICLOCKWISE.

Result: \(\tau \approx 1.4 \times 10^{-5}\ \mathrm{N\,m}\), rotating ANTICLOCKWISE. (In a real motor the commutator then reverses the current to keep it turning the same way.)

### Listing 4 — Worked example: maximum torque (exam Q5)
Given: \(n = 20\) turns, \(A = 5 \times 10^{-3}\ \mathrm{m^{2}}\), \(I = 2\ \mathrm{A}\), \(B = 0.1\ \mathrm{T}\).

Maximum torque \(\Rightarrow \cos\theta = 1 \Rightarrow \theta = 0° \Rightarrow\) COIL PLANE PARALLEL TO \(B\). Equation at maximum: \(\tau_{\max} = n B I A\).

$$
\begin{aligned}
20 \times 0.1 &= 2 \\
2 \times 2 &= 4 \\
4 \times (5 \times 10^{-3}) &= 2 \times 10^{-2}
\end{aligned}
$$

$$
\tau_{\max} = 2 \times 10^{-2}\ \mathrm{N\,m} = 0.02\ \mathrm{N\,m}
$$

occurring when the plane of the coil is PARALLEL to the field.

### Listing 5 — DC motor components and functions
| Component | Part of | Function (state this, not just the name) |
|-----------|---------|------------------------------------------|
| Rotor coil (armature coil) | Rotor | Carries the DC current; the conductor that feels the motor-effect force and rotates. Wound on the armature (soft-iron core) which concentrates the field. |
| Field magnets | Stator | Stationary permanent magnets or electromagnets; supply the external magnetic field (N→S) the coil sits in. |
| Brushes | Stationary | Graphite/carbon contacts (conduct + self-lubricate) that press on the rotating commutator to keep the spinning coil connected to the supply and stop the wires tangling. |
| Split-ring commutator | Rotor | Ring split into two insulated halves; reverses the coil current every half-turn at the zero-torque position so torque acts one way → continuous rotation. |

### Listing 6 — Key formulas and angle conventions
**Force on each active coil side (motor effect):**

$$
F = B I L \sin\theta \quad (\text{single conductor}) \qquad F = n B I L \sin\theta \quad (n \text{ turns})
$$

- \(\theta\) = angle between the CONDUCTOR and \(B\)
- \(F\) MAXIMUM at \(\theta = 90°\) (conductor \(\perp B\)); ZERO at \(\theta = 0°\) (conductor \(\parallel B\))
- Units: \(F\) (\(\mathrm{N}\)), \(B\) (\(\mathrm{T}\)), \(I\) (\(\mathrm{A}\)), \(L\) (\(\mathrm{m}\))

**Torque on the coil:**

$$
\tau = n B I A \cos\theta
$$

- \(\theta\) = angle between the COIL PLANE and \(B\)
- \(\tau\) MAXIMUM at \(\theta = 0°\) (plane \(\parallel B\)); ZERO at \(\theta = 90°\) (plane \(\perp B\))
- Units: \(\tau\) (\(\mathrm{N\,m}\)), \(A\) (\(\mathrm{m^{2}}\))
- Equivalent foundation: \(\tau = F d\) (\(d\) = perpendicular distance / moment arm)

NOTE on the two angles: \(F\) uses sin (angle from the conductor); \(\tau\) uses cos (angle from the coil plane). Same physics — different reference line. State which \(\theta\) you mean each time.

Factors that increase torque (read straight off \(\tau = nBIA\)):

- \(\uparrow n\) (more turns), \(\uparrow B\) (stronger magnets / soft-iron core)
- \(\uparrow I\) (more current/EMF), \(\uparrow A\) (larger coil area)
- radial pole pieces (keep sides \(\perp B\) for longer \(\to\) smoother torque)
- multiple coils + multi-segment commutator (no dead-spot \(\to\) higher average torque)

### Listing 7 — DC motor vs AC motor (the most-tested comparison)
| Feature | DC motor | AC motor (simple) |
|---------|----------|-------------------|
| Energy conversion | Electrical → rotational kinetic | Electrical → rotational kinetic |
| Supply current | One-directional (DC) | Alternating (reverses on its own) |
| Connection component | Split-ring commutator (split into 2 insulated halves) | Slip rings (continuous, unsplit) |
| Does it reverse coil current? | Yes — mechanically, every half-turn at the zero-torque point | No — the supply already reverses, so no mechanical reversal needed |
| Why that component | Reversal must be forced because DC flows one way | Slip rings only maintain continuous connection |
