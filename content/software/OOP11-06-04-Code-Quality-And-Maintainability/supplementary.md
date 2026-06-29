---
title: "Supplementary Materials — Code Quality and Maintainability"
module: OOP11
year: 11
lesson: "6.4"
script: script.md
---

# Supplementary Materials

Code listings for this episode. Nothing here is spoken in the audio — it's the read-along
reference. Every listing is referenced from the narration by its label. All code is Python.

### Listing 1 — Meaningful names: cryptic vs clear (the rewrite centrepiece)
```python
# ---- BEFORE: works, but unreadable ----
class C:
    def __init__(self, n, a, b):
        self.n = n
        self.a = a
        self.b = b

    def calc(self):
        return self.b - self.a

# Usage — no idea what any of this means
c = C("John", 1000, 1500)
result = c.calc()


# ---- AFTER: identical behaviour, self-documenting ----
class BankAccount:
    def __init__(self, account_holder, opening_balance, current_balance):
        self.account_holder = account_holder
        self.opening_balance = opening_balance
        self.current_balance = current_balance

    def calculate_net_change(self):
        return self.current_balance - self.opening_balance

# Usage — the names tell the story
account = BankAccount("John", 1000, 1500)
net_change = account.calculate_net_change()
```

### Listing 2 — Docstring template and the four conventions in one class
```python
# The four naming conventions:
#   Classes        -> PascalCase            (BankAccount, StudentRecord)
#   Methods/vars   -> snake_case            (calculate_total, student_name)
#   Constants      -> UPPER_SNAKE_CASE      (MAX_LOGIN_ATTEMPTS, DEFAULT_TIMEOUT)
#   Internal       -> _leading_underscore   (_loan_date — "don't touch from outside")

def method_name(parameter1, parameter2):
    """
    One-line summary of what the method does.

    Args:
        parameter1 (type): Description of parameter1.
        parameter2 (type): Description of parameter2.

    Returns:
        type: Description of what is returned.

    Raises:
        ExceptionType: The condition under which this exception is raised.
    """
    ...


class Student:
    """
    Represents a student with academic records and grade calculations.

    Manages personal details, enrolled subjects, and grade calculations.
    """

    MAX_GRADE = 100          # constant: shouted in UPPER_SNAKE_CASE
    MIN_GRADE = 0

    def __init__(self, student_id, name, email):
        """
        Initialise a new Student.

        Args:
            student_id (str): Unique identifier for the student.
            name (str): Full name of the student.
            email (str): Student's email address.
        """
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = {}

    def add_grade(self, subject, grade):
        """
        Record a grade for a subject.

        Args:
            subject (str): Name of the subject.
            grade (float): Grade value between MIN_GRADE and MAX_GRADE.

        Raises:
            ValueError: If grade is outside the valid range.
        """
        if not self.MIN_GRADE <= grade <= self.MAX_GRADE:
            raise ValueError("Grade must be between 0 and 100")
        self.grades[subject] = grade
```

### Listing 3 — Comments: restating the what (weak) vs explaining the why (strong)
```python
# ---- WEAK: comments restate the code (redundant, can go stale) ----
i += 1                          # add one to the counter
if self.balance > amount:       # check if balance is greater than amount
    self.balance -= amount      # subtract amount from balance


# ---- STRONG: comments explain WHY — context the code can't show ----

# Standard compound-interest formula:
#   A = P * (1 + r/n) ** (n*t)
#   P = principal, r = annual rate, n = compounds/year, t = years
final_amount = principal * (1 + annual_rate / compounds_per_year) ** (compounds_per_year * years)

# Business rule: a minimum balance of $10 must be maintained at all times.
if self.balance - amount >= MINIMUM_BALANCE:
    self.balance -= amount
else:
    raise InsufficientFundsError("Transaction would breach the minimum balance")
```

