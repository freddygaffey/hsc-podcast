---
title: "Supplementary Materials — Amazon's Biased Recruiting AI"
module: SA
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Amazon recruiting-AI case study. Nothing here is spoken in the audio —
the narration points at each listing by label only. Listing 1 is the timeline; Listing 2 demonstrates
"bias in, bias out" in runnable code; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
~2014        Amazon builds an experimental machine-learning tool to score job applicants' resumes
             (one to five stars), hoping to automate and speed up recruiting at huge scale.
Training     It is trained, in supervised fashion, on resumes submitted to Amazon over ~10 years and
             whether those people were hired -- i.e. it learns to imitate Amazon's PAST hiring decisions.
             But the tech-industry applicant pool over that decade was overwhelmingly male.
~2015        Engineers discover the model has taught itself to prefer men. It penalises resumes containing
             the word "women's" (e.g. "women's chess club captain") and downgrades graduates of two
             all-women's colleges; it favours male-associated phrasing. It learned the past's bias as if
             it were a rule about merit.
Mitigation   Amazon edits it to ignore those specific gendered terms -- but cannot guarantee the model
             won't find OTHER proxies for gender, and loses confidence in it.
~2017        The project is effectively abandoned. (Reported publicly by Reuters in October 2018.)
             Amazon says it was never the sole basis for hiring; it was scrapped rather than relied upon.
```

### Listing 2 — Bias in, bias out: a model that copies biased history (Python, runnable)
```python
# Past hiring decisions the model is TRAINED on. Group A and group B applicants are equally skilled,
# but past hiring favoured A -> the LABELS themselves carry historical bias.
history = [
    # (skill_score, group, proxy_word_on_cv, hired_in_the_past)
    (9, "A", False, True),
    (8, "A", False, True),
    (9, "B", True,  False),   # just as skilled as the A's, but not hired -> biased label
    (8, "B", True,  False),
    (3, "A", False, False),
]

def hire_rate_by(history, key):
    """A naive 'model': predict a hire from how often each value of `key` was hired in the past."""
    buckets = {}
    for skill, group, proxy, hired in history:
        value = group if key == "group" else proxy
        buckets.setdefault(value, []).append(1 if hired else 0)
    return {k: round(sum(v) / len(v), 2) for k, v in buckets.items()}


# Train on the group: the model 'prefers' A purely from biased history -- skill never enters into it.
by_group = hire_rate_by(history, "group")
assert by_group["A"] > by_group["B"]
assert by_group["B"] == 0.0        # it would NEVER recommend a group-B applicant, however skilled

# "Just delete the group feature" is not enough: a correlated PROXY (a word on the CV) still leaks it.
by_proxy = hire_rate_by(history, "proxy")
assert by_proxy[True] == 0.0       # CVs carrying the proxy word are still scored zero
print("By group:", by_group, "| by proxy word:", by_proxy, "-> removing the label leaves the proxy.")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
Amazon's recruiting AI is the textbook case of HISTORICAL BIAS: a supervised model learned to copy a
biased past and would have automated it at scale.

1  SUPERVISED LEARNING IS ONLY AS GOOD AS ITS LABELS  ("bias in, bias out")
   A supervised model (the S in SUSR = Supervised/Unsupervised/Semi-supervised/Reinforcement) learns to
   reproduce its training LABELS. Train it on biased decisions and it learns the bias as if it were truth.
   (SA 20-02 training models; the model optimises to match the past, not to be fair.)

2  KNOW YOUR BIAS SOURCES -- S-H-L-M
   Sampling, Historical, Labeler, Measurement bias. Amazon's was chiefly HISTORICAL (the past hiring it
   trained on was skewed) plus a skewed Sample (a male-dominated applicant pool). (SA 22-03.)

3  REMOVING THE SENSITIVE FEATURE IS NOT ENOUGH -- PROXIES REMAIN
   Delete "gender" and the model finds correlated proxies (the word "women's", a college name). You must
   test the OUTCOMES for fairness, not just hide the obvious feature. (SA 22-03; Listing 2.)

4  MITIGATION -- D-R-F, AND KEEP A HUMAN ACCOUNTABLE
   Diverse, representative data; Reweight/rebalance; Fairness metrics on the outputs. Plus human oversight
   and model cards / accountability -- and the willingness, as Amazon ultimately showed, to SCRAP a model
   you cannot trust rather than deploy it. (SA 22-03 mitigation; ties to SSA accountability.)

CASHES INTO: SA 20-02 (supervised learning learns the labels), 22-03 (bias sources + mitigation).
Companion to case_the_compas_recidivism (fairness of a risk-scoring model).
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| AI | Artificial Intelligence | Software that performs tasks normally needing human intelligence |
| D-R-F | Diverse data · Reweight · Fairness metrics | Techniques to reduce bias in datasets/models |
| S-H-L-M | Sampling · Historical · Labeler · Measurement | The sources of bias in machine learning |
