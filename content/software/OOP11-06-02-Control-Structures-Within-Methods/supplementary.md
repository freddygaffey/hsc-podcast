---
title: "Supplementary Materials — Control Structures Within Methods"
module: OOP11
year: 11
lesson: "6.2"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. Every listing is referenced from the narration by
its label.

### Listing 1 — Order processor: one giant method (bad) versus extracted helpers (good)
```python
class OrderProcessor:
    """The centrepiece: the same job written two ways."""

    def __init__(self):
        self.orders = []
        self.inventory = {}    # {item_name: quantity}
        self.customers = {}    # {customer_id: {"active": bool, "vip": bool}}

    # ---- BAD: one method doing everything (validate + check + price +
    #      discount + update + record). ~60 lines, three loops, low cohesion.
    def process_order_bad(self, customer_id, items):
        # Validate customer
        if customer_id not in self.customers:
            return False, "Invalid customer"
        customer = self.customers[customer_id]
        if not customer.get("active", False):
            return False, "Inactive customer"

        # Check inventory
        for item_name, quantity in items.items():
            if item_name not in self.inventory:
                return False, f"Item {item_name} not found"
            if self.inventory[item_name] < quantity:
                return False, f"Insufficient stock for {item_name}"

        # Calculate pricing
        total = 0
        for item_name, quantity in items.items():
            total += self.get_item_price(item_name) * quantity

        # Apply discounts
        if customer.get("vip", False):
            total *= 0.9      # 10% VIP discount
        if total > 100:
            total *= 0.95     # 5% bulk discount

        # Update inventory
        for item_name, quantity in items.items():
            self.inventory[item_name] -= quantity

        # Create order record
        order = {"customer_id": customer_id, "items": items,
                 "total": total, "status": "confirmed"}
        self.orders.append(order)
        return True, f"Order processed. Total: ${total:.2f}"

    # ---- GOOD: a short coordinator that reads like a table of contents,
    #      delegating each single responsibility to a focused private helper.
    def process_order_good(self, customer_id, items):
        if not self._validate_customer(customer_id):
            return False, "Customer validation failed"
        if not self._check_inventory_availability(items):
            return False, "Inventory check failed"

        total = self._calculate_order_total(customer_id, items)
        self._update_inventory(items)
        self._create_order_record(customer_id, items, total)
        return True, f"Order processed. Total: ${total:.2f}"

    def _validate_customer(self, customer_id):
        """One job: is this a known, active customer?"""
        if customer_id not in self.customers:
            return False
        return self.customers[customer_id].get("active", False)

    def _check_inventory_availability(self, items):
        """One job: is every item in stock in the required quantity?"""
        for item_name, quantity in items.items():
            if item_name not in self.inventory:
                return False
            if self.inventory[item_name] < quantity:
                return False
        return True

    def _calculate_order_total(self, customer_id, items):
        """One job: base total, then discounts."""
        total = sum(self.get_item_price(name) * qty
                    for name, qty in items.items())
        if self.customers[customer_id].get("vip", False):
            total *= 0.9
        if total > 100:
            total *= 0.95
        return total

    def _update_inventory(self, items):
        """One job: deduct purchased quantities."""
        for item_name, quantity in items.items():
            self.inventory[item_name] -= quantity

    def _create_order_record(self, customer_id, items, total):
        """One job: build and store the order record."""
        order = {"customer_id": customer_id, "items": items,
                 "total": total, "status": "confirmed"}
        self.orders.append(order)
        return order

    def get_item_price(self, item_name):
        prices = {"laptop": 999, "mouse": 25, "keyboard": 75}
        return prices.get(item_name, 0)
```

