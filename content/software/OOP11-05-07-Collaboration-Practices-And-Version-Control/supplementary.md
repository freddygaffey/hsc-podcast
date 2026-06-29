---
title: "Supplementary Materials — Collaboration Practices and Version Control"
module: OOP11
year: 11
lesson: "5.7"
script: script.md
---

# Supplementary Materials

Code listings and read-along references for this episode. Nothing here is spoken in the
audio — the narration describes each one in words and references it by label. Use these
to read along or revisit after listening.

### Listing 1 — A payment-processor interface and a mock implementation (Python)
```python
class PaymentProcessor:
    """Interface contract for processing payments.

    Any implementation MUST honour this contract so callers can depend on the
    interface, not the implementation. This is the 'stable front' a teammate
    builds against before the real class exists.
    """

    def process_payment(self, amount, payment_method):
        """Process a payment.

        Args:
            amount (float): payment amount in dollars (must be > 0)
            payment_method (str): e.g. "credit_card", "debit"

        Returns:
            PaymentResult: success/failure plus a transaction id

        Raises:
            InvalidAmountError: if amount <= 0
            PaymentDeclinedError: if the payment is rejected
        """
        raise NotImplementedError("Subclasses must implement process_payment")


class MockPaymentProcessor(PaymentProcessor):
    """A fake stand-in honouring the same interface.

    Lets the checkout developer build and test the whole flow today, with no
    blocking dependency on the real processor (no API keys, no live bank, no cost).
    """

    def process_payment(self, amount, payment_method):
        print(f"MOCK: would charge ${amount} via {payment_method}")
        return {"success": True, "transaction_id": "MOCK-123"}


class StripePaymentProcessor(PaymentProcessor):
    """The real implementation — written later, drops in unchanged (polymorphism)."""

    def process_payment(self, amount, payment_method):
        # ... real call to the payment gateway ...
        pass
```

### Listing 2 — Git command sequence: branch, commit, merge (bash)
```bash
# 1. Start from an up-to-date main branch
git checkout main
git pull origin main

# 2. Create and switch to a feature branch for your work
git checkout -b feature/user-management

# 3. Work, then stage and commit in small, single-purpose commits
#    ("one idea per commit" — one logical change, one clear message)
git add src/user_manager.py
git commit -m "Add UserManager with create_user and authenticate_user"

git add tests/test_user_manager.py
git commit -m "Add tests for UserManager authentication"

# 4. Push the branch and open a pull request for review (in GitHub/GitLab)
git push origin feature/user-management

# 5. Once approved, merge the feature branch back into main
git checkout main
git pull origin main
git merge feature/user-management
```

### Listing 3 — An annotated merge-conflict block (text)
```text
# Git could not auto-merge: both branches changed the SAME lines of the SAME file.
# It pauses and inserts conflict markers, leaving a human to resolve.

class UserManager:
    def __init__(self):
<<<<<<< HEAD                          # ── YOUR version (current branch) ──
        self.users = {}
        self.active_sessions = {}
=======                               # ── divider between the two versions ──
        self.user_database = []       # ── THEIR version (incoming branch) ──
        self.session_store = SessionStore()
>>>>>>> feature/session-management    # ── end marker + name of incoming branch ──

    def create_user(self, username, email):
        ...

# To resolve — "Talk, Edit, Strip, Commit":
#   1. TALK   : discuss with your teammate which approach is correct (or combine both)
#   2. EDIT   : rewrite the section into the correct combined version
#   3. STRIP  : delete the three marker lines (<<<<<<<, =======, >>>>>>>)
#   4. COMMIT : re-run the tests, then `git add` the file and commit the resolution
```

### Listing 4 — A sample pull-request description (markdown/text)
```text
# Pull Request: Add User Authentication

## Description
Implements user registration, login, and session handling for the blog platform,
following the agreed UserManager interface.

## Changes Made
- Added UserManager class (create_user, authenticate_user, get_user_profile)
- Added password hashing
- Added 15 unit tests

## Classes Added / Modified
- UserManager (new): handles user accounts and authentication
- DatabaseManager (modified): added a users table

## Testing
- All existing tests pass; added 15 new unit tests; login/logout tested manually

## Breaking Changes
None — new feature, no change to existing interfaces.

# A GOOD review comment (specific, reasoned, about the code):
#   "Consider pulling MAX_PASSWORD_LENGTH out as a named constant (line 45) so it's
#    easier to change later and the code is self-documenting."
#
# A POOR review comment (vague, hostile, about the coder):
#   "This is wrong, fix it."
#
# The rule: "comment the code, not the coder."
```
