---
title: "Supplementary Materials — Design Process: Task Definition and Decomposition"
module: OOP11
year: 11
lesson: "5.6"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration points at each listing by label.

### Listing 1 — Requirements → responsibilities (Library Management System)

```text
LIBRARY MANAGEMENT SYSTEM — DESIGN PROCESS, STAGES 1 & 2
========================================================

STAGE 1 — REQUIREMENTS
----------------------
Functional (WHAT the system does)        | Non-functional (HOW WELL it does it)
-----------------------------------------|-------------------------------------
Members can borrow and return books      | Search returns in under 2 seconds
Librarians add/remove books in inventory | Supports up to 1000 concurrent users
System tracks due dates and fines        | 99.9% uptime (availability)
Members search by title/author/category  | Interface is easy to use (usability)
System generates overdue notices         |

(Tell: response time, concurrency, uptime = non-functional. A feature = functional.)

STAGE 2 — RESPONSIBILITIES  (nouns -> classes, verbs -> methods; "who is responsible?")
--------------------------------------------------------------------------------------
Requirement                       -> Responsibility            -> Owning class (method)
----------------------------------------------------------------------------------------
A member may borrow more books    -> decide if borrowing allowed -> Member.can_borrow()
A book may be overdue             -> know its own due status      -> Book.is_overdue()
Coordinate a borrow request       -> validate + lend + notify     -> Library.borrow_book()
A book may be reserved/available  -> track its own availability   -> Book.is_available
Track what a member has out       -> hold the member's loans      -> Member.borrowed_books

Nouns found: Member, Book, Librarian, Library  -> candidate CLASSES
Verbs found: borrow, return, add, search, calculate -> candidate METHODS
Judgement call: calculate_fine() placed on Library — it is a coordination
responsibility needing the overdue duration (Book) under library policy (Library).
```

### Listing 2 — A LibraryFacade fronting three subsystems

```python
from datetime import datetime, timedelta


# ---- The messy "back office": three independent subsystems -------------------

class ValidationSubsystem:
    """Knows the borrowing rules. Nothing else does."""
    def member_can_borrow(self, member):
        return len(member.borrowed_books) < 5 and member.fines_owed < 10.0

    def book_is_available(self, book):
        return book.is_available


class InventorySubsystem:
    """Owns the act of moving a book in/out of the collection."""
    def mark_borrowed(self, book, member, loan_days=14):
        book.is_available = False
        book.borrowed_by = member.member_id
        book.due_date = datetime.now() + timedelta(days=loan_days)
        member.borrowed_books.append(book)


class NotificationSubsystem:
    """Owns talking to the member."""
    def confirm_loan(self, member, book):
        return f"Hi {member.name}, you borrowed '{book.title}'. Due {book.due_date:%d %b}."

    def schedule_due_reminder(self, member, book):
        # In a real system: queue a reminder job for (due_date - 2 days)
        return True


# ---- The "tidy front desk": ONE simple interface over all three --------------

class LibraryFacade:
    """
    Facade pattern: one front-of-house class hiding a messy subsystem.
    The client calls ONE method, borrow(). It coordinates validation,
    inventory and notification internally. The complexity is HIDDEN, not removed.
    """
    def __init__(self):
        self._validation = ValidationSubsystem()
        self._inventory = InventorySubsystem()
        self._notifications = NotificationSubsystem()

    def borrow(self, member, book):
        # The whole subsystem dance, behind one clean call.
        if not self._validation.member_can_borrow(member):
            return False, "Member cannot borrow more books"
        if not self._validation.book_is_available(book):
            return False, "Book is not available"

        self._inventory.mark_borrowed(book, member)
        message = self._notifications.confirm_loan(member, book)
        self._notifications.schedule_due_reminder(member, book)
        return True, message


# ---- Client code only ever sees the facade ----------------------------------
# library = LibraryFacade()
# ok, msg = library.borrow(alice, hobbit)     # one line; subsystems are invisible
```

### Listing 3 — NESA pseudocode: the Library coordinating the subsystem in one operation

```text
BEGIN BorrowBook(member, book)
    # Facade coordinates the validation, inventory and notification subsystems

    # 1. Validation subsystem
    IF member.borrowedCount >= 5 OR member.finesOwed >= 10.0 THEN
        RETURN False, "Member cannot borrow more books"
    ENDIF
    IF book.isAvailable = False THEN
        RETURN False, "Book is not available"
    ENDIF

    # 2. Inventory subsystem
    book.isAvailable ← False
    book.borrowedBy ← member.memberID
    book.dueDate ← TODAY + 14
    member.borrowedCount ← member.borrowedCount + 1

    # 3. Notification subsystem
    SEND confirmation TO member
    SCHEDULE dueReminder FOR (book.dueDate - 2)

    RETURN True, "Book borrowed successfully"
END BorrowBook
```

### Listing 4 — Responsibilities on the right class (Member, Book) in NESA pseudocode

```text
BEGIN Member.CanBorrow()
    # Member answers a question about the member's OWN state (encapsulation)
    IF borrowedCount < 5 AND finesOwed < 10.0 THEN
        RETURN True
    ELSE
        RETURN False
    ENDIF
END Member.CanBorrow

BEGIN Book.IsOverdue()
    # Book answers a question about the book's OWN state
    IF dueDate ≠ NONE AND TODAY > dueDate THEN
        RETURN True
    ELSE
        RETURN False
    ENDIF
END Book.IsOverdue
```
