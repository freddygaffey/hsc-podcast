---
title: "Supplementary Materials — Control Structures (Sequence, Selection, Iteration)"
module: PF11
year: 11
lesson: "2.1"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration points at each by label only.

### Listing 1 — Sequence, selection and iteration in one algorithm (Python)
```python
def process_scores(scores):
    # Sequence: set up the data we must store
    total = 0
    count = 0
    # Iteration: accumulate the total across every score
    for score in scores:
        total = total + score
        count = count + 1
    average = total / count
    # Selection: the first true branch wins, the rest are skipped
    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "F"
    return average, grade


assert process_scores([85, 92, 78]) == (85.0, "B")   # 255 / 3 = 85.0 -> B
assert process_scores([70, 70, 70]) == (70.0, "C")   # boundary: 70 lands in C
assert process_scores([40, 50, 30]) == (40.0, "F")   # 120 / 3 = 40.0 -> F
print("All process_scores assertions passed.")
```

### Listing 2 — The same algorithm in NESA pseudocode
```text
BEGIN ProcessScores
    total ← 0
    count ← 0
    FOR each score IN scores
        total ← total + score
        count ← count + 1
    NEXT score
    average ← total / count

    IF average ≥ 90 THEN
        grade ← "A"
    ELSE IF average ≥ 80 THEN
        grade ← "B"
    ELSE IF average ≥ 70 THEN
        grade ← "C"
    ELSE IF average ≥ 50 THEN
        grade ← "D"
    ELSE
        grade ← "F"
    ENDIF

    RETURN average, grade
END ProcessScores
```

### Listing 3 — Pre-test vs post-test loop: the same validation two ways (NESA pseudocode)
```text
BEGIN GetValidInput_PreTest        // WHILE = pre-test: may run zero times
    INPUT number
    WHILE number < 1 OR number > 100 DO
        OUTPUT "Invalid. Enter a number from 1 to 100."
        INPUT number
    ENDWHILE
    OUTPUT number
END GetValidInput_PreTest

BEGIN GetValidInput_PostTest       // REPEAT-UNTIL = post-test: always runs at least once
    REPEAT
        INPUT number
        IF number < 1 OR number > 100 THEN
            OUTPUT "Invalid. Enter a number from 1 to 100."
        ENDIF
    UNTIL number ≥ 1 AND number ≤ 100
    OUTPUT number
END GetValidInput_PostTest
```

### Listing 4 — The infinite-loop trap and its fix (Python)
```python
# BUG (do not run): the control variable never changes, so the
# condition stays true forever and the loop never terminates.
#
#     i = 5
#     while i > 0:
#         print(i)          # i is never decreased -> infinite loop

# FIX: every pass must make progress toward the exit condition.
def countdown(start):
    result = []
    i = start
    while i > 0:
        result.append(i)
        i = i - 1            # update the variable the condition depends on
    return result


assert countdown(5) == [5, 4, 3, 2, 1]
assert countdown(0) == []    # a pre-test while loop can run zero times
print("All countdown assertions passed.")
```

### Listing 5 — Identifying data to store: accumulator, running maximum and flag (Python)
```python
def summarise(scores, pass_mark=50):
    # The data this algorithm must store as it loops:
    total = 0                 # Accumulator (running total)
    highest = scores[0]       # running eXtreme (best so far)
    any_passed = False        # Flag (has any condition been met yet?)
    for score in scores:
        total = total + score
        if score > highest:
            highest = score
        if score >= pass_mark:
            any_passed = True
    average = total / len(scores)
    return {"average": average, "highest": highest, "any_passed": any_passed}


assert summarise([85, 92, 78]) == {"average": 85.0, "highest": 92, "any_passed": True}
assert summarise([10, 20, 30]) == {"average": 20.0, "highest": 30, "any_passed": False}
print("All summarise assertions passed.")
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
