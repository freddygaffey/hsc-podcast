---
title: "Supplementary Materials — LEO and Geostationary Satellites — Newton's Orbits in Practice"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Deriving orbital velocity (gravity = centripetal force)

Set the gravitational force equal to the centripetal force:

$$
\frac{G M m}{r^{2}} = \frac{m v^{2}}{r}
$$

Cancel the satellite mass \(m\) from both sides:

$$
\frac{G M}{r^{2}} = \frac{v^{2}}{r}
$$

Multiply both sides by \(r\):

$$
\frac{G M}{r} = v^{2}
$$

Take the square root:

$$
v = \sqrt{\frac{G M}{r}}
$$

where:

- \(v\) — orbital speed (m/s)
- \(G = 6.674\times 10^{-11}\ \mathrm{N\,m^{2}\,kg^{-2}}\) (universal gravitational constant)
- \(M = 5.972\times 10^{24}\ \mathrm{kg}\) (mass of the Earth)
- \(r\) — orbital radius from Earth's CENTRE (m) \(= R_{\text{earth}} + \text{altitude}\)

Key results:

- satellite mass \(m\) cancels: orbital speed is independent of satellite mass
- larger \(r\) \(\to\) smaller \(v\) (higher orbits are slower)

### Listing 2 — Deriving Kepler's Law of Periods from Newton

Start again from gravity = centripetal force:

$$
\frac{G M m}{r^{2}} = \frac{m v^{2}}{r}
$$

Orbital speed in terms of period \(T\) (one lap = circumference / time):

$$
v = \frac{2\pi r}{T}
$$

Substitute and simplify:

$$
\frac{G M}{r^{2}} = \frac{(2\pi r / T)^{2}}{r} = \frac{4\pi^{2} r}{T^{2}}
$$

Rearrange:

$$
\frac{r^{3}}{T^{2}} = \frac{G M}{4\pi^{2}} = \text{constant}
$$

This is Kepler's Third Law: \(T^{2}\) is proportional to \(r^{3}\), with the constant fixed by the mass of the central body only.

### Listing 3 — Worked example: solving for geostationary altitude

**Goal:** find the altitude where orbital period = 1 sidereal day.

Given: \(T = 86{,}164\ \mathrm{s}\) (one sidereal day, NOT the \(86{,}400\ \mathrm{s}\) solar day), \(G = 6.674\times 10^{-11}\ \mathrm{N\,m^{2}\,kg^{-2}}\), \(M = 5.972\times 10^{24}\ \mathrm{kg}\), \(R_{\text{earth}} = 6.378\times 10^{6}\ \mathrm{m}\).

Rearrange Kepler's law for \(r\):

$$
r^{3} = \frac{G M T^{2}}{4\pi^{2}}
$$

**Step 1 — numerator \(G M T^{2}\):**

$$
\begin{aligned}
G M &= 6.674\times 10^{-11} \times 5.972\times 10^{24} = 3.986\times 10^{14} \\
T^{2} &= (86{,}164)^{2} = 7.424\times 10^{9} \\
G M T^{2} &= 3.986\times 10^{14} \times 7.424\times 10^{9} = 2.959\times 10^{24}
\end{aligned}
$$

**Step 2 — divide by \(4\pi^{2}\) (\(= 39.48\)):**

$$
r^{3} = \frac{2.959\times 10^{24}}{39.48} = 7.495\times 10^{22}\ \mathrm{m^{3}}
$$

**Step 3 — cube root:**

