---
title: "Supplementary Materials — Chernobyl — The Physics of a Meltdown"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — Fission of uranium-235 and the chain reaction

A typical fission of U-235 after absorbing a slow (thermal) neutron:

$$
{}^{235}_{92}\mathrm{U} + {}^{1}_{0}\mathrm{n} \to {}^{236}_{92}\mathrm{U}^{*} \to \text{fission fragments} + k\,{}^{1}_{0}\mathrm{n} + \text{energy}
$$

Example reaction:

$$
{}^{235}_{92}\mathrm{U} + {}^{1}_{0}\mathrm{n} \to {}^{141}_{56}\mathrm{Ba} + {}^{92}_{36}\mathrm{Kr} + 3\,{}^{1}_{0}\mathrm{n} + {\sim}200\ \mathrm{MeV}
$$

Energy per fission:

$$
{\sim}200\ \mathrm{MeV} = 200\times 10^{6} \times 1.602\times 10^{-19}\ \mathrm{J} \approx 3.2\times 10^{-11}\ \mathrm{J}
$$

Neutrons released per fission, \(k\): typically 2 to 3 (average \(\sim 2.4\)).

**Why energy is released (binding energy per nucleon).** The two medium-mass fragments have a HIGHER binding energy per nucleon (are more tightly bound / more stable) than U-235. That gain in stability is released, mostly as kinetic energy of the fragments. Fission of heavy nuclei and fusion of light nuclei both move products TOWARD the iron-56 peak of the curve.

**Chain reaction condition (multiplication factor \(k_{\text{eff}}\)):**

- \(k_{\text{eff}} < 1\) — subcritical (chain dies out)
- \(k_{\text{eff}} = 1\) — critical (steady power — a CONTROLLED reactor)
- \(k_{\text{eff}} > 1\) — supercritical (power rises — UNCONTROLLED if sustained)

**Controlled vs uncontrolled (syllabus comparison):**

- Controlled \(\to\) on average EXACTLY 1 neutron per fission causes the next fission \(\to\) steady power (reactor).
- Uncontrolled \(\to\) MORE THAN 1 neutron per fission causes further fissions \(\to\) fissions multiply (\(2\to 4\to 8\ldots\)) \(\to\) power rises without limit (bomb / runaway).

**Energy comparison (syllabus: vs fossil fuels and explosives).**

- 1 fission of U-235: \({\sim}200\ \mathrm{MeV}\)
- 1 carbon atom burned: \({\sim}10\ \mathrm{eV}\)
- \(\Rightarrow\) fission yields \({\sim}2\times 10^{7}\) (20 million) times more energy per atom than burning coal.
- Chernobyl 2nd blast: \({\sim}225\) tonnes TNT equivalent
- \(\Rightarrow\) still thousands of times SMALLER than a nuclear weapon.

### Listing 2 — The four reactor components and their physics roles

| Component | Material at Chernobyl (RBMK) | Physics role |
|-----------|------------------------------|--------------|
| Fuel | Uranium oxide, ~2.0% U-235 enriched | Site of fission; releases energy + fast neutrons |
| Moderator | Graphite (1700 t, solid) | SLOWS fast neutrons to thermal speed (raises fission rate) |
| Control rods | Boron carbide (170 rods) | ABSORBS neutrons (lowers fission rate) — throttle/brake |
| Coolant | Light (ordinary) water | Carries heat away; boils to steam to drive turbine |

**Key distinction (common exam error):**

- Moderator \(\to\) SLOWS neutrons (so they CAN cause fission)
- Control rod \(\to\) ABSORBS neutrons (so they CANNOT cause fission)

These are different jobs done by different materials.

### Listing 3 — The positive void coefficient (the core fault)

A "void" is a bubble of steam in the coolant water. The void coefficient is the sign of (change in reactivity) per (steam fraction).

**Western water-moderated reactor (water = moderator AND coolant):** water boils \(\to\) lose MODERATOR \(\to\) fewer neutrons slowed \(\to\) fewer fissions \(\to\) power FALLS \(\Rightarrow\) NEGATIVE void coefficient (self-correcting, SAFE).

**RBMK reactor (graphite = moderator, water = coolant only):** water boils \(\to\) moderator (graphite) UNCHANGED \(\to\) but lose a neutron ABSORBER (the water) \(\to\) more free neutrons \(\to\) more fissions \(\to\) power RISES \(\to\) more heat \(\to\) more boiling \(\to \ldots\) (runaway loop) \(\Rightarrow\) POSITIVE void coefficient (self-reinforcing, DANGEROUS).

RBMK value at time of accident: \(+4.5\,\beta\) (largest of any commercial reactor ever built; worst at LOW power). Post-accident target after modifications: \(+0.7\,\beta\).

### Listing 4 — Xenon-135 poisoning

Production path of the neutron poison:

$$
\text{fission} \to \text{I-135} \xrightarrow{\text{beta decay, } t_{1/2} \sim 6.6\ \mathrm{h}} \text{Xe-135}
$$

Xe-135 has the largest thermal neutron absorption cross-section of any known nuclide (millions of barns).

