---
title: "Supplementary Materials — Pseudocode and Flowcharts (Including Subprograms)"
module: PF11
year: 11
lesson: "2.3"
script: script.md
---

# Supplementary Materials

NESA-style pseudocode, a flowchart symbol reference, and runnable code for this episode.
Nothing here is spoken in the audio — it's the read-along reference. The narration points
at each by label only. Flowcharts are described in text (no images, per the format).

### Listing 1 — Library book borrowing: the four-case decision (NESA pseudocode)
```text
BEGIN LibraryBookBorrowing
    OUTPUT "Enter your library card number:"
    INPUT cardNumber
    OUTPUT "Enter the book ID you want to borrow:"
    INPUT bookID

    INPUT hasOverdueBooks      // true / false
    INPUT isBookAvailable      // true / false

    IF hasOverdueBooks = false AND isBookAvailable = true THEN
        OUTPUT "Book borrowed successfully. Due date: 2 weeks from today."
    ELSE IF hasOverdueBooks = true AND isBookAvailable = false THEN
        OUTPUT "Denied: you have overdue books AND the book is unavailable."
    ELSE IF hasOverdueBooks = true THEN
        OUTPUT "Denied: please return your overdue books first."
    ELSE
        OUTPUT "Denied: the book is currently checked out."
    ENDIF
END LibraryBookBorrowing
```

### Listing 2 — The same algorithm decomposed into subprograms (NESA pseudocode)
```text
// A FUNCTION subprogram: takes an input, RETURNS a value
BEGIN FUNCTION HasOverdueBooks(cardNumber)
    // (a real system queries the loans database; simplified here)
    RETURN lookupOverdueStatus(cardNumber)
END FUNCTION

BEGIN FUNCTION IsBookAvailable(bookID)
    RETURN lookupAvailability(bookID)
END FUNCTION

BEGIN LibraryBookBorrowing
    OUTPUT "Enter your library card number:"
    INPUT cardNumber
    OUTPUT "Enter the book ID you want to borrow:"
    INPUT bookID

    overdue   ← HasOverdueBooks(cardNumber)     // CALL a subprogram, store result
    available ← IsBookAvailable(bookID)         // CALL a subprogram, store result

    IF overdue = false AND available = true THEN
        OUTPUT "Book borrowed successfully. Due date: 2 weeks from today."
    ELSE IF overdue = true AND available = false THEN
        OUTPUT "Denied: you have overdue books AND the book is unavailable."
    ELSE IF overdue = true THEN
        OUTPUT "Denied: please return your overdue books first."
    ELSE
        OUTPUT "Denied: the book is currently checked out."
    ENDIF
END LibraryBookBorrowing
```

### Listing 3 — Flowchart symbol reference
```text
SHAPE                          MEANING                    MEMORY HOOK
-----------------------------  -------------------------  ----------------------------
Rounded rectangle (terminator) Start / End of the flow    "rounded ends top-and-tail"
Parallelogram                  Input or Output            "lean it for in and out"
Rectangle                      Process (a step/calc/SET)  "the square box does the work"
Diamond                        Decision (a question)      "diamond decides" (only shape
                                                          that branches: one arrow per
                                                          answer, e.g. Yes / No)
Rectangle with double bars     Predefined process =       "the double-barred box is a
  (vertical lines each side)     a subprogram CALL          call"
Arrow / flow line              Order of execution         follow the arrow

KEY RULE: every arrow out of a Diamond must lead somewhere. A dangling branch
(e.g. a "Yes" path with no matching "No" path) is a logic error — a dead end.
```

### Listing 4 — Natural language to NESA pseudocode (find the largest of three)
```text
Natural language:
  "Ask the user for three numbers. Find the largest number and display it."

NESA pseudocode:
BEGIN FindLargestOfThree
    OUTPUT "Enter three numbers:"
    INPUT num1
    INPUT num2
    INPUT num3

    largest ← num1            // running EXTREME (best-so-far), the E in A-E-F

    IF num2 > largest THEN
        largest ← num2
    ENDIF
    IF num3 > largest THEN
        largest ← num3
    ENDIF

    OUTPUT "The largest number is: " + largest
END FindLargestOfThree
```

### Listing 5 — The borrowing decision as runnable Python (verifies all four cases)
```python
def borrow_decision(has_overdue, is_available):
    if not has_overdue and is_available:
        return "Book borrowed successfully"
    elif has_overdue and not is_available:
        return "Denied: overdue books AND book unavailable"
    elif has_overdue:
        return "Denied: return your overdue books first"
    else:  # not has_overdue and not is_available
        return "Denied: book is currently checked out"


# All four combinations of the two booleans are covered:
assert borrow_decision(False, True)  == "Book borrowed successfully"
assert borrow_decision(True,  False) == "Denied: overdue books AND book unavailable"
assert borrow_decision(True,  True)  == "Denied: return your overdue books first"
assert borrow_decision(False, False) == "Denied: book is currently checked out"
print("All borrow_decision assertions passed.")
```
