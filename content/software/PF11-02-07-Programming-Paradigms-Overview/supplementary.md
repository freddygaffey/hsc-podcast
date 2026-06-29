---
title: "Supplementary Materials — Programming Paradigms (Imperative, OOP, Logic, Functional)"
module: PF11
year: 11
lesson: "2.7"
script: script.md
---

# Supplementary Materials

The same problem (a shopping-cart total) in three paradigms, a logic-paradigm example, and a
paradigm reference. Nothing here is spoken in the audio — it's the read-along reference. The
narration points at each by label only. All three cart versions produce the same result: 66.0.

### Listing 1 — Shopping-cart total, IMPERATIVE style (Python, runnable)
```python
# "How to do it": explicit steps, a variable that changes over time.
def cart_total_imperative(prices, tax_rate=0.10):
    total = 0
    for price in prices:            # explicit loop (iteration)
        total = total + price       # accumulator: state changes each pass
    total = total + total * tax_rate
    return total


assert cart_total_imperative([10, 20, 30]) == 66.0   # 60 subtotal + 6 tax
print("Imperative total:", cart_total_imperative([10, 20, 30]))
```

### Listing 2 — Shopping-cart total, OBJECT-ORIENTED style (Python, runnable)
```python
# "Model the world": an object bundles the data (items) with the behaviour (total).
class ShoppingCart:
    def __init__(self, tax_rate=0.10):
        self.items = []
        self.tax_rate = tax_rate

    def add_item(self, price):
        self.items.append(price)

    def total(self):
        subtotal = sum(self.items)
        return subtotal + subtotal * self.tax_rate


cart = ShoppingCart()
for price in [10, 20, 30]:
    cart.add_item(price)
assert cart.total() == 66.0
print("Object-oriented total:", cart.total())
```

### Listing 3 — Shopping-cart total, FUNCTIONAL style (Python, runnable)
```python
# "Transform data": compose functions, no loop, no changing variable.
from functools import reduce


def cart_total_functional(prices, tax_rate=0.10):
    subtotal = reduce(lambda running, price: running + price, prices, 0)  # fold to a sum
    return subtotal + subtotal * tax_rate                                # transform: add tax


assert cart_total_functional([10, 20, 30]) == 66.0
print("Functional total:", cart_total_functional([10, 20, 30]))
# Same problem, three paradigms, identical answer (66.0) — the style of thinking differs.
```

### Listing 4 — Logic paradigm: facts, a rule, and a query (Prolog-style)
```text
% FACTS — things we declare to be true
man(socrates).

% RULE — how new truths are derived ( :- reads as "if" )
mortal(X) :- man(X).        % X is mortal IF X is a man

% QUERY — a question we ask
?- mortal(socrates).

% ANSWER: true
% We never wrote HOW to compute it. We stated WHAT is true (facts + rule);
% the logic engine DEDUCES the answer. That is "declarative" programming.
```

### Listing 5 — Paradigm reference: one-liners, typical languages, multi-paradigm note
```text
PARADIGM          ONE-LINE THINKING     FOCUS                 TYPICAL LANGUAGE
Imperative        "how to do it"        step-by-step control  C
Object-oriented   "model the world"     interacting entities  Java
Logic             "what is true"        facts + rules         Prolog
Functional        "transform data"      function composition  Haskell

Grouping:  Imperative + Object-oriented lean "HOW" (you specify the steps).
           Logic + Functional lean "WHAT" (declarative — more is left to the machine).

A LANGUAGE IS NOT A PARADIGM. Most modern languages are MULTI-PARADIGM:
  Python  = imperative + object-oriented + functional features (map / filter / reduce)
  JavaScript, C++, Scala ... likewise mix styles.
The paradigm is the STYLE you write in; the language usually lets you choose.
```