### Listing 4 — Extract Method: one long method vs a short coordinator
```python
# ---- BEFORE: one method doing many distinct tasks ----
def process_order(self, order_items, customer_info, payment_info):
    # validate customer
    if not customer_info.get("name"):
        raise ValueError("Customer name is required")
    if "@" not in customer_info.get("email", ""):
        raise ValueError("Invalid email format")
    # calculate subtotal
    subtotal = 0
    for item in order_items:
        if item["quantity"] <= 0 or item["price"] <= 0:
            raise ValueError("Item quantity and price must be positive")
        subtotal += item["quantity"] * item["price"]
    # apply discount
    discount = 0
    if subtotal > 100:
        discount = subtotal * 0.1
    elif subtotal > 50:
        discount = subtotal * 0.05
    # calculate tax
    tax = (subtotal - discount) * 0.1
    total = subtotal - discount + tax
    # process payment ...
    return total


# ---- AFTER: each task extracted; the original reads like a table of contents ----
class OrderProcessor:
    """Processes a customer order through small, focused steps."""

    def process_order(self, order_items, customer_info, payment_info):
        """
        Process a customer order and return the confirmation details.

        Args:
            order_items (list): Items being ordered.
            customer_info (dict): Customer details.
            payment_info (dict): Payment details.

        Returns:
            dict: Order confirmation with subtotal, discount, tax and total.
        """
        self._validate_customer_info(customer_info)
        subtotal = self._calculate_subtotal(order_items)
        discount = self._calculate_discount(subtotal)
        tax = self._calculate_tax(subtotal, discount)
        total = subtotal - discount + tax
        self._process_payment(payment_info, total)
        return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": total}

    def _validate_customer_info(self, customer_info):
        """Validate that customer details are present and well-formed."""
        if not customer_info.get("name"):
            raise ValueError("Customer name is required")
        if "@" not in customer_info.get("email", ""):
            raise ValueError("Valid email is required")

    def _calculate_subtotal(self, order_items):
        """Sum the line totals, validating each item."""
        subtotal = 0
        for item in order_items:
            self._validate_item(item)
            subtotal += item["quantity"] * item["price"]
        return subtotal

    def _validate_item(self, item):
        """Validate a single order line."""
        if item["quantity"] <= 0 or item["price"] <= 0:
            raise ValueError("Item quantity and price must be positive")

    def _calculate_discount(self, subtotal):
        """Apply the tiered discount rules to the subtotal."""
        if subtotal > 100:
            return subtotal * 0.1
        if subtotal > 50:
            return subtotal * 0.05
        return 0

    def _calculate_tax(self, subtotal, discount):
        """Apply tax to the discounted amount."""
        TAX_RATE = 0.1
        return (subtotal - discount) * TAX_RATE

    def _process_payment(self, payment_info, amount):
        """Process payment of the given amount (stubbed)."""
        ...
```

### Listing 5 — Replace Magic Numbers with Named Constants (library late-fee calculator)
```python
# ---- BEFORE: magic numbers — what are 7, 30, 0.5, 1.0, 2.0? ----
def calculate_late_fee(self, days_late):
    if days_late <= 7:
        return days_late * 0.5
    elif days_late <= 30:
        return 7 * 0.5 + (days_late - 7) * 1.0
    else:
        return 7 * 0.5 + 23 * 1.0 + (days_late - 30) * 2.0


# ---- AFTER: named constants — the logic now reads like English ----
class LibraryFeeCalculator:
    """Calculates overdue library fees using a tiered daily rate."""

    # One source of truth for every threshold and rate.
    GRACE_PERIOD_DAYS = 7        # days charged at the lowest rate
    STANDARD_PERIOD_DAYS = 30    # end of the standard tier

    GRACE_PERIOD_FEE_PER_DAY = 0.5
    STANDARD_FEE_PER_DAY = 1.0
    EXTENDED_FEE_PER_DAY = 2.0

    def calculate_late_fee(self, days_late):
        """
        Calculate the overdue fee for a book returned `days_late` days late.

        Args:
            days_late (int): Number of days the book is overdue.

        Returns:
            float: The total fee owed.
        """
        if days_late <= self.GRACE_PERIOD_DAYS:
            return days_late * self.GRACE_PERIOD_FEE_PER_DAY

        if days_late <= self.STANDARD_PERIOD_DAYS:
            grace_fee = self.GRACE_PERIOD_DAYS * self.GRACE_PERIOD_FEE_PER_DAY
            standard_days = days_late - self.GRACE_PERIOD_DAYS
            return grace_fee + standard_days * self.STANDARD_FEE_PER_DAY

        grace_fee = self.GRACE_PERIOD_DAYS * self.GRACE_PERIOD_FEE_PER_DAY
        standard_days = self.STANDARD_PERIOD_DAYS - self.GRACE_PERIOD_DAYS
        standard_fee = standard_days * self.STANDARD_FEE_PER_DAY
        extended_days = days_late - self.STANDARD_PERIOD_DAYS
        extended_fee = extended_days * self.EXTENDED_FEE_PER_DAY
        return grace_fee + standard_fee + extended_fee
```

### Listing 6 — The maintainability checklist (Name it · Document it · Size it · Structure it)
```text
MAINTAINABILITY CHECKLIST

NAME IT — naming and readability
  [ ] Classes use PascalCase and clearly describe what the class represents.
  [ ] Methods and variables use snake_case and describe what they do.
  [ ] Constants use UPPER_SNAKE_CASE and have meaningful names.
  [ ] Internal-only names carry a single leading underscore.
  [ ] Names are descriptive; no cryptic abbreviations.

DOCUMENT IT — documentation
  [ ] Every class has a docstring explaining its purpose.
  [ ] Every public method has a docstring with Args, Returns, Raises.
  [ ] Comments explain WHY, not WHAT.
  [ ] Business rules and non-obvious algorithms are documented.

SIZE IT — method design
  [ ] Each method has a single responsibility.
  [ ] Methods are generally fewer than ~20 lines.
  [ ] Parameter lists are reasonable (typically 4 or fewer).
  [ ] Methods have clear return values and error handling.

STRUCTURE IT — code structure
  [ ] Magic numbers are replaced with named constants.
  [ ] Repeated code is extracted into reusable methods.
  [ ] Complex conditionals are simplified or extracted.
  [ ] Version control is used; the project is backed up regularly.

EXAM USE: "List four features of maintainable code" -> take ONE from each
group (Name / Document / Size / Structure) for four genuinely distinct marks.
```
