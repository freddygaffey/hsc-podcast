---
title: "Supplementary Materials — Subprograms: Procedures and Functions"
module: PF11
year: 11
lesson: "2.5"
script: script.md
---

# Supplementary Materials

NESA-style pseudocode and runnable code for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration points at each by label only. The grade
scale (D at 50 and above) is kept consistent with episodes 2.1 and 2.2.

### Listing 1 — A function vs a procedure, side by side (NESA pseudocode)
```text
// FUNCTION: computes a value and RETURNS it (used for its result)
BEGIN FUNCTION CalculateAverage(scores)
    total ← 0
    FOR EACH score IN scores
        total ← total + score
    NEXT score
    RETURN total / length(scores)        // hands a value back to the caller
END FUNCTION

// PROCEDURE: performs an action, returns NOTHING (used for its effect)
BEGIN PROCEDURE DisplayStudentReport(name, average, grade)
    OUTPUT "Student: " + name
    OUTPUT "Average: " + average
    OUTPUT "Grade:   " + grade
    // no RETURN — the point is the on-screen effect
END PROCEDURE
```

### Listing 2 — The Grade Calculator decomposed, each subprogram tagged P/F (NESA pseudocode)
```text
BEGIN StudentGradeCalculator
    students ← LoadStudentData()                              // FUNCTION (returns data)
    FOR EACH student IN students
        average     ← CalculateStudentAverage(student.scores) // FUNCTION (returns a number)
        letterGrade ← DetermineLetterGrade(average)           // FUNCTION (returns a letter)
        gpa         ← ConvertGradeToGPA(letterGrade)          // FUNCTION (returns a number)
        DisplayStudentReport(student.name, average, letterGrade, gpa)  // PROCEDURE (effect only)
    NEXT student
    classAverage ← CalculateClassAverage(students)           // FUNCTION (returns a number)
    DisplayClassSummary(students, classAverage)              // PROCEDURE (effect only)
    SaveResultsToFile(students, "grade_report.txt")          // PROCEDURE (effect only)
END StudentGradeCalculator

BEGIN FUNCTION DetermineLetterGrade(average)
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

// Tell: a returned value that is ASSIGNED/USED => FUNCTION.
//       a call standing alone for its EFFECT     => PROCEDURE.
```

### Listing 3 — Parameter directions: IN, OUT, IN-OUT (NESA pseudocode)
```text
// IN: read-only input (the normal case)
BEGIN FUNCTION CalculateCircleArea(IN radius)
    RETURN 3.14159 * radius * radius
END FUNCTION

// OUT: the subprogram writes results back through the parameter
// (how a PROCEDURE returns more than one value, having no RETURN)
BEGIN PROCEDURE GetStudentInfo(OUT studentName, OUT studentID)
    OUTPUT "Enter student name:"
    INPUT studentName
    OUTPUT "Enter student ID:"
    INPUT studentID
END PROCEDURE

// IN-OUT: data comes in, is modified, and goes back out
BEGIN PROCEDURE ApplyDeposit(IN_OUT account, IN amount)
    account.balance ← account.balance + amount
END PROCEDURE
```

### Listing 4 — The print-vs-return trap (Python, runnable)
```python
# TRAP: a "function" that PRINTS instead of RETURNING hands the caller nothing.
def average_bad(scores):
    print(sum(scores) / len(scores))   # shows the number, but returns None


# CORRECT: return the value so the caller can assign and reuse it.
def average_good(scores):
    return sum(scores) / len(scores)


assert average_bad([80, 90]) is None     # caller receives None -> later maths breaks
assert average_good([80, 90]) == 85.0    # caller receives the value -> usable
print("All print-vs-return assertions passed.")
```

### Listing 5 — The Grade Calculator subprograms as runnable Python (functions + a procedure)
```python
def calculate_average(scores):                 # FUNCTION: returns a number
    return sum(scores) / len(scores)


def determine_letter_grade(average):           # FUNCTION: returns a letter
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


def convert_grade_to_gpa(letter):              # FUNCTION: returns a number
    return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}[letter]


def display_report(name, average, letter, gpa):  # PROCEDURE: performs an action, returns None
    print(name + ": average " + str(average) + ", grade " + letter + ", GPA " + str(gpa))


assert calculate_average([85, 92, 78]) == 85.0
assert determine_letter_grade(85.0) == "B"
assert convert_grade_to_gpa("B") == 3.0
assert display_report("Alice", 85.0, "B", 3.0) is None   # a procedure returns nothing
print("All grade-calculator assertions passed.")
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| GPA | Grade Point Average | A numeric summary of academic grades (used as example data) |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
