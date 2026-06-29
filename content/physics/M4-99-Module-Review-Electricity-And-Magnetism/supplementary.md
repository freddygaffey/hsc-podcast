---
title: "Supplementary Materials — Module Review: Electricity and Magnetism"
module: M4
lesson: "99"
script: script.md
---

# Supplementary Materials

A consolidated reference for the whole Electricity and Magnetism module, with worked integrated solutions. Nothing here is spoken in the audio — it is the read-along reference.

### Listing 1 — The Module 4 toolkit (all four episodes)
```text
ELECTROSTATICS (M4-01):  two charges; LIKE repel, UNLIKE attract; charge CONSERVED & QUANTISED.
   charging: FRICTION (rub) · CONDUCTION (contact → SAME sign) · INDUCTION (no contact → OPPOSITE).
   Coulomb's law:  F = k q₁ q₂ / r²   (k = 9.0×10⁹ ; inverse-square, like gravity).
   electric field:  E = F/q  (N C⁻¹) — force per unit + charge; away from +, toward −.
   parallel plates (uniform field):  E = V/d.

CIRCUITS (M4-02):  current I = q/t (A) — rate of flow of charge (conventional + → −, electrons − → +).
   voltage V = W/q (V) — energy per charge.   resistance R = V/I (Ω); OHM'S LAW V = IR.
   OHMIC = constant R, straight I–V line ; NON-OHMIC (filament/diode) = curved.
   power P = VI = I²R = V²/R ;  energy W = Pt.

SERIES & PARALLEL (M4-03):  Kirchhoff: ΣI = 0 (CHARGE) at junctions ; ΣV = 0 (ENERGY) round loops.
   SERIES: same CURRENT, voltage divides, R_T = R₁+R₂+…
   PARALLEL: same VOLTAGE, current divides, 1/R_T = Σ1/R (R_T < smallest branch).

MAGNETISM (M4-04):  poles N/S, like repel/unlike attract, NO monopoles. Ferromagnetic = Fe, Ni, Co.
   magnetised when DOMAINS align. Field lines N→S outside; Earth ≈ bar magnet (geo-N is mag-S).
   CURRENT MAKES MAGNETISM:  wire → circles, right-hand GRIP rule, B = μ₀I/2πr ;
   solenoid → bar-magnet field, B = μ₀NI/L ; + iron core = ELECTROMAGNET.

FORWARD → M6 Electromagnetism (charged particle in E=V/d ; motor effect ; induction ;
   motors/generators/transformers).  BACK → M2 (force, energy conservation).
```

### Listing 2 — Worked integrated solutions
```text
(Field + force) plates d = 0.02 m, V = 400 V, q = 5×10⁻⁶ C:
   E = V/d = 400/0.02 = 20 000 N C⁻¹ ;  F = Eq = 20 000 × 5×10⁻⁶ = 0.1 N

(Coulomb proportions) F → triple one charge (×3) AND halve distance (×1/½² = ×4) → ×12.
   (12 N, double charge ×2 AND double distance ×¼ → ×½ = 6 N)

(Circuit basics) q = 120 C in t = 40 s, V = 12 V:
   I = q/t = 120/40 = 3 A ;  R = V/I = 12/3 = 4 Ω ;  P = VI = 12×3 = 36 W

(Network) 3 Ω in series with (6 Ω ∥ 6 Ω) on 12 V:
   parallel: 1/R = 1/6 + 1/6 = 1/3 → 3 Ω ;  R_T = 3 + 3 = 6 Ω ; I = 12/6 = 2 A
   V across parallel = IR = 2×3 = 6 V ; series 3 Ω drops 6 V ; 6+6 = 12 ✓
   (9 V, 2 Ω series + (3 Ω ∥ 6 Ω = 2 Ω) → R_T = 4 Ω ; I = 9/4 = 2.25 A)

(Heater) R = 20 Ω on 240 V:  I = V/R = 12 A ; P = VI = V²/R = 2880 W ;
   W = Pt = 2880 × 300 s = 864 000 J (5 min)

(Solenoid combo) N = 300, L = 0.2 m, I = 4 A, 12 V source:
   B = μ₀NI/L = (4π×10⁻⁷ × 300 × 4)/0.2 ≈ 7.5×10⁻³ T
   R = V/I = 12/4 = 3 Ω ; P = VI = 12×4 = 48 W ; iron core → field ×much stronger (domains align).
```

### Listing 3 — Mnemonic / rule registry (M4)
| Topic | Hook |
|-------|------|
| Charge force | LIKE repel, UNLIKE attract; charge conserved & quantised (×e = 1.6×10⁻¹⁹ C) |
| Charging | friction (rub) · conduction (contact, SAME sign) · induction (no contact, OPPOSITE) |
| Coulomb's law | F = kq₁q₂/r² — inverse square; double q ×2, double r ÷4 |
| Field vs force | E = F/q (property of the LOCATION) ; F = Eq (what a charge FEELS) |
| Parallel plates | uniform field, E = V/d |
| Current vs voltage | current = flow I = q/t ; voltage = energy per charge V = W/q (NOT the same) |
| Ohm's law | V = IR ; ohmic = straight I–V ; non-ohmic (lamp) curves (R rises with heat) |
| Power | P = VI = I²R = V²/R ; energy W = Pt |
| Kirchhoff | current law ΣI=0 = CHARGE ; voltage law ΣV=0 = ENERGY |
| Series vs parallel | series: same Current, V shares, R adds ; parallel: same Voltage, I shares, R drops |
| Magnetic poles | like repel/unlike attract; NO monopoles (cut → two whole magnets) |
| Magnetisation | random domains cancel → aligned domains add (Fe, Ni, Co) |
| Wire vs solenoid | wire = circles (grip rule, B=μ₀I/2πr) ; solenoid = bar magnet (B=μ₀NI/L) |
| Earth | acts like a bar magnet; geographic North is a magnetic SOUTH |

### Listing 4 — Which equation / approach? (decision guide)
```text
ELECTROSTATICS:
   force between point charges?         → Coulomb:  F = k q₁ q₂ / r²
   field at a point / force on a charge?→ E = F/q   (then F = Eq)
   field between parallel plates?       → E = V/d

CIRCUITS — what are you given?
   charge & time?                       → I = q/t
   energy & charge?                     → V = W/q
   any two of V, I, R?                  → Ohm's law V = IR
   power: know V&I → P=VI ; I&R → P=I²R ; V&R → P=V²/R ; energy → W = Pt

NETWORKS:
   reduce series (R adds) & parallel (1/R_T = Σ1/R) to ONE equivalent R,
   then I = V/R_T, then work back. CHECK: series V's add to supply ; branch I's add to total.

MAGNETISM:
   field around a straight wire?        → B = μ₀ I / (2π r)  (direction: right-hand GRIP rule)
   field inside a solenoid?             → B = μ₀ N I / L     (direction: right-hand coil rule)

GOLDEN RULE: ask "what FIELD acts and what FORCE does it make?" and "where do CHARGE
   and ENERGY go, and what is CONSERVED?" — those two questions open almost anything.
```
