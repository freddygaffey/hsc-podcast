---
title: "Supplementary Materials — Testing: Unit, Subsystem, System and QA"
module: OOP11
year: 11
lesson: "6.5"
script: script.md
---

# Supplementary Materials

Code listings for this episode. Nothing here is spoken in the audio — it's the read-along
reference. All examples use Python's standard `unittest` framework. Each listing is
referenced from the narration by its label.

### Listing 1 — `TestBankAccount`: a unit-test suite with `setUp` + `assertEqual` / `assertRaises`
```python
import unittest


class BankAccount:
    """A single bank account — the unit under test."""

    def __init__(self, account_holder, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transaction_history.append(f"Deposit: +${amount:.2f}")
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transaction_history.append(f"Withdrawal: -${amount:.2f}")
        return self.balance

    def get_balance(self):
        return self.balance


class TestBankAccount(unittest.TestCase):
    """Unit tests — one class, in isolation. Each test checks one behaviour."""

    def setUp(self):
        # Runs automatically BEFORE EVERY test → a fresh, clean fixture.
        # This is what makes the tests Independent and Repeatable (FIRST).
        self.account = BankAccount("Alice Johnson", 100.0)

    # --- initialisation: valid / zero / negative ---
    def test_init_with_valid_balance(self):
        account = BankAccount("Bob Smith", 50.0)
        self.assertEqual(account.balance, 50.0)
        self.assertEqual(len(account.transaction_history), 0)

    def test_init_with_zero_balance(self):
        account = BankAccount("Charlie Brown")
        self.assertEqual(account.balance, 0.0)

    def test_init_with_negative_balance_raises_error(self):
        with self.assertRaises(ValueError):
            BankAccount("Dave Wilson", -10.0)

    # --- deposit: valid / zero / negative ---
    def test_deposit_positive_amount(self):
        new_balance = self.account.deposit(25.0)
        self.assertEqual(new_balance, 125.0)
        self.assertEqual(self.account.get_balance(), 125.0)

    def test_deposit_zero_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_negative_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-10.0)

    # --- withdraw: valid / whole balance / over-withdraw / zero ---
    def test_withdraw_valid_amount(self):
        new_balance = self.account.withdraw(30.0)
        self.assertEqual(new_balance, 70.0)

    def test_withdraw_entire_balance(self):
        self.assertEqual(self.account.withdraw(100.0), 0.0)

    def test_withdraw_more_than_balance_raises_error(self):
        # The star test — proves the guard clause actually fires.
        with self.assertRaises(ValueError) as ctx:
            self.account.withdraw(150.0)
        self.assertIn("insufficient", str(ctx.exception).lower())

    def test_withdraw_zero_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)


if __name__ == "__main__":
    unittest.main()
```

### Listing 2 — `TestLibrarySubsystem`: an integration (subsystem) test of two classes cooperating
```python
import unittest


class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_available = True
        self.borrower = None

    def check_out(self, borrower_name):
        if not self.is_available:
            raise ValueError(f"'{self.title}' is already checked out")
        self.is_available = False
        self.borrower = borrower_name

    def return_book(self):
        if self.is_available:
            raise ValueError(f"'{self.title}' is not currently checked out")
        self.is_available = True
        self.borrower = None


class Library:
    def __init__(self, name):
        self.name = name
        self.books = {}            # isbn -> Book
        self.borrower_records = {}  # borrower_name -> [isbn, ...]

    def add_book(self, book):
        if book.isbn in self.books:
            raise ValueError(f"Book {book.isbn} already exists")
        self.books[book.isbn] = book

    def find_book(self, isbn):
        return self.books.get(isbn)

    def check_out_book(self, isbn, borrower_name):
        book = self.find_book(isbn)
        if not book:
            raise ValueError(f"Book {isbn} not found")
        book.check_out(borrower_name)
        self.borrower_records.setdefault(borrower_name, []).append(isbn)

    def return_book(self, isbn, borrower_name):
        book = self.find_book(isbn)
        if not book:
            raise ValueError(f"Book {isbn} not found")
        if book.borrower != borrower_name:
            raise ValueError(f"Book is not checked out to {borrower_name}")
        book.return_book()
        self.borrower_records[borrower_name].remove(isbn)

    def get_books_by_borrower(self, borrower_name):
        return self.borrower_records.get(borrower_name, [])


class TestLibrarySubsystem(unittest.TestCase):
    """Integration tests — Library and Book working TOGETHER across their interface."""

    def setUp(self):
        self.library = Library("Central Library")
        self.book1 = Book("978-0-13-110362-7", "Clean Code", "Robert Martin")
        self.book2 = Book("978-0-13-235088-4", "Clean Architecture", "Robert Martin")
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

    def test_complete_borrow_return_workflow(self):
        borrower, isbn = "Alice Johnson", "978-0-13-110362-7"

        # Available to start — both objects agree.
        book = self.library.find_book(isbn)
        self.assertTrue(book.is_available)

        # Borrow: assert BOTH objects updated consistently.
        self.library.check_out_book(isbn, borrower)
        self.assertFalse(book.is_available)              # the Book's own state
        self.assertEqual(book.borrower, borrower)        # the Book's own state
        self.assertIn(isbn, self.library.get_books_by_borrower(borrower))  # the Library's records

        # Return: assert the reverse — the two objects stay in agreement.
        self.library.return_book(isbn, borrower)
        self.assertTrue(book.is_available)
        self.assertIsNone(book.borrower)
        self.assertNotIn(isbn, self.library.get_books_by_borrower(borrower))

    def test_multiple_borrowers_different_books(self):
        self.library.check_out_book("978-0-13-110362-7", "Alice")
        self.library.check_out_book("978-0-13-235088-4", "Bob")
        self.assertEqual(self.library.find_book("978-0-13-110362-7").borrower, "Alice")
        self.assertEqual(self.library.find_book("978-0-13-235088-4").borrower, "Bob")

    def test_error_handling_across_the_interface(self):
        self.library.check_out_book("978-0-13-110362-7", "Alice")
        # Bob can't take Alice's book...
        with self.assertRaises(ValueError):
            self.library.check_out_book("978-0-13-110362-7", "Bob")
        # ...and Bob can't return a book that isn't his.
        with self.assertRaises(ValueError):
            self.library.return_book("978-0-13-110362-7", "Bob")


if __name__ == "__main__":
    unittest.main()
```