**At full power:** Xe-135 is burned away by neutrons as fast as it forms \(\to\) low, steady xenon level.

**After a power drop:**

- neutron flux falls \(\to\) Xe-135 no longer burned away
- but stored I-135 keeps decaying \(\to\) Xe-135 keeps being made
- \(\to\) xenon SURGES (the "xenon pit")
- \(\to\) chain reaction smothered; reactor hard to restart

Chernobyl: the 9-hour hold + power crash to \({\sim}30\ \mathrm{MW}\) created a huge xenon load. Operators withdrew control rods to fight it, leaving almost no reactivity margin.

### Listing 5 — Key numbers of the accident

| Quantity | Value |
|----------|-------|
| Reactor | RBMK-1000, Unit 4 |
| Rated thermal power | 3200 MW (1000 MW electrical) |
| Core size | 11.8 m diameter x 7.0 m high |
| Required reactivity margin | 26–30 equivalent rods |
| Actual margin ~01:22 | ~8 equivalent rods |
| Power at test start (01:23:04) | ~200 MW |
| AZ-5 button pressed | 01:23:40, 26 April 1986 |
| Peak power reached | ~30 000 MW (~10x rated) in ~3 s |
| 2nd explosion energy | ~225 tonnes TNT equivalent |
| Reactor-floor radiation | ~5.6 R/s (~20 000 R/hr) |
| Lethal dose (LD50) | ~400–500 R |
| Graphite displacer tip length | 4.5 m |
| Direct deaths | 2 (blast) + 28 (acute radiation) = 30 |
| Exclusion zone radius | 30 km |

### Listing 6 — Half-life: equations and the caesium-137 worked example

Exponential decay law (HSC Module 8):

$$
N_{t} = N_{0}\, e^{-\lambda t}
$$

Decay constant from half-life:

$$
\lambda = \frac{\ln 2}{t_{1/2}} = \frac{0.6931}{t_{1/2}}
$$

Simple half-life rule (whole numbers of half-lives):

$$
\text{fraction remaining after } n \text{ half-lives} = \left(\tfrac{1}{2}\right)^{n}
$$

Key Chernobyl isotopes:

- Iodine-131: \(t_{1/2} = 8.02\) days (short-lived; thyroid hazard)
- Caesium-137: \(t_{1/2} = 30.04\) years (long-lived; defines zone)
- Strontium-90: \(t_{1/2} = 28.8\) years (bone-seeking)

Cs-137 decay:

$$
\text{Cs-137} \xrightarrow{\beta} \text{Ba-137m} \xrightarrow{\gamma\ 0.662\ \mathrm{MeV}} \text{Ba-137 (stable)}
$$

**Worked example — how long until Cs-137 falls to 0.1% of its level?**

Want fraction remaining \(= 0.001 = \left(\tfrac{1}{2}\right)^{n}\). Take logs:

$$
n = \frac{\ln(0.001)}{\ln(0.5)} = \frac{-6.908}{-0.6931} \approx 9.97 \to \text{about 10 half-lives}
$$

$$
\text{Time} = n \times t_{1/2} = 10 \times 30.04\ \text{years} \approx 300\ \text{years}
$$

So \({\sim}300\) years are needed for Cs-137 contamination to fall to \({\sim}0.1\%\) of its 1986 level — the physical reason the most contaminated land stays restricted into the 23rd century.

Check after a single 30-year half-life (1986 \(\to\) 2016):

$$
\text{fraction remaining} = \left(\tfrac{1}{2}\right)^{1} = 0.5
$$

i.e. half the original Cs-137 had decayed by 2016.

### Listing 7 — Scientists who discovered fission, and the first controlled reactor

| Scientist(s) | Year | Contribution |
|--------------|------|--------------|
| Enrico Fermi | 1934 | Fired neutrons at uranium; produced new half-lives (misread as new elements) |
| Otto Hahn & Fritz Strassmann | 1938 | Chemically detected barium after bombarding uranium — evidence the nucleus had split |
| Lise Meitner & Otto Frisch | 1938–39 | Explained the result, named it "fission", estimated ~200 MeV per event from binding energies |
| Frederic Joliot (and team) | 1939 | Confirmed 2–3 neutrons released per fission — making a chain reaction possible |
| Enrico Fermi (and team) | 1942 | Built the first controlled chain reaction (Chicago Pile-1): graphite-moderated, uranium fuel, cadmium control rods |

**Nuclear equation for fission** (syllabus: use equations to describe fission of large nuclei). One representative U-235 fission:

$$
{}^{235}_{92}\mathrm{U} + {}^{1}_{0}\mathrm{n} \to {}^{236}_{92}\mathrm{U} \to {}^{141}_{56}\mathrm{Ba} + {}^{92}_{36}\mathrm{Kr} + 3\,{}^{1}_{0}\mathrm{n} + {\sim}200\ \mathrm{MeV}
$$

Mass numbers balance: \(235 + 1 = 141 + 92 + 3(1) = 236\). Atomic numbers balance: \(92 + 0 = 56 + 36 + 0 = 92\). (Many fragment pairs are possible — e.g. La-148 + Br-85 + 3n.)
