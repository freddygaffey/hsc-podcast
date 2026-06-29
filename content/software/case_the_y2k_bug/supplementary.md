---
title: "Supplementary Materials — The Y2K Bug"
module: PF11
year: 11
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Y2K case study. Nothing here is spoken in the audio — the narration
points at each listing by label only. Listing 1 is the timeline; Listing 2 is a runnable demonstration
of the bug and its fixes; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
1960s-80s   Memory and storage are scarce and expensive, so programmers store the YEAR as just two
            digits -- "99" for 1999 -- to save space. It is everywhere: banking, payroll, government,
            embedded systems, and especially huge COBOL business systems. A sensible shortcut... for now.
1980s-90s   The shortcut becomes invisible infrastructure. The original programmers move on; the code
            keeps running, decade after decade, mostly forgotten -- but still assuming the year starts "19".
~1995-99    The realisation goes mainstream: when "99" rolls over to "00", systems will read "00" as 1900,
            not 2000. Date arithmetic will break -- ages, interest, expiry dates, sorting, schedules.
            A massive global remediation begins: auditing and fixing billions of lines of legacy code.
            Estimates of the worldwide effort run into the hundreds of billions of dollars.
31 Dec 1999 The world holds its breath at midnight as the date rolls to 1 January 2000.
2000        Almost nothing serious happens. A handful of minor glitches; no catastrophe. Because of the
            preparation -- not despite it -- the rollover is a non-event. Which then sparks an argument:
            "was it ever a real threat, or an overhyped waste?" Most engineers credit the remediation.
```

### Listing 2 — The bug, and the two ways it was fixed (Python, runnable)
```python
# THE SHORTCUT: store only the last two digits of the year to save memory.
def age_two_digit(birth_yy, now_yy):
    return now_yy - birth_yy

assert age_two_digit(85, 99) == 14      # born '85, year '99 -> 14. Fine, while we stay in the 1900s.
assert age_two_digit(85, 0) == -85      # THE BUG: year 2000 is stored as '00' -> 0 - 85 = a NEGATIVE age.

# FIX 1 -- EXPANSION (the proper fix): store the FULL four-digit year. Date maths just works.
def age_four_digit(birth_year, now_year):
    return now_year - birth_year

assert age_four_digit(1985, 1999) == 14
assert age_four_digit(1985, 2000) == 15     # crosses the year-2000 boundary correctly

# FIX 2 -- WINDOWING (the cheap stopgap): keep two digits, but INTERPRET them with a pivot --
# years below the pivot mean 2000s, the rest mean 1900s. Buys time without rewriting storage.
def windowed_year(yy, pivot=30):
    return 2000 + yy if yy < pivot else 1900 + yy

assert windowed_year(99) == 1999
assert windowed_year(0)  == 2000
assert windowed_year(25) == 2025
print("Two-digit years give a negative age in 2000; full years and windowing both fix it.")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
Y2K is, at heart, a DATA-REPRESENTATION story: how you choose to store a value has consequences that
can outlive the programmer by decades.

1  CHOOSING A DATA TYPE / FORMAT IS A REAL ENGINEERING DECISION
   Two digits vs four digits is a choice about storage, range, and the future. The "save two digits"
   shortcut was reasonable in 1970 and catastrophic in 2000. (PF11 3.1 number systems/storage; 3.2 data
   types -- e.g. "never store money in a float", store dates as a proper date type.)

2  SHORTCUTS BECOME TECHNICAL DEBT THAT COMPOUNDS
   A small saving, multiplied across billions of records and decades, became a global, hundreds-of-
   billions-of-dollars problem. The bill for a shortcut is paid later, with interest.

3  BOUNDARIES ARE WHERE THINGS BREAK
   The failure was at a boundary -- the 99 -> 00 rollover. Test the edges and the rollovers, not just the
   middle. (PF11 4.6 test data: boundary values; the date boundary was THE case to test.)

4  SUCCESSFUL ENGINEERING IS OFTEN INVISIBLE
   Because the fix worked, nothing happened -- and people then called it a hoax. Prevention that works
   looks like nothing was ever wrong. Don't mistake a problem that was quietly prevented for one that
   never existed.

FIX STYLES: EXPANSION (store the full year -- the real fix) vs WINDOWING (reinterpret two digits with a
pivot -- a cheap stopgap that just moves the problem to a future pivot year). CASHES INTO: PF11 3.1, 3.2,
4.6. A companion to case_the_mariner_1 (a tiny representational/coding slip with outsized cost).
```
