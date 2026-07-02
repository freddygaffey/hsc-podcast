---
title: "Supplementary Materials — The Knight Capital Glitch"
module: SEE
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

The read-along reference for the Knight Capital case study. Nothing here is spoken in the audio — the
narration points at each listing by label only. Listing 1 is the timeline; Listing 2 models the
inconsistent-deploy + dead-code failure; Listing 3 maps the lessons onto the course.

### Listing 1 — Timeline (reference)
```text
Background  Knight Capital is a major US "market maker" -- automated software that buys and sells huge
            volumes of shares at machine speed. Its trading software is mission-critical and fast.
Setup       Knight prepares a new feature. Deployment is a MANUAL process across 8 production servers.
            To switch the new behaviour on, an engineer REUSES an old, retired feature flag -- one that
            years earlier had controlled long-dead code nicknamed "Power Peg" that was never removed.
1 Aug 2012  The new code is deployed to 7 of the 8 servers. ONE server is missed and keeps the old code.
            When the market opens, the reused flag turns ON -- and on that one stale server it wakes the
            dormant "Power Peg" code, which starts firing millions of erroneous orders into the market
            (buying high, selling low) at machine speed.
+~45 min    It takes about 45 minutes to work out what is happening and stop it. By then Knight has executed
            millions of unintended trades across ~150 stocks and lost about US$440 million -- roughly four
            times the company's annual profit, in three quarters of an hour.
After       The loss nearly bankrupts Knight overnight; it is rescued by investors and soon absorbed in a
            merger. One inconsistent deployment plus un-removed dead code ended the company's independence.
```

### Listing 2 — One stale server + reused flag = catastrophe (Python, runnable)
```python
def run_server(version, reused_flag_on):
    """Each server runs whatever code was deployed to it. On the OLD code, the reused flag wakes the
    long-dead 'Power Peg' routine, which floods the market with orders."""
    if version == "old" and reused_flag_on:
        return 1_000_000          # dormant code, reactivated by the repurposed flag -> a flood of orders
    return 1                      # the new code: one normal order


# A botched MANUAL deploy: 7 servers get the new code, 1 is missed and left on the old code.
# The flag was REUSED, so on the stale server it switches ON code that should have been deleted years ago.
servers = ["new"] * 7 + ["old"]
orders = sum(run_server(v, reused_flag_on=True) for v in servers)
assert orders >= 1_000_000        # a single inconsistent server floods the market

# THE FIX: deploy CONSISTENTLY to every server, and REMOVE dead code / never repurpose an old flag.
fixed = ["new"] * 8
orders_fixed = sum(run_server(v, reused_flag_on=True) for v in fixed)
assert orders_fixed == 8          # every server behaves; there is no dormant code left to wake
print("One stale server ->", orders, "orders (a flood). Consistent deploy + no dead code ->", orders_fixed, ".")
```

### Listing 3 — The lessons, mapped to the course (reference)
```text
Knight Capital is the marquee DEPLOYMENT + VERSION-CONTROL-HYGIENE failure: one botched release, lost a
company in 45 minutes.

1  DEPLOYMENTS MUST BE AUTOMATED, REPEATABLE, AND VERIFIED -- not error-prone manual steps
   A human manually copying code to 8 servers missed one. An automated, scripted deploy that verifies
   every server is identical would not have left a stale machine. Consistency across all servers is the
   whole point. (SEE 25-04 deployment hygiene; ties to the direct/big-bang risk in 23-03.)

2  REMOVE DEAD CODE; NEVER REPURPOSE AN OLD FLAG
   "Power Peg" should have been deleted long before. Leaving years-dead code in the system, then reusing
   its flag for something new, is what turned a missed server into a money-firing machine. Version-control
   hygiene -- R-C-B-M-T (Repository, Commit, Branch, Merge, Tag), small commits, clean releases -- includes
   actually retiring old code. (SEE 25-04.)

3  YOU NEED A FAST ROLLBACK / KILL SWITCH -- and a tested one
   It took ~45 minutes to stop, at machine speed -- an eternity. A safe system can be halted or rolled back
   to the last good release in seconds. Rollback is a planned feature, not an improvisation. (SEE 25-04
   rollback; 25-05 overcoming difficulties -- escalate and act fast under pressure.)

4  TEST THE DEPLOYMENT + MONITOR FOR RUNAWAY BEHAVIOUR
   Test the release process itself (does every server end up identical?), and monitor production for
   abnormal behaviour -- a flood of orders should trip an automatic circuit-breaker, not run for 45 minutes.
   (SEE 26-01 testing.)

5  AUTOMATION x SPEED x SCALE = the blast radius
   Software acting automatically, at machine speed, turns a deploy slip into a $440M loss in under an hour.
   The faster and more automated the system, the more it needs guardrails. (Compare case_the_cloudflare_2019_outage.)

CASHES INTO: SEE 25-04 (version control/deployment/rollback), 26-01 (testing), 25-05 (difficulties).
Companion to case_the_denver_airport_baggage and case_the_healthcare_gov_launch.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| R-C-B-M-T | Repository · Commit · Branch · Merge · Tag | Core version-control concepts |
