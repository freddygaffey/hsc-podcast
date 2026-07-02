---
title: "Supplementary Materials — Evaluating Solutions"
module: PF11
year: 11
lesson: "4.8"
script: script.md
---

# Supplementary Materials

The four-aspect evaluation framework, runnable evidence for functionality / performance /
readability, and a weak-vs-strong evaluation reference. Nothing here is spoken in the audio —
it's the read-along reference. The narration points at each by label only. (Evaluation is a
judgement skill, not an algorithm — no NESA pseudocode this episode.)

### Listing 1 — The evaluation framework: F-P-R-D (reference)
```text
EVALUATING A SOLUTION — four aspects (F-P-R-D)
"Evaluate" = an evidence-based JUDGEMENT against criteria, with a conclusion — NOT an opinion.

  FUNCTIONALITY    Does it do what it should? -> meets the REQUIREMENTS / SPEC (1.1),
                   passes its TEST DATA incl. boundary + faulty (4.6), free of errors (4.7).
                   Evidence: test results measured against the specification.
  PERFORMANCE      How efficiently does it run? -> speed, memory, responsiveness, SCALING.
                   Evidence: timing / resource measurements; behaviour as input grows.
  READABILITY      Can another person read + maintain it? -> descriptive names, consistent
   of code         indentation, structure, single-responsibility functions (1.3, 4.3).
                   Evidence: the naming, layout and cohesion of the code itself.
  QUALITY of       Is it explained? -> README, docstrings, why-not-what comments (1.3 = R-D-C).
   documentation   Evidence: presence + clarity of the documentation.

STRONG evaluation = CRITERIA + EVIDENCE + a balanced CONCLUSION.   WEAK = vague praise.
Address ALL FOUR aspects — not just functionality. Test produces evidence; evaluate judges it.
```

### Listing 2 — Functionality evidence: the grade calculator with passing tests (runnable)
```python
def calculate_average(scores):
    """Return the mean of the scores."""
    return sum(scores) / len(scores)


def determine_grade(average):
    """Return the letter grade (A>=90, B>=80, C>=70, D>=50, else F)."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


# FUNCTIONALITY evidence = it passes its test data (normal + boundary):
assert calculate_average([85, 92, 78]) == 85.0   # normal
assert determine_grade(85.0) == "B"
assert determine_grade(50) == "D"                # boundary
assert determine_grade(49) == "F"                # boundary
assert determine_grade(90) == "A"                # boundary
print("Functionality evidence: all grade-calculator tests pass.")
```

### Listing 3 — Performance: two correct solutions, very different efficiency (runnable)
```python
def has_duplicates_slow(items):       # O(n^2): compares every pair
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


def has_duplicates_fast(items):       # O(n): a set membership check
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False


# SAME correct result (functionality)...
assert has_duplicates_slow([1, 2, 3, 2]) is True
assert has_duplicates_fast([1, 2, 3, 2]) is True
assert has_duplicates_slow([1, 2, 3]) is False
assert has_duplicates_fast([1, 2, 3]) is False
# ...but the set-based version SCALES far better on large lists (n vs n-squared work).
print("Both functionally correct; the fast version wins on PERFORMANCE.")
```

### Listing 4 — Readability: cryptic vs clear, same behaviour (runnable)
```python
# POOR readability — one-letter name, no docstring, unclear purpose:
def c(x, y, z):
    return (x + y + z) / 3


# GOOD readability — descriptive name, a docstring, one clear job:
def calculate_average_of_three(score1, score2, score3):
    """Return the average of three scores."""
    return (score1 + score2 + score3) / 3


# Identical behaviour, very different maintainability:
assert c(80, 90, 100) == calculate_average_of_three(80, 90, 100) == 90.0
print("Same behaviour; the second is readable and maintainable.")
```

### Listing 5 — Weak vs strong evaluation, per aspect (band-4 vs band-6)
```text
FUNCTIONALITY
  WEAK:   "It works well."
  STRONG: "It meets the spec — all test cases pass, including the boundary marks 49/50 and
          89/90 and the invalid -1/101 — so the grade logic is correct."
PERFORMANCE
  WEAK:   "It's fast."
  STRONG: "It processes the scores in a single pass; instant for a class of 30, and it would
          still scale to thousands of students."
READABILITY
  WEAK:   "The code is good / easy to read."
  STRONG: "Functions are single-purpose with descriptive names (calculate-average,
          determine-grade) and consistent indentation, so it's easy to maintain."
DOCUMENTATION
  WEAK:   "It has comments."
  STRONG: "Each function has a docstring stating its contract and a README explains how to
          run it; comments explain WHY, not what."

The difference every time: EVIDENCE and SPECIFICS, not adjectives.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| R-D-C | Read-me · Docstring · Comment | Levels of code documentation |
