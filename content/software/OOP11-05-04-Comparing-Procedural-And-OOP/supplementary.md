---
title: "Supplementary Materials — Comparing Procedural Programming and OOP"
module: OOP11
year: 11
lesson: "5.4"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. Every listing is referenced from the narration by
its label.

### Listing 1 — The same Rectangle, procedural vs OOP (side by side)
```python
# ---------- PROCEDURAL: data and functions live apart ----------
# length and width are loose values, passed into every function.

def calculate_area(length, width):
    return length * width

def calculate_perimeter(length, width):
    return 2 * (length + width)

def display_info(length, width):
    print(f"Rectangle: {length}x{width}")
    print(f"Area: {calculate_area(length, width)}")
    print(f"Perimeter: {calculate_perimeter(length, width)}")

rect_length = 5          # data sits outside the functions
rect_width = 3
display_info(rect_length, rect_width)


# ---------- OBJECT-ORIENTED: data walks with its methods ----------
# length and width live inside the object; methods reach into their own data.

class Rectangle:
    def __init__(self, length, width):
        self.length = length     # data belongs to the object
        self.width = width

    def calculate_area(self):
        return self.length * self.width

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)

    def display_info(self):
        print(f"Rectangle: {self.length}x{self.width}")
        print(f"Area: {self.calculate_area()}")
        print(f"Perimeter: {self.calculate_perimeter()}")

rect = Rectangle(5, 3)   # the object holds its own dimensions
rect.display_info()
```

### Listing 2 — The trade-offs, lined up by dimension
```text
DIMENSION          PROCEDURAL                      OBJECT-ORIENTED
-----------------  ------------------------------  ------------------------------
Organisation       functions operate on data       objects bundle data + methods
Data handling      global or passed as parameters  encapsulated inside objects
Problem approach   top-down decomposition          identify objects + interactions
Code reuse         function libraries              inheritance and composition
Modularity         separate functions              classes with clear interfaces
State management   external / global variables     object state managed internally

Every row is a consequence of ONE sentence:
  Procedural: data and functions live apart.
  OOP:        data walks with its methods.
```

### Listing 3 — Keep procedural: a one-shot tax calculation
```python
# A simple calculation. Clear input, clear output, no state to carry.
# Wrapping this in a class would add ceremony and buy nothing.

def calculate_tax(income, tax_rate):
    return income * tax_rate

def calculate_net_income(gross_income, tax_rate):
    tax = calculate_tax(gross_income, tax_rate)
    return gross_income - tax

net = calculate_net_income(50000, 0.25)
```

### Listing 4 — Keep procedural: pure algorithms (factorial, Fibonacci)
```python
# Pure functions: input in, output out. No entity, no state to model.

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Listing 5 — Go OOP: modelling real-world entities (Student, Course)
```python
# Entities with their own data AND behaviour → objects fit naturally.

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = []

    def add_grade(self, grade):
        if 0 <= grade <= 100:
            self.grades.append(grade)

    def get_average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0


class Course:
    def __init__(self, course_name):
        self.course_name = course_name
        self.students = []

    def enroll_student(self, student):
        self.students.append(student)

    def get_class_average(self):
        if not self.students:
            return 0
        total = sum(s.get_average() for s in self.students)
        return total / len(self.students)
```

### Listing 6 — Go OOP: interacting components (BankAccount, Bank)
```python
# Multiple objects collaborating, each guarding its own data.

class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposit: +${amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawal: -${amount}")
            return True
        return False


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, initial_deposit=0):
        account = BankAccount(account_number, initial_deposit)
        self.accounts[account_number] = account
        return account

    def transfer_money(self, from_account, to_account, amount):
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            return True
        return False
```

### Listing 7 — The symptom: a giant parameter list crying out for a class
```python
# Loose related variables → the function needs SIX parameters to do anything.
# Player's three values are one object; enemy's three are another.

player_name = "Alice"
player_health = 100
player_level = 5
enemy_name = "Dragon"
enemy_health = 200
enemy_level = 8

def battle(p_name, p_health, p_level, e_name, e_health, e_level):
    # Six loose parameters = data that travels together,
    # begging to be wrapped into a Player object and an Enemy object,
    # so this becomes:  battle(player, enemy)
    pass
```

### Listing 8 — Converting procedural to OOP (before / after)
```python
# ---------- BEFORE (procedural): scattered data + free functions ----------
customer_name = "John Doe"
customer_email = "john@email.com"
customer_orders = []

def add_order(orders_list, order):
    orders_list.append(order)

def get_total_spent(orders_list):
    return sum(order['amount'] for order in orders_list)

def send_email(email, message):
    print(f"Sending to {email}: {message}")


# ---------- AFTER (OOP): the 3-step conversion ----------
# Step 1: find the data that travels together  -> name, email, orders
# Step 2: wrap it in a class                   -> Customer
# Step 3: turn the functions into methods      -> add_order / get_total_spent / send_email

class Customer:
    def __init__(self, name, email):
        self.name = name            # data that travels together,
        self.email = email          # now held by the object
        self.orders = []

    def add_order(self, order):                  # function -> method
        self.orders.append(order)

    def get_total_spent(self):                   # function -> method
        return sum(order['amount'] for order in self.orders)

    def send_email(self, message):               # function -> method
        print(f"Sending to {self.email}: {message}")

customer = Customer("John Doe", "john@email.com")
customer.add_order({'item': 'Book', 'amount': 25})
total = customer.get_total_spent()
customer.send_email(f"Your total spending: ${total}")
```

### Listing 9 — OOP overkill: when a class is the wrong choice
```python
# A trivial calculator does NOT need to be an object.
# This is over-engineering: more code, no benefit.

class Calculator:
    def add(self, a, b):
        return a + b
    def subtract(self, a, b):
        return a - b

# When a plain function would do:
def add(a, b):
    return a + b
```

### Listing 10 — NESA pseudocode: the procedural→OOP conversion as an algorithm
```text
BEGIN ConvertProceduralToOOP
    # Step 1 — find the data that travels together
    FOR each group of variables that always describe the same thing
        RECORD them as one candidate set of attributes
    NEXT group

    # Step 2 — wrap each set in a class
    FOR each candidate set
        DEFINE a class
        FOR each variable IN the set
            ADD it as an attribute, set in the constructor
        NEXT variable
    NEXT set

    # Step 3 — turn the functions into methods
    FOR each function that operated on that data
        MOVE it INTO the matching class AS a method
        REPLACE its data parameters WITH the object's own attributes (self)
    NEXT function
END ConvertProceduralToOOP
```

### Listing 11 — NESA pseudocode: the same operation, procedural vs method
```text
# PROCEDURAL — data passed in as parameters
BEGIN GetTotalSpent(ordersList)
    total ← 0
    FOR each order IN ordersList
        total ← total + order.amount
    NEXT order
    RETURN total
END GetTotalSpent

# OBJECT-ORIENTED — a method reaching into its own object's data
BEGIN Customer.GetTotalSpent()
    total ← 0
    FOR each order IN self.orders
        total ← total + order.amount
    NEXT order
    RETURN total
END Customer.GetTotalSpent
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| OOP | Object-Oriented Programming | A paradigm structuring software around objects that bundle data and behaviour |
