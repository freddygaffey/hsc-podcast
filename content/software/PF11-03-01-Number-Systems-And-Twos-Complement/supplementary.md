---
title: "Supplementary Materials — Number Systems and Two's Complement"
module: PF11
year: 11
lesson: "3.1"
script: script.md
---

# Supplementary Materials

Worked conversions and runnable Python verification. Nothing here is spoken in the audio —
it's the read-along reference. The narration points at each by label only.

### Listing 1 — Decimal ↔ binary (45)
```text
DECIMAL -> BINARY (repeated division by 2; read remainders BOTTOM to TOP)
    45 ÷ 2 = 22  remainder 1   ^ read
    22 ÷ 2 = 11  remainder 0   |  up
    11 ÷ 2 = 5   remainder 1   |
     5 ÷ 2 = 2   remainder 1   |
     2 ÷ 2 = 1   remainder 0   |
     1 ÷ 2 = 0   remainder 1   | start
  => 101101₂

BINARY -> DECIMAL (sum the positional values where there is a 1)
  position:  5    4    3    2    1    0
  bit:       1    0    1    1    0    1
  value:    32  +  0 +  8 +  4 +  0 +  1   = 45
```

### Listing 2 — Binary ↔ hexadecimal (each hex digit = exactly 4 bits)
```text
BINARY -> HEX (group into 4-bit chunks FROM THE RIGHT; pad the LEFT with 0s)
  101101  ->  0010 | 1101
              0010 = 2
              1101 = 13 = D
  => 2D₁₆

4-bit reference table:
  0=0000  1=0001  2=0010  3=0011   4=0100  5=0101  6=0110  7=0111
  8=1000  9=1001  A=1010  B=1011   C=1100  D=1101  E=1110  F=1111

Check: 2D₁₆ = 2×16 + 13 = 32 + 13 = 45 ✓
```

### Listing 3 — Two's complement of −18 in 8 bits ("flip the bits, add 1")
```text
  +18 in 8 bits :   0001 0010
  step 1 — flip  :   1110 1101     (one's complement = JUST the flip)
  step 2 — add 1 :   1110 1110     (two's complement = flip AND add 1)

  => −18 = 11101110  (8-bit two's complement)
           ^ leftmost bit = 1 => negative (sign bit: 0 = positive, 1 = negative)

RANGE for N-bit two's complement:  −2^(N−1)  ..  +2^(N−1) − 1
   8-bit :  −128 .. +127     (asymmetric: one more negative, because 0 takes a positive slot)
  16-bit :  −32768 .. +32767
```

### Listing 4 — Verifying with Python's built-in bin / hex / int
```python
n = 45
assert bin(n) == "0b101101"          # decimal -> binary
assert hex(n) == "0x2d"              # decimal -> hexadecimal
assert int("101101", 2) == 45        # binary string -> decimal
assert int("2d", 16) == 45           # hex string -> decimal

# 8-bit two's complement bit pattern: mask with 0xFF (eight 1s)
assert (-18) & 0xFF == 0b11101110    # == 238
assert bin((-18) & 0xFF) == "0b11101110"
print("All number-system assertions passed.")
```

### Listing 5 — A reusable two's-complement function (runnable)
```python
def twos_complement(n, bits=8):
    """Return the `bits`-wide two's complement bit string of integer n."""
    low = -(2 ** (bits - 1))
    high = 2 ** (bits - 1) - 1
    if not (low <= n <= high):
        raise ValueError(f"{n} is out of range for {bits}-bit two's complement")
    return format(n & ((1 << bits) - 1), "0" + str(bits) + "b")


assert twos_complement(18) == "00010010"     # +18
assert twos_complement(-18) == "11101110"    # −18: flip the bits, add 1
assert twos_complement(-25) == "11100111"    # −25
assert twos_complement(-128) == "10000000"   # minimum of the 8-bit range
assert twos_complement(127) == "01111111"    # maximum of the 8-bit range
print("All twos_complement assertions passed.")
```

### Listing 6 — Decimal-to-binary conversion in NESA pseudocode (the examinable algorithm)
```text
BEGIN DecimalToBinary
    INPUT number                      // a non-negative integer
    bits ← ""                         // build the bit string
    IF number = 0 THEN
        bits ← "0"
    ENDIF
    WHILE number > 0 DO
        remainder ← number MOD 2      // 0 or 1
        bits ← remainder + bits       // PREPEND — same as "read remainders bottom to top"
        number ← number DIV 2         // integer division
    ENDWHILE
    OUTPUT bits
END DecimalToBinary
```
