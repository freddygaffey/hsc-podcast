---
title: "Supplementary Materials — Module Review: Programming in OOP (Whole Module)"
module: OOP11
year: 11
lesson: "6"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for the whole-module review. Nothing here is
spoken in the audio — it's the read-along reference. Every listing is referenced from the
narration by its label. This review pulls the whole object-oriented paradigm module
together (Chapters 05 and 06), so the listings are a compact consolidation, not new
material.

### Listing 1 — The whole-module mnemonic set, grouped by chapter
```text
CHAPTER 05 — DESIGN THE OBJECTS
  Seven key features      = O-C-G (Objects, Classes, Generalisation)
                            + A-PIE (Abstraction, Polymorphism, Inheritance, Encapsulation)
  Message-passing dispatch= L-B-P-E-R (Lookup, Bind self, Pass params, Execute, Return)
  Why encapsulate         = I-C-F-S (Integrity, Consistency, Flexibility, Security)
  Generalise vs inherit   = "generalise to model, inherit to reuse"
  Polymorphism w/o parent = "duck typing: if it quacks, it'll do"
  Procedural vs OOP       = "Procedural: data and functions live apart.
                             OOP: data walks with its methods."
  Three diagram views     = "Class = things, Chart = jobs, DFD = data"
  Composition relationship= "filled diamond = composition" (part dies with the whole)
  Design pipeline         = R-R-C-I (Requirements, Responsibilities,
                             Collaborations, Implementation) — always "iterative"
  Responsibility heuristic= "nouns become classes, verbs become methods"
  Facade pattern          = "a facade is a tidy front desk over a messy back office"
                            (hides complexity, does NOT remove it)
  Collaboration spine     = "clear interfaces let teams work apart, then merge"

CHAPTER 06 — BUILD, REFINE, TEST, OPTIMISE
  Composition vs inheritance = "is-a vs has-a -> favour has-a when unsure"
  Method cohesion         = "SRP: one method, one job, under ~20 lines"
  Mainline / coordinator  = "the mainline reads like a table of contents"
  Incremental build       = "stub first, fill later"
  Method signature        = "signature = name + parameters + return = the promise"
  Commenting              = "comment the why" (the code already shows the what)
  Constants               = "no magic numbers — name them"
  Test levels             = U-S-S (Unit, Subsystem, System)
  Good unit test          = FIRST (Fast, Independent, Repeatable,
                             Self-validating, Timely)
  Test strategies         = "Black = spec, White = code, Grey = both"
  Black-box techniques    = BVA + EP (Boundary Value Analysis + Equivalence Partitioning)
  Code effectiveness      = C-C-P-M (Correctness, Clarity, Performance, Maintainability)
  Optimisation workflow   = "measure first, optimise second"
                             (Clear -> Profile -> Optimise -> Re-verify)

EXAM-START DUMP (write these five lines first):
  A-PIE | I-C-F-S | R-R-C-I | U-S-S & FIRST | C-C-P-M
```

### Listing 2 — The module spine: a stable public interface over hidden, validated state
```python
class BankAccount:
    """A bank account: a stable public interface over hidden internal state.

    Demonstrates the module's spine instinct — hide the messy inside,
    publish a stable front. The public methods (the interface) stay stable
    while the internal state (_balance) is funnelled through validation.
    """

    def __init__(self, owner_name, opening_balance=0.0):
        if not owner_name:
            raise ValueError("owner name must not be empty")
        if opening_balance < 0:
            raise ValueError("opening balance must not be negative")
        self.owner_name = owner_name
        self._balance = opening_balance          # internal state ("the wiring")

    def deposit(self, amount):                   # public interface ("the buttons")
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:               # invariant: balance >= 0
            raise ValueError("insufficient funds")
        self._balance -= amount

    def get_balance(self):
        return self._balance


# The "underscore isn't privacy" trap, made concrete — Python does NOT stop this:
account = BankAccount("Alice", 100.0)
account._balance = 999_999      # bypasses every validating method -> invalid state
# Underscores are a polite request, not a locked door.
```

### Listing 3 — The integrated-task class diagram (Gradebook composed of Students)
```text
+------------------------------+
|          Gradebook           |
+------------------------------+
| - students : List[Student]   |
+------------------------------+
| + add_student(student)       |
| + record_grade(id, grade)    |
| + class_average() : float    |
+------------------------------+
            ◆ 1
            |
            | 1  *            ◆ = filled diamond = COMPOSITION
            |                     (the part dies with the whole)
            v *
+------------------------------+
|           Student            |
+------------------------------+
| - name : str                 |   -  = private  (internal state, encapsulated)
| - student_id : str           |   +  = public   (the interface)
| - grades : List[float]       |
+------------------------------+
| + add_grade(grade)           |
| + calculate_average() : float|
+------------------------------+

Reads: one Gradebook is composed of zero-or-more (*) Students.
calculate_average lives on Student because that is where the grade data lives
(each method lives where its data lives = encapsulation given a job).
```

