---
title: "Supplementary Materials — Back-EMF: The Motor That Fights Itself"
module: M6
lesson: "08"
script: script.md
---

# Supplementary Materials

Key equations, derivations, and worked numerical solutions for this episode. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The load-bearing relationships of this episode

**Where back-EMF comes from (production).** Magnetic flux through the coil:

$$
\Phi = B A \cos\theta
$$

- \(\Phi\) = magnetic flux (weber, \(\mathrm{Wb}\))
- \(B\) = magnetic field strength (tesla, \(\mathrm{T}\))
- \(A\) = coil area (\(\mathrm{m^{2}}\))
- \(\theta\) = angle between \(B\) and the coil's normal (area vector)

Rotating the coil sweeps \(\theta\) \(\to\) flux \(\Phi\) changes continuously. Faraday's law of induction:

$$
\varepsilon = -N \frac{\Delta\Phi}{\Delta t}
$$

- \(\varepsilon\) = induced EMF, here the back-EMF (volt, \(\mathrm{V}\))
- \(N\) = number of turns in the coil
- \(\Delta\Phi\) = change in flux (\(\mathrm{Wb}\))
- \(\Delta t\) = time interval (\(\mathrm{s}\))
- The minus sign IS Lenz's law: the EMF opposes the change.

Faster spin \(\to\) larger \(\Delta\Phi/\Delta t\) \(\to\) larger back-EMF. Zero spin (start-up or stall) \(\to\) \(\Delta\Phi/\Delta t = 0\) \(\to\) back-EMF = 0.

**What back-EMF does (effect on current) — the key equation.** Net (effective) voltage driving current:

$$
V_{\text{net}} = V_{\text{supply}} - \varepsilon_{\text{back}}
$$

Ohm's law on the armature (resistance \(R\)):

$$
I = \frac{V_{\text{net}}}{R} = \frac{V_{\text{supply}} - \varepsilon_{\text{back}}}{R}
$$

- \(I\) = current through the motor (ampere, \(\mathrm{A}\))
- \(V_{\text{supply}}\) = supply voltage (volt, \(\mathrm{V}\))
- \(\varepsilon_{\text{back}}\) = back-EMF (volt, \(\mathrm{V}\))
- \(R\) = armature resistance (ohm, \(\Omega\))

So: speed \(\uparrow\) \(\to\) \(\varepsilon_{\text{back}} \uparrow\) \(\to\) \(V_{\text{net}} \downarrow\) \(\to\) \(I \downarrow\).

**Supporting relations:**

- Motor-effect force (why current \(\to\) torque): \(F = B I L \sin\theta\)
- Resistive (Joule) heating (why stall burns out): \(P = I^{2} R\)

### Listing 2 — Worked example: motor current at start-up vs normal running

Given: armature resistance \(R = 10\ \Omega\), supply voltage \(V_{\text{supply}} = 240\ \mathrm{V}\), back-EMF (normal load) \(\varepsilon_{\text{back}} = 232\ \mathrm{V}\).

(a) CURRENT AT START-UP — coil stationary \(\to\) \(\varepsilon_{\text{back}} = 0\):

$$
V_{\text{net}} = V_{\text{supply}} - \varepsilon_{\text{back}} = 240 - 0 = 240\ \mathrm{V}
$$

$$
I = \frac{V_{\text{net}}}{R} = \frac{240}{10} = 24\ \mathrm{A} \quad \leftarrow \text{the start-up surge}
$$

(b) CURRENT AT NORMAL RUNNING SPEED — \(\varepsilon_{\text{back}} = 232\ \mathrm{V}\):

$$
V_{\text{net}} = V_{\text{supply}} - \varepsilon_{\text{back}} = 240 - 232 = 8\ \mathrm{V}
$$

$$
I = \frac{V_{\text{net}}}{R} = \frac{8}{10} = 0.8\ \mathrm{A} \quad \leftarrow \text{small, efficient running current}
$$

INTERPRETATION: start-up current / running current = \(24 / 0.8 = 30\times\). The motor draws 30 times its running current at switch-on, because no back-EMF exists until the coil moves.

### Listing 3 — Worked example (other way round): find the back-EMF

Given — electric drill: armature resistance \(R = 10\ \Omega\), supply voltage \(V_{\text{supply}} = 240\ \mathrm{V}\), running current \(I = 2.0\ \mathrm{A}\).

FIND THE BACK-EMF — net voltage when running = \(I \times R = 2.0 \times 10 = 20\ \mathrm{V}\). This \(V_{\text{net}}\) is \(V_{\text{supply}} - \varepsilon_{\text{back}}\), so:

$$
\varepsilon_{\text{back}} = V_{\text{supply}} - V_{\text{net}} = 240 - 20 = 220\ \mathrm{V}
$$

BONUS — start-up current (\(\varepsilon_{\text{back}} = 0\)):

$$
I = \frac{V_{\text{supply}}}{R} = \frac{240}{10} = 24\ \mathrm{A}
$$

WATCH THE TRAP: \(I \times R\) gives the NET voltage (\(20\ \mathrm{V}\)), not the supply. Subtract it FROM the supply to get the back-EMF.

### Listing 4 — Why a stalled motor burns out (the cause-and-effect chain)

STALL = rotor held stationary by an excessive load. The cause-and-effect chain:

$$
\text{speed} = 0 \to \frac{\Delta\Phi}{\Delta t} = 0 \to \varepsilon_{\text{back}} = 0 \to V_{\text{net}} = V_{\text{supply}} - 0 \to I = \frac{V_{\text{supply}}}{R} = \text{MAXIMUM}
$$

and it is CONTINUOUS (the coil never speeds up).

Heating: \(P = I^{2} R\). Current is ~30× the running value \(\to\) heating is \(\sim 30^{2} = 900\times\). Sustained heat cannot escape \(\to\) insulation fails \(\to\) motor burns out.

START-UP vs STALL — same physics, different duration:

- Start-up: max current for a split second, then back-EMF chokes it.
- Stall: max current forever, because the coil never moves.

MITIGATION at start-up: a SERIES STARTING RESISTOR limits the surge, then is switched out once back-EMF builds.

### Listing 5 — Exam question worked solution: 5 Ω motor

Given: \(R = 5.0\ \Omega\), \(V_{\text{supply}} = 240\ \mathrm{V}\), \(\varepsilon_{\text{back}}\) (normal speed) = \(237\ \mathrm{V}\).

START-UP (\(\varepsilon_{\text{back}} = 0\)):

$$
V_{\text{net}} = 240\ \mathrm{V} \qquad I = \frac{240}{5.0} = 48\ \mathrm{A}
$$

NORMAL OPERATING SPEED:

$$
V_{\text{net}} = V_{\text{supply}} - \varepsilon_{\text{back}} = 240 - 237 = 3\ \mathrm{V} \qquad I = \frac{3}{5.0} = 0.6\ \mathrm{A}
$$

COMMENT: \(48\ \mathrm{A} / 0.6\ \mathrm{A} = 80\times\) larger at start-up. The surge exists because there is no back-EMF until the coil moves; it falls sharply once the motor speeds up and back-EMF builds, reducing the net voltage and the current.