### Listing 2 — Guard-clause `withdraw`: early returns instead of nested ifs
```python
class BankAccount:
    """Selection inside a method, driven by the object's own state."""

    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.balance = initial_balance
        self.is_frozen = False

    # WEAK: nested ifs — the "arrow of doom" (shown for contrast).
    def withdraw_nested(self, amount):
        if not self.is_frozen:
            if amount > 0:
                if amount <= self.balance:
                    self.balance -= amount
                    return True, f"Withdrew ${amount}. Balance: ${self.balance}"
                else:
                    return False, "Insufficient funds"
            else:
                return False, "Amount must be positive"
        else:
            return False, "Account is frozen"

    # STRONG: guard clauses — each failure handled and dismissed up front,
    # so the success path sits flat and unindented at the bottom.
    def withdraw(self, amount):
        if self.is_frozen:                 # guard: object state
            return False, "Account is frozen"
        if amount <= 0:                    # guard: parameter
            return False, "Amount must be positive"
        if amount > self.balance:          # guard: state vs parameter
            return False, "Insufficient funds"

        # Happy path — flat, readable, one level of indentation.
        self.balance -= amount
        return True, f"Withdrew ${amount}. Balance: ${self.balance}"
```

### Listing 3 — NESA pseudocode for the validated order flow (the good version)
```text
BEGIN ProcessOrder(customerId, items)
    IF NOT ValidateCustomer(customerId) THEN
        RETURN False, "Customer validation failed"
    ENDIF

    IF NOT CheckInventoryAvailability(items) THEN
        RETURN False, "Inventory check failed"
    ENDIF

    total ← CalculateOrderTotal(customerId, items)
    UpdateInventory(items)
    CreateOrderRecord(customerId, items, total)

    RETURN True, "Order processed"
END ProcessOrder

BEGIN ValidateCustomer(customerId)
    IF customerId NOT IN customers THEN
        RETURN False
    ENDIF
    RETURN customers[customerId].active
END ValidateCustomer

BEGIN CheckInventoryAvailability(items)
    FOR each itemName, quantity IN items
        IF itemName NOT IN inventory THEN
            RETURN False
        ENDIF
        IF inventory[itemName] < quantity THEN
            RETURN False
        ENDIF
    NEXT itemName
    RETURN True
END CheckInventoryAvailability
```

### Listing 4 — For-loops over an object's own data structures (inventory report)
```python
class Inventory:
    """Definite iteration: visit every item in the collection once."""

    def __init__(self):
        self.items = {}     # {item_name: quantity}
        self.prices = {}    # {item_name: price}

    def add_item(self, name, quantity, price):
        self.items[name] = self.items.get(name, 0) + quantity
        self.prices[name] = price

    def calculate_total_value(self):
        """For-loop accumulating a running total."""
        total_value = 0
        for item_name, quantity in self.items.items():
            if item_name in self.prices:
                total_value += quantity * self.prices[item_name]
        return total_value

    def find_low_stock_items(self, threshold=10):
        """For-loop collecting items below a stock threshold."""
        low_stock = []
        for item_name, quantity in self.items.items():
            if quantity < threshold:
                low_stock.append({
                    "name": item_name,
                    "quantity": quantity,
                    "price": self.prices.get(item_name, 0),
                })
        return low_stock
```

### Listing 5 — Safety-limited while loop (indefinite iteration with a guaranteed exit)
```python
class Queue:
    """Indefinite iteration: a while loop that MUST be able to terminate."""

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def process_all_items(self, processor_func, max_iterations=100):
        """Drain the queue, but with a safety limit so a bug in
        processor_func (e.g. one that re-enqueues) can't hang the program."""
        processed_count = 0
        iterations = 0

        # Two-part condition: the real condition AND the safety cap.
        while self.items and iterations < max_iterations:
            item = self.dequeue()
            if item is not None:
                processor_func(item)
                processed_count += 1
            iterations += 1   # the circuit breaker increments every pass

        return processed_count
```

### Listing 6 — NESA pseudocode: a while loop with an explicit safety limit
```text
BEGIN ProcessAllItems(processorFunc, maxIterations)
    processedCount ← 0
    iterations ← 0

    WHILE queue is not empty AND iterations < maxIterations
        item ← Dequeue()
        IF item ≠ NULL THEN
            processorFunc(item)
            processedCount ← processedCount + 1
        ENDIF
        iterations ← iterations + 1
    ENDWHILE

    RETURN processedCount
END ProcessAllItems
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
