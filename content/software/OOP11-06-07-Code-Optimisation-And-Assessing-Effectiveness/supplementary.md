---
title: "Supplementary Materials — Code Optimisation and Assessing Effectiveness"
module: OOP11
year: 11
lesson: "6.7"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the audio — it is the read-along reference. Each listing is referenced from the narration by its number, in the order it appears.

### Listing 1 — Slow student-manager: O(n) list search and a recomputed average
```python
class StudentManager:
    """First-cut student manager. Works correctly, but every lookup is a
    linear scan and the average is recomputed from scratch each call."""

    def __init__(self):
        self.students = []  # a plain list

    def add_student(self, student_id, name):
        self.students.append({"id": student_id, "name": name, "grades": []})

    def add_grade(self, student_id, grade):
        for student in self.students:          # O(n) scan to find the student
            if student["id"] == student_id:
                student["grades"].append(grade)
                return

    def find_student(self, student_id):
        """O(n) linear search — checks every student until it finds a match."""
        for student in self.students:
            if student["id"] == student_id:
                return student
        return None

    def average_grade(self, student_id):
        """Recomputes the average from scratch every single call."""
        student = self.find_student(student_id)      # another O(n) scan
        grades = student["grades"]
        if not grades:
            return 0.0
        return sum(grades) / len(grades)             # recomputed every time
```

### Listing 2 — Fast student-manager: O(1) dictionary lookup and a cached average
```python
class OptimizedStudentManager:
    """Same public behaviour as StudentManager — same method names, same
    return values — but a dict gives O(1) lookup and the average is cached."""

    def __init__(self):
        self.students = {}        # dict keyed by student_id → O(1) lookup
        self._average_cache = {}  # cached averages, cleared when grades change

    def add_student(self, student_id, name):
        self.students[student_id] = {"id": student_id, "name": name, "grades": []}

    def add_grade(self, student_id, grade):
        if student_id in self.students:              # O(1) membership test
            self.students[student_id]["grades"].append(grade)
            self._average_cache.pop(student_id, None)  # invalidate the cache

    def find_student(self, student_id):
        """O(1) hash-table lookup — no scan."""
        return self.students.get(student_id)

    def average_grade(self, student_id):
        """Returns the cached value if grades have not changed."""
        if student_id in self._average_cache:
            return self._average_cache[student_id]    # cache hit, no work
        student = self.students.get(student_id)
        grades = student["grades"]
        average = sum(grades) / len(grades) if grades else 0.0
        self._average_cache[student_id] = average     # store for next time
        return average
```

### Listing 3 — Benchmark the two managers AND assert they agree (correctness preserved)
```python
import time
import random

def benchmark_student_managers(n=10000, lookups=5000):
    slow = StudentManager()
    fast = OptimizedStudentManager()

    # Build identical data in both managers.
    for i in range(n):
        sid = f"S{i:05d}"
        slow.add_student(sid, f"Student {i}")
        fast.add_student(sid, f"Student {i}")
        for _ in range(5):
            grade = random.uniform(50, 100)
            slow.add_grade(sid, grade)
            fast.add_grade(sid, grade)

    target = f"S{n // 2:05d}"  # a student in the middle of the list

    # Time the slow (O(n) linear search) version.
    start = time.time()
    for _ in range(lookups):
        slow.find_student(target)
    slow_time = time.time() - start

    # Time the fast (O(1) dict) version.
    start = time.time()
    for _ in range(lookups):
        fast.find_student(target)
    fast_time = time.time() - start

    # CORRECTNESS GATE: the optimisation is only valid if both still agree.
    assert slow.find_student(target)["name"] == fast.find_student(target)["name"]
    assert abs(slow.average_grade(target) - fast.average_grade(target)) < 1e-9

    print(f"Slow lookup (O(n) list)  : {slow_time:.4f} s")
    print(f"Fast lookup (O(1) dict)  : {fast_time:.4f} s")
    print(f"Speed-up                 : {slow_time / fast_time:.0f}x faster")
```