### Listing 3 — `TestLibrarySystem`: an end-to-end (system) test of a whole day of operations
```python
import unittest

# Uses the Book and Library classes from Listing 2.


class TestLibrarySystem(unittest.TestCase):
    """System test — the WHOLE application through a realistic scenario."""

    def setUp(self):
        self.library = Library("University Library")
        for isbn, title, author in [
            ("978-0-13-110362-7", "Clean Code", "Robert Martin"),
            ("978-0-13-235088-4", "Clean Architecture", "Robert Martin"),
            ("978-0-134-494162", "Design Patterns", "Gang of Four"),
        ]:
            self.library.add_book(Book(isbn, title, author))

    def test_daily_operations(self):
        # Morning: three students each borrow a book.
        self.library.check_out_book("978-0-13-110362-7", "Alice")
        self.library.check_out_book("978-0-13-235088-4", "Bob")
        self.library.check_out_book("978-0-134-494162", "Charlie")
        for isbn in ("978-0-13-110362-7", "978-0-13-235088-4", "978-0-134-494162"):
            self.assertFalse(self.library.find_book(isbn).is_available)

        # Afternoon: two return; a new student borrows a just-returned book.
        self.library.return_book("978-0-13-110362-7", "Alice")
        self.library.return_book("978-0-13-235088-4", "Bob")
        self.library.check_out_book("978-0-13-110362-7", "Diana")

        # End of day: assert the full, consistent final state.
        self.assertEqual(len(self.library.get_books_by_borrower("Alice")), 0)
        self.assertEqual(len(self.library.get_books_by_borrower("Bob")), 0)
        self.assertEqual(len(self.library.get_books_by_borrower("Charlie")), 1)
        self.assertEqual(self.library.get_books_by_borrower("Diana"), ["978-0-13-110362-7"])


if __name__ == "__main__":
    unittest.main()
```

### Listing 4 — A QA review checklist (lift straight into an answer)
```text
QUALITY ASSURANCE — CODE REVIEW CHECKLIST
(Run before merging. Every line is a concept from this module.)

DESIGN
[ ] Single responsibility — each class has one clear purpose
[ ] Encapsulation      — internal data is hidden behind a public interface
[ ] Clear names        — class and method names describe what they do
[ ] Method size        — each method does one focused job
[ ] Error handling      — invalid input raises a clear, specific exception
[ ] Documentation       — classes and public methods have docstrings
[ ] Test coverage       — critical methods have unit tests

TESTING
[ ] Independent         — tests do not depend on each other or on run order
[ ] Clear test names    — each test name says what behaviour it checks
[ ] Right assertions    — tests assert the actual expected result
[ ] Edge cases          — boundaries are tested (zero, empty, max)
[ ] Error cases         — invalid input is tested for the correct exception
[ ] Realistic data      — controlled, representative test data is used

ACCEPTANCE
[ ] User stories        — each feature traces to "As a ... I want ... so that ..."
[ ] Given/When/Then     — acceptance criteria are written and pass as tests
[ ] Levels covered      — unit, subsystem (integration) AND system tested (U-S-S)
```

### Listing 5 — A Given / When / Then acceptance test (user story in the docstring)
```python
import unittest


class TestStudentRegistrationAcceptance(unittest.TestCase):
    """Acceptance tests — does the feature meet the USER's agreed criteria?"""

    def setUp(self):
        self.student_mgr = StudentManager()

    def test_register_a_new_student(self):
        """
        User Story:
            As a registrar, I want to add a new student
            so that they can enrol in courses.

        Acceptance Criteria (Given / When / Then):
            GIVEN a new student's details (a unique id, a name, an email)
            WHEN  I add the student to the system
            THEN  the system confirms success
            AND   I can afterwards retrieve the student's correct details
        """
        # GIVEN — the starting context (mirrors setUp / a known state)
        student_id, name, email = "S001", "Alice Johnson", "alice@university.edu"

        # WHEN — the action under test
        result = self.student_mgr.add_student(student_id, name, email)

        # THEN — the expected outcome, as assertions
        self.assertTrue(result.success)
        student = self.student_mgr.find_student(student_id)
        self.assertEqual(student.name, name)
        self.assertEqual(student.email, email)

    def test_reject_duplicate_student_id(self):
        """
        User Story:
            As a registrar, I want duplicate student ids prevented
            so that every student has a unique identity.

        Acceptance Criteria (Given / When / Then):
            GIVEN a student already exists in the system
            WHEN  I try to add another student with the same id
            THEN  the operation is rejected with a clear error
            AND   the original student's data is unchanged
        """
        # GIVEN
        self.student_mgr.add_student("S001", "Alice", "alice@uni.edu")

        # WHEN / THEN — the action must be rejected
        with self.assertRaises(ValueError) as ctx:
            self.student_mgr.add_student("S001", "Bob", "bob@uni.edu")
        self.assertIn("already exists", str(ctx.exception))

        # AND — the original is untouched
        self.assertEqual(self.student_mgr.find_student("S001").name, "Alice")
```
