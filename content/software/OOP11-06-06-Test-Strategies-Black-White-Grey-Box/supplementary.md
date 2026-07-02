---
title: "Supplementary Materials — Test Strategies: Black, White and Grey Box"
module: OOP11
year: 11
lesson: "6.6"
script: script.md
---

# Supplementary Materials

Code listings for this episode. Nothing here is spoken in the audio — it's the read-along
reference. The narration refers to each listing by its label.

Each listing is a worked test suite for one of the three strategies, in the order the
narration introduces them: black-box grade calculator (Listing 1), black-box password
validator with boundary value analysis (Listing 2), white-box discount calculator covering
every branch including the cap (Listing 3), and a grey-box authentication suite probing
hashing, session timeout and rate limiting (Listing 4). The NESA-pseudocode listings
(5 and 6) rehearse the two examinable algorithms — the boundary-test design loop and the
branch-coverage check — in exam form.

---

### Listing 1 — Black-box test: grade calculator (boundaries + equivalence classes)

```python
import unittest


class GradeCalculator:
    """Converts a numerical score (0-100) to a letter grade.

    Spec (the ONLY thing a black-box test may use):
        A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: 0-59.
        Scores outside 0-100, or non-numeric input, raise ValueError.
    """

    def calculate_grade(self, score):
        if not isinstance(score, (int, float)):
            raise ValueError("Score must be a number")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


class TestGradeCalculatorBlackBox(unittest.TestCase):
    """Tests designed from the SPEC only — the code is never inspected.

    Two black-box techniques are applied:
      * Equivalence partitioning — one representative from each grade class.
      * Boundary value analysis  — the value at each edge AND the value just
        on either side of it (this is where off-by-one bugs hide).
    """

    def setUp(self):
        self.calc = GradeCalculator()

    # --- Equivalence partitioning: one representative per valid class ---
    def test_one_representative_per_class(self):
        self.assertEqual(self.calc.calculate_grade(95), "A")  # A class
        self.assertEqual(self.calc.calculate_grade(85), "B")  # B class
        self.assertEqual(self.calc.calculate_grade(75), "C")  # C class
        self.assertEqual(self.calc.calculate_grade(65), "D")  # D class
        self.assertEqual(self.calc.calculate_grade(30), "F")  # F class

    # --- Boundary value analysis: the pair straddling each edge ---
    def test_f_to_d_boundary(self):
        self.assertEqual(self.calc.calculate_grade(59), "F")  # last F
        self.assertEqual(self.calc.calculate_grade(60), "D")  # first D

    def test_d_to_c_boundary(self):
        self.assertEqual(self.calc.calculate_grade(69), "D")
        self.assertEqual(self.calc.calculate_grade(70), "C")

    def test_c_to_b_boundary(self):
        self.assertEqual(self.calc.calculate_grade(79), "C")
        self.assertEqual(self.calc.calculate_grade(80), "B")

    def test_b_to_a_boundary(self):
        # The single most valuable test: catches "> 90" written for ">= 90".
        self.assertEqual(self.calc.calculate_grade(89), "B")  # last B
        self.assertEqual(self.calc.calculate_grade(90), "A")  # first A

    # --- Outer boundaries of the valid range ---
    def test_outer_boundaries_valid(self):
        self.assertEqual(self.calc.calculate_grade(0), "F")   # min valid
        self.assertEqual(self.calc.calculate_grade(100), "A") # max valid

    # --- Invalid equivalence classes (faulty / abnormal data) ---
    def test_invalid_classes_raise(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_grade(-1)     # just below the floor
        with self.assertRaises(ValueError):
            self.calc.calculate_grade(101)    # just above the ceiling
        with self.assertRaises(ValueError):
            self.calc.calculate_grade("85")   # non-numeric


if __name__ == "__main__":
    unittest.main()
```

---

### Listing 2 — Black-box test: password validator (boundary value analysis on length)

