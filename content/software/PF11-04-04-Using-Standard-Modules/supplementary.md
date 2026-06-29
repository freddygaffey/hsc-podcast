---
title: "Supplementary Materials — Using Standard Modules"
module: PF11
year: 11
lesson: "4.4"
script: script.md
---

# Supplementary Materials

Import styles, the math and random modules, and the purity issue. Random examples are SEEDED
so the assertions are reproducible. Nothing here is spoken in the audio — it's the read-along
reference. The narration points at each by label only.

### Listing 1 — Three import styles (and why to avoid the star)
```python
# STYLE 1 — import the module; call with its prefix (PREFERRED: clear origin)
import math
print(math.sqrt(16))            # use as math.<name>

# STYLE 2 — import a specific name; call it directly
from math import sqrt
print(sqrt(16))                 # no prefix needed

# STYLE 3 — import EVERYTHING with a star (AVOID)
from math import *              # dumps every name into your namespace
print(sqrt(16))
# Problem: NAMESPACE POLLUTION — you can't tell where a name came from, and two
# modules defining the same name (e.g. two different 'sqrt') silently clash.
# Rule: import the module, or import the name — never import the star.
```

### Listing 2 — The math module in real formulas (Python, runnable)
```python
import math


def circle_area(radius):
    return math.pi * math.pow(radius, 2)


def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def compound_interest(principal, rate_pct, years, times_per_year):
    # A = P * (1 + r/n) ^ (n*t)
    return principal * math.pow(1 + (rate_pct / 100) / times_per_year, times_per_year * years)


assert distance(0, 0, 3, 4) == 5.0
assert round(circle_area(5), 2) == 78.54
assert round(compound_interest(1000, 5, 3, 12), 2) == 1161.47
assert math.floor(4.7) == 4 and math.ceil(4.7) == 5 and math.trunc(4.7) == 4
print("Math-module assertions passed.")
```

### Listing 3 — The random module (SEEDED so results are reproducible) (Python, runnable)
```python
import random

random.seed(42)
assert random.randint(1, 6) == 6                 # randint INCLUDES both ends (a fair die)

random.seed(42)
assert [random.randint(1, 6) for _ in range(3)] == [6, 1, 1]

random.seed(7)
assert random.choice(["red", "green", "blue", "yellow"]) == "blue"   # pick one

random.seed(1)
deck = [1, 2, 3, 4, 5]
random.shuffle(deck)                              # reorder IN PLACE
assert deck == [3, 4, 5, 1, 2]

random.seed(123)
assert random.sample([10, 20, 30, 40, 50], 3) == [10, 30, 50]   # distinct, no repeats

# NOTE: randint(1, 6) can return 6; range(1, 6)/randrange(1, 6) stop at 5.
print("Random-module assertions passed.")
```

### Listing 4 — Pure vs impure: making random code testable (Python, runnable)
```python
import random


# IMPURE: randomness is hidden inside -> same call, different result -> hard to test
def roll_impure():
    return random.randint(1, 6)


# TESTABLE option A — SEED it so the sequence is reproducible:
random.seed(42)
assert roll_impure() == 6


# TESTABLE option B (cleaner) — INJECT the randomness; the core stays a PURE function:
def apply_roll(position, roll):
    return position + roll


assert apply_roll(10, 6) == 16        # pure: same inputs -> same output, every time
assert apply_roll(10, 6) == 16
print("Purity assertions passed.")
```

### Listing 5 — A password generator (and why random is the WRONG tool for real passwords)
```python
import random


def make_password(length, seed=None):
    if seed is not None:
        random.seed(seed)                         # seed -> reproducible (for testing only)
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))


assert make_password(8, seed=99) == "zymMlopi"    # seeded -> deterministic, so testable
assert len(make_password(12, seed=1)) == 12
print("Password-generator assertions passed.")

# SECURITY: the `random` module is a PRNG — predictable, NOT cryptographically secure.
# For real passwords / tokens / keys, use the `secrets` module instead, e.g.:
#     import secrets
#     secrets.choice(chars)        # cryptographically secure
```
