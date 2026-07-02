---
title: "Supplementary Materials — Module Review: Planning and Algorithms (Chapters 1–2)"
module: PF11
year: 11
lesson: "1-2"
script: script.md
---

# Supplementary Materials

The Chapters 1–2 mnemonic master sheet, plus the review's two worked tasks (a trace and a
design). Nothing here is spoken in the audio — it's the read-along reference. The narration
points at each by label only.

### Listing 1 — Chapters 1–2 mnemonic master sheet (the exam-dump reference)
```text
CHAPTER 1 — SOFTWARE DEVELOPMENT (the process)
  R-S-D-D-I-T-I-M  8 dev steps: Requirements, Specifications, Design, Development,
                   Integration, Testing, Installation, Maintenance.  (lifecycle is
                   ITERATIVE, not linear)   order sentence: "Real Software Demands
                   Discipline: Integrate, Test, Install, Maintain."
  W-S-R            Git's 3 places: Write (working tree), Stage (staging area), Record (repo).
  CRAB             Online-collaboration benefits: Collaboration, Review, Accountability, Backup.
  R-D-C            Documentation levels (widest->narrowest): Read-me, Docstring, Comment.
                   Rule: a comment explains WHY, not WHAT.
  Waterfall/Agile  "Waterfall falls once; Agile loops."  Compare on R-F-D-C =
                   Requirements, Feedback, Documentation, Change.  No universal winner —
                   depends on REQUIREMENT STABILITY.

CHAPTER 2 — DESIGNING ALGORITHMS (the thing you build)
  S-S-I            Control structures: Sequence, Selection, Iteration.
  loops            "For counts, While checks first, Repeat checks last."
                   "While may run never; Repeat runs once for sure." (pre-test 0+, post-test 1+)
  A-E-F            Data a loop stores: Accumulator, Extreme, Flag.
  flowchart sym.   rounded=terminator, parallelogram=I/O, rectangle=process,
                   DIAMOND=decision (only brancher), double-barred box=subprogram call.
  one-liners       "Flowchart shows what the program does, in order; a DFD shows where the
                   data goes."  "Structure chart shows who calls whom + the data passed."
  design           "Top-down splits; bottom-up builds."  "High cohesion, low coupling."
  strategies       Divide&conquer = SPLIT, SOLVE, COMBINE.  Backtracking = TRY, FAIL, UNDO, RETRY.
  subprograms      "A FUNCTION returns; a PROCEDURE performs."  Params: "IN reads, OUT writes
                   back, IN-OUT does both."
  analysis         I-O-P = Inputs, Outputs, Purpose.  "Desk is solo, peer is social."
                   Full method: "Read, I-O-P, Map, Trace, Check."  A connection is a CALL
                   (who runs whom) or a DATA hand-off (whose result feeds whom).
  paradigms        I-O-L-F = Imperative ("how to do it"), Object-oriented ("model the world"),
                   Logic ("what is true"), Functional ("transform data").
                   No best paradigm; a language is NOT a paradigm (most are multi-paradigm).

OUTCOMES: SE-11-01 (plan/develop/engineer software) · SE-11-02 (structural elements develop code).
```

### Listing 2 — Trace task: results-summary algorithm (NESA pseudocode)
```text
BEGIN ResultsSummary
    total ← 0
    highest ← scores[0]          // running EXTREME, seeded with the first score
    passCount ← 0                // a counter / flag-style tally
    FOR EACH score IN scores
        total ← total + score    // ACCUMULATOR
        IF score > highest THEN
            highest ← score
        ENDIF
        IF score ≥ 50 THEN       // boundary: 50 counts as a PASS (≥, not >)
            passCount ← passCount + 1
        ENDIF
    NEXT score
    average ← total / length(scores)
    OUTPUT average, highest, passCount
END ResultsSummary
```