```python
import unittest


class PasswordValidator:
    """Spec: a valid password is 8-20 characters and contains at least one
    uppercase letter, one lowercase letter, one digit and one special
    character. Anything else raises ValueError."""

    SPECIALS = "!@#$%^&*()-_+="

    def validate(self, password):
        if not (8 <= len(password) <= 20):
            raise ValueError("Password must be 8-20 characters")
        if not any(c.isupper() for c in password):
            raise ValueError("Need an uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("Need a lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Need a digit")
        if not any(c in self.SPECIALS for c in password):
            raise ValueError("Need a special character")
        return True


class TestPasswordValidatorBlackBox(unittest.TestCase):
    """Boundary value analysis on the 8-20 length rule.

    The four-value fingerprint around each edge:
        one BELOW the edge (fail), the EDGE (pass),
        the other EDGE (pass), one ABOVE it (fail).
    """

    def setUp(self):
        self.validator = PasswordValidator()

    def test_length_boundaries(self):
        # 7 chars — just below the minimum — must FAIL
        with self.assertRaises(ValueError):
            self.validator.validate("Abc123!")
        # 8 chars — the minimum — must PASS
        self.assertTrue(self.validator.validate("Abc1234!"))
        # 20 chars — the maximum — must PASS
        self.assertTrue(self.validator.validate("Abc123!@#$%^&*()1234"))
        # 21 chars — just above the maximum — must FAIL
        with self.assertRaises(ValueError):
            self.validator.validate("Abc123!@#$%^&*()12345")

    def test_character_class_equivalence(self):
        # Each missing-requirement input is its own invalid equivalence class.
        with self.assertRaises(ValueError):
            self.validator.validate("abc123!@")   # no uppercase
        with self.assertRaises(ValueError):
            self.validator.validate("ABC123!@")   # no lowercase
        with self.assertRaises(ValueError):
            self.validator.validate("Abcdef!@")   # no digit
        with self.assertRaises(ValueError):
            self.validator.validate("Abcdefg1")   # no special character
        # A representative of the VALID class.
        self.assertTrue(self.validator.validate("Abcdef1!"))
```

---

### Listing 3 — White-box test: discount calculator (every branch, including the cap)

```python
import unittest


class DiscountCalculator:
    """Discount = base (by customer type) + order bonus + holiday bonus,
    capped at 30%. White-box testing reads THIS code and covers every branch."""

    MAX_DISCOUNT = 0.3

    def calculate_discount(self, customer_type, order_amount, is_holiday=False):
        # Decision 1: customer type — 4 branches (incl. the error branch)
        if customer_type == "regular":
            discount = 0.0
        elif customer_type == "premium":
            discount = 0.1
        elif customer_type == "vip":
            discount = 0.2
        else:
            raise ValueError(f"Invalid customer type: {customer_type}")

        # Decision 2: order amount — 3 branches
        if order_amount > 1000:
            discount += 0.1
        elif order_amount > 500:
            discount += 0.05

        # Decision 3: holiday season — 2 branches
        if is_holiday:
            discount += 0.05

        # Decision 4: the CAP — the branch students forget to cover
        if discount > self.MAX_DISCOUNT:
            discount = self.MAX_DISCOUNT

        return round(discount, 4)


class TestDiscountCalculatorWhiteBox(unittest.TestCase):
    """Branch coverage: every branch of every decision, true AND false."""

    def setUp(self):
        self.calc = DiscountCalculator()

    def test_customer_type_branches(self):
        self.assertEqual(self.calc.calculate_discount("regular", 100), 0.0)
        self.assertEqual(self.calc.calculate_discount("premium", 100), 0.1)
        self.assertEqual(self.calc.calculate_discount("vip", 100), 0.2)
        with self.assertRaises(ValueError):                # the error branch
            self.calc.calculate_discount("invalid", 100)

    def test_order_amount_branches(self):
        self.assertEqual(self.calc.calculate_discount("regular", 400), 0.0)   # <= 500
        self.assertEqual(self.calc.calculate_discount("regular", 600), 0.05)  # 500-1000
        self.assertEqual(self.calc.calculate_discount("regular", 1200), 0.1)  # > 1000

    def test_holiday_branch_both_ways(self):
        self.assertEqual(self.calc.calculate_discount("premium", 600, False), 0.15)
        self.assertEqual(self.calc.calculate_discount("premium", 600, True), 0.2)

    def test_cap_branch_is_actually_reached(self):
        # Ordinary combos stay UNDER the 30% cap, so they never test the clamp:
        # premium(0.1) + big order(0.1) + holiday(0.05) = 0.25 — cap branch NOT hit.
        self.assertEqual(self.calc.calculate_discount("premium", 1200, True), 0.25)

        # To FORCE the cap branch, deliberately stack the worst case:
        # the highest tier vip(0.2) + big order(0.1) + holiday(0.05) = 0.35 raw,
        # which the cap must clamp to exactly 0.30.
        result = self.calc.calculate_discount("vip", 1200, True)
        self.assertEqual(result, DiscountCalculator.MAX_DISCOUNT)  # 0.30, capped
```

