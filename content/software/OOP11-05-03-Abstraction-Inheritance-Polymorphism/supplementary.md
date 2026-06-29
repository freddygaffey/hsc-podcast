---
title: "Supplementary Materials — Abstraction, Generalisation, Inheritance and Polymorphism"
module: OOP11
year: 11
lesson: "5.3"
script: script.md
---

# Supplementary Materials

Code listings and NESA-style pseudocode for this episode. Nothing here is spoken in the
audio — it's the read-along reference. The narration refers to each item by its label
only (e.g. "the full version is in Listing 1"), and never depends on you seeing it.

### Listing 1 — Abstraction: a `FileManager` hiding file-handling complexity
```python
class FileManager:
    """Abstraction in action.

    The CALLER sees two simple methods, save_data() and load_data().
    Hidden behind them: file handles, write buffers, flushing, error
    handling, and resource cleanup. The interface is simple; the
    complexity is hidden. Abstraction hides the COMPLEXITY (compare with
    encapsulation, which hides the DATA).
    """

    def save_data(self, filename, data):
        """Simple interface — the complexity is hidden inside."""
        try:
            with open(filename, "w") as file:
                # Hidden complexity: open handle, manage buffer, flush,
                # handle disk-full / bad-path errors, close & clean up.
                file.write(data)
            return "File saved successfully"
        except OSError as error:
            return f"Error saving file: {error}"

    def load_data(self, filename):
        """Another simple interface over complex operations."""
        try:
            with open(filename, "r") as file:
                return file.read()
        except FileNotFoundError:
            return None


# Usage: simple and clean. The caller never touches the complexity.
file_manager = FileManager()
file_manager.save_data("notes.txt", "My important notes")
content = file_manager.load_data("notes.txt")
```

### Listing 2 — Inheritance + `super()` + overriding: the `Vehicle` hierarchy
```python
class Vehicle:
    """The GENERAL model (generalisation): the shared traits of all
    vehicles, captured once. Car and Motorcycle will INHERIT this."""

    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.speed = 0
        self.is_running = False

    def start(self):                       # shared — inherited as-is
        self.is_running = True
        return f"{self.make} {self.model} started"

    def stop(self):                        # shared — inherited as-is
        self.speed = 0
        self.is_running = False
        return f"{self.make} {self.model} stopped"


class Car(Vehicle):
    """Car IS-A Vehicle. Inherits start()/stop(); adds + overrides."""

    def __init__(self, make, model, doors):
        super().__init__(make, model)      # run the PARENT constructor
        self.doors = doors                 # car-specific attribute

    def accelerate(self):                  # overridden behaviour
        self.speed += 10
        return f"Car accelerating, speed: {self.speed} km/h"


class Motorcycle(Vehicle):
    """Motorcycle IS-A Vehicle. Same start()/stop(), different accelerate()."""

    def __init__(self, make, model, engine_size):
        super().__init__(make, model)      # forget this line and make/model
        self.engine_size = engine_size     # are NEVER set — the classic bug

    def accelerate(self):                  # overridden — bikes accelerate harder
        self.speed += 20
        return f"Motorcycle accelerating, speed: {self.speed} km/h"


car = Car("Toyota", "Camry", 4)
bike = Motorcycle("Honda", "CBR", 600)
print(car.start())          # inherited from Vehicle
print(car.accelerate())     # Car's overridden version (+10)
print(bike.accelerate())    # Motorcycle's overridden version (+20)
```

### Listing 3 — Polymorphism: the "Animal Concert" loop
```python
class Dog:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        return f"{self.name} says Woof!"


class Cat:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        return f"{self.name} says Meow!"


class Bird:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        return f"{self.name} says Tweet!"


def animal_concert(animals):
    """ONE loop, ONE method call — each object responds in its own form.
    The loop never checks the type. Note: Dog/Cat/Bird do NOT share a
    parent class. This is polymorphism via DUCK TYPING."""
    for animal in animals:
        print(animal.make_sound())


pets = [Dog("Buddy"), Cat("Whiskers"), Bird("Tweety")]
animal_concert(pets)   # Woof! / Meow! / Tweet! — add a Cow and nothing changes
```

### Listing 4 — Duck typing: polymorphism with NO shared parent
```python
class WashingMachine:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        return f"{self.brand} washing machine starting wash cycle"


class Dishwasher:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        return f"{self.brand} dishwasher starting cleaning cycle"


class Printer:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        return f"{self.brand} printer initialising"


def run_appliance(appliance):
    """Duck typing: works with ANY object that has start().
    A printer is NOT a kind of washing machine — there is no sensible
    shared parent — yet all three are polymorphic here, because they
    share the start() INTERFACE, not a bloodline. If it quacks, it'll do."""
    print(appliance.start())


for appliance in [WashingMachine("Samsung"), Dishwasher("Bosch"), Printer("HP")]:
    run_appliance(appliance)
```

### Listing 5 — The capstone: `Shape` showing all four concepts at once
```python
class Shape:
    """GENERALISATION: the general model of "a shape" — every shape has a
    name and (in principle) an area and a perimeter.

    ABSTRACTION: area() and perimeter() are ABSTRACT METHODS. The base
    class refuses to implement them (there is no area of a generic shape)
    and forces every subclass to provide a real version by raising
    NotImplementedError. Any subclass that forgets will crash loudly the
    first time the method is called."""

    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError("Subclasses must implement area()")

    def perimeter(self):
        raise NotImplementedError("Subclasses must implement perimeter()")

    def describe(self):                    # shared behaviour for all shapes
        return f"This is a {self.name}"


class Rectangle(Shape):                    # INHERITANCE: Rectangle IS-A Shape
    def __init__(self, width, height):
        super().__init__("Rectangle")      # super(): set the inherited name
        self.width = width
        self.height = height

    def area(self):                        # POLYMORPHISM: own implementation
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):                       # INHERITANCE: Circle IS-A Shape
    PI = 3.14159

    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):                        # POLYMORPHISM: own implementation
        return Circle.PI * self.radius ** 2

    def perimeter(self):
        return 2 * Circle.PI * self.radius


def calculate_total_area(shapes):
    """ABSTRACTION + POLYMORPHISM: works at the level of "a shape has an
    area". It never checks which shape is which — each runs its own area()."""
    total = 0
    for shape in shapes:
        total += shape.area()
    return total


shapes = [Rectangle(5, 3), Circle(4), Rectangle(2, 8)]
print(calculate_total_area(shapes))        # 15 + ~50.27 + 16 = ~81.27
```

### Listing 6 — NESA pseudocode: an overridden method in a class hierarchy
```text
BEGIN CLASS Shape
    METHOD Area()
        DISPLAY "Error: subclasses must implement Area"   // abstract method
    END METHOD
END CLASS

BEGIN CLASS Rectangle INHERITS Shape
    METHOD Area()                                         // overrides Shape.Area
        RETURN width * height
    END METHOD
END CLASS

BEGIN CLASS Circle INHERITS Shape
    METHOD Area()                                         // overrides Shape.Area
        RETURN 3.14159 * radius * radius
    END METHOD
END CLASS

BEGIN CalculateTotalArea(shapeList)                       // polymorphic loop
    total ← 0
    FOR each shape IN shapeList
        total ← total + shape.Area()    // each shape runs its OWN Area()
    NEXT shape
    RETURN total
END CalculateTotalArea
```
