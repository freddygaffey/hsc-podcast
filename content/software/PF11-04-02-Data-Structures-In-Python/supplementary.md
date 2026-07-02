---
title: "Supplementary Materials — Data Structures in Python (Arrays, Lists, Trees, Stacks, Hash Tables)"
module: PF11
year: 11
lesson: "4.2"
script: script.md
---

# Supplementary Materials

Runnable Python for the required data-structure set, plus the stack in NESA pseudocode.
Nothing here is spoken in the audio — it's the read-along reference. The narration points at
each by label only.

### Listing 1 — Arrays: 1D find-max-and-position, and a 2D grade book (Python, runnable)
```python
# 1D array (list): find the maximum value AND its position
def find_max(scores):
    max_score = scores[0]
    max_pos = 0
    for i in range(len(scores)):
        if scores[i] > max_score:
            max_score = scores[i]
            max_pos = i
    return max_score, max_pos


assert find_max([78, 95, 85, 67]) == (95, 1)
assert max([78, 95, 85, 67]) == 95          # built-ins exist too
assert sum([78, 95, 85, 67]) == 325

# 2D array (list of lists): a grade book, accessed by [row][column]
grade_book = [
    [85, 92, 78],   # row 0 = Alice
    [91, 87, 94],   # row 1 = Bob
    [76, 83, 81],   # row 2 = Charlie
]
assert grade_book[0][0] == 85               # row 0, column 0
assert grade_book[1][2] == 94               # row 1, column 2
averages = [sum(row) / len(row) for row in grade_book]
assert averages[0] == 85.0                  # (85 + 92 + 78) / 3
print("Array assertions passed.")
```

### Listing 2 — Core list operations (Python, runnable)
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")               # add to the END
fruits.insert(1, "blueberry")       # insert at index 1
assert fruits == ["apple", "blueberry", "banana", "cherry", "date"]

fruits.remove("banana")             # remove first matching value
assert fruits == ["apple", "blueberry", "cherry", "date"]

last = fruits.pop()                 # remove + RETURN the last element
assert last == "date"
assert fruits == ["apple", "blueberry", "cherry"]

assert fruits.index("cherry") == 2  # position of a value
assert ("apple" in fruits) is True  # membership test
assert len(fruits) == 3
print("List-operation assertions passed.")
```

### Listing 3 — A stack built from a list (LIFO) (Python, runnable)
```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)      # push = append to the end (the TOP)

    def pop(self):
        return self.items.pop()      # pop = remove + return the end (the TOP)

    def peek(self):
        return self.items[-1]        # look at the top WITHOUT removing

    def is_empty(self):
        return len(self.items) == 0


s = Stack()
s.push("a")
s.push("b")
s.push("c")
assert s.peek() == "c"               # last pushed is on top
assert s.pop() == "c"                # LIFO: last in, first out
assert s.pop() == "b"
assert s.is_empty() is False
assert s.pop() == "a"
assert s.is_empty() is True
print("Stack assertions passed.")
```

### Listing 4 — A stack in NESA pseudocode (the examinable algorithm)
```text
BEGIN Stack
    items ← empty list

    BEGIN PROCEDURE Push(item)
        APPEND item TO items                 // add to the end = the TOP
    END PROCEDURE

    BEGIN FUNCTION Pop()
        IF length(items) = 0 THEN
            RETURN error "stack is empty"
        ENDIF
        top ← items[length(items) - 1]       // the last element = the TOP
        REMOVE last element FROM items
        RETURN top                           // last in, first out
    END FUNCTION

    BEGIN FUNCTION IsEmpty()
        RETURN length(items) = 0
    END FUNCTION
END Stack
```

### Listing 5 — A hash table (dictionary): lookup and counting (Python, runnable)
```python
# A HASH TABLE = a Python dict: key -> value, near-instant lookup by key
phone_book = {"Alice": "555-0101", "Bob": "555-0102"}
assert phone_book["Alice"] == "555-0101"     # straight to the value, no search
phone_book["Carol"] = "555-0103"             # add a new entry
assert ("Bob" in phone_book) is True


# Classic second use: COUNTING with a dict (item -> tally)
def count_letters(text):
    counts = {}
    for ch in text.lower():
        if ch.isalpha():
            counts[ch] = counts.get(ch, 0) + 1
    return counts


assert count_letters("Hello") == {"h": 1, "e": 1, "l": 2, "o": 1}
print("Hash-table assertions passed.")
```

### Listing 6 — A tree (nested dict) traversed recursively (Python, runnable)
```python
family = {
    "name": "John",
    "children": [
        {"name": "Michael", "children": [
            {"name": "Sarah", "children": []},
            {"name": "David", "children": []},
        ]},
        {"name": "Lisa", "children": [
            {"name": "Emma", "children": []},
        ]},
    ],
}


def count_members(node):
    total = 1                              # count this node...
    for child in node["children"]:         # ...then recurse into each subtree
        total = total + count_members(child)
    return total


# John, Michael, Sarah, David, Lisa, Emma = 6
assert count_members(family) == 6
print("Tree assertions passed.")
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| LIFO | Last In · First Out | Access order of a stack: the most recently added item is removed first |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
