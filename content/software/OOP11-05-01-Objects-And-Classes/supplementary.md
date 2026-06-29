---
title: "Supplementary Materials — Objects, Classes and Message-Passing"
module: OOP11
year: 11
lesson: "5.1"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration refers to each item by its label
only.

### Listing 1 — The `BankAccount` class (the blueprint)
```python
class BankAccount:
    """A simple bank account. This is the blueprint — the class."""

    def __init__(self, account_number, owner_name, initial_balance=0):
        # Attributes (the object's data / state)
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = initial_balance

    def deposit(self, amount):
        """A method (behaviour) — receives a 'deposit' message."""
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: ${self.balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount):
        """A method (behaviour) — receives a 'withdraw' message."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Insufficient funds or invalid amount"

    def check_balance(self):
        """A simple getter method."""
        return f"Current balance: ${self.balance}"
```

### Listing 2 — Two instances, and message-passing
```python
# BankAccount is the class (blueprint).
# alice_account and bob_account are two instances built from it,
# each holding its own data.
alice_account = BankAccount("ACC001", "Alice Smith", 1000)
bob_account = BankAccount("ACC002", "Bob Jones", 500)

# Message-passing: calling a method IS sending a message to an object.
result = alice_account.deposit(200)   # send "deposit" message to Alice's object
print(result)                         # Deposited $200. New balance: $1200

result = bob_account.withdraw(100)    # send "withdraw" message to Bob's object
print(result)                         # Withdrew $100. New balance: $400

# What Python does internally when you write alice_account.deposit(200):
#   1. Lookup  — find deposit() on the BankAccount class
#   2. Bind    — pass alice_account in as the first parameter, self
#   3. Pass    — pass 200 in as the parameter `amount`
#   4. Execute — run the body using self.balance (Alice's balance)
#   5. Return  — hand the result back to the caller
# i.e.  BankAccount.deposit(alice_account, 200)   <-- written as  alice_account.deposit(200)
```

### Listing 3 — `Deposit` as a class method, in NESA pseudocode
```text
BEGIN Deposit(self, amount)
    IF amount > 0 THEN
        self.balance ← self.balance + amount
        RETURN "Deposited " + amount + ". New balance: " + self.balance
    ELSE
        RETURN "Invalid deposit amount"
    ENDIF
END Deposit
```

### Listing 4 — Message-passing dispatch (the five L-B-P-E-R steps) in NESA pseudocode
```text
BEGIN SendMessage(receiver, messageName, arguments)
    method ← LOOKUP messageName ON CLASS OF receiver   // L — Lookup
    self ← receiver                                    // B — Bind self automatically
    PASS arguments TO method parameters                // P — Pass parameters
    result ← EXECUTE method USING self                 // E — Execute with access to state
    RETURN result                                      // R — Return to the caller
END SendMessage
```
