---
title: "Supplementary Materials — Modelling: Class Diagrams, Structure Charts and DFDs"
module: OOP11
year: 11
lesson: "5.5"
script: script.md
---

# Supplementary Materials

Diagram listings for this episode. Nothing here is spoken in the audio — it's the
read-along reference. Every diagram is described in full in the narration; these are the
written-out notations so you can redraw them. Class diagrams and DFDs are written in
PlantUML; the structure chart is an indented ASCII tree.

### Listing 1 — Class diagram: a School system (composition + association + multiplicity)
```plantuml
@startuml
' Minus (-) = private (internal state); Plus (+) = public (interface)

class School {
    - name: string
    - address: string
    + enroll_student(student: Student)
    + add_course(course: Course)
}

class Student {
    - name: string
    - student_id: string
    - grades: list
    + add_grade(grade: float)
    + get_average(): float
    + get_info(): string
}

class Course {
    - course_name: string
    - course_code: string
    + get_enrolled_count(): int
}

class Teacher {
    - name: string
    - employee_id: string
    - subject: string
    + teach_course(course: Course)
}

' Filled diamond (*--) = COMPOSITION: the part dies with the whole.
' "1" to "many" (1 .. *) = one School composed of many Students / Courses.
School "1" *-- "many" Student   : enrolls
School "1" *-- "many" Course    : offers

' Plain line (--) = ASSOCIATION: connected, but neither owns the other.
Course "many" -- "1" Teacher    : taught by

' Star at BOTH ends = MANY-TO-MANY association.
Course "many" -- "many" Student : enrolled in
@enduml
```

### Listing 2 — Structure chart: a Library Management System (functional decomposition as a tree)
```text
Library Management System
├── User Management
│   ├── Add Member
│   ├── Remove Member
│   └── Update Member Info
├── Book Management
│   ├── Add Book
│   ├── Remove Book
│   └── Search Books
└── Lending Operations
    ├── Borrow Book
    ├── Return Book
    └── Calculate Fines
```

### Listing 3 — Data flow diagram: an ATM (Level 1 — processes, data stores, external entities, labelled flows)
```plantuml
@startuml
' Symbols:  circle = process (numbered, transforms data)
'           rectangle = external entity (source/destination outside the system)
'           folder = data store (data at rest)
'           arrow + label = data flow (the actual data travelling)

rectangle "Customer" as customer
rectangle "Bank System" as bank

circle "1\nValidate\nPIN" as p1
circle "2\nProcess\nWithdrawal" as p2
circle "3\nProcess\nDeposit" as p3
circle "4\nCheck\nBalance" as p4
circle "5\nLog\nTransaction" as p5

folder "Account Database" as db1
folder "Transaction Log" as db2

customer --> p1 : "card + PIN"
p1 --> db1 : "account lookup"
db1 --> p1 : "account details"
p1 --> customer : "validation result"

customer --> p2 : "withdrawal request"
p2 --> db1 : "balance check"
db1 --> p2 : "current balance"
p2 --> db1 : "balance update"
p2 --> customer : "cash + receipt"
p2 --> p5 : "transaction details"

customer --> p3 : "deposit amount"
p3 --> db1 : "balance update"
p3 --> customer : "deposit receipt"
p3 --> p5 : "transaction details"

customer --> p4 : "balance inquiry"
p4 --> db1 : "balance request"
db1 --> p4 : "account balance"
p4 --> customer : "balance display"

p5 --> db2 : "transaction record"
db2 --> bank : "audit trail"
@enduml
```

### Listing 4 — Level 0 (context) then Level 1 DFD for a Library (the zoom-in)
```plantuml
@startuml
title Level 0 -- Context Diagram (whole system as ONE process)

rectangle "Student" as student
rectangle "Teacher" as teacher
rectangle "Administrator" as admin

circle "Library\nManagement\nSystem" as system

student --> system : "borrow request"
system --> student : "book + due date"
teacher --> system : "book recommendation"
system --> teacher : "availability status"
admin --> system : "new book details"
system --> admin : "inventory report"
@enduml
```

```plantuml
@startuml
title Level 1 -- the single bubble exploded into its major processes

rectangle "Student" as student
rectangle "Teacher" as teacher

circle "1\nManage\nBorrowing" as p1
circle "2\nManage\nInventory" as p2
circle "3\nGenerate\nReports" as p3

folder "Book Database" as db1
folder "User Database" as db2

student --> p1 : "borrow request"
p1 --> db1 : "book query"
db1 --> p1 : "book details"
p1 --> student : "borrowed book"
teacher --> p2 : "book recommendation"
p2 --> db1 : "new book"
p3 --> db1 : "book data"
p3 --> db2 : "user data"
@enduml
```

### Listing 5 — The online-shopping system in all three views (the capstone)
```plantuml
@startuml
title View 1 of 3 -- CLASS DIAGRAM (the things / static structure)

class Customer {
    - customer_id: string
    - name: string
    - email: string
    + place_order(cart: ShoppingCart)
    + view_order_history()
}

class ShoppingCart {
    - items: list
    - total: float
    + add_item(product: Product)
    + remove_item(product: Product)
    + calculate_total(): float
}

class Product {
    - product_id: string
    - name: string
    - price: float
    - stock_quantity: int
    + update_stock(quantity: int)
}

class Order {
    - order_id: string
    - date: datetime
    - status: string
    - total_amount: float
    + process_payment()
    + ship_order()
}

Customer "1" *-- "many" Order        : places
Customer "1" -- "1" ShoppingCart      : has
ShoppingCart "many" -- "many" Product : contains
Order "many" -- "many" Product        : includes
@enduml
```

```text
View 2 of 3 -- STRUCTURE CHART (the jobs / functional decomposition)

Online Shopping System
├── Customer Management
│   ├── Register Customer
│   ├── Authenticate User
│   └── Update Profile
├── Product Catalog
│   ├── Browse Products
│   ├── Search Products
│   └── View Product Details
├── Shopping Cart
│   ├── Add to Cart
│   ├── Remove from Cart
│   └── Calculate Total
└── Order Processing
    ├── Process Payment
    ├── Update Inventory
    └── Generate Invoice
```

```plantuml
@startuml
title View 3 of 3 -- DATA FLOW DIAGRAM (the data / movement + transformation)

rectangle "Customer" as customer
rectangle "Payment Gateway" as payment

circle "1\nProcess\nOrder" as p1
circle "2\nUpdate\nInventory" as p2
circle "3\nGenerate\nInvoice" as p3

folder "Product Database" as db1
folder "Order Database" as db2

customer --> p1 : "order details"
p1 --> db1 : "product request"
db1 --> p1 : "product info"
p1 --> p2 : "ordered items"
p2 --> db1 : "stock update"
p1 --> db2 : "order record"
p1 --> p3 : "order summary"
p3 --> customer : "invoice"
p1 --> payment : "payment request"
payment --> p1 : "payment confirmation"
@enduml
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| DFD | Data Flow Diagram | A model showing how data moves between processes, stores and external entities |
