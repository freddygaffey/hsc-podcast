---
title: "Supplementary Materials — Project Management Models"
module: PF11
year: 11
lesson: "1.4"
script: script.md
---

# Supplementary Materials

Read-along reference for this episode. Nothing here is spoken — the narration points at
each listing by label. Listings 1 and 2 deliberately use the same eight lifecycle steps
from lesson 1.1, arranged two different ways: a sequence ("falls once") versus a loop
("loops").

### Listing 1 — Waterfall as exam pseudocode: a single sequential pass
```text
BEGIN WaterfallProject
    Requirements    ← gather and document ALL requirements up front
    Design          ← design the whole system on paper
    Implementation  ← build all of it
    Testing         ← test the complete system in one phase
    Deployment      ← release to users
    Maintenance     ← fix defects, minor enhancements
    // No loop: each phase runs once, in order, and you do not go back up.
END WaterfallProject
```

### Listing 2 — Agile as exam pseudocode: the lifecycle wrapped in a loop
```text
BEGIN AgileProject
    backlog ← initial list of desired features (allowed to change)

    REPEAT
        sprintFeatures ← choose a small slice from backlog   // Sprint Planning
        Plan
        Design
        Code
        Test
        Review with stakeholders                              // demo working software
        feedback ← stakeholder response
        backlog ← re-prioritise backlog using feedback        // requirements may change
    UNTIL product is complete

    Deployment
    Maintenance
END AgileProject
```

### Listing 3 — One Agile sprint in practice: a Git feature-branch workflow
```bash
# Agile loops fast because the tools (lesson 1.2) make each iteration cheap.
# A sprint's slice of work lives on its own branch, reviewed before it merges.

git switch -c sprint3-weighted-grades   # start the sprint's feature branch
# ...plan, design, code, test the slice...
git add grade_calculator.py
git commit -m "Add weighted-grade option"

# Push the branch and open a pull request; teammates review it there (code review).
git push -u origin sprint3-weighted-grades

# Once the pull request is approved, the reviewed slice is merged into main
# (on the platform, or locally as shown here) and the branch is tidied up.
git switch main
git merge sprint3-weighted-grades       # integrate the reviewed slice
git branch -d sprint3-weighted-grades   # next sprint starts fresh
```
