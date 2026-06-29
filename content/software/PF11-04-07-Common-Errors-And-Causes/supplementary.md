---
title: "Supplementary Materials — Common Errors and Their Causes"
module: PF11
year: 11
lesson: "4.7"
script: script.md
---

# Supplementary Materials

The three error types, syntax examples, runtime errors handled, a silent logic error, and a
classify-the-error practice table. Nothing here is spoken in the audio — it's the read-along
reference. The narration points at each by label only. (Syntax-error examples can't be run —
they're shown broken-vs-fixed; runtime and logic examples are runnable.)

### Listing 1 — The three error types: S-L-R (reference)
```text
S-L-R  =  Syntax, Logic, Runtime

  SYNTAX   breaks the grammar -> WON'T RUN at all. Python flags it BEFORE running,
           with a line number and a ^ caret pointing at the confusion.
           Causes: missing colon / bracket / quote; inconsistent indentation.
           Easiest to find — Python points at it.
  RUNTIME  valid code that CRASHES mid-run with an EXCEPTION + a traceback.
           Causes: ZeroDivisionError, IndexError, KeyError, TypeError, ValueError, NameError.
           Find it: read the LAST line of the traceback.  Fix: guard first, or try/except.
  LOGIC    runs to completion, NO crash, but the WRONG ANSWER — SILENT.
           Causes: off-by-one; wrong operator (> vs >=); wrong formula/condition.
           Hardest to find (no message) -> needs TESTING + desk checking.

One-liner:  "syntax won't run, runtime crashes, logic is silently wrong."
TRAP: code that RUNS is NOT proof it's CORRECT (a logic error raises nothing).
```

### Listing 2 — Syntax errors: broken vs fixed (illustrative — these won't run)
```text
BROKEN                         FIXED                       LIKELY CAUSE
print "Hello"                  print("Hello")              missing parentheses
print("Hello"                  print("Hello")              missing closing bracket
if x > 5                       if x > 5:                   missing colon
message = "Hello'              message = "Hello"           mismatched quotes
def f(n):                      def f(n):                   body must be indented
total = sum(n)                     total = sum(n)          (IndentationError otherwise)

Reading the message:
  File "prog.py", line 2
      if x > 5
              ^
  SyntaxError: invalid syntax
  -> go to the line, look at the ^, add the missing colon.
```

### Listing 3 — Runtime errors (exceptions): guard first, or try/except (Python, runnable)
```python
# Each is valid code that would CRASH on the bad case; here we prevent / catch it.

def average(numbers):
    if not numbers:                 # GUARD against ZeroDivisionError (empty -> len 0)
        return None
    return sum(numbers) / len(numbers)


assert average([]) is None          # would otherwise raise ZeroDivisionError
assert average([2, 4]) == 3.0


def safe_get(items, i):
    if 0 <= i < len(items):         # GUARD against IndexError
        return items[i]
    return None


assert safe_get([1, 2, 3], 5) is None
assert safe_get([1, 2, 3], 1) == 2

grades = {"Alice": 92}
assert grades.get("David") is None  # .get avoids KeyError
assert grades.get("Alice") == 92


def divide_caught(a, b):
    try:
        return a / b                # try/except CATCHES the exception
    except ZeroDivisionError:
        return None


assert divide_caught(10, 2) == 5.0
assert divide_caught(10, 0) is None
print("Runtime-error handling assertions passed.")
```

### Listing 4 — A logic error: runs fine, wrong answer, no crash (Python, runnable)
```python
def average_buggy(numbers):
    return sum(numbers) / (len(numbers) - 1)   # BUG: off-by-one in the divisor


# It runs with NO error or crash — but the result is WRONG:
assert average_buggy([2, 4, 6]) == 6.0    # WRONG: should be 4.0 (12/3); got 12/2 = 6.0
# No exception was raised. The bug is SILENT — only a test reveals it.

def average_fixed(numbers):
    return sum(numbers) / len(numbers)


assert average_fixed([2, 4, 6]) == 4.0    # correct
print("Logic-error demonstration passed (the bug runs silently).")
```

### Listing 5 — Classify the error (example -> type -> likely cause)
```text
EXAMPLE                                    TYPE      LIKELY CAUSE
print("hi"                                 SYNTAX    missing closing parenthesis
if score >= 50          (no colon)         SYNTAX    missing colon
total / len(items)      on empty items     RUNTIME   ZeroDivisionError (len is 0)
my_list[len(my_list)]                      RUNTIME   IndexError (off the end by one)
scores["Dave"]          key absent         RUNTIME   KeyError (key not in dict)
"17" + 1                                   RUNTIME   TypeError (str + int)
int("abc")                                 RUNTIME   ValueError (not a number)
using a never-assigned variable            RUNTIME   NameError
range(n)  where range(1, n+1) was meant    LOGIC     off-by-one -> wrong result, no crash
using >  where >= was meant                LOGIC     boundary handled wrong, silently
```
