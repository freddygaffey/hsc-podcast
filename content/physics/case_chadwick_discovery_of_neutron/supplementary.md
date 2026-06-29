---
title: "Supplementary Materials — Chadwick and the Discovery of the Neutron"
kind: case-study
script: script.md
---

# Supplementary Materials

Key equations, derivations, worked solutions and data tables for this episode. Nothing
here is spoken in the audio — it is the read-along reference. Each listing is referenced
by label in the narration.

### Listing 1 — Chadwick's mass calculation from conservation of momentum and energy

**Setup:** a neutral particle of unknown mass \(m_{n}\) and unknown speed \(v_{n}\) strikes a STATIONARY target nucleus head-on in an ELASTIC collision. The target recoils with speed \(v_{\text{target}}\). The mass of the target is \(m_{\text{target}}\).

Two conservation laws apply to the head-on elastic collision.

Conservation of momentum:

$$
m_{n} v_{n} = m_{n} v_{n}' + m_{\text{target}} v_{\text{target}}
$$

Conservation of kinetic energy (elastic):

$$
\tfrac{1}{2} m_{n} v_{n}^{2} = \tfrac{1}{2} m_{n} v_{n}'^{2} + \tfrac{1}{2} m_{\text{target}} v_{\text{target}}^{2}
$$

Standard result for a 1-D elastic collision (max recoil, head-on), the target recoil speed is:

$$
v_{\text{target}} = \left(\frac{2 m_{n}}{m_{n} + m_{\text{target}}}\right) v_{n}
$$

Do this for two different, known targets.

Target 1 — hydrogen (a proton), mass \(m_{H}\), measured recoil speed \(v_{H}\):

$$
v_{H} = \left(\frac{2 m_{n}}{m_{n} + m_{H}}\right) v_{n}
$$

Target 2 — nitrogen nucleus, mass \(m_{N}\), measured recoil speed \(v_{N}\):

$$
v_{N} = \left(\frac{2 m_{n}}{m_{n} + m_{N}}\right) v_{n}
$$

Divide the two equations — the unknown incoming speed \(v_{n}\) CANCELS:

$$
\frac{v_{H}}{v_{N}} = \frac{m_{n} + m_{N}}{m_{n} + m_{H}}
$$

Rearrange to isolate the neutron mass \(m_{n}\) (everything else is measured):

$$
m_{n} = \frac{v_{N} m_{N} - v_{H} m_{H}}{v_{H} - v_{N}}
$$

**Result:** Chadwick obtained \(m_{n} \approx 1.15 \times m_{\text{proton}}\). Crucially: the particle has mass \(\approx\) a proton AND no charge \(\to\) the NEUTRON.

### Listing 2 — Key masses and energies in the discovery

| Quantity | Value | Note |
|----------|-------|------|
| Proton mass | 1.67 × 10⁻²⁷ kg | hydrogen nucleus |
| Neutron mass (Chadwick, 1932) | ≈ 1.15 × proton mass | his measured figure |
| Neutron mass (modern value) | ≈ 1.0014 × proton mass | neutron just heavier than proton |
| Ejected proton speed (from wax) | 3.3 × 10⁷ m s⁻¹ | about 0.1 × speed of light |
| Energy required IF radiation were gamma | ≈ 50 MeV per photon | to eject protons at that speed |
| Energy actually available (incident alphas) | ≈ 5 MeV | ~10× less than 50 MeV → impossible |
| Bothe & Becker estimate (1930) | ≈ 10 MeV "gamma" | the original mislabelling |

### Listing 3 — The beryllium reaction that produces neutrons

Chadwick's neutron source: alpha particles from a polonium source strike beryllium-9. The nuclear equation is:

$$
\text{beryllium-9} + \alpha \to \text{carbon-12} + \text{neutron}
$$

In symbol form (mass number on top, atomic number below):

$$
{}^{9}_{4}\mathrm{Be} + {}^{4}_{2}\mathrm{He} \to {}^{12}_{6}\mathrm{C} + {}^{1}_{0}\mathrm{n}
$$

Check conservation of nucleon number (top): \(9 + 4 = 12 + 1\) ✓. Check conservation of charge / proton number (bottom): \(4 + 2 = 6 + 0\) ✓.

This was the first practical way to make a beam of free neutrons: a high-energy alpha source (polonium) plus beryllium.

### Listing 4 — Why gamma rays fail but a massive neutral particle works

**The contradiction (gamma-ray hypothesis).** A photon's momentum is small for its energy:

$$
p = \frac{E}{c}
$$

(\(c = 3\times 10^{8}\ \mathrm{m\,s^{-1}}\) is huge, so \(p\) is small). To shove a heavy proton to \(3.3\times 10^{7}\ \mathrm{m\,s^{-1}}\) by a photon "kick" (Compton-style) would need a photon of about 50 MeV. But the incident alpha particles supply only about 5 MeV:

$$
50\ \mathrm{MeV}\ \text{needed} \quad \text{vs} \quad {\sim}5\ \mathrm{MeV}\ \text{available} = {\sim}10\times\ \text{shortfall}
$$

This violates conservation of energy. CONCLUSION: the radiation cannot be gamma rays.

**The resolution (neutral particle of mass \(\approx\) proton).** An equal-mass head-on elastic collision transfers nearly ALL the speed from projectile to target (like billiard balls):

$$
v_{\text{target}} \approx v_{\text{projectile}} \quad \text{when} \quad m_{\text{projectile}} \approx m_{\text{target}}
$$

So a neutral particle of \(\approx\) proton mass, moving at the modest speed expected from a few-MeV reaction, ejects the proton at the observed speed WITHOUT any energy violation. CONCLUSION: the radiation is a stream of NEUTRONS.

### Listing 5 — Comparison of penetrating ability and charge

| Particle / radiation | Charge | Rest mass | Penetrating ability | Detectable by charge? |
|----------------------|--------|-----------|---------------------|-----------------------|
| Alpha (helium nucleus) | +2 | ≈ 4 proton masses | low — stopped by paper | yes (ionises strongly) |
| Proton | +1 | 1 proton mass | low–moderate | yes |
| Gamma ray (photon) | 0 | 0 | very high | no (but few interactions) |
| Neutron | 0 | ≈ 1 proton mass | very high | no — leaves no track |

### Listing 6 — Timeline of the discovery

| Year | Event |
|------|-------|
| 1919 | Rutherford identifies the proton (bombarding nitrogen with alphas). |
| 1920 | Rutherford's Bakerian Lecture predicts a neutral particle ≈ proton mass, and names it the "neutron". |
| 1930 | Bothe & Becker (Germany): alpha + beryllium → penetrating radiation, ≈ 10 MeV, mislabelled as gamma rays. |
| 1932 | Joliot-Curies (Paris): that radiation ejects fast protons from paraffin wax — still called gamma rays. |
| 1932 | Chadwick (Cambridge) reads the paper; in barely a fortnight applies conservation of energy + momentum, measures neutron mass ≈ 1.15 proton masses. Paper "Possible Existence of a Neutron" submitted to *Nature* on 17 February 1932. |
| 1935 | Chadwick awarded the Nobel Prize in Physics. |
| 1938 | Neutron-induced nuclear fission of uranium discovered (Hahn, Meitner, Strassmann) — opening the nuclear age. |
