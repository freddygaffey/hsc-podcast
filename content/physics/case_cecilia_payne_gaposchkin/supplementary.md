---
title: "Supplementary Materials — Cecilia Payne-Gaposchkin — What Stars Are Made Of"
kind: case-study
script: script.md
---

# Supplementary Materials

### Listing 1 — The Saha ionisation equation

The equation Payne applied across hundreds of stellar spectra. It gives the
ratio of atoms in two consecutive ionisation states as a function of
temperature and electron density. The key idea: ionisation state depends on T
and electron density n_e, NOT on the total abundance of the element.

$$
\frac{n_{i+1}\,n_e}{n_i} = \frac{2}{\lambda_{th}^{3}}\,\frac{g_{i+1}}{g_i}\,\exp\!\left[-\frac{E_{i+1}-E_i}{k_B T}\right]
$$

with the thermal de Broglie wavelength of the electron

$$
\lambda_{th} = \frac{h}{\sqrt{2\pi m_e k_B T}}
$$

where:

- \(n_i\) — number density of atoms in ionisation state \(i\)
- \(n_{i+1}\) — number density in the next higher ionisation state
- \(n_e\) — number density of free electrons
- \(g_i,\ g_{i+1}\) — statistical weights (degeneracies) of each state
- \(E_{i+1}-E_i\) — ionisation energy from state \(i\) to \(i+1\)
- \(k_B = 1.38\times10^{-23}\ \mathrm{J/K}\) — Boltzmann constant
- \(T\) — temperature (K)
- \(h = 6.63\times10^{-34}\ \mathrm{J\,s}\), \(\ m_e = 9.11\times10^{-31}\ \mathrm{kg}\)

### Listing 2 — Why a spectral line is not a direct measure of abundance

The strength of an absorption line depends on the number of atoms in the ONE
state that can absorb at that wavelength — a temperature-dependent fraction of
the total — not on the total number of atoms of that element.

$$
\text{line strength} \ \propto\ N_{\text{abs}}, \qquad
N_{\text{abs}} = N_{\text{total}}\, f_{\text{ion}}(T, n_e)\, f_{\text{exc}}(T)
$$

where \(f_{\text{ion}}\) is the fraction in the correct ionisation state (from Saha)
and \(f_{\text{exc}}\) the fraction in the correct energy level (from Boltzmann). To
recover the true abundance you invert it:

$$
N_{\text{total}} = \frac{N_{\text{abs}}}{f_{\text{ion}}(T, n_e)\, f_{\text{exc}}(T)}
$$

This inversion — done star by star, element by element — is Payne's method.

### Listing 3 — Hydrogen visibility versus temperature

The visible (Balmer) hydrogen lines require the electron to be in the n = 2
level. This explains why hydrogen lines peak in A-type stars even though
hydrogen abundance is roughly constant across all main-sequence stars.

| Spectral class | Surface temperature (K) | State of hydrogen          | Visible H lines |
|----------------|-------------------------|----------------------------|-----------------|
| O              | 28 000 – 50 000         | Almost fully ionised (H+)  | Very weak / none |
| A (e.g. Sirius)| 7 500 – 10 000          | Neutral, many in n = 2     | Strongest       |
| G (the Sun)    | 5 000 – 6 000           | Neutral, mostly ground (n=1)| Weak            |
| M              | 2 500 – 3 500           | Neutral, too cold to excite | Very weak       |

### Listing 4 — Payne's abundance result versus modern values

In astronomy, "metal" means ANY element heavier than hydrogen and helium
(carbon, oxygen, iron, silicon, calcium, etc. are all "metals").

| Quantity                              | Payne (1925)                     | Modern accepted value        |
|---------------------------------------|----------------------------------|------------------------------|
| Hydrogen relative to metals (by number) | ~1 000 000 times more abundant   | Confirmed — H vastly dominant |
| Helium relative to metals (by number)   | ~1 000 times more abundant       | Confirmed                    |
| Hydrogen (universe, by mass)            | dominant                         | ~74–75%                      |
| Helium (universe, by mass)              | second                           | ~24–25%                      |
| Everything else ("metals", by mass)     | trace                            | ~1–2%                        |
| Sun, by number of nuclei                | mostly H (not iron)              | H ~92%, He ~7.8%, C/N/O <0.1% |
| Russell 1929 (Sun, by number of atoms)  | —                                | H ~92%, He ~3%, O ~3%, metals ~1.5% |

Note: the ~75% H / ~25% He by mass figure is the primordial (Big Bang)
composition the textbook quotes; the Sun's ~92% H / ~7.8% He figure is by
COUNT of nuclei, which weights the light hydrogen nucleus differently from
mass-fraction figures.

### Listing 5 — The spectral classification sequence (OBAFGKM)

