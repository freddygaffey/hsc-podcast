---
title: "Supplementary Materials — Heat Transfer and Latent Heat"
module: M3
lesson: "06"
script: script.md
---

# Supplementary Materials

The read-along reference for how heat moves and what happens during a change of state. Nothing here is spoken in the audio. Symbols: Q = heat energy (J); t = time (s); k = thermal conductivity (W m⁻¹ K⁻¹); A = area (m²); d = thickness (m); ΔT = temperature difference; m = mass (kg); L = specific latent heat (J kg⁻¹); c = specific heat capacity.

### Listing 1 — The three modes of heat transfer
```text
                MECHANISM                                    MEDIUM?       OCCURS IN
CONDUCTION   particle-to-particle COLLISIONS pass energy     YES (needs    mainly SOLIDS
             along; material does NOT move. Metals fast        a material)  (metals best)
             due to FREE ELECTRONS.

CONVECTION   BULK MOVEMENT of a heated fluid: warm fluid      YES (a        LIQUIDS & GASES
             expands → less dense → RISES; cool denser fluid   FLUID)       (fluids that flow)
             SINKS → convection current. "hot rises, cool sinks."

RADIATION    energy carried by ELECTROMAGNETIC WAVES.         NO — crosses  any (incl. VACUUM)
             Hotter → radiates more, shorter wavelength.       a VACUUM     → Sun → Earth
             dull/black surfaces absorb & emit well;
             shiny/white reflect.

⇒ ONLY RADIATION can cross a vacuum (how the Sun heats the Earth).

VACUUM FLASK defeats all three: vacuum gap kills conduction & convection;
   silvered walls reflect radiation; insulating stopper blocks conduction at the top.
```

### Listing 2 — Thermal conductivity
```text
RATE of conduction through a slab:

        Q       k A ΔT
       ─── =  ─────────
        t          d

   k  = thermal conductivity (high for metals, low for insulators)
   A  = cross-sectional area        ΔT = temperature difference across the slab
   d  = thickness                   Q/t = heat energy per second (watts)

Faster conduction when: k large (metal), A large, ΔT large, d SMALL (thin).
⇒ Insulation = LOW k, made THICK (large d) to cut the rate of heat loss.

WORKED: k = 0.04 W m⁻¹ K⁻¹ (fibreglass), A = 10 m², ΔT = 20 K, d = 0.1 m:
   Q/t = (0.04 × 10 × 20) / 0.1 = 8 / 0.1 = 80 W of heat loss.
```

### Listing 3 — Latent heat and the heating curve
```text
CHANGE OF STATE: temperature stays CONSTANT while a substance melts or boils,
   even though energy is still supplied. That energy = LATENT HEAT ("hidden").

WHY (particle model): the energy breaks the BONDS between particles (raising their
   POTENTIAL energy / separating them), NOT their KINETIC energy. Since temperature =
   average KINETIC energy, temperature is unchanged until the change of state finishes.

HEATING CURVE (temperature vs time, steady heating):  ice −20 °C → steam
   /        ‾‾‾‾        /         ‾‾‾‾‾‾‾‾        /
  ice     MELTING     water       BOILING       steam
 warms   (0 °C flat)  warms    (100 °C flat)    warms
   ▲ sloping = warming (KE ↑)    ▲ FLAT plateaus = change of state (latent heat)
   The boiling plateau is LONGER (L_vap ≫ L_fus).

EQUATION CHOICE:
   temperature CHANGING  → Q = m c ΔT
   STATE changing (const. T) → Q = m L
```

### Listing 4 — Worked latent-heat problems (Q = mL)
```text
SPECIFIC LATENT HEAT L = energy to change the state of 1 kg (J kg⁻¹), no temp change.
   water — fusion (melt/freeze):     L_fus ≈ 334 000 J kg⁻¹  (334 kJ kg⁻¹)
   water — vaporisation (boil/cond): L_vap ≈ 2 260 000 J kg⁻¹ (2260 kJ kg⁻¹)
   (vaporisation ≫ fusion: fully separating particles into gas costs far more.)

(1) Melt 2 kg of ice at 0 °C:    Q = m L_fus = 2 × 334 000 = 668 000 J (668 kJ)
(2) Boil 3 kg of water at 100 °C: Q = m L_vap = 3 × 2 260 000 = 6 780 000 J (6.78 MJ)

(3) COMBINED — heat 0.5 kg ice at 0 °C to water at 100 °C (sum the stages):
       melt:   Q₁ = m L_fus = 0.5 × 334 000 = 167 000 J
       warm:   Q₂ = m c ΔT  = 0.5 × 4200 × 100 = 210 000 J
       total = 377 000 J (377 kJ)
   ⇒ pick m L for each phase change, m c ΔT for each temperature change, then ADD.
```
