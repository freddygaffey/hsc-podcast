---
title: "Supplementary Materials — Designing Subroutines and Stubs"
module: OOP11
year: 11
lesson: "6.3"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. Each listing is referenced by label in the
narration.

### Listing 1 — A shopping cart with real signatures but stubbed bodies (Python)
```python
class ShoppingCart:
    def __init__(self):
        """Create an empty shopping cart."""
        self.items = []

    def add_item(self, product_id, quantity):
        """Add an item to the cart. (Easy enough to implement for real.)"""
        self.items.append({"id": product_id, "qty": quantity})
        print(f"Added {quantity} of product {product_id}")

    def remove_item(self, product_id):
        """Remove an item from the cart. Returns True if removed.

        STUB: real signature, placeholder body — prints a TODO and
        returns a dummy value of the correct type (a bool).
        """
        print(f"TODO: remove product {product_id}")
        return False

    def calculate_total(self):
        """Return the total price of items in the cart.

        STUB: real signature, placeholder body — returns a dummy 0.0
        of the correct type (a float) so callers still run.
        """
        print("TODO: calculate the real total (pricing, tax, discounts)")
        return 0.00

    def checkout(self):
        """Process the purchase. Returns True on success.

        Calls calculate_total — so the integration between methods is
        exercised even though the total is still a stubbed dummy.
        """
        total = self.calculate_total()
        print(f"Processing checkout for ${total:.2f}")
        return True
```

### Listing 2 — A clear, uncluttered mainline that calls one-task subroutines (Python)
```python
def main():
    """The mainline orchestrates; it does not implement.

    Read top to bottom and you see the SHAPE of the program — like a
    table of contents. Each step is one call to one well-named method.
    The real work lives down in those methods, not up here.
    """
    cart = ShoppingCart()

    add_demo_items(cart)          # load
    review_cart(cart)             # process
    finish_order(cart)            # display / act


def add_demo_items(cart):
    """One task: put some items in the cart."""
    cart.add_item("APPLE-01", 3)
    cart.add_item("BREAD-02", 1)


def review_cart(cart):
    """One task: show the running total."""
    total = cart.calculate_total()
    print(f"Current total: ${total:.2f}")


def finish_order(cart):
    """One task: attempt the checkout."""
    if cart.checkout():
        print("Order complete.")
    else:
        print("Checkout failed.")


if __name__ == "__main__":
    main()
```

### Listing 3 — A CLUTTERED mainline (the weak version, for contrast)
```python
# WEAK: the mainline does the work itself instead of orchestrating.
# Loops, conditionals and detail are tangled at the top level, so you
# must read every line to learn that it "loads, processes, displays".
if __name__ == "__main__":
    cart = ShoppingCart()
    raw = [("APPLE-01", 3), ("BREAD-02", 1), ("MILK-03", 0)]
    for pid, qty in raw:                      # parsing logic up here...
        if qty > 0:                           # ...validation up here...
            cart.items.append({"id": pid, "qty": qty})
            print(f"Added {qty} of product {pid}")
    running = 0.0
    for item in cart.items:                   # pricing loop up here...
        running += 0.0                        # (real pricing would go here)
    print(f"Current total: ${running:.2f}")
    if running >= 0:                          # checkout decision up here...
        print("Processing checkout...")
        print("Order complete.")
```

### Listing 4 — A student gradebook built signatures-first, with stubs (Python)
```python
class Student:
    def __init__(self, student_id, name):
        """Create a student with an ID and a name."""
        self.student_id = student_id
        self.name = name
        self.grades = []

    def add_grade(self, subject, score):
        """Record a grade for a subject. (Easy — real body.)"""
        self.grades.append({"subject": subject, "score": score})

    def get_average(self):
        """Return the average score across all subjects (float)."""
        if not self.grades:
            return 0.0
        return sum(g["score"] for g in self.grades) / len(self.grades)

    def get_grades_for_subject(self, subject):
        """Return all grades for one subject (list).

        STUB: real signature, placeholder body for now.
        """
        print(f"TODO: get grades for {subject}")
        return []


class Gradebook:
    def __init__(self):
        """Create an empty gradebook."""
        self.students = {}

    def add_student(self, student):
        """Add a student to the gradebook. (Easy — real body.)"""
        self.students[student.student_id] = student

    def record_grade(self, student_id, subject, score):
        """Record a grade for a student. Returns True on success.

        Real-but-thin body: delegates to the student object. This is
        the INTEGRATION point we want to test early — does a grade
        recorded on the gradebook actually reach the student object?
        """
        if student_id not in self.students:
            print(f"Student {student_id} not found")
            return False
        self.students[student_id].add_grade(subject, score)
        return True

    def get_class_average(self, subject):
        """Return the class average for a subject (float).

        STUB: the complex aggregation isn't written yet — dummy 0.0.
        """
        print(f"TODO: calculate the class average for {subject}")
        return 0.0

    def generate_report(self, student_id):
        """Return a one-line report for a student (str)."""
        if student_id not in self.students:
            return "Student not found"
        student = self.students[student_id]
        return f"{student.name}: average = {student.get_average():.1f}"
```

### Listing 5 — Running the stubbed gradebook end-to-end (Python)
```python
# The whole system RUNS on placeholders. We can confirm the objects
# connect — that record_grade on the gradebook reaches the student —
# before the class-average maths exists.
gradebook = Gradebook()
gradebook.add_student(Student("12345", "Alice"))

gradebook.record_grade("12345", "Math", 85)
gradebook.record_grade("12345", "Science", 92)

print(gradebook.generate_report("12345"))   # Alice: average = 88.5
print(gradebook.get_class_average("Math"))   # 0.0  ← still a stub
```

### Listing 6 — PlantUML class diagram: a Gradebook manages many Students
```text
@startuml
skinparam monochrome true
skinparam shadowing false

class Student {
    - student_id : str
    - name : str
    - grades : list
    + add_grade(subject, score)
    + get_average() : float
    + get_grades_for_subject(subject) : list
}

class Gradebook {
    - students : dict
    + add_student(student)
    + record_grade(student_id, subject, score) : bool
    + get_class_average(subject) : float
    + generate_report(student_id) : str
}

' One Gradebook manages MANY Students — the "*" multiplicity at the
' Student end, read toward the far class: one gradebook to many students.
Gradebook --> "*" Student : manages
@enduml
```

### Listing 7 — NESA pseudocode: the stubbed CalculateTotal as a method
```text
BEGIN CalculateTotal()
    REM STUB — real signature, placeholder body.
    REM Returns a dummy value of the correct type so callers still run.
    DISPLAY "TODO: calculate the real total"
    RETURN 0.00
END CalculateTotal
```

### Listing 8 — NESA pseudocode: an uncluttered mainline orchestrating one-task subroutines
```text
BEGIN Main
    cart ← NEW ShoppingCart()
    AddDemoItems(cart)        REM load
    ReviewCart(cart)          REM process
    FinishOrder(cart)         REM display / act
END Main

BEGIN AddDemoItems(cart)
    cart.AddItem("APPLE-01", 3)
    cart.AddItem("BREAD-02", 1)
END AddDemoItems

BEGIN ReviewCart(cart)
    total ← cart.CalculateTotal()
    DISPLAY "Current total: ", total
END ReviewCart

BEGIN FinishOrder(cart)
    IF cart.Checkout() = TRUE THEN
        DISPLAY "Order complete."
    ELSE
        DISPLAY "Checkout failed."
    ENDIF
END FinishOrder
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
