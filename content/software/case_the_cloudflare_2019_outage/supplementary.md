---
title: "Supplementary Materials — The Cloudflare 2019 Outage"
module: PFW
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Cloudflare 2019 outage case study. Nothing here is spoken in the audio —
the narration points at each listing by label only. Listing 1 is the timeline; Listing 2 demonstrates why
catastrophic backtracking explodes; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
Background  Cloudflare sits in front of a large fraction of the web as a reverse proxy + CDN + security
            layer. Its Web Application Firewall (WAF) runs rules -- many of them regular expressions --
            to spot malicious requests. A huge amount of the web's traffic flows through this one layer.
2 Jul 2019  Cloudflare deploys a new WAF managed rule (meant to better catch malicious inline JavaScript)
            GLOBALLY, to its entire network, in one go. The rule contains a regular expression with a
            pattern that can backtrack catastrophically: roughly ".*(?:.*=.*)".
~13:42 UTC  On real traffic, that pattern causes CPU to spike toward 100% on every core, network-wide.
            The proxy can no longer serve requests; visitors to sites behind Cloudflare get HTTP 502 errors.
            A large slice of the web appears to "go down" at once -- one rule, one regex, global blast radius.
~14:09 UTC  Engineers identify the WAF as the cause and use a global "kill switch" to disable it; CPU
            recovers and traffic returns. Total impact ~27 minutes.
After       Root cause: catastrophic backtracking in one regex, deployed everywhere at once with no
            performance guard. Fixes: performance budgets/limits on rules, staged (gradual) rollout
            instead of global-all-at-once, and moving toward a LINEAR-time regex engine (e.g. RE2).
```

### Listing 2 — Why catastrophic backtracking explodes (Python, runnable)
```python
def backtracking_attempts(n):
    """Illustrative model of a CATASTROPHIC-BACKTRACKING regex (e.g. nested quantifiers like '(a*)*'):
    on a non-matching input the engine tries an exponentially growing number of ways to match.
    Work roughly DOUBLES for every extra character -> 2**n."""
    return 2 ** n

def linear_attempts(n):
    """A LINEAR-time engine (e.g. RE2) does work proportional to the input length -- no explosion."""
    return n


# For a tiny input the difference is invisible -- which is why it sails through a quick test.
assert backtracking_attempts(5) == 32
assert linear_attempts(5) == 5

# As the input grows a little, the backtracking engine explodes while the linear one barely moves.
assert backtracking_attempts(30) == 1073741824           # ~1.07 BILLION attempts for 30 characters
assert linear_attempts(30) == 30                         # the safe engine: 30
assert backtracking_attempts(30) // linear_attempts(30) > 35_000_000   # ~36 million times more work

print("30 characters:", backtracking_attempts(30), "backtracking attempts vs",
      linear_attempts(30), "for a linear engine -- same input, wildly different cost.")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
The Cloudflare 2019 outage = one regex's ALGORITHMIC COST x a GLOBAL-all-at-once deployment.

1  AN ALGORITHM'S TIME COMPLEXITY IS A REAL RISK (not just "does it work?")
   A regex that works on test inputs can still be O(2^n) on a crafted/real input -- "catastrophic
   backtracking". Code review and unit tests that only check correctness miss it; you must consider
   WORST-CASE performance (Big-O), not just "did it return the right answer". (Ties to algorithmic
   efficiency / "order n" from OOP optimisation, and PFW 13-03 performance/page-load.)

2  BLAST RADIUS: DON'T DEPLOY GLOBALLY ALL AT ONCE
   The rule went to the ENTIRE network simultaneously, so one bad regex took down everything at once.
   A STAGED / gradual rollout (a small % first, watch, then expand) would have caught it on a sliver of
   traffic. (PFW 11-04 architecture/blast radius; SEE deployment methods -- phased/pilot beats big-bang.)

3  PERFORMANCE-TEST AND BUDGET, AND KEEP A KILL SWITCH
   Run new rules against a CPU/time budget before and during rollout; have a fast, global way to turn a
   change OFF. The kill switch is what ended the outage. (PFW 13-03 performance; SEE testing.)

4  CONCENTRATION IS POWER AND RISK
   Putting a huge slice of the web behind one fast, shared layer is great for performance and security --
   and means a single fault has enormous reach. Architecture decisions trade efficiency against blast
   radius. (PFW 11-04.) Compare case_the_dyn_dns_ddos_2016 (one DNS provider = a single point of failure).

PREVENTION: prefer LINEAR-time regex engines (RE2); cap regex complexity; staged rollout; performance
budgets; a kill switch. CASHES INTO: PFW 11-04 (architecture/blast radius), 13-03 (performance); SEE testing/deployment.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| CDN | Content Delivery Network | Geographically distributed servers that cache and serve content close to the user |
| CPU | Central Processing Unit | The processor that executes program instructions |
| DNS | Domain Name System | The system that translates human-readable domain names into IP addresses |
| HTTP | HyperText Transfer Protocol | The request/response protocol used to transfer web resources |
| OOP | Object-Oriented Programming | A paradigm structuring software around objects that bundle data and behaviour |
| UTC | Coordinated Universal Time | The primary global time standard, used for unambiguous timestamps |
| WAF | Web Application Firewall | A filter that inspects HTTP traffic to block web attacks |
