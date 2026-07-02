---
title: "Supplementary Materials — Building Classes and Composition"
module: OOP11
year: 11
lesson: "6.1"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration points at each listing by label.

### Listing 1 — A bank-account class with a validating constructor (Python)
```python
class BankAccount:
    """A bank account that refuses to be constructed in an invalid state."""

    def __init__(self, account_number, owner_name, initial_balance=0):
        # Validate BEFORE storing — the object must be born valid.
        if not account_number or not account_number.strip():
            raise ValueError("Account number cannot be empty")
        if not owner_name or not owner_name.strip():
            raise ValueError("Owner name cannot be empty")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        # All checks passed — set up the initial state.
        self.account_number = account_number.strip()
        self.owner_name = owner_name.strip()
        self.balance = initial_balance
        self.transaction_history = []
        if initial_balance > 0:
            self.transaction_history.append(f"Initial deposit: +${initial_balance}")

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        self.transaction_history.append(f"Deposit: +${amount}")

    def __str__(self):
        return f"Account {self.account_number}, owner {self.owner_name}, ${self.balance}"


# A good account is built; a broken one is rejected at construction time.
account = BankAccount("ACC001", "Alice Johnson", 1000)
try:
    bad = BankAccount("", "Bob", -100)   # raises ValueError on the first failed check (empty account number)
except ValueError as e:
    print(f"Rejected: {e}")
```

### Listing 2 — Composition spine: a Car *has-a* Engine and Wheels (Python)
```python
class Engine:
    """A small, cohesive component: it only knows about being an engine."""

    def __init__(self, horsepower, fuel_type):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            return f"{self.horsepower}hp {self.fuel_type} engine started"
        return "Engine already running"


class Wheels:
    def __init__(self, count, size_inches):
        self.count = count
        self.size_inches = size_inches

    def get_info(self):
        return f"{self.count} wheels, {self.size_inches} inch"


class Car:
    """Car uses COMPOSITION, not inheritance: a Car HAS-A Engine and HAS Wheels."""

    def __init__(self, make, model, engine, wheels):
        self.make = make
        self.model = model
        self.engine = engine      # has-a: injected, not inherited
        self.wheels = wheels      # has-a
        self.speed = 0

    def start(self):
        # Delegate to the component — the Car forwards the message to its Engine.
        return f"{self.make} {self.model}: {self.engine.start()}"


# Build the components, then hand them to the car (dependency injection).
v8 = Engine(400, "petrol")
standard_wheels = Wheels(4, 18)
sports_car = Car("Ferrari", "F40", v8, standard_wheels)
print(sports_car.start())
```

### Listing 3 — A Laptop composed of CPU, Display and Battery (Python)
```python
class CPU:
    def __init__(self, speed_ghz, cores):
        self.speed_ghz = speed_ghz
        self.cores = cores
        self.is_active = False

    def start(self):
        self.is_active = True
        return f"CPU: {self.cores} cores at {self.speed_ghz}GHz"

    def stop(self):
        self.is_active = False
        return "CPU stopped"


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        return f"Display on: {self.width}x{self.height}"

    def turn_off(self):
        self.is_on = False
        return "Display off"


class Battery:
    def __init__(self, capacity_mah):
        self.capacity_mah = capacity_mah
        self.charge = capacity_mah

    def percent(self):
        return (self.charge / self.capacity_mah) * 100

    def use(self, amount):
        self.charge = max(0, self.charge - amount)


class Laptop:
    """A Laptop HAS-A CPU, HAS-A Display and HAS-A Battery. It conducts; it is not a one-man band."""

    def __init__(self, brand, model, cpu, display, battery):
        self.brand = brand
        self.model = model
        self.cpu = cpu          # composition
        self.display = display  # composition
        self.battery = battery  # composition
        self.is_running = False

    def power_on(self):
        if self.battery.percent() < 5:
            return "Cannot power on: battery too low"
        self.is_running = True
        cpu_msg = self.cpu.start()
        display_msg = self.display.turn_on()
        self.battery.use(50)
        return f"{self.brand} {self.model} on. {cpu_msg}. {display_msg}."


# Components are built separately, then composed — swap any one without touching Laptop.
laptop = Laptop("Apple", "MacBook Pro", CPU(2.8, 4), Display(1920, 1080), Battery(5000))
print(laptop.power_on())
```

