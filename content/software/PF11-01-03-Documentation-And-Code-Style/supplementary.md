---
title: "Supplementary Materials — Documentation and Code Style"
module: PF11
year: 11
lesson: "1.3"
script: script.md
---

# Supplementary Materials

Read-along reference for this episode. Nothing here is spoken — the narration points at
each listing by label.

### Listing 1 — A complete README.md for the Grade Calculator project
```markdown
# Grade Calculator

A simple program that calculates the average of three test scores and assigns a letter grade.

## Requirements
- Python 3.8 or higher
- No external dependencies

## How to run
python main.py

## Usage
Enter three grades when prompted; the program prints your average and letter grade.

Example:
    Enter grade 1: 85
    Enter grade 2: 92
    Enter grade 3: 78
    Average: 85.0 (Grade: B)

## Files
- main.py — entry point and user interaction
- grade_calculator.py — the grade calculation functions
```

### Listing 2 — Docstrings: documenting each function's contract
```python
"""Grade Calculator — average and letter grade from three test scores.

Demonstrates the three documentation levels: this module docstring (project/file),
the function docstrings below (interface), and a why-comment (line).
"""

# Constants use UPPER_CASE (PEP 8): values that never change.
MAX_GRADE = 100
MIN_GRADE = 0


def get_valid_grade(prompt):
    """Ask the user for a grade until they enter a valid one.

    Args:
        prompt: text shown when asking for input.
    Returns:
        int: a grade in the range MIN_GRADE..MAX_GRADE.
    """
    while True:
        try:
            grade = int(input(prompt))
            if MIN_GRADE <= grade <= MAX_GRADE:
                return grade
            print(f"Grade must be between {MIN_GRADE} and {MAX_GRADE}")
        except ValueError:
            print("Please enter a whole number.")


def calculate_average(grade1, grade2, grade3):
    """Return the mean of three grades, rounded to one decimal place."""
    return round((grade1 + grade2 + grade3) / 3, 1)


def get_letter_grade(average):
    """Convert a numeric average to a letter grade (standard 10-point scale)."""
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


if __name__ == "__main__":
    # Self-test of the pure functions (get_valid_grade is interactive, so not tested here).
    assert calculate_average(85, 92, 78) == 85.0
    assert get_letter_grade(95) == "A"
    assert get_letter_grade(90) == "A"      # boundary
    assert get_letter_grade(80) == "B"      # boundary
    assert get_letter_grade(72) == "C"
    assert get_letter_grade(50) == "D"      # boundary
    assert get_letter_grade(49) == "F"
    print(f"Average: {calculate_average(85, 92, 78)} "
          f"(Grade: {get_letter_grade(calculate_average(85, 92, 78))})")
    print("All tests passed.")
```

### Listing 3 — Comments: explain *why*, not *what*
```python
grades = [85, 92, 78]

# BAD — the comment just restates the code; pure noise that rots out of sync.
total = 0                 # initialise total to zero
for grade in grades:      # loop through each grade
    total += grade        # add the grade to the total

# GOOD — let clean code show the "what"; comment only the non-obvious "why".
total = sum(grades)

# Grade boundaries follow the university standard (90+ = A), not an arbitrary choice.
THRESHOLD_A = 90
```

### Listing 4 — Readability refactor: same behaviour, different maintainability
```python
# BEFORE — works, but every name hides its meaning and nothing is documented.
def calc(x, y, z):
    a = x + y + z
    r = a / 3
    if r >= 90:
        g = "A"
    elif r >= 80:
        g = "B"
    else:
        g = "F"
    return r, g


# AFTER — identical logic; descriptive names, a docstring, and one why-comment.
def calculate_grade_average(test1_score, test2_score, test3_score):
    """Return (average, letter_grade) for three test scores."""
    total_points = test1_score + test2_score + test3_score
    average = total_points / 3
    # Boundaries follow the standard scale (90+ = A, 80+ = B).
    if average >= 90:
        letter_grade = "A"
    elif average >= 80:
        letter_grade = "B"
    else:
        letter_grade = "F"
    return average, letter_grade


if __name__ == "__main__":
    # The refactor changed names and docs, not behaviour — prove it.
    assert calc(85, 92, 78) == calculate_grade_average(85, 92, 78) == (85.0, "B")
    print("Refactor preserves behaviour.")
```
