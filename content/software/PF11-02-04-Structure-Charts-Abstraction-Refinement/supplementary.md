---
title: "Supplementary Materials — Structure Charts, Abstraction & Refinement (Divide-and-Conquer, Backtracking)"
module: PF11
year: 11
lesson: "2.4"
script: script.md
---

# Supplementary Materials

Stepwise-refinement pseudocode, a structure chart, a symbol/module reference, and runnable
divide-and-conquer and backtracking code. Nothing here is spoken in the audio — it's the
read-along reference. The narration points at each by label only. Diagrams are drawn in text
(no images, per the format).

### Listing 1 — Stepwise refinement of the Library system (NESA pseudocode, four layers)
```text
STEP 1 — High-level solution (the whole system in three lines)
BEGIN LibrarySystem
    Handle book borrowing
    Handle book returns
    Generate reports
END LibrarySystem

STEP 2 — Refine the top level into a menu loop
BEGIN LibrarySystem
    WHILE system is running DO
        Display main menu
        INPUT choice
        IF choice = "borrow" THEN
            Process book borrowing
        ELSE IF choice = "return" THEN
            Process book return
        ELSE IF choice = "report" THEN
            Generate system reports
        ELSE IF choice = "exit" THEN
            Stop the loop
        ENDIF
    ENDWHILE
END LibrarySystem

STEP 3 — Refine ONE box: "Process book borrowing"
BEGIN ProcessBookBorrowing
    INPUT cardNumber
    valid ← ValidateCard(cardNumber)
    INPUT bookID
    available ← CheckBookAvailable(bookID)
    withinLimit ← CheckBorrowingLimit(cardNumber)
    IF valid = true AND available = true AND withinLimit = true THEN
        Create borrowing record
        Update book status
        Set due date
        Print receipt
    ELSE
        Display error message
    ENDIF
END ProcessBookBorrowing

STEP 4 — Refine ONE box: "Validate card"
BEGIN FUNCTION ValidateCard(cardNumber)
    Look up cardNumber in database
    IF card not found THEN
        RETURN false
    ELSE IF card is expired THEN
        RETURN false
    ELSE IF card is suspended THEN
        RETURN false
    ELSE
        RETURN true
    ENDIF
END FUNCTION
```

### Listing 2 — Structure chart of the Library Management System (hierarchy + data flow)
```text
                          [ Main Controller ]
                                  |
     -----------------------------+-----------------------------
     |                  |                   |                   |
[ Display Menu ]  [ Process Borrowing ] [ Process Return ] [ Generate Reports ]
                         |                     |                    |
        -----------------+------          -----+-----        -------+-------
        |        |        |     |         |         |        |             |
 [Validate  [Check    [Check  [Create  [Calculate [Update  [Overdue     [Popular
   Card]    Available] Limits] Record]   Fines]   Records]  Report]      Report]
     |          |                 |
 [Read Card][Read Book]      [Write Borrowing]

Data flow (data items passed between modules, shown as labels on the call lines):
    Main Controller --(cardNumber)-->        Process Borrowing
    Process Borrowing --(cardNumber)-->      Validate Card        --(valid: true/false)-->  back up
    Process Borrowing --(bookID)-->          Check Available      --(available: true/false)--> back up
    Validate Card --(cardNumber)-->          Read Card            --(card record)--> back up
```

### Listing 3 — Structure chart symbols, and good vs poor modules
```text
STRUCTURE CHART SYMBOLS
  Rectangle ............... a module / subprogram (named with a verb phrase)
  Arrow (A --> B) ......... A CALLS / uses B
  Small circle on a line .. a DATA item passed along that call (a "data couple")
  Diamond ................. a conditional call (the call happens only on a condition)
  Curved arrow ............ an iterated call (the call repeats in a loop)

  Contrast: a STRUCTURE CHART shows WHO CALLS WHOM + the data passed (static hierarchy).
  A FLOWCHART shows the ORDER steps execute in, with decisions and loops (control flow).

WELL-DESIGNED MODULES  ->  high cohesion (one job), low coupling (few dependencies)
  GOOD:  CalculateGPA(grades_list) -> gpa_value          (one clear responsibility)
         ValidateEmailAddress(email) -> boolean
         FormatCurrency(amount, currencyCode) -> string

POORLY-DESIGNED MODULES
  POOR:  DoEverything()                                   (low cohesion: too broad)
         GetAndValidateAndStoreData()                     (three jobs in one)
         ProcessInputAndCalculateAndDisplay()             (low cohesion + high coupling)
         X()                                              (unclear purpose / poor name)
```

### Listing 4 — Divide and conquer: merge sort (Python, runnable)
```python
def merge_sort(items):
    if len(items) <= 1:               # base case: a 0- or 1-element list is already sorted
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])     # DIVIDE + conquer the left half
    right = merge_sort(items[mid:])    # DIVIDE + conquer the right half
    return merge(left, right)          # COMBINE the two sorted halves


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


assert merge_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
assert merge_sort([]) == []
assert merge_sort([3]) == [3]
print("All merge_sort assertions passed.")
```

### Listing 5 — Backtracking: solve a maze (Python, runnable)
```python
def solve_maze(grid, start, goal):
    # grid: 0 = open, 1 = wall.  Returns a path from start to goal, or None.
    rows, cols = len(grid), len(grid[0])
    path = []
    visited = set()

    def backtrack(cell):
        if cell == goal:                 # success: a complete solution
            path.append(cell)
            return True
        r, c = cell
        if (cell in visited or r < 0 or r >= rows or c < 0 or c >= cols
                or grid[r][c] == 1):     # dead end: seen, off-grid, or a wall
            return False
        visited.add(cell)
        path.append(cell)                # TRY this cell
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if backtrack((nr, nc)):      # explore a neighbour
                return True
        path.pop()                       # UNDO: this cell leads nowhere -> backtrack
        return False

    return path if backtrack(start) else None


maze = [
    [0, 0, 1],
    [1, 0, 1],
    [1, 0, 0],
]
assert solve_maze(maze, (0, 0), (2, 2)) == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
assert solve_maze([[0, 1], [1, 0]], (0, 0), (1, 1)) is None   # no path -> backtracks out
print("All solve_maze assertions passed.")
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