### Listing 4 — find-duplicates: O(n^2) nested loops vs O(n) with a set
```python
def find_duplicates_slow(items):
    """O(n^2): for every item, scan the whole list again looking for a twin."""
    duplicates = []
    for i, item in enumerate(items):
        for j, other in enumerate(items):
            if i != j and item == other and item not in duplicates:
                duplicates.append(item)
    return duplicates


def find_duplicates_fast(items):
    """O(n): one pass, using a set for O(1) membership tests."""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:          # O(1) — have we met this before?
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


# Same answer, wildly different cost. On 5,000 items the O(n^2) version does
# ~25 million comparisons; the O(n) version does ~5,000.
def check_find_duplicates_agree():
    import random
    data = [random.randint(1, 1000) for _ in range(5000)]
    assert sorted(find_duplicates_slow(data)) == sorted(find_duplicates_fast(data))
```

### Listing 5 — A simple timing/profiling decorator (measure first, optimise second)
```python
import time
import functools

def time_function(func):
    """Wrap a function so it prints how long each call took.
    Decorate the methods you SUSPECT are slow, run the program, and let the
    numbers — not your hunch — tell you where the time actually goes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f} s")
        return result
    return wrapper


class ReportBuilder:
    @time_function
    def load_data(self, source):
        time.sleep(0.30)            # turns out THIS is the bottleneck
        return list(range(100000))

    @time_function
    def transform(self, data):
        return [x * 2 for x in data]   # fast — not worth optimising

    @time_function
    def summarise(self, data):
        return sum(data)               # fast — not worth optimising
```

### Listing 6 — Readable vs "performance-optimised" grade calculator (keep the readable one)
```python
class ReadableGradeCalculator:
    """Clear, obvious, easy to change. Prefer this unless profiling proves it
    is a real bottleneck."""
    def letter_grade(self, score):
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


class OptimisedGradeCalculator:
    """A 'clever' tuple-table version. Marginally faster per call, but harder
    to read — and on a benchmark the gain is under 2x, so it is NOT worth it."""
    THRESHOLDS = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F")]

    def letter_grade(self, score):
        for threshold, grade in self.THRESHOLDS:
            if score >= threshold:
                return grade
        return "F"


def compare_grade_calculators():
    import random, time
    scores = [random.uniform(0, 100) for _ in range(100000)]
    readable = ReadableGradeCalculator()
    optimised = OptimisedGradeCalculator()

    start = time.time()
    r = [readable.letter_grade(s) for s in scores]
    readable_time = time.time() - start

    start = time.time()
    o = [optimised.letter_grade(s) for s in scores]
    optimised_time = time.time() - start

    assert r == o   # identical output — correctness preserved
    speedup = readable_time / optimised_time
    print(f"Speed-up: {speedup:.2f}x")
    if speedup < 2.0:
        print("Recommendation: keep the readable version — gain too small.")
```

### Listing 7 — NESA pseudocode: the optimisation workflow (Clear, Profile, Optimise, Re-verify)
```text
BEGIN OptimiseModule
    Step 1 -- write CLEAR, correct code first
    WriteClearWorkingVersion()

    Step 2 -- PROFILE: measure where the time actually goes
    timings <- Profile(program)
    bottleneck <- the operation with the largest timing

    Step 3 -- OPTIMISE only that bottleneck
    IF bottleneck is a slow algorithm OR a poor data structure THEN
        Replace with a better algorithm or data structure
    ELSE
        DISPLAY "no worthwhile optimisation -- leave the clear code"
    ENDIF

    Step 4 -- RE-VERIFY correctness with the test suite
    IF all tests PASS AND new version is faster THEN
        Keep the optimised version
    ELSE
        Revert to the clear version
    ENDIF
END OptimiseModule
```

### Listing 8 — NESA pseudocode: O(n) linear search vs O(1) lookup (the data-structure choice)
```text
BEGIN FindStudent_LinearSearch        // O(n)
    FOR each student IN studentList
        IF student.id = targetId THEN
            RETURN student
        ENDIF
    NEXT student
    RETURN Null
END FindStudent_LinearSearch

BEGIN FindStudent_DictionaryLookup    // O(1)
    RETURN studentDictionary.Get(targetId)
END FindStudent_DictionaryLookup
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
