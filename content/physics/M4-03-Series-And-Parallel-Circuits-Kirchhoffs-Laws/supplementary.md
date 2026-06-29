---
title: "Supplementary Materials — Series and Parallel Circuits (Kirchhoff's Laws)"
module: M4
lesson: "03"
script: script.md
---

# Supplementary Materials

The read-along reference for analysing series and parallel circuits with Kirchhoff's laws. Nothing here is spoken in the audio. Symbols: I = current (A); V = voltage (V); R = resistance (Ω); P = power (W).

### Listing 1 — Kirchhoff's two laws (the foundation)
```text
KIRCHHOFF'S CURRENT LAW (KCL):  Σ I = 0
   currents INTO a junction = currents OUT of it.
   ⇒ expresses CONSERVATION OF CHARGE (charge can't pile up or vanish at a junction).

KIRCHHOFF'S VOLTAGE LAW (KVL):  Σ V = 0
   around any closed loop, voltage SUPPLIED = total voltage DROPPED.
   ⇒ expresses CONSERVATION OF ENERGY (a charge gains = loses energy round a loop).

⭐ MARK-EARNING MOVE: always NAME the conservation principle (charge for KCL, energy for KVL).

ANSWER CHECKS (use after every network problem):
   • series voltages add to the supply (KVL)
   • branch currents add to the total (KCL)
   • component powers add to the supply power (P = VI)
```

### Listing 2 — Series vs parallel rules
```text
                    SERIES (one path)            PARALLEL (multiple paths)
  CURRENT      SAME through all components    DIVIDES among branches (Σ = total)
  VOLTAGE      DIVIDES (∝ resistance)         SAME across every branch (= supply)
  RESISTANCE   ADDS: R_T = R₁ + R₂ + …        RECIPROCAL: 1/R_T = 1/R₁ + 1/R₂ + …
  R_total      INCREASES with more parts      DECREASES; < smallest branch
  one breaks   ALL stop (single path)         others keep working (own paths)

HOOK:  SERIES — same Current, voltage Shares, R adds.
       PARALLEL — same Voltage, current Shares, R drops.

WHO GETS THE BIGGER SHARE?
   series voltage divider : BIGGER R → bigger VOLTAGE drop (∝ R)
   parallel current divider: SMALLER R → bigger CURRENT (∝ 1/R)

POWER in a network (total P_supply = VI = Σ component powers):
   series (same I)    → use P = I²R → BIGGEST resistor dissipates MOST
   parallel (same V)  → use P = V²/R → SMALLEST resistor dissipates MOST

HOUSEHOLD WIRING is PARALLEL: each appliance gets full voltage, switches
   independently, draws only the current it needs (fuses/breakers cap the total).
```

### Listing 3 — Worked networks
```text
(A) SERIES: 4 Ω + 2 Ω on 12 V
    R_T = 4 + 2 = 6 Ω ;  I = V/R_T = 12/6 = 2 A (same in both)
    V across 4 Ω = IR = 2×4 = 8 V ;  V across 2 Ω = 2×2 = 4 V ;  check 8+4 = 12 V ✓ (KVL)
    power: P(4Ω) = I²R = 2²×4 = 16 W ; P(2Ω) = 2²×2 = 8 W ; total 24 W = VI = 12×2 ✓

(B) PARALLEL: 6 Ω ∥ 3 Ω on 12 V
    1/R_T = 1/6 + 1/3 = 1/6 + 2/6 = 3/6 = 1/2 → R_T = 2 Ω (< 3 Ω ✓)
    each branch has 12 V:  I(6Ω) = 12/6 = 2 A ;  I(3Ω) = 12/3 = 4 A
    total I = 2 + 4 = 6 A = 12/2 ✓ (KCL).  Smaller R (3 Ω) carries more current.

(C) PARALLEL: 6 Ω ∥ 12 Ω on 9 V
    1/R_T = 1/6 + 1/12 = 2/12 + 1/12 = 3/12 = 1/4 → R_T = 4 Ω
    total I = V/R_T = 9/4 = 2.25 A

(D) COMBINED: 4 Ω in SERIES with (4 Ω ∥ 4 Ω) on 12 V
    parallel part: 1/R = 1/4 + 1/4 = 1/2 → 2 Ω
    R_T = 4 + 2 = 6 Ω ;  I = 12/6 = 2 A (through the series 4 Ω)
    V across parallel section = IR = 2×2 = 4 V ; V across series 4 Ω = 2×4 = 8 V ; 8+4 = 12 ✓
```
