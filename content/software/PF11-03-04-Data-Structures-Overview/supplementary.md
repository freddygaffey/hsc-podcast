---
title: "Supplementary Materials — Data Structures Overview (Arrays, Records, Trees, Sequential Files)"
module: PF11
year: 11
lesson: "3.4"
script: script.md
---

# Supplementary Materials

Runnable Python for each of the four data structures, the 2D-array traversal in NESA
pseudocode, and a choose-the-structure reference. Nothing here is spoken in the audio — it's
the read-along reference. The narration points at each by label only.

### Listing 1 — Arrays: 1D and 2D (Python, runnable)
```python
# 1D ARRAY (Python list): ordered, indexed from 0
grades = [85, 92, 78, 96, 88]
assert grades[0] == 85           # first element (index 0)
assert grades[-1] == 88          # last element
assert len(grades) == 5

# 2D ARRAY (list of lists): a table — rows x columns
grade_book = [
    [85, 92, 78, 88],   # row 0 = Alice's grades
    [91, 87, 94, 89],   # row 1 = Bob's grades
    [76, 83, 81, 85],   # row 2 = Charlie's grades
]
assert grade_book[0][1] == 92    # row 0, column 1 -> Alice's 2nd subject
assert grade_book[1][2] == 94    # row 1, column 2 -> Bob's 3rd subject

# nested loop (outer = rows, inner = columns) to sum every grade
total = 0
for row in grade_book:
    for grade in row:
        total = total + grade
assert total == 1029             # 343 + 361 + 325
print("Array assertions passed; total =", total)
```

### Listing 2 — 2D-array traversal in NESA pseudocode (the examinable algorithm)
```text
BEGIN FUNCTION SumGradeBook(gradeBook, numRows, numCols)
    total ← 0
    FOR row = 0 TO numRows - 1
        FOR col = 0 TO numCols - 1
            total ← total + gradeBook[row][col]
        NEXT col
    NEXT row
    RETURN total
END FUNCTION
```

### Listing 3 — Records: one entity, and a list of records (Python, runnable)
```python
# A RECORD groups related fields of DIFFERENT types, accessed by NAME (not by index)
student = {
    "name": "Sarah Johnson",     # string
    "age": 17,                   # integer
    "grade_average": 87.5,       # float
    "enrolled": True,            # boolean
}
assert student["name"] == "Sarah Johnson"
assert student["age"] == 17

# Many records = a list of records (a class roster)
roster = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
]
high_achievers = [s["name"] for s in roster if s["grade"] > 80]
assert high_achievers == ["Alice", "Bob"]
print("Record assertions passed; high achievers =", high_achievers)
```

### Listing 4 — A tree, traversed recursively (Python, runnable)
```python
# A TREE: hierarchical — a root node with children, each child a subtree.
family = {
    "name": "Grandpa John",
    "children": [
        {"name": "Mike", "children": [
            {"name": "Sarah", "children": []},
            {"name": "Tom", "children": []},
        ]},
        {"name": "Lisa", "children": [
            {"name": "Emma", "children": []},
        ]},
    ],
}


def count_people(node):
    total = 1                            # count this node...
    for child in node["children"]:       # ...then recurse into each subtree (divide & conquer)
        total = total + count_people(child)
    return total


# John, Mike, Sarah, Tom, Lisa, Emma = 6 nodes
assert count_people(family) == 6
print("Tree assertions passed; people =", count_people(family))
```

### Listing 5 — A sequential file (CSV), written then read in order (Python, runnable)
```python
import csv
import io

# SEQUENTIAL FILE: records stored in order, read start-to-end. CSV = a common format.
# (An in-memory buffer stands in for a file on disk, so this runs anywhere.)
buffer = io.StringIO()
writer = csv.writer(buffer)
writer.writerow(["name", "age", "grade"])    # header row
writer.writerow(["Alice", 16, 85])
writer.writerow(["Bob", 17, 92])

buffer.seek(0)                                # rewind, then read sequentially
rows = list(csv.reader(buffer))

assert rows[0] == ["name", "age", "grade"]
assert rows[1] == ["Alice", "16", "85"]       # NOTE: CSV reads every field back as a STRING
assert len(rows) == 3
print("Sequential-file (CSV) assertions passed; rows =", len(rows))
```

### Listing 6 — Choosing the right data structure (reference)
```text
CHOOSE THE RIGHT DATA STRUCTURE

Need                                     Structure           Why / example
--------------------------------------   -----------------   ----------------------------------
Ordered collection, access by position   1D ARRAY (list)     grades, a shopping list
Table / grid (rows x columns)            2D ARRAY            a gradebook, a game board, seating
Group related fields of ONE entity       RECORD              a student (name + age + grade)
Hierarchical (parent-child) data         TREE                family tree, file system, org chart
Persist / exchange data in a file        SEQUENTIAL FILE     students.csv, a log

Match the SHAPE of the structure to the SHAPE of the data
(don't flatten a table, a hierarchy, or a record into a plain list).

Note: STACKS and HASH TABLES are also data structures, but they are implemented in
Chapter 4 (lesson 04-02), not part of this dot-point.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| CSV | Comma-Separated Values | A plain-text file format storing tabular data as comma-delimited rows |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
