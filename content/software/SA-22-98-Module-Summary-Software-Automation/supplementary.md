---
title: "Supplementary Materials — Module Summary: Software Automation"
module: SA
year: 12
lesson: "20–22"
script: script.md
---

# Supplementary Materials

The one-page revision references for the whole Software Automation module. Nothing here is
spoken in the audio — it's the read-along sheet. Listing 1 is the master mnemonic table;
Listing 2 is the key-terms checklist by topic.

### Listing 1 — Master mnemonic table (every SA mnemonic + full expansion)
```text
EXAM-DUMP MARQUEE HOOKS (write these first):
  "A-I is the goal, M-L is one way"  ·  R-P-A=Robot/Task, B-P-A=Process  ·  S-U-S-R
  ·  L-L-K  ·  S-H-L-M  ·  S-P-E-E

CH 20 — THE LANDSCAPE (what AI/ML are, training, applications, models, RPA/BPA)
  "A-I is the goal, M-L is one way"  = AI = behave intelligently (may/may not learn);
                       Machine Learning = a SUBSET that LEARNS patterns from data. Line = learning.
  DevOps / C-I-C-D   = automates the build-test-deploy pipeline (inward, at the team)
  R-P-A vs B-P-A     = R-P-A is a Robot doing a Task (mimics a human at the UI, low-code,
                       brittle); B-P-A is redesigning a Process (deep integration, workflow
                       engine, approvals, audit trail)
  "Automation provides the hands; machine learning provides the eyes and judgement"
  S-U-S-R            = training models: Supervised (labelled), Unsupervised (no labels,
                       find structure), Semi-supervised (few labels + big unlabelled pool),
                       Reinforcement (no dataset; agent + reward signal)
  "Garbage labels in, bias out"   (supervised is only as good as its labels)
  F-A-I ("fie")      = applications: Forecasting, Assistants, Image recognition
                       (always: name it, what it does, the technique, the data it needs)
  R-N-L              = decision-tree parts: Root, Node, Leaf  (trace root->leaf, state the path)
  "A Tree is readable if-questions; a Net is weighted neurons"  (interpretable vs black box
                       = transparency vs power; explainability ties to Accountability, CIA-AAA)
  "R-P-A is brittle — it breaks when the user interface changes"

CH 21 — THE PROGRAMMING (regression, algorithm types, neural networks in OOP)
  L-L-K              = core algorithm types: Linear regression, Logistic regression,
                       K-nearest neighbour
  "Linear predicts a NUMBER; Logistic predicts a YES-OR-NO"  (logistic = classification via
                       the sigmoid + 0.5 threshold; polynomial = the curve = how you overfit)
  "Fit learns, predict applies"  (models = fit/predict classes, e.g. scikit-learn .fit/.predict)
  "Train on one set, test on a separate unseen set"  (a big train-vs-test gap = OVERFITTING;
                       a perfect training fit is a red flag, not a triumph)
  P-L-A              = neural-net training loop: Predict (forward pass), Loss (distance from
                       label), Adjust (nudge weights) — over many epochs
                       (technically backpropagation + gradient descent)
  "A neuron is a weighted sum then an activation"  ·  "Layers learn features" (edges -> faces)

CH 22 — THE SIGNIFICANCE (impact, human behaviour, bias)
  S-P-E-E            = impacts (assess BOTH sides + a judgement): Safety and access,
                       People and skills (employment = a SHIFT, not just jobs gone),
                       Efficiency and Environment (incl. AI's own carbon/water cost),
                       Economy and wealth (gains concentrate -> inequality)
  P-S-C-B ("Please See, Curious Brain") = human-behaviour factors influencing ML/AI:
                       Psychological, acute Stress response, Cultural protocols, Belief systems
                       (name the factor + the concrete design response)
  S-H-L-M ("SHaLuM") = bias sources: Sampling (who's missing?), Historical (a true record of an
                       unfair past — more data does NOT fix it), Labeler, Measurement (flawed proxy)
  D-R-F ("Don't Reinforce unFairness") = mitigations: Diverse data, Reweight (fairness
                       constraints in training), Fairness metrics per GROUP (not overall accuracy)
  "The algorithm isn't neutral — it mirrors and amplifies its data"
                       (accountability lift = model cards + provenance + reproducibility = the
                       Accountability A of CIA-AAA applied to AI)
```

