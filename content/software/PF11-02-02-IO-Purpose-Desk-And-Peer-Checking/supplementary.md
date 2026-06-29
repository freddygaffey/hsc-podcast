---
title: "Supplementary Materials — Analysing Algorithms (I/O, Purpose, Desk & Peer Checking)"
module: PF11
year: 11
lesson: "2.2"
script: script.md
---

# Supplementary Materials

Code listings, NESA-style pseudocode and completed trace tables for this episode. Nothing
here is spoken in the audio — it's the read-along reference. The narration points at each by
label only. The grade scale (D at 50 and above) is kept consistent with episode 2.1.

### Listing 1 — The grade-calculator algorithm under analysis (NESA pseudocode)
```text
BEGIN CalculateGrade
    INPUT studentName        // string, from the user
    INPUT assignment1        // number 0–100, from the user
    INPUT assignment2        // number 0–100, from the user
    INPUT finalExam          // number 0–100, from the user

    average ← (assignment1 + assignment2 + finalExam) / 3

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

    OUTPUT studentName + " earned grade: " + grade   // string, to the screen
    OUTPUT "Average score: " + average               // number, to the screen
END CalculateGrade
```

### Listing 2 — The same algorithm as runnable Python (used to verify the desk checks)
```python
def calculate_grade(name, assignment1, assignment2, final_exam):
    average = (assignment1 + assignment2 + final_exam) / 3
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
    return name, average, grade


# Alice: 255 / 3 = 85.0 -> B
assert calculate_grade("Alice", 85, 92, 78) == ("Alice", 85.0, "B")
# Boundary: exactly 80.0 -> B (because the test is >=, not >)
assert calculate_grade("Bob", 80, 80, 80) == ("Bob", 80.0, "B")
# Fail path: 145 / 3 = 48.33 -> F
name, avg, grade = calculate_grade("Cara", 45, 52, 48)
assert grade == "F" and round(avg, 2) == 48.33
print("All calculate_grade assertions passed.")
```

### Listing 3 — Completed desk check (trace table) for name=Alice, 85, 92, 78
```text
Step  Action                       studentName  assignment1  assignment2  finalExam  average  grade  Output
----  ---------------------------  -----------  -----------  -----------  ---------  -------  -----  ------------------------
 1    INPUT studentName            "Alice"      -            -            -          -        -      -
 2    INPUT assignment1            "Alice"      85           -            -          -        -      -
 3    INPUT assignment2            "Alice"      85           92           -          -        -      -
 4    INPUT finalExam              "Alice"      85           92           78         -        -      -
 5    average ← 255 / 3            "Alice"      85           92           78         85.0     -      -
 6    85.0 ≥ 90 ? False            "Alice"      85           92           78         85.0     -      -
 7    85.0 ≥ 80 ? True             "Alice"      85           92           78         85.0     "B"    -
 8    OUTPUT grade message         "Alice"      85           92           78         85.0     "B"    Alice earned grade: B
 9    OUTPUT average               "Alice"      85           92           78         85.0     "B"    Average score: 85.0

Expected outputs:  "Alice earned grade: B"  and  "Average score: 85.0"
```

### Listing 4 — Completed desk check (trace table) for the boundary case name=Bob, 80, 80, 80
```text
Step  Action                       studentName  assignment1  assignment2  finalExam  average  grade  Output
----  ---------------------------  -----------  -----------  -----------  ---------  -------  -----  -------------------
 1    INPUT name and scores        "Bob"        80           80           80         -        -      -
 2    average ← 240 / 3            "Bob"        80           80           80         80.0     -      -
 3    80.0 ≥ 90 ? False            "Bob"        80           80           80         80.0     -      -
 4    80.0 ≥ 80 ? True             "Bob"        80           80           80         80.0     "B"    -
 5    OUTPUT grade message         "Bob"        80           80           80         80.0     "B"    Bob earned grade: B
 6    OUTPUT average               "Bob"        80           80           80         80.0     "B"    Average score: 80.0

Boundary note: 80.0 lands in "B", NOT "C", because the test is "≥ 80" (greater than OR EQUAL).
Had the algorithm used "> 80", an average of exactly 80 would wrongly fall through to "C".
```

### Listing 5 — Peer-checking checklist (apply to someone else's algorithm)
```text
PEER-CHECK CHECKLIST
[ ] Purpose       Is the algorithm's goal clear, and stated in one sentence?
[ ] Inputs        Are all necessary inputs identified (with type and source)?
[ ] Outputs       Do the outputs actually solve the intended problem?
[ ] Logic         Does the control flow make sense (sequence/selection/iteration)?
[ ] Completeness  Are all cases handled (every selection branch reachable)?
[ ] Edge cases    What happens with boundary, empty, or abnormal input?
[ ] Efficiency    Could this be done more simply?

This is just I-O-P (Inputs, Outputs, Purpose) + logic + edge cases, applied to another
person's work — the same analysis skills, used as a reviewer with fresh eyes.
```
