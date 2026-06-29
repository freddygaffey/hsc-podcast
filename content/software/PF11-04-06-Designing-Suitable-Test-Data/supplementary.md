---
title: "Supplementary Materials — Designing Suitable Test Data"
module: PF11
year: 11
lesson: "4.6"
script: script.md
---

# Supplementary Materials

The test-data types, and runnable demonstrations of normal-isn't-enough, boundary values,
path coverage / equivalence partitioning, and faulty-and-abnormal data. Nothing here is
spoken in the audio — it's the read-along reference. The narration points at each by label
only. The grade scale (D at 50 and above) is kept consistent with episodes 2.1, 2.2 and 4.x.

### Listing 1 — Why normal data is not enough (Python, runnable)
```python
def calculate_discount(price, percent):
    return price - price * (percent / 100)


# NORMAL data passes — looks fine:
assert calculate_discount(100, 10) == 90.0
assert calculate_discount(50, 20) == 40.0

# ...but EDGE / FAULTY data reveals bugs (there is no validation):
assert calculate_discount(100, 150) == -50.0   # 150% off -> the shop PAYS the customer
assert calculate_discount(-10, 10) == -9.0      # a negative price is accepted


# FIXED: validate the inputs, reject the impossible
def calculate_discount_safe(price, percent):
    if price < 0 or not (0 <= percent <= 100):
        return None
    return price - price * (percent / 100)


assert calculate_discount_safe(100, 10) == 90.0
assert calculate_discount_safe(100, 150) is None   # rejected
assert calculate_discount_safe(-10, 10) is None    # rejected
print("Normal-isn't-enough demonstrated.")
```

### Listing 2 — Types of test data (B-P-F) and equivalence partitioning (reference)
```text
NORMAL / typical    the common, expected inputs — necessary but NOT enough on its own.

THE SYLLABUS TRIO  (B-P-F):
  BOUNDARY values   the edge of a range — the value ON a cut-off and JUST EITHER SIDE
                    (e.g. 49 / 50 at a "pass = 50" line; 0 and 100; -1 and 101 just outside).
                    Boundaries are where OFF-BY-ONE bugs live.
  PATH COVERAGE     data that exercises EVERY branch/path: each if / elif / else, and the
                    loop running 0, 1, and many times. A branch never run is never tested.
  FAULTY / abnormal  invalid input — wrong type, out of range, empty, negative, garbage —
                     to check the program REJECTS it gracefully (validates; no crash).

EQUIVALENCE PARTITIONING — group inputs that behave the same; test ONE representative per
  group + the BOUNDARIES between groups. Cuts the test count without losing coverage.

EVERY test = compare the ACTUAL output to the EXPECTED output.
```

### Listing 3 — Boundary values for a grade function (Python, runnable)
```python
def grade_assignment(score):
    if score < 0 or score > 100:
        return "Invalid"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


# BOUNDARY test data: each cut-off, and the value just either side
assert grade_assignment(49) == "F"        # just below the pass mark
assert grade_assignment(50) == "D"        # ON the pass-mark boundary
assert grade_assignment(69) == "D"        # top of D
assert grade_assignment(70) == "C"        # bottom of C
assert grade_assignment(89) == "B"
assert grade_assignment(90) == "A"        # bottom of A
assert grade_assignment(0) == "F"         # lower limit
assert grade_assignment(100) == "A"       # upper limit
assert grade_assignment(-1) == "Invalid"  # just below the valid range
assert grade_assignment(101) == "Invalid" # just above the valid range
print("Boundary-value assertions passed.")
```

### Listing 4 — Path coverage and equivalence partitioning (Python, runnable)
```python
def classify_number(n):
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"


# PATH COVERAGE: one test per branch -> all three paths executed
assert classify_number(-5) == "negative"   # branch 1
assert classify_number(0) == "zero"        # branch 2
assert classify_number(7) == "positive"    # branch 3


def categorize_age(age):
    if age < 0:
        return "Invalid"
    elif age < 13:
        return "Child"
    elif age < 20:
        return "Teenager"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"


# EQUIVALENCE PARTITIONING: one representative per partition...
assert categorize_age(7) == "Child"
assert categorize_age(16) == "Teenager"
assert categorize_age(35) == "Adult"
assert categorize_age(70) == "Senior"
# ...plus the BOUNDARIES between partitions:
assert categorize_age(12) == "Child"       # 12/13 edge
assert categorize_age(13) == "Teenager"
assert categorize_age(19) == "Teenager"    # 19/20 edge
assert categorize_age(20) == "Adult"
print("Path-coverage and partitioning assertions passed.")
```

### Listing 5 — Faulty and abnormal data, handled gracefully (Python, runnable)
```python
def parse_age(text):
    if not isinstance(text, str):
        return None                  # wrong type
    if not text.isdigit():
        return None                  # empty, non-numeric, negative, decimal, spaces
    age = int(text)
    if age > 130:
        return None                  # out of range
    return age


assert parse_age("17") == 17         # normal
assert parse_age("") is None         # empty
assert parse_age("abc") is None      # non-numeric
assert parse_age("-5") is None       # isdigit() rejects the minus sign
assert parse_age("1.5") is None      # isdigit() rejects the decimal point
assert parse_age(17) is None         # wrong type (int, not str)
assert parse_age("200") is None      # out of range
print("Faulty/abnormal-data assertions passed.")
```