$$
r = (7.495\times 10^{22})^{1/3} = 4.216\times 10^{7}\ \mathrm{m} = 42{,}164\ \mathrm{km} \quad \text{(from Earth's centre)}
$$

**Step 4 — subtract Earth's radius for altitude:**

$$
\text{altitude} = 42{,}164 - 6{,}378 = 35{,}786\ \mathrm{km}
$$

Orbital speed at this radius (from Listing 1):

$$
v = \sqrt{\frac{3.986\times 10^{14}}{4.216\times 10^{7}}} = 3{,}075\ \mathrm{m/s} \quad \text{(about 3.07 km/s)}
$$

### Listing 4 — Orbit comparison table
| Orbit type | Altitude | Radius from centre | Orbital speed | Period | Example uses |
|------------|----------|--------------------|---------------|--------|--------------|
| Low Earth Orbit (LEO) | 200–2,000 km | ~6,600–8,400 km | ~7.7 km/s | ~90–127 min | ISS, imaging, weather |
| Medium Earth Orbit (MEO) | ~20,200 km | ~26,560 km | ~3.87 km/s | ~11 h 58 min | GPS / GNSS navigation |
| Geostationary (GEO) | 35,786 km | 42,164 km | ~3.07 km/s | 23 h 56 min 4 s | TV broadcast, weather, comms |
| ISS (specific LEO) | ~408–420 km | ~6,790 km | ~7.66 km/s | ~92.7 min | crewed station |

Note: ISS inclination 51.6 degrees; GEO inclination must be 0 degrees (equatorial) and eccentricity 0.

### Listing 5 — GPS relativistic clock correction

Two relativistic effects act on a GPS satellite clock vs a ground clock.

**Special relativity** (satellite moves fast \(\to\) its clock runs SLOW), fractional rate \(\approx -v^{2} / (2 c^{2})\), with \(v = 3{,}870\ \mathrm{m/s}\), \(c = 3.00\times 10^{8}\ \mathrm{m/s}\):

$$
-\frac{(3870)^{2}}{2 \cdot (3.00\times 10^{8})^{2}} = -8.32\times 10^{-11}\ \text{per second} \to \text{about } -7.2\ \mu\mathrm{s}\ \text{per day}
$$

**General relativity** (weaker gravity at altitude \(\to\) clock runs FAST), fractional rate:

$$
+5.31\times 10^{-10}\ \text{per second} \to \text{about } +45.9\ \mu\mathrm{s}\ \text{per day}
$$

**Net effect** (gravity term dominates):

$$
+45.9 - 7.2 = +38.4\ \mu\mathrm{s}\ \text{per day} \quad \text{(satellite clock runs FAST)}
$$

Why it matters (convert timing error to position error):

$$
\text{distance error} = (38.4\times 10^{-6}\ \mathrm{s}) \cdot (3.00\times 10^{8}\ \mathrm{m/s}) = 11{,}520\ \mathrm{m} \approx 11.5\ \mathrm{km}\ \text{PER DAY}
$$

**Engineering fix:** pre-set clocks to 10.22999999543 MHz on the ground instead of 10.23 MHz, so they tick at exactly 10.23 MHz once in orbit.

### Listing 6 — Gravitational field strength and why orbits are not "zero gravity"

Gravitational field strength (inverse square law), where \(r = R_{\text{earth}} + \text{altitude}\):

$$
g = \frac{G M}{r^{2}}
$$

At Earth's surface (\(r = 6.378\times 10^{6}\ \mathrm{m}\)):

$$
g = \frac{6.674\times 10^{-11} \times 5.972\times 10^{24}}{(6.378\times 10^{6})^{2}} = 9.80\ \mathrm{N/kg}\ (= 9.8\ \mathrm{m/s^{2}})
$$

At ISS altitude (\({\sim}400\ \mathrm{km}\), \(r = 6.778\times 10^{6}\ \mathrm{m}\)):

$$
g = \frac{3.986\times 10^{14}}{(6.778\times 10^{6})^{2}} = 8.68\ \mathrm{N/kg}\ ({\sim}89\%\ \text{of surface value})
$$

**Key teaching point.** Orbit is NOT a zero-gravity region. At LEO altitudes \(g\) still exceeds \(9\ \mathrm{N/kg}\) for most satellites. Weightlessness = experiencing ONLY gravity, in free fall, with no supporting (normal) force from below. It is not the absence of gravity.

The field strength \(g = G M / r^{2}\) is the SAME quantity as the centripetal acceleration \(a = v^{2} / r\) for a satellite, because gravity alone supplies the centripetal force.

### Listing 7 — Energy of a satellite in orbit (and changing orbits)

Convention: gravitational potential energy \(U = 0\) at \(r = \infty\), so \(U\) is NEGATIVE everywhere closer in.

Gravitational potential energy:

$$
U = -\frac{G M m}{r}
$$

Kinetic energy (from orbital speed \(v = \sqrt{G M / r}\)), noting \(K = -U/2\):

$$
K = \tfrac{1}{2} m v^{2} = \frac{G M m}{2 r}
$$

Total mechanical energy of a circular orbit, noting \(E = -K\):

$$
E = U + K = -\frac{G M m}{2 r}
$$

Consequences:

- \(E\) is negative \(\to\) the satellite is gravitationally bound.
- Larger \(r\) (higher orbit) \(\to\) LESS negative \(E\) \(\to\) MORE total energy.
- To raise an orbit you must ADD energy, yet the higher orbit is SLOWER (\(v\) decreases), because added energy goes mostly into potential energy.

Work to move between orbits:

$$
W = E_{\text{final}} - E_{\text{initial}} = \frac{G M m}{2}\left(\frac{1}{r_{\text{initial}}} - \frac{1}{r_{\text{final}}}\right)
$$

Worked example (\(m = 1000\ \mathrm{kg}\) satellite at 400 km altitude, \(r = 6.778\times 10^{6}\ \mathrm{m}\)):

$$
\begin{aligned}
U &= -\frac{G M m}{r} = -5.88\times 10^{10}\ \mathrm{J} \\
K &= +\frac{G M m}{2 r} = +2.94\times 10^{10}\ \mathrm{J} \\
E &= -\frac{G M m}{2 r} = -2.94\times 10^{10}\ \mathrm{J}
\end{aligned}
$$

### Listing 8 — Escape velocity

Escape velocity is the minimum launch speed for an object to leave a body's gravitational field entirely (total energy = 0). Derived from \(K + U = 0\):

$$
\tfrac{1}{2} m v_{\text{esc}}^{2} - \frac{G M m}{r} = 0 \quad\Rightarrow\quad v_{\text{esc}} = \sqrt{\frac{2 G M}{r}}
$$

Depends only on \(G\) and the mass \(M\) and radius \(r\) of the body — NOT on the mass of the escaping object.

For Earth (\(r = R_{\text{earth}} = 6.378\times 10^{6}\ \mathrm{m}\)):

$$
v_{\text{esc}} = \sqrt{\frac{2 \times 3.986\times 10^{14}}{6.378\times 10^{6}}} = 1.12\times 10^{4}\ \mathrm{m/s} \approx 11.2\ \mathrm{km/s}\ ({\sim}40{,}000\ \mathrm{km/h})
$$

Compare: at any altitude, orbital speed \(v_{\text{orbit}} = \sqrt{G M / r}\), so \(v_{\text{esc}} = \sqrt{2}\, v_{\text{orbit}}\). Below \(v_{\text{esc}}\) you orbit; at or above it you leave.
