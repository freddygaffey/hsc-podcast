---
title: "Supplementary Materials — Software Development Steps"
module: PF11
year: 11
lesson: "1.1"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration points at these by label only.

### Listing 1 — Grade Calculator: the worked example, built across the lifecycle
```python
# The Grade Calculator from the episode: validate, calculate, format.
# Design step → three single-responsibility functions (separation of concerns).
# Development step → implement each one. Integration → wire them together.

def validate_grade(grade):
    """Validate a single grade input (the specification: numeric, 0–100)."""
    if not isinstance(grade, (int, float)):
        raise TypeError(f"Grade must be numeric, got {type(grade).__name__}")
    if grade < 0 or grade > 100:
        raise ValueError(f"Grade must be between 0 and 100, got {grade}")
    return float(grade)


def calculate_average(grade1, grade2, grade3):
    """Validate all three grades, then return the mean to one decimal place."""
    grades = [validate_grade(grade1), validate_grade(grade2), validate_grade(grade3)]
    return round(sum(grades) / len(grades), 1)


def format_result(average_value):
    """Format the average for display (the user-facing output)."""
    return f"Average: {average_value}"


# Integration: the three pieces run as one flow — validate → calculate → format.
if __name__ == "__main__":
    print(format_result(calculate_average(80, 72, 90)))   # Average: 80.7
    print(format_result(calculate_average(100, 0, 50)))   # Average: 50.0
```

### Listing 2 — The same algorithm in NESA-style pseudocode
```text
BEGIN GradeCalculator

    FUNCTION ValidateGrade(grade)
        IF grade IS NOT numeric THEN
            RAISE error "Grade must be numeric"
        ENDIF
        IF grade < 0 OR grade > 100 THEN
            RAISE error "Grade must be between 0 and 100"
        ENDIF
        RETURN grade AS real
    END FUNCTION

    FUNCTION CalculateAverage(grade1, grade2, grade3)
        g1 ← ValidateGrade(grade1)
        g2 ← ValidateGrade(grade2)
        g3 ← ValidateGrade(grade3)
        total ← g1 + g2 + g3
        average ← total / 3
        RETURN ROUND(average, 1)
    END FUNCTION

    FUNCTION FormatResult(averageValue)
        RETURN "Average: " + averageValue
    END FUNCTION

    result ← CalculateAverage(80, 72, 90)
    DISPLAY FormatResult(result)

END GradeCalculator
```

### Listing 3 — The testing-and-debugging step: typical, boundary, and faulty data
```python
# Tests written straight from the specification. This IS the "testing and
# debugging" step from the episode: typical, boundary, and faulty/abnormal data.
# The two functions under test are the same ones built in Listing 1, repeated
# here so this listing runs on its own.

def validate_grade(grade):
    if not isinstance(grade, (int, float)):
        raise TypeError(f"Grade must be numeric, got {type(grade).__name__}")
    if grade < 0 or grade > 100:
        raise ValueError(f"Grade must be between 0 and 100, got {grade}")
    return float(grade)


def calculate_average(grade1, grade2, grade3):
    grades = [validate_grade(grade1), validate_grade(grade2), validate_grade(grade3)]
    return round(sum(grades) / len(grades), 1)


def run_tests():
    # Typical data — an ordinary, valid case.
    assert calculate_average(80, 72, 90) == 80.7

    # Boundary data — the edges of the valid 0–100 range, where bugs hide.
    assert calculate_average(0, 0, 0) == 0.0
    assert calculate_average(100, 100, 100) == 100.0
    assert validate_grade(0) == 0.0
    assert validate_grade(100) == 100.0

    # Faulty / abnormal data — must be rejected, not silently accepted.
    for bad in (-5, 150):
        try:
            validate_grade(bad)
            assert False, f"{bad} should have been rejected"
        except ValueError:
            pass  # correct: out-of-range value raised ValueError

    try:
        validate_grade("ninety")            # wrong type, not a number
        assert False, "non-numeric input should have been rejected"
    except TypeError:
        pass  # correct: non-numeric input raised TypeError

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
```
