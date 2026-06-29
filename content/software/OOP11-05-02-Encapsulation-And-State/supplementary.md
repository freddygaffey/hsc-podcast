---
title: "Supplementary Materials — Encapsulation and State"
module: OOP11
year: 11
lesson: "5.2"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration refers to each item by its label
only.

### Listing 1 — `BankAccount` with a protected `_balance` and validating methods
```python
class BankAccount:
    """The 05-01 BankAccount, upgraded for encapsulation.

    Invariant: self._balance >= 0 must ALWAYS be true for a valid account.
    The balance is now internal (_balance) and can only change through the
    validating deposit() / withdraw() methods, which protect the invariant.
    """

    def __init__(self, account_number, owner_name, initial_balance=0):
        self.account_number = account_number   # public — fine to read
        self.owner_name = owner_name            # public — fine to read
        self._balance = 0                       # internal state (protected by convention)
        self._transaction_count = 0             # internal state kept in sync
        # Only a positive starting balance is accepted; anything else leaves
        # the balance at the safe default of 0, so the invariant holds from creation.
        if initial_balance > 0:
            self.deposit(initial_balance)

    # ---- public interface: the approved ways to change the account ----

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._transaction_count += 1        # consistency: count stays in sync
            return f"Deposited ${amount}. Balance: ${self._balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount):
        # The guard that enforces the invariant balance >= 0:
        if 0 < amount <= self._balance:
            self._balance -= amount
            self._transaction_count += 1
            return f"Withdrew ${amount}. Balance: ${self._balance}"
        return "Insufficient funds or invalid amount"

    def get_balance(self):                       # controlled read access (a getter)
        return self._balance


# --- The bug encapsulation is designed to prevent ---
account = BankAccount("ACC001", "Alice Smith", 1000)
print(account.get_balance())   # 1000  — read through the public interface  ✅
print(account.withdraw(2000))  # "Insufficient funds..." — invariant protected ✅

# Direct attribute access bypasses ALL of the above control:
account._balance = 999999      # ❌ bypasses validation — invariant no longer guaranteed
account._balance = -500        # ❌ object is now in an INVALID state (negative balance)
```

### Listing 2 — `Temperature`: a validating setter (absolute-zero guard) and a calculated getter
```python
class Temperature:
    """Invariant: _celsius >= -273.15 (cannot be below absolute zero)."""

    def __init__(self, celsius=0):
        self._celsius = 0
        self.set_celsius(celsius)   # validate even the initial value

    def get_celsius(self):
        return self._celsius

    def set_celsius(self, celsius):
        if celsius < -273.15:                       # the absolute-zero guard
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = celsius

    def get_fahrenheit(self):
        # A CALCULATED getter — no _fahrenheit attribute is stored;
        # it is derived from internal state on demand.
        return (self._celsius * 9 / 5) + 32

    def set_fahrenheit(self, fahrenheit):
        celsius = (fahrenheit - 32) * 5 / 9
        self.set_celsius(celsius)                    # reuse the same validation


temp = Temperature(25)
print(temp.get_fahrenheit())   # 77.0 — computed, not stored
temp.set_fahrenheit(86)
print(temp.get_celsius())      # 30.0
# temp.set_celsius(-300)       # would raise ValueError — invariant enforced
```

### Listing 3 — `Rectangle`: a positive-dimension invariant enforced via setters
```python
class Rectangle:
    """Invariant: width > 0 AND height > 0 for a valid rectangle."""

    def __init__(self, width, height):
        self._width = 0
        self._height = 0
        # Enforce the invariant from the moment the object is created
        # by routing construction through the validating setters.
        self.set_width(width)
        self.set_height(height)

    def set_width(self, width):
        if width > 0:
            self._width = width
        else:
            raise ValueError("Width must be positive")

    def set_height(self, height):
        if height > 0:
            self._height = height
        else:
            raise ValueError("Height must be positive")

    def get_area(self):
        # Trustworthy: the only values that ever got in were positive,
        # so the area is always valid — no defensive re-checking needed.
        return self._width * self._height


rect = Rectangle(5, 3)
print(rect.get_area())   # 15
# rect.set_width(-2)     # would raise ValueError — invariant protected
```

### Listing 4 — A validating `Withdraw` method in NESA pseudocode
```text
BEGIN Withdraw(self, amount)
    IF amount > 0 AND amount <= self._balance THEN
        self._balance ← self._balance - amount
        self._transactionCount ← self._transactionCount + 1
        RETURN "Withdrew " + amount + ". Balance: " + self._balance
    ELSE
        RETURN "Insufficient funds or invalid amount"
    ENDIF
END Withdraw
```

### Listing 5 — `Circle`: the `@property` decorator (getters/setters that look like attributes)
```python
class Circle:
    """The @property approach: validation hidden behind plain attribute syntax.

    `circle.radius = 3` LOOKS like a direct assignment but actually runs the
    setter (with validation). Reach for this only when there's an invariant to
    guard — a plain public attribute is correct when any value is fine.
    """

    def __init__(self, radius):
        self._radius = 0
        self.radius = radius          # goes through the property setter below

    @property
    def radius(self):                 # getter — accessed as circle.radius
        return self._radius

    @radius.setter
    def radius(self, value):          # setter — runs on circle.radius = ...
        if value <= 0:                # invariant: radius must be positive
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self):                   # a calculated, read-only property
        return 3.14159 * self._radius ** 2


circle = Circle(5)
print(circle.radius)   # 5     — looks like attribute access, runs the getter
print(circle.area)     # 78.53975  — computed on demand
circle.radius = 3      # runs the setter, with validation
# circle.radius = -1   # would raise ValueError — invariant enforced
```