### Listing 4 — Composition with a validating constructor (build the two classes)
```python
class Student:
    """A single student. Owns its own grades and the logic over them.

    Born valid: the constructor validates THEN stores (fails fast at the boundary).
    """

    MIN_GRADE = 0
    MAX_GRADE = 100

    def __init__(self, name, student_id):
        if not name:
            raise ValueError("name must not be empty")
        if not student_id:
            raise ValueError("student id must not be empty")
        self.name = name
        self.student_id = student_id
        self.grades = []

    def add_grade(self, grade):
        if not (self.MIN_GRADE <= grade <= self.MAX_GRADE):
            raise ValueError("grade must be between 0 and 100")
        self.grades.append(grade)

    def calculate_average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)


class Gradebook:
    """Composed of Students (has-a, not is-a). Coordinates; delegates the work."""

    def __init__(self):
        self.students = {}                       # keyed by id for O(1) lookup

    def add_student(self, student):
        self.students[student.student_id] = student

    def record_grade(self, student_id, grade):
        self.students[student_id].add_grade(grade)   # message-passing / delegation

    def class_average(self):
        if not self.students:
            return 0.0
        averages = [s.calculate_average() for s in self.students.values()]
        return sum(averages) / len(averages)
```

### Listing 5 — The unit test (one class in isolation: Student)
```python
import unittest


class TestStudentUnit(unittest.TestCase):
    def setUp(self):
        # Fresh fixture before EVERY test -> Independent + Repeatable (FIRST)
        self.student = Student("Alice", "S001")

    def test_average_of_three_grades(self):       # happy path
        self.student.add_grade(80)
        self.student.add_grade(90)
        self.student.add_grade(100)
        self.assertEqual(self.student.calculate_average(), 90.0)

    def test_no_grades_returns_zero(self):
        self.assertEqual(self.student.calculate_average(), 0.0)

    def test_grade_above_max_raises(self):        # boundary / error case
        with self.assertRaises(ValueError):
            self.student.add_grade(110)

    def test_grade_below_min_raises(self):
        with self.assertRaises(ValueError):
            self.student.add_grade(-10)

    def test_empty_name_rejected_at_construction(self):
        with self.assertRaises(ValueError):
            Student("", "S002")


if __name__ == "__main__":
    unittest.main()
```

### Listing 6 — The integration test (Gradebook + Student working together)
```python
import unittest


class TestGradebookIntegration(unittest.TestCase):
    """Subsystem / integration level: TWO classes cooperating across their interface.
    Only this catches a mismatch in the Gradebook <-> Student handshake — no
    single-class unit test can.
    """

    def setUp(self):
        self.gradebook = Gradebook()
        self.gradebook.add_student(Student("Alice", "S001"))
        self.gradebook.add_student(Student("Bob", "S002"))

    def test_class_average_across_students(self):
        # record grades THROUGH the Gradebook's interface (data crosses the boundary)
        self.gradebook.record_grade("S001", 80)
        self.gradebook.record_grade("S001", 100)   # Alice avg = 90
        self.gradebook.record_grade("S002", 60)
        self.gradebook.record_grade("S002", 80)     # Bob   avg = 70
        # class average = (90 + 70) / 2 = 80 — passes only if every message
        # and every reply flows correctly across the interface
        self.assertEqual(self.gradebook.class_average(), 80.0)

    def test_record_to_unknown_student_raises(self):
        with self.assertRaises(KeyError):
            self.gradebook.record_grade("S999", 50)


if __name__ == "__main__":
    unittest.main()
```

### Listing 7 — NESA pseudocode: the integrated build-and-assess workflow
```text
BEGIN BuildAndAssessGradebook
    REM ---- DESIGN (Chapter 05) ----
    Choose paradigm                          REM entities + state -> OOP, justified
    Draw class diagram                        REM Gradebook ◆-- "*" Student (composition)

    REM ---- BUILD (Chapter 06) ----
    FOR each class IN {Student, Gradebook}
        Write validating constructor          REM validate THEN store
        Write one-task methods                REM SRP: one method, one job
    NEXT class

    REM ---- TEST (Chapter 06) ----
    Run unit tests on Student IN isolation    REM count classes = 1 -> unit
    Run integration tests on Gradebook+Student REM count classes > 1 -> subsystem

    REM ---- ASSESS + OPTIMISE (Chapter 06) ----
    FOR each dimension IN {Correctness, Clarity, Performance, Maintainability}
        Assess code against dimension          REM C-C-P-M: name AND apply all four
    NEXT dimension

    IF performance is a profiled bottleneck THEN
        Optimise                               REM e.g. list search -> dict lookup
        Re-run all tests                       REM re-verify correctness
        IF tests fail THEN
            Revert                             REM faster wrong code is a regression
        ENDIF
    ENDIF
END BuildAndAssessGradebook
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| C-C-P-M | Correctness · Clarity · Performance · Maintainability | Dimensions of code quality |
| DFD | Data Flow Diagram | A model showing how data moves between processes, stores and external entities |
| I-C-F-S | Integrity · Consistency · Flexibility · Security | Reasons to use a database |
| L-B-P-E-R | Lookup · Bind self · Pass params · Execute · Return | The steps of a method/subroutine call |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| O-C-G | Objects · Classes · Generalisation | Core object-oriented modelling ideas |
| OOP | Object-Oriented Programming | A paradigm structuring software around objects that bundle data and behaviour |
| R-R-C-I | Requirements · Responsibilities · Collaborations · Implementation | The (iterative) object-oriented design pipeline |
| U-S-S | Unit · Subsystem · System | The levels of testing |