---

### Listing 4 — Grey-box test: authentication system (hashing, session timeout, rate limiting)

```python
import unittest


class TestUserAuthenticationGreyBox(unittest.TestCase):
    """Grey box: we DON'T have the source, but we KNOW three things about the
    internals — passwords are hashed, sessions time out, and failed logins are
    rate-limited — and we use that knowledge to AIM tests at the risky spots."""

    def setUp(self):
        self.auth = UserAuthenticationSystem()

    def test_passwords_are_not_stored_in_plaintext(self):
        username, password = "testuser", "SecurePass123!"
        self.auth.create_user(username, password)

        # Grey-box knowledge: hashing is used. So peek at the stored record
        # (limited internal access) and assert it is NOT the raw password.
        stored = self.auth._get_user_data(username)        # internal method
        self.assertNotEqual(stored["password_hash"], password)

        # ...but logging in with the real password must still work.
        self.assertTrue(self.auth.authenticate(username, password))

    def test_session_times_out(self):
        username, password = "testuser", "SecurePass123!"
        self.auth.create_user(username, password)
        session_id = self.auth.login(username, password)

        self.assertTrue(self.auth.is_session_valid(session_id))

        # Grey-box knowledge: sessions expire. Advance the clock past timeout.
        self.auth._advance_time(hours=25)                  # internal method
        self.assertFalse(self.auth.is_session_valid(session_id))

    def test_rate_limiting_blocks_then_recovers(self):
        username, password = "testuser", "SecurePass123!"
        self.auth.create_user(username, password)

        # Grey-box knowledge: repeated failures trigger a lockout.
        for _ in range(5):
            self.assertFalse(self.auth.authenticate(username, "WrongPassword"))

        # Even the CORRECT password is now temporarily blocked.
        self.assertFalse(self.auth.authenticate(username, password))

        # The block is temporary: after the cooldown, it works again.
        self.auth._advance_time(minutes=15)                # internal method
        self.assertTrue(self.auth.authenticate(username, password))
```

---

### Listing 5 — NESA pseudocode: designing black-box boundary tests for a range

```text
BEGIN DesignBoundaryTests(lowerBound, upperBound)
    testCases ← empty list

    ADD (lowerBound - 1, "INVALID")  TO testCases   # just below the edge
    ADD (lowerBound,     "VALID")    TO testCases   # the lower edge
    ADD (upperBound,     "VALID")    TO testCases   # the upper edge
    ADD (upperBound + 1, "INVALID")  TO testCases   # just above the edge

    FOR each (input, expected) IN testCases
        actual ← RunFunctionUnderTest(input)
        IF actual = expected THEN
            DISPLAY "PASS", input
        ELSE
            DISPLAY "FAIL", input, "expected", expected, "got", actual
        ENDIF
    NEXT (input, expected)
END DesignBoundaryTests
```

---

### Listing 6 — NESA pseudocode: branch coverage check on a single decision

```text
BEGIN CheckBranchCoverage(condition)
    # Branch coverage = every decision tested BOTH true AND false.
    trueCovered  ← FALSE
    falseCovered ← FALSE

    FOR each testCase IN testSuite
        IF EvaluatesTrue(condition, testCase) THEN
            trueCovered ← TRUE
        ELSE
            falseCovered ← TRUE
        ENDIF
    NEXT testCase

    IF trueCovered = TRUE AND falseCovered = TRUE THEN
        DISPLAY "Branch fully covered"
    ELSE
        DISPLAY "Branch NOT covered — add a test for the missing case"
    ENDIF
END CheckBranchCoverage
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
