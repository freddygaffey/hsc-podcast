---
title: "Supplementary Materials — Zillow Offers"
module: SA
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Zillow Offers case study. Nothing here is spoken in the audio — the
narration points at each listing by label only. Listing 1 is the timeline; Listing 2 demonstrates how a
confident forecast goes wrong when the trend turns; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
Background  Zillow runs an estimate of what any home is worth (the "Zestimate"), powered by machine
            learning. It launches Zillow Offers -- an "iBuying" business: use a price-prediction model to
            make instant cash offers, BUY homes, then resell ("flip") them for a small profit. The whole
            business rests on the model predicting future sale prices accurately, at scale.
2018-21     Zillow Offers expands aggressively, buying thousands of homes based on the model's forecasts.
2021        The housing market shifts and becomes volatile. The model -- tuned on recent history -- keeps
            forecasting prices that don't hold. Zillow finds it has been paying MORE for homes than it can
            resell them for: bought high, must sell low.
Nov 2021    Zillow announces it is SHUTTING DOWN Zillow Offers. It writes down hundreds of millions of
            dollars (a ~US$300M+ write-down, ~US$500M+ in total losses on the unit), is left holding
            thousands of homes worth less than it paid, and lays off about a quarter of its staff (~2,000
            people). The CEO concedes home prices proved far less predictable than the model assumed.
Lesson      A forecasting model that worked while the trend held broke when the trend turned -- and the
            business had bet enormous, real money on the forecast being right.
```

### Listing 2 — A confident forecast that breaks when the trend turns (Python, runnable)
```python
# The model learns from a recent run of steadily rising prices (in $1000s) and assumes the trend continues.
training_prices = [300, 310, 320, 330, 340]

def naive_forecast(history):
    """Extrapolate the recent trend: assume the next change equals the last change. Confident -- and blind
    to the possibility that the world changes."""
    last_change = history[-1] - history[-2]
    return history[-1] + last_change


predicted_next = naive_forecast(training_prices)
assert predicted_next == 350            # the model confidently predicts the rise continues -> buy at ~350

# But the market TURNED -- the actual next price fell. The model had already bought at its prediction.
actual_next = 325
overpay_per_house = (predicted_next - actual_next) * 1000   # $ per house (prices are in $1000s)
assert overpay_per_house == 25_000                          # bought ~25k too high on every house

# Acting on the forecast AT SCALE multiplies a per-house error into a company-sized loss.
houses_bought = 1000
toy_total_loss = overpay_per_house * houses_bought
assert toy_total_loss == 25_000_000                         # illustrative: $25M at this toy scale
print("Predicted", predicted_next, "but reality was", actual_next,
      "-> overpaid $", overpay_per_house, "per house x", houses_bought, "houses = $", toy_total_loss)
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
Zillow Offers is a FORECASTING-OVERCONFIDENCE story: a regression/prediction model bet real money on the
future continuing to look like the past.

1  A MODEL OUTPUT IS A PREDICTION, NOT A GUARANTEE
   Forecasting (the F in F-A-I = Forecasting / Assistants / Image recognition) is regression: it predicts
   a number with uncertainty. Treating that number as a certainty -- and buying thousands of houses at it --
   removed the safety margin. (SA 20-03 applications; 21-01 regression.)

2  OVERFITTING + DISTRIBUTION SHIFT: the past is not a promise about the future
   A model tuned tightly to recent history captures that period -- and fails when conditions change
   (the market turned = "distribution shift": the live data no longer matches the training data). An
   overfitted/over-trusted model looks brilliant until the world moves. (SA 21-01 overfitting; train/test split.)

3  ERROR x SCALE = DISASTER
   A modest per-house misprediction is survivable on one house. Multiplied across thousands of automated
   purchases, it became a loss of hundreds of millions. Automating a decision multiplies BOTH its upside
   and its error. (Compare case_the_cloudflare_2019_outage: one fault x global scale.)

4  KEEP HUMAN JUDGEMENT + GUARDRAILS AROUND A MODEL
   Acting automatically and aggressively on model output, with thin margins and no brake for "what if the
   model is wrong?", is the trap. Respect the model's uncertainty; cap exposure; keep a human in the loop.

CASHES INTO: SA 20-03 (forecasting applications), 21-01 (regression overconfidence/overfitting).
Companion to case_the_amazon_recruiting_ai and case_the_compas_recidivism (the limits of trusting a model).
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| F-A-I | Forecasting · Assistants · Image recognition | Common applications of machine learning |
