---
title: "Supplementary Materials — Module Review: Programming Fundamentals (Chapters 1–4)"
module: PF11
year: 11
lesson: "1-4"
script: script.md
---

# Supplementary Materials

The whole-module mnemonic master sheet, the end-to-end worked task (design → code → test),
and a mnemonic-to-exam-question map. Nothing here is spoken in the audio — it's the read-along
reference. The narration points at each by label only.

### Listing 1 — Programming Fundamentals master sheet (the exam-dump reference)
```text
CHAPTER 1 — SOFTWARE DEVELOPMENT (the process)
  R-S-D-D-I-T-I-M   8 steps: Requirements, Specifications, Design, Development, Integration,
                    Testing, Installation, Maintenance.  Lifecycle is ITERATIVE, not linear.
  W-S-R             Git's 3 places: Write (working tree), Stage (index), Record (repo).
  CRAB              Collaboration-tool benefits: Collaboration, Review, Accountability, Backup.
  R-D-C             Documentation: Read-me, Docstring, Comment.  A comment explains WHY not WHAT.
  Waterfall/Agile   "Waterfall falls once; Agile loops."  Compare on R-F-D-C (Requirements,
                    Feedback, Documentation, Change).  No universal winner — fit requirement stability.

CHAPTER 2 — DESIGNING ALGORITHMS (the algorithm)
  S-S-I             Control structures: Sequence, Selection, Iteration.
  loops             "For counts, While checks first, Repeat checks last." / "While may run never,
                    Repeat runs once for sure."     A-E-F = data stored: Accumulator, Extreme, Flag.
  flowchart         rounded=terminator, parallelogram=I/O, rectangle=process, DIAMOND=decision,
                    double-bar=subprogram call.  "Flowchart = order; DFD = where the data goes."
  I-O-P             Analyse: Inputs, Outputs, Purpose.  "Desk is solo, peer is social."
                    Full method "Read, I-O-P, Map, Trace, Check."  Connection = a CALL or a DATA hand-off.
  design            "Top-down splits; bottom-up builds."  "High cohesion, low coupling."
                    Divide & conquer = split/solve/combine.  Backtracking = try/fail/undo/retry.
  subprograms       "A FUNCTION returns; a PROCEDURE performs."  Params: IN reads / OUT writes back / IN-OUT both.
  I-O-L-F           Paradigms: Imperative, Object-oriented, Logic, Functional.

CHAPTER 3 — DATA
  number systems    base-2 / base-10 / base-16; "each hex digit is 4 bits";
                    two's complement = "flip the bits, add one"; leftmost bit = sign; 8-bit -128..+127.
  data types        4 families: "Words, Numbers, Truth, Time".  "Integer EXACT, float APPROXIMATE."
  F-T-C-R           Data dictionary entry: Field, Type, Constraints, Relationship.
                    Constraints: how long / how big / what shape / must it be there.
                    Relationships: one-to-one, one-to-many, many-to-many.
  A-R-T-S           Data structures: Arrays, Records, Trees, Sequential files.
                    "Array indexes by number; record names by field."

CHAPTER 4 — DEVELOPING WITH CODE (the build)
  Python            "the indent is the block"; "range stops one before the stop";
                    list=array, dict=hash table, list+append/pop=stack (LIFO).
  functions         P-D-K params (Positional, Default, Keyword); one job per function.
  modules           "import the module, or the name — never the star."  "seed it to repeat it."
  debugging         trio = Breakpoint (pause), Step (walk), Watch (watch a variable).
  test data         B-P-F = Boundary, Path coverage, Faulty-and-abnormal.  Test = actual vs expected.
  errors            S-L-R = Syntax (won't run), Logic (silently wrong), Runtime (crashes).
  evaluation        F-P-R-D = Functionality, Performance, Readability, Documentation. Evidence, not opinion.

OUTCOMES: SE-11-01 / -02 / -03 / -04 / -06 / -07 (the PF outcome set).
```

### Listing 2 — End-to-end task, DESIGN phase: grade report decomposed (NESA pseudocode)
```text
BEGIN FUNCTION CalculateAverage(scores)
    total ← 0
    FOR EACH s IN scores
        total ← total + s
    NEXT s
    RETURN total / length(scores)
END FUNCTION

BEGIN FUNCTION DetermineGrade(average)
    IF average ≥ 90 THEN RETURN "A"
    ELSE IF average ≥ 80 THEN RETURN "B"
    ELSE IF average ≥ 70 THEN RETURN "C"
    ELSE IF average ≥ 50 THEN RETURN "D"
    ELSE RETURN "F"
    ENDIF
END FUNCTION

BEGIN GradeReport(name, scores)
    IF length(scores) = 0 THEN          // faulty/abnormal guard -> no division by zero
        OUTPUT name + ": no scores"
    ELSE
        avg ← CalculateAverage(scores)
        OUTPUT name + ": " + avg + " -> " + DetermineGrade(avg)
    ENDIF
END GradeReport
```

### Listing 3 — End-to-end task, CODE + TEST phase (Python, runnable; B-P-F test data)
```python
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
    if not scores:                       # FAULTY/ABNORMAL guard (empty -> avoid ZeroDivisionError)
        return name + ": no scores"
    avg = calculate_average(scores)
    return name + ": " + str(avg) + " -> " + determine_grade(avg)


# TEST with B-P-F data:
assert grade_report("Alice", [85, 92, 78]) == "Alice: 85.0 -> B"   # NORMAL
assert determine_grade(50) == "D"                                  # BOUNDARY (>= 50)
assert determine_grade(49) == "F"                                  # BOUNDARY
assert determine_grade(90) == "A"                                  # BOUNDARY
assert grade_report("Bob", []) == "Bob: no scores"                 # FAULTY/ABNORMAL
print("End-to-end task: all assertions pass (design -> code -> test).")
```

### Listing 4 — Mnemonic → exam-question quick map
```text
WHEN THE QUESTION SAYS...                          REACH FOR...
"list / order the development steps"               R-S-D-D-I-T-I-M
"compare Waterfall and Agile"                      "Waterfall falls once; Agile loops" + R-F-D-C
"benefits of collaboration tools"                  CRAB
"how should code be documented"                    R-D-C (why-not-what)
"key features of an algorithm / control structures" S-S-I
"data an algorithm must store"                     A-E-F
"analyse this algorithm"                           Read, I-O-P, Map, Trace, Check
"distinguish procedure and function"              "a function returns, a procedure performs"
"name the programming paradigms"                   I-O-L-F
"represent a negative number"                      two's complement = "flip the bits, add one"
"name the standard data types"                     Words, Numbers, Truth, Time
"construct a data dictionary"                       F-T-C-R
"name the data structures"                          A-R-T-S
"design suitable test data"                         B-P-F
"classify / explain this error"                     S-L-R
"evaluate the solution"                             F-P-R-D (with EVIDENCE)
```
