---
title: "Supplementary Materials — From Pseudocode to Python Functions"
module: PF11
year: 11
lesson: "4.3"
script: script.md
---

# Supplementary Materials

The pseudocode-to-Python function mapping, plus runnable examples of parameters, single
responsibility, and the print-vs-return trap. Nothing here is spoken in the audio — it's the
read-along reference. The narration points at each by label only.

### Listing 1 — Function anatomy and the pseudocode → Python mapping
```text
PSEUDOCODE                              PYTHON
------------------------------------    --------------------------------------
FUNCTION name(params)                   def name(params):
    ...                                     """docstring — what it does"""
    RETURN value                            ...
END FUNCTION                                return value          # END FUNCTION -> indentation

PROCEDURE name(params)                   def name(params):
    ...                                     ...                   # no return -> returns None
END PROCEDURE

ANATOMY of a Python function:
  def            keyword that starts the definition
  name           descriptive snake_case name
  (params)       inputs — zero or more parameters
  """docstring"""  documentation: what the function does (its contract)
  body           indented code that does the work
  return         sends a value back to the caller (omit it -> the function returns None)
```

### Listing 2 — Translating pseudocode functions to Python (runnable)
```python
def calculate_area(length, width):
    """Return the area of a rectangle."""
    return length * width


def find_maximum(a, b, c):
    """Return the largest of three numbers."""
    max_value = a
    if b > max_value:
        max_value = b
    if c > max_value:
        max_value = c
    return max_value


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


assert calculate_area(4, 5) == 20
assert find_maximum(45, 89, 67) == 89
assert celsius_to_fahrenheit(0) == 32.0
assert celsius_to_fahrenheit(100) == 212.0
print("Function-translation assertions passed.")
```

### Listing 3 — Parameter passing: Positional, Default, Keyword (runnable)
```python
def format_name(first, last):                 # POSITIONAL: order matters
    return first + " " + last


assert format_name("Alice", "Smith") == "Alice Smith"
assert format_name("Smith", "Alice") == "Smith Alice"   # swapped -> wrong, but no error


def greet(name, greeting="Hello"):            # DEFAULT: greeting is optional
    return greeting + ", " + name + "!"


assert greet("Alice") == "Hello, Alice!"
assert greet("Bob", "Good morning") == "Good morning, Bob!"


def create_student(name, age, grade):
    return {"name": name, "age": age, "grade": grade}


# KEYWORD arguments — named at the call site, so order doesn't matter:
assert create_student(grade=87, name="Bob", age=17) == {"name": "Bob", "age": 17, "grade": 87}
print("Parameter-passing assertions passed.")
```

### Listing 4 — One job per function (single responsibility) (runnable)
```python
def calculate_average(s1, s2, s3):
    """Return the mean of three scores."""
    return (s1 + s2 + s3) / 3


def determine_letter_grade(average):
    """Return the letter grade for an average (A>=90, B>=80, C>=70, D>=50, else F)."""
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


def format_report(name, average, grade):
    """Return a one-line formatted report string."""
    return f"{name}: average {average:.1f}, grade {grade}"


def process_student(name, t1, t2, t3):
    """Coordinator: each step delegated to a single-responsibility function."""
    avg = calculate_average(t1, t2, t3)
    grade = determine_letter_grade(avg)
    return format_report(name, avg, grade)


assert calculate_average(85, 92, 78) == 85.0
assert determine_letter_grade(85.0) == "B"
assert process_student("Alice", 85, 92, 78) == "Alice: average 85.0, grade B"
print("Single-responsibility assertions passed.")
```

### Listing 5 — The print-vs-return trap (runnable)
```python
# TRAP: a "function" that PRINTS returns None — the caller gets nothing back.
def average_bad(a, b, c):
    print((a + b + c) / 3)        # shows the number, but returns None


# CORRECT: RETURN the value so the caller can assign and reuse it.
def average_good(a, b, c):
    return (a + b + c) / 3


assert average_bad(80, 90, 100) is None     # caller receives None -> later code breaks
assert average_good(80, 90, 100) == 90.0    # caller receives the value -> usable
print("Print-vs-return assertions passed.")
```
