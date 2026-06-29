---
title: "Supplementary Materials — Module Review: OOP Foundations (Chapter 5)"
module: OOP11
year: 11
lesson: "5"
script: script.md
---

# Supplementary Materials

A read-along reference for the Chapter 5 review. Nothing here is spoken — the narration is
self-contained. These listings consolidate the chapter's code touchpoints so you can see, in
one place, the structures the review talks about. They re-use the labels from the original
lessons' supplementary files (e.g. "the `BankAccount` spine from `OOP11-05-01`"). Every listing
is referenced by label in the script.

### Listing 1 — The seven key features, grouped (O-C-G + A-PIE)
```text
The 7 key features of an OOP language
=====================================

STRUCTURAL TRIO  — "O-C-G"
  Objects         a unit bundling data (attributes) + behaviour (methods)
  Classes         the blueprint; one class, many instances
  Generalisation  the MODELLING act: capture shared traits in a general class

FOUR BEHAVIOURS  — "A-PIE"   ("have a slice of A-PIE")
  Abstraction     hide the COMPLEXITY; expose only the essentials
  Polymorphism    one interface, many behaviours
  Inheritance     the IMPLEMENTATION act: a subclass reuses a parent's members
  Encapsulation   bundle data + methods AND restrict direct access

O-C-G  +  A-PIE  =  all seven  =  your exam paragraph headings.
```

### Listing 2 — Encapsulation: stable interface, hidden state (the `BankAccount` spine)
```python
class BankAccount:
    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = balance          # internal state — leading underscore = "hands off"

    # public interface: every change funnels through a validating method
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")     # invariant: balance >= 0
        self._balance -= amount

    def check_balance(self):
        return self._balance

# The trap: this BYPASSES the interface and breaks the invariant.
# Python does NOT stop you — the underscore is a convention, not a lock.
account = BankAccount("A-100", "Alice", 1000)
account._balance = 999999      # nothing protects the wiring; only convention says don't
```

### Listing 3 — The four behaviours in ONE integrated example (the `Shape` capstone)
```python
class Shape:                              # GENERALISATION: the shared model
    def area(self):
        raise NotImplementedError        # ABSTRACT method — forces subclasses to implement
    def perimeter(self):
        raise NotImplementedError

class Rectangle(Shape):                   # INHERITANCE: is-a Shape
    def __init__(self, width, height):
        self.width, self.height = width, height
    def area(self):                       # OVERRIDE → POLYMORPHISM
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14159 * self.radius ** 2

# ABSTRACTION + POLYMORPHISM: one loop, one message, each shape runs its own area()
def total_area(shapes):
    return sum(shape.area() for shape in shapes)

# total_area([Rectangle(2, 3), Circle(5)]) handles both via the shared interface.
# This single example demonstrates all four behaviours — the band-6 move on the 8-marker.
```

### Listing 4 — The same idea, procedural vs OOP (lesson 5.4 contrast)
```python
# PROCEDURAL: data and functions live apart.
def rectangle_area(width, height):
    return width * height
def rectangle_perimeter(width, height):
    return 2 * (width + height)
w, h = 4, 5                               # the data sits outside, passed around as parameters
print(rectangle_area(w, h))

# OOP: data walks with its methods.
class Rectangle:
    def __init__(self, width, height):
        self.width, self.height = width, height
    def area(self):
        return self.width * self.height
    def perimeter(self):
        return 2 * (self.width + self.height)
r = Rectangle(4, 5)                       # data + behaviour bundled in one object
print(r.area())

# Neither is "better": procedural suits a simple stateless calc;
# OOP suits real entities with state that interact. The mark is "it depends".
```

### Listing 5 — The facade: a tidy front desk over a messy back office (lesson 5.6)
```python
class LibraryFacade:
    """One simple front-of-house class over the validation/inventory/notification subsystems.
       The client calls borrow(); it never touches the messy internals.
       Note: the facade HIDES complexity — it does not remove it."""
    def __init__(self, validation, inventory, notifications):
        self._validation = validation        # the subsystems still exist
        self._inventory = inventory           # and still do all the work
        self._notifications = notifications

    def borrow(self, member, book):           # the clean, stable public interface
        if not self._validation.can_borrow(member):
            return False
        self._inventory.reserve(book)
        self._notifications.send_due_date(member, book)
        return True
```

### Listing 6 — Interface as contract: a mock drops in unchanged (lesson 5.7 — the Mars lesson)
```python
# The interface (the CONTRACT): "this is what you call, what you pass, what you get back."
# An UNSTATED contract is what doomed the Mars Climate Orbiter — units never agreed.
class PaymentProcessor:
    def charge(self, amount):
        raise NotImplementedError

class MockPaymentProcessor(PaymentProcessor):     # build against the interface BEFORE the real one
    def charge(self, amount):
        return {"status": "ok", "amount": amount}  # canned value, no real network call

class StripePaymentProcessor(PaymentProcessor):   # the real one honours the SAME interface…
    def charge(self, amount):
        # ... real API call ...
        return {"status": "ok", "amount": amount}

# …so it DROPS IN UNCHANGED. That substitutability is polymorphism — and it is exactly what
# lets a team work apart, then merge. (Write the contract down. Document the units.)
```

### Listing 7 — NESA pseudocode: the R-R-C-I responsibility on the right class
```text
BEGIN Library.BorrowBook(member, book)
    IF NOT member.CanBorrow() THEN          // Member owns its own loan-count + fines
        RETURN False
    ENDIF
    IF book.IsOverdue() THEN                // Book owns its own due-date
        RETURN False
    ENDIF
    member.AddLoan(book)
    book.SetDueDate(Today + LOAN_PERIOD)
    DISPLAY "Borrowed: " + book.Title
    RETURN True
END Library.BorrowBook

// Each method lives where its data lives (encapsulation).
// The Library only COORDINATES — that is its responsibility (collaboration).
// Nouns became classes (Member, Book, Library); verbs became methods.
```
