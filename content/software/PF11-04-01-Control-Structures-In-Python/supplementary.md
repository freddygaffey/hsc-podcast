---
title: "Supplementary Materials — Control Structures in Python"
module: PF11
year: 11
lesson: "4.1"
script: script.md
---

# Supplementary Materials

The pseudocode-to-Python mapping, plus runnable Python for the worked examples and the range
function. Nothing here is spoken in the audio — it's the read-along reference. The narration
points at each by label only.

### Listing 1 — NESA pseudocode ↔ Python mapping reference
```text
PSEUDOCODE (NESA)                       PYTHON
-------------------------------------   ----------------------------------------
BEGIN ... END                           (no keywords; indentation marks blocks)
SET x = value   /   x ← value           x = value
INPUT x                                  x = input("...")          # always a STRING
                                         x = int(input("..."))     # convert for a number
OUTPUT "msg"  /  OUTPUT x                print("msg")  /  print(x)
IF cond THEN ... ENDIF                   if cond:
                                             ...
IF a THEN ... ELSE IF b THEN ...         if a:
   ... ELSE ... ENDIF                    elif b:
                                         else:
WHILE cond DO ... ENDWHILE               while cond:
                                             ...
FOR i = a TO b ... NEXT i                for i in range(a, b + 1):   # +1: range stops early
REPEAT ... UNTIL cond                    while True:
                                             ...
                                             if cond:
                                                 break
AND  /  OR  /  NOT                        and  /  or  /  not

KEY DIFFERENCE: pseudocode CLOSES blocks (ENDIF / ENDWHILE / NEXT). Python has NO closers —
the ':' opens a block and INDENTATION defines it. The indent IS the block.
```

### Listing 2 — Grade calculator: sequence + selection (Python, runnable)
```python
def calculate_average(assignment1, assignment2, test):
    return (assignment1 + assignment2 + test) / 3          # sequence


def get_letter_grade(score):                                # selection (if/elif/else)
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


assert calculate_average(85, 92, 78) == 85.0
assert get_letter_grade(85) == "B"
assert get_letter_grade(50) == "D"     # boundary: 50 -> D (>= 50)
assert get_letter_grade(49) == "F"
print("Grade-calculator assertions passed.")
```

### Listing 3 — The range function in every form (Python, runnable)
```python
assert list(range(1, 6)) == [1, 2, 3, 4, 5]          # FOR i = 1 TO 5  (stop 6 -> includes 5)
assert list(range(5)) == [0, 1, 2, 3, 4]             # one arg: 0 up to 4
assert list(range(3, 8)) == [3, 4, 5, 6, 7]          # start, stop
assert list(range(0, 11, 2)) == [0, 2, 4, 6, 8, 10]  # step 2 (stop 11 -> includes 10)
assert list(range(5, 0, -1)) == [5, 4, 3, 2, 1]      # negative step: countdown

# RULE: range(a, b) yields a .. b-1 — it STOPS ONE BEFORE the stop value.
print("Range assertions passed.")
```

### Listing 4 — Number-guessing game: pseudocode converted to Python (runnable)
```python
# Pseudocode -> Python: WHILE + if/elif/else; the testable core is split out as a function.
def check_guess(guess, secret):
    if guess < secret:
        return "Too low!"
    elif guess > secret:
        return "Too high!"
    else:
        return "Correct!"


def play(secret, guesses):
    attempts = 0
    for guess in guesses:                  # stands in for the WHILE loop, over fixed input
        attempts += 1
        if check_guess(guess, secret) == "Correct!":
            return attempts
    return None                            # never guessed


assert check_guess(4, 7) == "Too low!"
assert check_guess(9, 7) == "Too high!"
assert check_guess(7, 7) == "Correct!"
assert play(7, [3, 9, 7]) == 3            # won on the 3rd attempt
print("Number-guessing assertions passed.")
```

### Listing 5 — The infinite-loop trap and its fix (Python, runnable)
```python
# BUG (do not run): the counter never changes, so the condition stays true forever.
#   i = 5
#   while i > 0:
#       print(i)          # i is never decreased -> infinite loop
#
# A related bug: putting "i -= 1" at the WRONG indentation (outside the loop) does the same.

# FIX: change the variable the condition depends on, inside the loop body, each pass.
def countdown(start):
    result = []
    i = start
    while i > 0:
        result.append(i)
        i -= 1            # progress toward the exit condition (and correctly indented INSIDE)
    return result


assert countdown(5) == [5, 4, 3, 2, 1]
assert countdown(0) == []     # condition false at once -> loop body runs zero times
print("Countdown assertions passed.")
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
