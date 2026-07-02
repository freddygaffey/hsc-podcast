---
title: "Supplementary Materials — Security in Development Teams"
module: SSA
year: 12
lesson: "19.1"
script: script.md
---

# Supplementary Materials

Read-along reference for this episode. Nothing here is spoken. The narration teaches the three
benefits of collaboration — **V-D-Q: Views (various points of view), Delegate by expertise,
Quality of the solution** — and shows why code review, pair programming and collaborative threat
modelling are these benefits in action. These listings give the security review checklist, the
pair-programming role split, and a pseudocode model of a pull-request review gate.

### Listing 1 — A security-focused code-review checklist (text)

```text
SECURITY CODE REVIEW — a second point of view on every change (the "V" in V-D-Q).
Assign ONE accountable reviewer per change (avoids the bystander effect).

INPUT & DATA HANDLING
[ ] Every external input validated server-side with an allow-list?        (VSE, 16-01)
[ ] All DB access parameterised — no string-built SQL?                     (16-01 / PFW 13-02)
[ ] Output encoded before display — no XSS?                                (18-02 Part 1)

AUTH & ACCESS
[ ] Authorisation checked per request, not just authentication?           ("logged in is not allowed")
[ ] Sessions: strong random ID, HttpOnly/Secure/SameSite, regen on login? (S-A-F-E, 17-01)

SECRETS & CRYPTO
[ ] No hard-coded passwords / API keys / secrets in source?
[ ] Passwords hashed + salted + slowed; audited crypto library, not home-rolled? (15-02)

ERRORS & LOGIC
[ ] Errors fail securely — log private, show generic, default-deny?       (17-02)
[ ] Business logic safe — negative amounts, skipped steps, race windows?  (TOCTOU, 18-02 Part 2)

TRUST
[ ] Is this contributor trusted for this level of access? (x-z backdoor lesson)
```

### Listing 2 — Security-focused pair programming: the two roles (text)

```text
PAIR PROGRAMMING FOR SECURITY — two points of view on every line, in real time.

DRIVER (functional)                  NAVIGATOR (security)
- writes the primary functionality   - watches for security anti-patterns
- meets the business requirement     - asks the security questions, continuously:
- implements the security            "How do we validate this input?"
  suggestions as they come up        "What happens if this fails?"
- keeps the code readable            "Who should have access to this?"
                                     "How do we log this securely?"
                                     "What are the attack vectors here?"

Roles swap regularly. Result: the blind spot of one is covered by the other (the V in V-D-Q).
```

### Listing 3 — NESA pseudocode: a pull-request security review gate

```text
BEGIN ReviewPullRequest(change, author)
    // Structured collaboration: an ASSIGNED reviewer, not "the whole team"
    reviewer ← AssignReviewerByExpertise(change.area)   // DELEGATE by expertise (D)
    IF reviewer = author THEN
        REJECT "Self-review only — needs a second point of view"   // the V in V-D-Q
    ENDIF

    findings ← reviewer.ApplyChecklist(change)          // various points of view (V)
    runScanners(change)                                 // SAST/DAST complement, never replace, the human

    IF findings CONTAINS critical THEN
        REQUEST_CHANGES(findings)                       // raises QUALITY (Q) before merge
    ELSE
        DocumentSecurityDecisions(change)               // share knowledge → team standard rises
        APPROVE_AND_MERGE(change)
    ENDIF
END ReviewPullRequest
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| API | Application Programming Interface | A defined contract that lets one piece of software request services from another |
| DAST | Dynamic Application Security Testing | Testing a running application from the outside for security flaws ("doing") |
| DB | Database | An organised, queryable store of persistent data |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| S-A-F-E | Status · Abort · Feedback · Errors | Design principles for a safe control interface |
| SAST | Static Application Security Testing | Analysing source code for security flaws without running it ("source") |
| SQL | Structured Query Language | The standard language for querying and manipulating relational databases |
| TOCTOU | Time-Of-Check to Time-Of-Use | A race-condition flaw where state changes between validating and using it |
| V-D-Q | Various Views · Delegate by expertise · Quality | The benefits of collaborating in a development team rather than working solo |
| VSE | Validate · Sanitise · handle Errors | How to treat untrusted input at a trust boundary (server-side) |
| XSS | Cross-Site Scripting | An attack injecting malicious scripts into pages viewed by other users |
