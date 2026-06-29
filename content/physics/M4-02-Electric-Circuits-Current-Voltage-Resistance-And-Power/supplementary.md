---
title: "Supplementary Materials — Electric Circuits: Current, Voltage, Resistance and Power"
module: M4
lesson: "02"
script: script.md
---

# Supplementary Materials

The read-along reference for the quantities of a circuit and Ohm's law. Nothing here is spoken in the audio. Symbols: I = current (A); q = charge (C); t = time (s); V = voltage/potential difference (V); W = energy (J); R = resistance (Ω); P = power (W).

### Listing 1 — Current and voltage (the two most-confused quantities)
```text
CURRENT  I = q / t       rate of FLOW of charge.  unit: AMPERE (A) = 1 coulomb per second.
   needs a complete circuit + a source (battery) to drive it.
   CONVENTIONAL current: + terminal → − terminal (the convention you use).
   ELECTRON flow (in metal): − → +  (OPPOSITE to conventional current).
   particle picture: electrons DRIFT slowly (<1 mm/s) but the FIELD starts them
      all at once (~light speed) → bulb lights instantly.
   charge conserved → current is the SAME all around a single loop.

VOLTAGE (potential difference)  V = W / q    ENERGY transferred per unit CHARGE.
   unit: VOLT (V) = 1 joule per coulomb.   (rearrange: energy W = V q)
   EMF = energy per unit charge SUPPLIED by a source (also in volts).

⚠ CURRENT = flow (charge/time) ;  VOLTAGE = energy per charge.  NOT the same thing.
```

### Listing 2 — Resistance, Ohm's law, ohmic vs non-ohmic
```text
RESISTANCE  R = V / I    opposition to current flow.  unit: OHM (Ω).
OHM'S LAW trio:   R = V/I      V = I R      I = V/R     (same relation rearranged)

WHAT SETS RESISTANCE (of a wire):
   ↑ LENGTH → ↑ R (R ∝ length)        thicker AREA → ↓ R (R ∝ 1/area)
   MATERIAL (resistivity): copper/silver low ; nichrome high
   ↑ TEMPERATURE (metal) → ↑ R (vibrating atoms impede electrons more)
   ⇒ connecting wires: short, thick, copper (low R) ; heater: long, thin, nichrome (high R)

OHMIC vs NON-OHMIC (current–voltage graph):
   OHMIC      : R CONSTANT → I ∝ V → STRAIGHT line through origin.
                (metal resistor at constant temperature; Ohm's law applies)
   NON-OHMIC  : R CHANGES → I–V graph CURVES.
       filament lamp: ↑I heats filament → ↑R → curve bends over (flattens).
       diode: conducts one way, blocks the other.
   ⚠ Ohm's law applies ONLY to ohmic conductors at CONSTANT temperature.

   I |   ohmic /              I |  filament lamp
     |     _ /                  |        ____
     |   /                      |     _/
     | /                        |   /
     +————— V                   +————— V   (curve flattening = rising R)
```

### Listing 3 — Worked Ohm's law & power problems
```text
(1) V = 12 V, I = 3 A:  R = V/I = 12/3 = 4 Ω.  Double V to 24 V → I = V/R = 24/4 = 6 A.
(2) q = 60 C in t = 30 s:  I = q/t = 60/30 = 2 A.  V = 6 V → energy W = Vq = 6 × 60 = 360 J.
(3) Heater: V = 240 V, I = 5 A:  P = VI = 240 × 5 = 1200 W.
       energy in 60 s:  W = Pt = 1200 × 60 = 72 000 J (72 kJ).
(4) Kettle 2400 W on 240 V:  I = P/V = 2400/240 = 10 A ;  R = V/I = 240/10 = 24 Ω.
(5) Same 240 V across two elements (use P = V²/R for fixed voltage):
       A (12 Ω): P = 240²/12 = 57600/12 = 4800 W
       B (24 Ω): P = 240²/24 = 57600/24 = 2400 W
       ⇒ LOWER resistance dissipates MORE power at fixed voltage (P ∝ 1/R).
```

### Listing 4 — Electrical power and energy
```text
POWER (rate of energy conversion):   P = V I        unit: WATT (W) = 1 joule per second.
   via Ohm's law (substitute V = IR or I = V/R):
        P = I² R         (use when you know I and R)
        P = V² / R       (use when you know V and R — e.g. fixed supply voltage)

ENERGY:   W = P t        (joules)   |   electricity bills use kWh = kilowatt × hour.
   high power × long time = most energy (2 kW heater × 3 h = 6 kWh).

CHOOSE THE FORMULA by what's held constant / given:
   know V and I → P = VI ;  know I and R → P = I²R ;  know V and R → P = V²/R.

MEASURING (investigation): AMMETER in SERIES (same current as component);
   VOLTMETER in PARALLEL (reads p.d. across component). Plot I vs V → straight = ohmic.
```
