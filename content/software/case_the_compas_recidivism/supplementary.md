---
title: "Supplementary Materials — COMPAS and the Many Meanings of Fairness"
module: SA
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the COMPAS case study. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 is the timeline; Listing 2 demonstrates how two fairness
definitions can conflict; Listing 3 maps the lessons onto the course. (A sensitive topic — handled factually.)

### Listing 1 — Timeline (reference)
```text
2000s-      US courts increasingly use risk-assessment software to help inform bail, sentencing and parole
            decisions. One widely-used tool is COMPAS (by Northpointe, later Equivant): from a long
            questionnaire it produces a recidivism RISK SCORE (1-10) -- a prediction of how likely a
            defendant is to reoffend. The model's internals are proprietary -- a "black box" to the court.
May 2016    ProPublica publishes "Machine Bias", an investigation of COMPAS scores for ~7,000 defendants
            in Broward County, Florida. Its finding: among people who did NOT go on to reoffend, BLACK
            defendants were about twice as likely as white defendants to have been wrongly labelled
            high-risk (a higher false-positive rate); white defendants who DID reoffend were more often
            wrongly labelled low-risk.
Rebuttal    Northpointe responds that the tool is CALIBRATED: within any given risk score, the share who
            actually reoffend is about the same across races (this is "predictive parity"). By that
            definition, it is fair.
2016-17     Researchers (e.g. Kleinberg and colleagues; Chouldechova) prove a hard result: when the base
            rates differ between groups, you CANNOT satisfy calibration AND equal false-positive/negative
            rates at the same time. Both sides were right -- about DIFFERENT definitions of "fair".
After       The debate reshapes the field: "fairness" is not one number, and choosing which fairness
            definition to enforce is a value/policy decision, not a purely technical one.
```

### Listing 2 — Two definitions of "fair" that cannot both hold (Python, runnable)
```python
# Toy outcomes for two groups. Each tuple = (TP, FP, FN, TN):
#   TP = flagged high-risk AND reoffended      FP = flagged high-risk but did NOT reoffend
#   FN = flagged low-risk but reoffended       TN = flagged low-risk and did not reoffend
# The two groups have DIFFERENT base rates of reoffending (0.5 vs 0.6) -- as real populations do.
group_A = (30, 20, 20, 30)
group_B = (45, 30, 15, 10)

def precision(counts):
    """CALIBRATION / predictive parity: of those flagged high-risk, the share who truly reoffended."""
    tp, fp, fn, tn = counts
    return round(tp / (tp + fp), 2)

def false_positive_rate(counts):
    """Of those who did NOT reoffend, the share WRONGLY flagged high-risk."""
    tp, fp, fn, tn = counts
    return round(fp / (fp + tn), 2)


# Fairness definition 1 -- CALIBRATION: equal precision across groups. SATISFIED here.
assert precision(group_A) == precision(group_B) == 0.6

# Fairness definition 2 -- EQUAL FALSE-POSITIVE RATES. VIOLATED here.
assert false_positive_rate(group_A) != false_positive_rate(group_B)   # 0.4 vs 0.75

print("Equally calibrated (precision", precision(group_A), "for both groups) --",
      "yet false-positive rates differ:", false_positive_rate(group_A), "vs", false_positive_rate(group_B),
      "-> you cannot have both when base rates differ.")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
COMPAS is the case that proves "FAIR" IS NOT ONE THING -- and that some fairness definitions are
mathematically incompatible.

1  THERE ARE MULTIPLE, COMPETING DEFINITIONS OF FAIRNESS
   - CALIBRATION / predictive parity: within each risk score, the reoffend rate is equal across groups.
   - EQUAL ERROR RATES: equal false-positive (and false-negative) rates across groups.
   COMPAS met the first; ProPublica showed it failed the second. Both measurements were correct.
   (SA 22-03 fairness metrics -- there is more than one, and they trade off.)

2  THE IMPOSSIBILITY RESULT
   When two groups have different base rates, you provably CANNOT satisfy calibration AND equal error
   rates simultaneously. So "make it fair" has no single technical answer -- you must CHOOSE which
   fairness you prioritise, and that is a value/policy judgement with real human stakes. (22-03.)

3  IMPACT ON INDIVIDUALS AND SOCIETY IS PROFOUND HERE
   These scores influence bail, sentencing and parole -- a person's liberty. A model's error is not an
   abstract statistic; it is a human being wrongly labelled. Automation in justice raises the stakes of
   every error. (SA 22-01 impact on individuals/society; 22-02 human/legal context.)

4  TRANSPARENCY + ACCOUNTABILITY
   COMPAS's internals were proprietary -- defendants could not inspect the basis of a score used against
   them. High-stakes automated decisions need explainability, the right to challenge, and a human who is
   accountable for the decision -- not "the algorithm decided". (22-02; ties to SSA accountability.)

CASHES INTO: SA 22-03 (fairness metrics), 22-01 (impact), 22-02 (human/justice context).
Companion to case_the_amazon_recruiting_ai (historical bias in a model that judges people).
```
