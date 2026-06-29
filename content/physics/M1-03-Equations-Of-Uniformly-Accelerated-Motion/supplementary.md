---
title: "Supplementary Materials — Equations of Uniformly Accelerated Motion"
module: M1
lesson: "03"
script: script.md
---

# Supplementary Materials

The four equations of motion, the selection method, and worked solutions. Nothing here is spoken in the audio — it is the read-along reference. Valid ONLY for constant (uniform) acceleration. Symbols: s = displacement; u = initial velocity; v = final velocity; a = acceleration; t = time.

### Listing 1 — The four equations and the missing-variable method
```text
SUVAT — the five quantities:  s, u, v, a, t

Equation                          omits     use when you don't have / want…
  v = u + a t                     (no s)    displacement
  s = u t + ½ a t²                (no v)    final velocity
  v² = u² + 2 a s                 (no t)    time
  s = ½ (u + v) t                 (no a)    acceleration

METHOD:
  1. Write the five letters s u v a t.
  2. Fill in the 3 values you're given (with SIGNS, from your chosen + direction).
  3. Identify the unknown you want AND the one quantity that's missing.
  4. Pick the equation that does NOT contain the missing quantity. Substitute, solve.

Constants: g (free-fall acceleration) ≈ 9.8 m s⁻² downward.
"from rest" / "dropped" ⇒ u = 0.   At the top of a vertical throw: v = 0 (but a is still g).
```

### Listing 2 — Worked examples (horizontal)
```text
(A) Car: u = 10, v = 30 m s⁻¹ over s = 100 m. Find a.  (t missing → v² = u² + 2as)
   30² = 10² + 2·a·100
   900 = 100 + 200a   →   800 = 200a   →   a = 4.0 m s⁻²

(B) Cyclist from rest, a = 2.0 m s⁻², t = 8 s.  (Exam Q2)
   v = u + a t = 0 + 2·8 = 16 m s⁻¹
   s = u t + ½ a t² = 0 + ½·2·8² = 64 m

(C) Braking: u = 30, v = 0, t = 5 s. Find s.  (a missing → s = ½(u+v)t)
   s = ½(30 + 0)(5) = 75 m
   (acceleration, if asked: v = u + at → 0 = 30 + a·5 → a = −6 m s⁻², negative = decelerating)
```

### Listing 3 — Worked examples (vertical, under gravity)
```text
(A) Ball thrown UP at 20 m s⁻¹. Take UP as +, so a = −9.8 m s⁻².
   Max height: at top v = 0  (t missing → v² = u² + 2as)
     0 = 20² + 2(−9.8)s = 400 − 19.6s → s = 20.4 m
   Time of flight (returns to start, s = 0)  (v missing → s = ut + ½at²)
     0 = 20t − 4.9t² = t(20 − 4.9t) → t = 0 (launch) or t = 4.1 s

(B) Exam Q3 — thrown up at 25 m s⁻¹, up +, a = −9.8. Max height (v = 0):
     0 = 25² + 2(−9.8)s = 625 − 19.6s → s ≈ 31.9 m

(C) Exam Q5 — thrown DOWN at 8 m s⁻¹, t = 2 s. Take DOWN as +, a = +9.8, u = +8.
     Height:  s = ut + ½at² = 8·2 + ½·9.8·2² = 16 + 19.6 = 35.6 m
     Impact v = u + at = 8 + 9.8·2 = 27.6 m s⁻¹ (downward)
```

### Listing 4 — Where the equations come from (velocity-time graph)
```text
Straight v–t line for constant a: from u up to v over time t.

  GRADIENT = a = (v − u)/t        ⇒  v = u + a t            [equation 1]

  AREA under the line = displacement s (a trapezium):
    as average height × width:    s = ½(u + v) t            [equation 4]
    as rectangle (u·t) + triangle (½·(at)·t):
                                  s = u t + ½ a t²           [equation 2]

  Combine 1 and 4 to eliminate t:  v² = u² + 2 a s           [equation 3]

⇒ The four equations are just the velocity-time graph (M1-02) written as algebra.
```