### Listing 4 — A shopping cart with an injected logger (dependency injection, Python)
```python
class ConsoleLogger:
    """One logging strategy: print to the screen."""
    def log(self, message):
        print(f"LOG: {message}")


class FileLogger:
    """Another strategy with the SAME interface: write to a file."""
    def __init__(self, filename):
        self.filename = filename

    def log(self, message):
        with open(self.filename, "a") as f:
            f.write(f"{message}\n")


class ShoppingCart:
    """The cart depends on a logger, but is given one from outside — dependency injection.
    It only ever calls logger.log(...), so any logger with that interface drops in."""

    def __init__(self, logger):
        self.items = []
        self.logger = logger          # injected dependency

    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})
        self.logger.log(f"Added {item} (${price})")

    def get_total(self):
        total = sum(i["price"] for i in self.items)
        self.logger.log(f"Total: ${total}")
        return total


# Same cart class, different behaviour — decided at construction time (polymorphism via injection).
cart_a = ShoppingCart(ConsoleLogger())       # logs to the screen
cart_b = ShoppingCart(FileLogger("cart.log"))  # logs to a file
cart_a.add_item("Book", 25.99)
cart_b.add_item("Phone", 699.99)
```

### Listing 5 — Refactoring a low-cohesion class into focused, composable classes (Python)
```python
# BEFORE — low cohesion: one "god class" doing five unrelated jobs.
class UserAccount:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.password_hash = None

    def set_password(self, password):          # user data — appropriate
        self.password_hash = hash(password)

    def send_welcome_email(self):              # email — should be its own class
        print(f"Sending welcome email to {self.email}")

    def save_to_file(self, filename):          # persistence — should be its own class
        with open(filename, "w") as f:
            f.write(f"{self.username},{self.email}")

    def save_to_database(self, connection):    # persistence — should be its own class
        pass

    def log_login_attempt(self, success):      # logging — should be its own class
        print(f"Login {self.username}: {'OK' if success else 'FAIL'}")


# AFTER — high cohesion: each class has ONE responsibility (R-R-C-I: a home per responsibility).
class User:
    """Just holds user data and checks passwords."""
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.password_hash = None

    def set_password(self, password):
        self.password_hash = hash(password)

    def check_password(self, password):
        return self.password_hash == hash(password)


class EmailService:
    """Just sends emails."""
    def send_welcome_email(self, user):
        print(f"Sending welcome email to {user.email}")


class UserRepository:
    """Just saves and loads users."""
    def save(self, user, filename):
        with open(filename, "w") as f:
            f.write(f"{user.username},{user.email}")


class LoginLogger:
    """Just records login attempts."""
    def log_attempt(self, username, success):
        print(f"Login {username}: {'OK' if success else 'FAIL'}")


# The cohesive pieces are then composed/injected by higher-level code:
user = User("alice", "alice@example.com")
emailer = EmailService()
repo = UserRepository()
emailer.send_welcome_email(user)
repo.save(user, "users.csv")
```

### Listing 6 — A Temperature class with a validating constructor (Python)
```python
class Temperature:
    """Rejects any value below absolute zero at construction time."""

    ABSOLUTE_ZERO_C = -273.15   # named constant, not a magic number

    def __init__(self, celsius):
        # Validate BEFORE storing.
        if celsius < Temperature.ABSOLUTE_ZERO_C:
            raise ValueError("Temperature below absolute zero is impossible")
        self.celsius = celsius

    def to_fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    def __str__(self):
        return f"{self.celsius} degrees C"


room = Temperature(21.0)          # fine
try:
    impossible = Temperature(-300)  # raises ValueError
except ValueError as e:
    print(f"Rejected: {e}")
```

### Listing 7 — NESA pseudocode: a constructor with validation
```text
BEGIN Constructor BankAccount(accountNumber, ownerName, initialBalance)
    IF accountNumber = "" THEN
        RAISE Error "Account number cannot be empty"
    ENDIF
    IF ownerName = "" THEN
        RAISE Error "Owner name cannot be empty"
    ENDIF
    IF initialBalance < 0 THEN
        RAISE Error "Initial balance cannot be negative"
    ENDIF

    this.accountNumber ← accountNumber
    this.ownerName ← ownerName
    this.balance ← initialBalance
    this.transactionHistory ← empty list
END Constructor
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| CPU | Central Processing Unit | The processor that executes program instructions |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| R-R-C-I | Requirements · Responsibilities · Collaborations · Implementation | The (iterative) object-oriented design pipeline |