### Listing 3 — Completed trace table for scores = 40, 75, 50
```text
Step  Action                       score  total  highest  passCount
----  ---------------------------  -----  -----  -------  ---------
 0    initialise                   -      0      40       0
 1    score=40: +total             40     40     40       0     (40>40? no; 40≥50? no)
 2    score=75: +total, new max,   75     115    75       1     (75>40 yes; 75≥50 yes)
 3    score=50: +total, pass       50     165    75       2     (50>75? no; 50≥50 YES -> pass)
 -    average ← 165 / 3                                          average = 55.0

Output: average = 55.0, highest = 75, passCount = 2
Boundary note: 50 is a PASS because the test is "≥ 50" (greater than OR equal).
```

### Listing 4 — Design task: grade-report, decomposed (NESA pseudocode)
```text
BEGIN FUNCTION CalculateAverage(scores)        // FUNCTION: returns a value
    total ← 0
    FOR EACH s IN scores
        total ← total + s
    NEXT s
    RETURN total / length(scores)
END FUNCTION

BEGIN FUNCTION DetermineGrade(average)          // FUNCTION: returns a value
    IF average ≥ 90 THEN
        RETURN "A"
    ELSE IF average ≥ 80 THEN
        RETURN "B"
    ELSE IF average ≥ 70 THEN
        RETURN "C"
    ELSE IF average ≥ 50 THEN
        RETURN "D"
    ELSE
        RETURN "F"
    ENDIF
END FUNCTION

BEGIN PROCEDURE DisplayReport(name, average, grade)   // PROCEDURE: performs an action
    OUTPUT name + " — average " + average + ", grade " + grade
END PROCEDURE

BEGIN GradeReport
    INPUT name
    INPUT scores
    average ← CalculateAverage(scores)          // call a function, store the result
    grade   ← DetermineGrade(average)           // DATA DEPENDENCY: grade depends on average
    DisplayReport(name, average, grade)         // call a procedure for its effect
END GradeReport
```

### Listing 5 — Both review tasks as runnable Python (verifies the traces and the design)
```python
# TASK 1: results-summary — uses A-E-F (accumulator, extreme, flag/count)
def results_summary(scores):
    total = 0
    highest = scores[0]
    pass_count = 0
    for score in scores:
        total = total + score
        if score > highest:
            highest = score
        if score >= 50:                 # boundary: 50 counts as a pass
            pass_count = pass_count + 1
    return total / len(scores), highest, pass_count


assert results_summary([40, 75, 50]) == (55.0, 75, 2)
assert results_summary([90, 40, 90]) == (220 / 3, 90, 2)   # equal case: highest stays 90


# TASK 2: grade-report design — two FUNCTIONS + a main (DisplayReport omitted here)
def calculate_average(scores):
    return sum(scores) / len(scores)


def determine_grade(average):
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


def grade_report(name, scores):
    average = calculate_average(scores)
    grade = determine_grade(average)        # grade depends on average (data dependency)
    return name, average, grade


assert grade_report("Alice", [85, 92, 78]) == ("Alice", 85.0, "B")
assert determine_grade(55.0) == "D"          # 55 falls in the D band (50-69)
print("All review-task assertions passed.")
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| A-E-F | Accumulator · Extreme · Flag | Kinds of variable that store data across an algorithm |
| DFD | Data Flow Diagram | A model showing how data moves between processes, stores and external entities |
| I-O-L-F | Imperative · Object-oriented · Logic · Functional | The programming paradigms |
| I-O-P | Inputs · Outputs · Purpose | What to identify when analysing a written algorithm |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| R-D-C | Read-me · Docstring · Comment | Levels of code documentation |
| R-F-D-C | Requirements · Feedback · Documentation · Change | Axes for comparing Waterfall vs Agile |
| R-S-D-D-I-T-I-M | Requirements · Specifications · Design · Development · Integration · Testing · Installation · Maintenance | The eight software-development steps |
| S-S-I | Sequence · Selection · Iteration | The three control structures |
| W-S-R | Write (working tree) · Stage (index) · Record (repo) | Git's three places |
