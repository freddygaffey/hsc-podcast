---
title: "Supplementary Materials — Debugging Tools and Techniques"
module: PF11
year: 11
lesson: "4.5"
script: script.md
---

# Supplementary Materials

The three bug types, print debugging, the buggy-vs-fixed factorial, and an IDE-debugger
reference. Nothing here is spoken in the audio — it's the read-along reference. The narration
points at each by label only.

### Listing 1 — The three types of bug
```text
SYNTAX error   — breaks Python's rules; the program WON'T RUN at all.
                 e.g.  def f(x:            # missing ')'
                       print("hi"          # missing ')'

RUNTIME error  — runs, then CRASHES mid-execution with an exception.
                 e.g.  sum(nums) / len(nums)   when nums is []  -> ZeroDivisionError
                       my_list[10]             when the list has 3 items -> IndexError

LOGIC error    — runs fine, NO crash, but produces the WRONG ANSWER (silent).
                 e.g.  range(n) instead of range(1, n + 1) in a factorial.

Debugging tools help find ALL three — but they matter MOST for the silent logic error,
which produces no message and no crash. (Bug types covered in depth in 04-07.)
```

### Listing 2 — Debugging output statements (print) to trace a program (runnable)
```python
def find_maximum(numbers):
    print(f"DEBUG: starting with {numbers}")          # trace the input
    max_value = numbers[0]
    print(f"DEBUG: initial max = {max_value}")
    for i in range(1, len(numbers)):
        print(f"DEBUG: checking {numbers[i]} against {max_value}")
        if numbers[i] > max_value:
            max_value = numbers[i]
            print(f"DEBUG: new max = {max_value}")
    print(f"DEBUG: final max = {max_value}")
    return max_value


assert find_maximum([3, 7, 2, 9, 1]) == 9
print("find_maximum assertion passed.")
# (Remove DEBUG prints before shipping — they clutter output and leak information.)
```

### Listing 3 — The BUGGY factorial (a logic error), demonstrated (runnable)
```python
def factorial_buggy(n):
    result = 1
    for i in range(n):            # BUG: range(n) = 0, 1, ..., n-1  -> starts at 0
        result = result * i       # first multiply is by 0 -> result becomes 0 and stays 0
    return result


# The bug, demonstrated deterministically:
assert factorial_buggy(5) == 0    # WRONG — should be 120 (multiplied by 0 on pass 1)
assert factorial_buggy(1) == 0    # WRONG — should be 1
assert factorial_buggy(0) == 1    # accidentally correct (loop runs zero times)
print("Buggy factorial reproduced (returns 0 for positive n).")
```

### Listing 4 — The FIXED factorial (runnable)
```python
def factorial(n):
    result = 1
    for i in range(1, n + 1):     # FIX: 1..n, never 0;  n=0 -> range(1,1) empty -> result 1
        result = result * i
    return result


assert factorial(0) == 1
assert factorial(1) == 1
assert factorial(5) == 120
assert factorial(10) == 3628800
print("Fixed factorial assertions passed.")
```

### Listing 5 — IDE debugger tools (reference)
```text
IDE DEBUGGER TOOLS  (the dot-point's "debugging software available in an IDE")

  Breakpoint          a marker on a line that PAUSES execution there, so you can
                      inspect the program's state (all variable values) at that moment.
  Single-stepping     execute ONE LINE at a time from a paused point, watching each line's effect.
  Watch               monitor a chosen VARIABLE's value LIVE — see exactly when it changes / goes wrong.
  Interfaces          inspect the values PASSED INTO and RETURNED FROM each function
   between functions   (arguments in, value out) — isolates which function is at fault.
  Debug output        print() statements reporting values as the code runs — the simplest tool.

HOOK: the debugger trio = BREAKPOINT (pause), STEP (walk), WATCH (watch a variable).
A breakpoint + single-stepping + a watch is a TRACE TABLE run by the computer.
```
