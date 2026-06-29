---
title: "Supplementary Materials — Standard Data Types"
module: PF11
year: 11
lesson: "3.2"
script: script.md
---

# Supplementary Materials

Runnable Python demonstrating the standard data types, the char-as-number and single-vs-double
precision points, and the two marquee traps. Nothing here is spoken in the audio — it's the
read-along reference. The narration points at each by label only. (No NESA pseudocode this
episode — choosing data types is not an algorithm.)

### Listing 1 — A char is a number underneath (links to number systems, 3.1)
```python
# Every character has a numeric code (ASCII / Unicode code point):
assert ord("A") == 65                        # 'A' -> 65
assert chr(65) == "A"                        # 65 -> 'A'
assert ord("a") == 97                        # 'a' -> 97

# ...and that code is just binary (the two's-complement / number-systems episode):
assert bin(ord("A")) == "0b1000001"          # 65 = 1000001 in binary
print("Char-as-number demonstrated.")
```

### Listing 2 — Single-precision vs double-precision floating point (Python, runnable)
```python
import struct


def to_single(x):
    # round-trip x through a 32-bit SINGLE-precision float
    return struct.unpack("f", struct.pack("f", x))[0]


# Python's native float is 64-bit DOUBLE precision — yet still only approximate:
assert (0.1 + 0.2) != 0.3

# A 32-bit SINGLE-precision float is LESS precise (~7 significant digits):
assert to_single(0.1) != 0.1                 # narrower format -> extra error
assert round(to_single(0.1), 7) == 0.1       # accurate to ~7 digits, not beyond

# real = the concept; floating point = the storage method; single (32-bit) vs double (64-bit)
# = how many bits, and therefore how much precision.
print("Single vs double precision demonstrated.")
```

### Listing 3 — Trap 1: a number stored as a string concatenates, it does not add
```python
age_text = "17"                              # the CHARACTERS '1' and '7', not the number 17

assert age_text + "1" == "171"               # '+' on strings CONCATENATES -> "171"
assert int(age_text) + 1 == 18               # convert to INTEGER first -> real addition

# This is why age/quantity/score must be stored as integers, not text.
print("Age-as-string trap demonstrated.")
```

### Listing 4 — Trap 2: never store money in a float (it drifts); use whole cents
```python
# Floats are APPROXIMATE — decimal fractions can't be stored exactly in binary:
assert (0.1 + 0.2) != 0.3                    # the classic: 0.30000000000000004
assert round(0.1 + 0.2, 2) == 0.3            # rounding only hides it for display

# FIX: store money as an INTEGER number of cents — all arithmetic is exact.
price_cents = 1999                           # $19.99
tax_cents   = price_cents * 10 // 100        # 10% tax = 199 cents (integer division)
total_cents = price_cents + tax_cents
assert total_cents == 2198                   # $21.98 — exact, no drift
print("Money-as-float trap demonstrated; cents are exact.")
```

### Listing 5 — A student record with appropriate types (Python, runnable)
```python
from datetime import date

# Field            value                       type chosen + why
student_id    = "S10234"                     # STRING  — a non-arithmetic label (keep leading chars)
full_name     = "Sarah Chen"                 # STRING  — text
date_of_birth = date(2006, 3, 15)            # DATE    — enables date arithmetic (compute age)
grade_average = 78.5                          # REAL/FLOAT — has a fractional part
is_enrolled   = True                         # BOOLEAN — two-state status
initial       = "S"                          # CHAR    — a single character

assert type(student_id) is str
assert type(date_of_birth) is date           # a real date type, not a string or an int year
assert type(grade_average) is float
assert type(is_enrolled) is bool
assert len(initial) == 1                     # a "char" = a single character
print("Student record types OK.")
```