### Listing 2 — Key-terms checklist by topic
```text
[ ] 20-01 AI vs ML: AI = broad field (reason/perceive/decide, may/may not learn); ML = subset
        that learns from data; line = LEARNING; rule-based expert system = AI that is NOT ML
        (transparent, hand-written rules). Trap: a plain if-statement is not AI.
[ ] 20-02 Training models (S-U-S-R): Supervised = labelled (answer key) -> classification
        (category) / regression (number); Unsupervised = no labels -> clustering / anomaly;
        Semi-supervised = few labels + large unlabelled pool (labels costly, e.g. medical imaging);
        Reinforcement = agent acts in an environment, learns from reward/penalty (no dataset).
        Decider: do you have labels, how many, or an environment with rewards?
[ ] 20-03 Applications (F-A-I): Forecasting (supervised regression on history; fails when the
        world shifts — Zillow ~$500M); Assistants (NLP + supervised on language); Image
        recognition (deep nets, supervised/semi-supervised on labelled images).
[ ] 20-04 Models (decision trees vs neural networks): tree = learned if-then tests, R-N-L
        (Root/Node/Leaf), INTERPRETABLE; neural net = layers of weighted-sum+activation neurons,
        BLACK BOX. Key exam axis = explainability: interpretable-but-weaker vs powerful-but-opaque.
        Trap: a net is not a brain; "deeper is better" is false (overfits).
[ ] 20-05 RPA vs BPA: R-P-A = tactical, low-code, on top of existing UIs, screen-scrapes, BRITTLE
        (breaks on UI change) = treats the symptom; B-P-A = strategic, deep integration, workflow
        engine + approvals + audit trail = treats the cause. Security: protect bot credentials
        (secrets manager), least privilege, validate input. Ethics verb = EVALUATE (employment
        = reskilling shift; accountability + audit trail).
[ ] 21-01 Regression & algorithm types (L-L-K): Linear (continuous number, best-fit line =
        slope*x+intercept); Logistic (CLASSIFICATION via sigmoid + 0.5 threshold); Polynomial
        (curve; overfits); K-nearest neighbour (majority vote of K closest). Models = fit/predict
        classes. OVERFITTING = memorising noise -> fails on new data; fix = simpler model / more
        data / regularisation; always train-test split. Trap: logistic is classification.
[ ] 21-02 Neural networks (apply: describe/trace/explain): perceptron = one neuron (inputs*weights
        + bias -> activation); forward pass = multiply/sum/activate; structure = input / hidden
        / output layers, weighted links, "layers learn features"; training = P-L-A (Predict, Loss,
        Adjust) over epochs = backpropagation + gradient descent. Trap: "it just learns" = band 4.
[ ] 22-01 Impact of automation (assess/evaluate, BOTH sides + judgement) — S-P-E-E: Safety & access
        (incl. disability — enabling if inclusive); People & skills (employment = transformation +
        reskilling, not just jobs gone); Efficiency & Environment (output up, but e-waste + AI's
        training energy/water); Economy & wealth (growth but concentrated gains -> inequality).
        Trap: one-sided answers; forgetting AI's own environmental cost.
[ ] 22-02 Human behaviour -> ML/AI (P-S-C-B, "by implementation" = factor + design response):
        Psychological (trust via transparency + override; cognitive load); acute Stress response
        (train on realistic high-stress data — the 3am clinician); Cultural protocols (authority,
        comms, individual vs collective, privacy; incl. Indigenous cultural & IP); Belief systems
        (tech-optimism / agency / privacy -> accept or reject). Thesis: AI adapts to humans.
[ ] 22-03 Bias (S-H-L-M sources; D-R-F mitigations): bias = systematic unfair skew (not noise);
        "the algorithm isn't neutral — it mirrors + amplifies its data" (even without the sensitive
        attribute, via proxies). Sources: Sampling / Historical (more data ≠ fix) / Labeler /
        Measurement. Mitigate: Diverse data, Reweight, Fairness metrics PER GROUP; accountability =
        model cards + provenance + reproducibility (the Accountability A of CIA-AAA).
```