Created by Annie Jump Cannon; the order is a TEMPERATURE sequence, which is
exactly what Payne's work proved. All main-sequence stars share essentially the
same composition.

| Class | Surface temperature (K) | Colour     | Defining spectral features          |
|-------|-------------------------|------------|-------------------------------------|
| O     | 28 000 – 50 000         | Blue       | Ionised helium lines; strong UV     |
| B     | 10 000 – 28 000         | Blue       | Neutral helium lines                |
| A     | 7 500 – 10 000          | Blue-white | Strong hydrogen lines; ionised metals |
| F     | 6 000 – 7 500           | White      | Strong metal lines; weak hydrogen   |
| G     | 5 000 – 6 000           | Yellow     | Ionised calcium lines; metals present |
| K     | 3 500 – 5 000           | Orange     | Neutral metals dominate; molecular lines |
| M     | 2 500 – 3 500           | Red        | Molecular bands dominate; neutral metals |

### Listing 6 — Key dates and people

| Year | Event                                                                       |
|------|------------------------------------------------------------------------------|
| 1900 | Cecilia Helena Payne born, Wendover, England (10 May)                         |
| 1919 | Eddington's eclipse lecture (2 Dec) redirects her from botany to physics      |
| 1920–21 | Meghnad Saha publishes the ionisation equation                            |
| 1923 | Moves to Harvard College Observatory on a fellowship via Harlow Shapley       |
| 1925 | PhD thesis "Stellar Atmospheres"; adds caveat after Russell calls it impossible |
| 1929 | Henry Norris Russell publishes the same result; credits Payne in passing      |
| 1939 | Hans Bethe works out hydrogen fusion (proton-proton chain, CNO cycle)         |
| 1956 | First woman appointed full professor in Harvard Faculty of Arts and Sciences |
| 1976 | Receives the Henry Norris Russell Prize                                       |
| 1979 | Dies, Cambridge, Massachusetts (7 Dec)                                        |

### Listing 7 — The three types of spectra (Kirchhoff's laws)

The syllabus requires comparing emission and absorption spectra with a
continuous black-body spectrum. A stellar spectrum is a continuous black-body
background (from the hot, dense interior) with dark absorption lines stamped in
by the cooler outer atmosphere.

| Spectrum type        | Produced when                                              | Appearance              | Astronomical source                 |
|----------------------|------------------------------------------------------------|-------------------------|-------------------------------------|
| Continuous (black body) | Hot, dense solid/liquid/gas under pressure              | Unbroken rainbow        | Dense interior of a star            |
| Absorption           | Continuous source viewed THROUGH a cooler thin gas         | Dark lines on a rainbow | Atmospheres of stars                |
| Emission             | A hot, thin (low-density) gas with no continuous source behind it | Bright lines on black   | Emission nebulae, glowing gas clouds |

Same element ⇒ same characteristic wavelengths. Whether those wavelengths show
as dark gaps or bright lines depends only on whether a hot continuous source
shines through from behind. Wien's law links the peak of the black-body curve to
temperature, which is how a star's surface temperature is read from its colour.

```text
Wien's displacement law (surface temperature from peak wavelength):
  lambda_max * T = b

  lambda_max = wavelength of peak emission (m)
  T          = surface temperature (K)
  b          = Wien's constant = 2.898 x 10^-3 m K
```

### Listing 8 — Nucleosynthesis in main-sequence stars

Once Payne established that stars are mostly hydrogen, the fuel for these
reactions was known. Both chains fuse 4 protons into one helium-4 nucleus; the
CNO cycle dominates in stars more massive (hotter-cored) than the Sun, the
proton-proton chain in the Sun and cooler stars.

```text
Proton-proton (PP1) chain — overall:
  4 (1H) -> (4He) + 2 e^+ + 2 nu + gamma   (releases ~26.7 MeV)

Step by step:
  (1H) + (1H) -> (2H) + e^+ + nu      (+1.44 MeV)
  (2H) + (1H) -> (3He) + gamma        (+5.49 MeV)
  (3He) + (3He) -> (4He) + 2 (1H)     (+12.9 MeV)
```

```text
CNO cycle — carbon-12 acts as a catalyst (consumed then regenerated):
  (12C) + (1H) -> (13N) + gamma
  (13N)        -> (13C) + e^+ + nu
  (13C) + (1H) -> (14N) + gamma
  (14N) + (1H) -> (15O) + gamma
  (15O)        -> (15N) + e^+ + nu
  (15N) + (1H) -> (12C) + (4He)

Overall:
  4 (1H) -> (4He) + 2 e^+ + 2 nu + 3 gamma   (releases ~24.7 MeV)
```

Mass-energy released per reaction follows E = mc^2, where the products are
slightly less massive than the four protons that went in (the mass defect).
