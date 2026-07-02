---
title: "Supplementary Materials — Wiring Diagrams and Power Requirements"
module: PM11
year: 11
lesson: "8.2"
script: script.md
---

# Supplementary Materials

The read-along reference for the power-and-wiring lesson. Nothing here is spoken in the audio — the
narration points at each listing by label only. Listing 1 is a runnable power-and-battery budget;
Listing 2 is a worked wiring diagram (data lines vs power lines); Listing 3 is the revision reference.

### Listing 1 — Power budget and battery sizing for the thermostat-fan (Python, runnable)
```python
def power_w(voltage_v, current_a):
    """Power equation: P = V x I  (watts = volts x amps)."""
    return voltage_v * current_a

# The thermostat-fan: a controller + a temperature sensor draw little; the fan MOTOR dominates.
components = {
    "controller":  (5, 0.20),     # 1.00 W
    "temp_sensor": (5, 0.02),     # 0.10 W
    "fan_motor":   (12, 0.40),    # 4.80 W  <- the actuator is the big draw
}

per_component = {name: round(power_w(v, a), 2) for name, (v, a) in components.items()}
total_w = round(sum(per_component.values()), 2)

assert per_component["fan_motor"] == 4.8          # the actuator dominates the budget
assert total_w == 5.9

# Battery sizing: add a 20% safety margin, supplied from a 12 V battery.
SAFETY = 1.20
BATTERY_V = 12
draw_a = round(total_w * SAFETY / BATTERY_V, 3)   # current the battery must supply

def runtime_hours(capacity_ah, draw_a, usable=0.8):
    """Usable capacity / current draw = hours. Only ~80% of a battery is safely usable."""
    return (capacity_ah * usable) / draw_a

hrs = runtime_hours(2.0, draw_a)

assert draw_a < 1.0                                # a modest, battery-friendly draw
assert hrs > 2                                     # a 2 Ah battery lasts over 2 hours here
print("per-component W:", per_component, "| total:", total_w,
      "| battery draw A:", draw_a, "| runtime h:", round(hrs, 1))
```

### Listing 2 — A wiring diagram for the thermostat-fan: data lines vs power lines (reference)
```text
TWO NETWORKS ON ONE MACHINE — power lines FEED, data lines TALK, all sharing one common GROUND.

                         +12V (red)            +12V (red, switched by the driver)
   [ 12V BATTERY ] --[FUSE]--+---------------------------------------> [ FAN MOTOR ]
        |  |                 |                                              ^
        |  |                 +--> [ 12V->5V REGULATOR ] --+5V (red)--> [ CONTROLLER ]
        |  |                                              +5V (red)--> [ TEMP SENSOR ]
        |  |
        |  +--- GND (black) ---+------------------+----------------+-----+   <- ONE common ground
        |                   CONTROLLER         TEMP SENSOR       FAN/driver
        |
   DATA / SIGNAL LINES (thin, low current):
        TEMP SENSOR --(reading, e.g. analog signal)--> CONTROLLER        ("talk")
        CONTROLLER  --(drive signal)--> FAN DRIVER --> switches the 12V power line to the motor

  WHY A SEPARATE POWER PATH FOR THE MOTOR (the key idea):
    a controller output pin can supply only a few milliamps — nowhere near a motor's amps.
    So the controller's signal SWITCHES a driver/transistor that feeds the motor from the
    battery's own 12V line. NEVER run an actuator straight off a controller pin.

  CONVENTIONS:  red = positive supply · black = ground · other colours = signal
                fuse near the battery + · wire gauge sized to the current it carries
```

### Listing 3 — Revision reference: power, battery, materials, safe wiring (reference)
```text
ELECTRICAL BASICS — V-I-P:
  Voltage (V, volts) = electrical "push"   ·   Current (I, amps) = rate of charge flow
  Power (P, watts)   = energy per second
  P = V x I   (Power = volts x amps)        Ohm's law: V = I x R   (R = resistance, ohms)

POWER & BATTERY BUDGET (a design/engineering skill — SE-11-01/06):
  1. Power of each component = its V x I, in watts.   2. Sum them = total system power.
  3. Add headroom (~+20%) and allow for inefficiency.
  4. Battery current draw = total power / battery voltage.
  5. RUNTIME = (capacity in amp-hours x ~0.8 usable) / current draw, in hours.
     "amp-hours over amps gives hours."

MATERIAL REQUIREMENTS (the dot-point also says "material"):
  chassis/enclosure (strength vs weight), wire gauge + connectors, and environment fit
  (waterproof? heat-resistant? vibration?). The build's physical parts, chosen for the job.

WIRING-DIAGRAM = the system's blueprint (data + power):
  POWER lines carry supply (+ and ground) and the heavy current; DATA/SIGNAL lines carry the
  small control signals. Actuators get their OWN power path (a pin can't drive a motor).
  SAFE-WIRING checklist: Colour-code · Fuse · Wire-gauge to current · Strain-relief ·
  Isolate high/low voltage · ONE common ground · an emergency-stop on main power.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| V-I-P | Voltage · current (I) · Power | The electrical quantities (P = V × I) |
