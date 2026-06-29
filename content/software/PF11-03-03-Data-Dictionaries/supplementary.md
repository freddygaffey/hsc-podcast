---
title: "Supplementary Materials — Data Dictionaries"
module: PF11
year: 11
lesson: "3.3"
script: script.md
---

# Supplementary Materials

Two data dictionaries (the artefacts themselves), runnable validators that enforce them, and
the validation in NESA pseudocode. Nothing here is spoken in the audio — it's the read-along
reference. The narration points at each by label only.

### Listing 1 — Student record data dictionary (the artefact)
```text
STUDENT RECORD — DATA DICTIONARY        (entry = Field, Type, Constraints, Relationship + desc/example)

Field Name          Data Type   Constraints                                  Description               Example
-----------------   ---------   ------------------------------------------   -----------------------   --------------
name                String      Required; 2–50 characters (length)           Student's full name       "Sarah Johnson"
age                 Integer     Required; range 16–25 (years)                Age in years              17
grade_average       Float       Required; range 0.0–100.0; 1 dp (percent)    Overall grade percentage  87.5
enrollment_status   Boolean     Required                                     Currently enrolled?       True
student_id          String      Required; format "S" + 5 digits              Unique ID                 "S10234"

RELATIONSHIPS:
  one-to-one    each student has exactly one student_id
  one-to-many   one teacher has many students
  many-to-many  students enrol in many subjects; each subject has many students
```

### Listing 2 — Validation code enforcing the dictionary (Python, runnable)
```python
def validate_student_data(name, age, grade_average, enrolled):
    if not isinstance(name, str):
        return False, "Name must be a string"
    if len(name) < 2 or len(name) > 50:                 # LENGTH constraint
        return False, "Name must be 2 to 50 characters"
    if not isinstance(age, int):
        return False, "Age must be an integer"
    if age < 16 or age > 25:                            # RANGE constraint
        return False, "Age must be 16 to 25"
    if not isinstance(grade_average, (int, float)):
        return False, "Grade average must be a number"
    if grade_average < 0.0 or grade_average > 100.0:    # RANGE constraint
        return False, "Grade average must be 0.0 to 100.0"
    if not isinstance(enrolled, bool):
        return False, "Enrolment status must be True or False"
    return True, "All data is valid"


assert validate_student_data("Sarah Johnson", 17, 87.5, True) == (True, "All data is valid")
assert validate_student_data("", 17, 87.5, True) == (False, "Name must be 2 to 50 characters")
assert validate_student_data("Sarah Johnson", 30, 87.5, True) == (False, "Age must be 16 to 25")
assert validate_student_data("Sarah Johnson", 16, 87.5, True)[0] is True    # boundary 16 — OK
assert validate_student_data("Sarah Johnson", 26, 87.5, True)[0] is False   # boundary 26 — fails
print("All validate_student_data assertions passed.")
```

### Listing 3 — The same validation in NESA pseudocode (the examinable algorithm)
```text
BEGIN FUNCTION ValidateStudent(name, age, average, enrolled)
    IF length(name) < 2 OR length(name) > 50 THEN
        RETURN false, "Name must be 2 to 50 characters"
    ENDIF
    IF age < 16 OR age > 25 THEN
        RETURN false, "Age must be 16 to 25"
    ENDIF
    IF average < 0.0 OR average > 100.0 THEN
        RETURN false, "Grade average must be 0.0 to 100.0"
    ENDIF
    RETURN true, "All data is valid"
END FUNCTION
```

### Listing 4 — A FORMAT constraint via a pattern (Python, runnable)
```python
import re


def validate_product_id(product_id):
    # FORMAT constraint: the letters "PRD" followed by exactly 5 digits
    return bool(re.match(r"^PRD\d{5}$", product_id))


assert validate_product_id("PRD00123") is True
assert validate_product_id("ABC00123") is False    # wrong prefix
assert validate_product_id("PRD123") is False       # too few digits
print("All validate_product_id assertions passed.")
```

### Listing 5 — A CONDITIONAL constraint (a relationship expressed as a rule) (Python, runnable)
```python
def validate_stock_rules(in_stock, stock_quantity):
    # conditional: one field's rule depends on another
    if in_stock and stock_quantity <= 0:
        return False, "In-stock items must have quantity greater than 0"
    return True, "Stock rules valid"


assert validate_stock_rules(True, 45) == (True, "Stock rules valid")
assert validate_stock_rules(True, 0) == (False, "In-stock items must have quantity greater than 0")
assert validate_stock_rules(False, 0) == (True, "Stock rules valid")    # not in stock -> 0 is fine
print("All validate_stock_rules assertions passed.")
```

### Listing 6 — Library book data dictionary (exam practice)
```text
LIBRARY BOOK — DATA DICTIONARY

Field Name         Data Type   Constraints                                       Example
----------------   ---------   ----------------------------------------------    ------------------
isbn               String      Required; format exactly 13 digits                "9780132350884"
title              String      Required; max 200 characters                      "Clean Code"
author             String      Required; max 100 characters                      "Robert C. Martin"
publication_year   Integer     Required; range 1800–current year                 2008
available          Boolean     Required                                          True
borrower_id        String      Optional; format 6 digits; ONLY if NOT available  "100245"

CONDITIONAL RULE (a relationship as a constraint):
  borrower_id may be set ONLY when available = False
  (a book on loan has a borrower; an available book has none).
```
