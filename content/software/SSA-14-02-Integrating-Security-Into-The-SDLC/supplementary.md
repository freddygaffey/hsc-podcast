---
title: "Supplementary Materials — Integrating Security into the SDLC"
module: SSA
year: 12
lesson: "14.2"
script: script.md
---

# Supplementary Materials

Read-along reference for this episode. Nothing here is spoken. The narration teaches the
eight SDLC steps with a security activity each, shift-left, and threat modelling with STRIDE.

### Listing 1 — STRIDE threat model for a login feature (threat modelling at design)

```text
Component: user login / authentication

STRIDE category          Threat (how it could go wrong here)            Countermeasure
-----------------------  --------------------------------------------   --------------------------------
S poofing                attacker logs in as another user               strong auth + MFA
T ampering               credentials/session altered in transit         TLS (HTTPS), integrity checks
R epudiation             user denies an action they performed           audit logging (accountability)
I nformation disclosure  password database leaks                        store SALTED HASHES, not plaintext
D enial of service       login flooded so real users can't sign in      rate limiting, account lockout
E levation of privilege  normal user gains admin access                 role-based access control, least privilege

Process: model the system -> identify threats (STRIDE) -> assess risk (Likelihood × Impact)
         -> define countermeasures -> validate. Done at DESIGN = cheapest to fix.
```

### Listing 2 — Security activity at each of the 8 SDLC steps (the six-marker scaffold)

```text
"Really Smart Developers Don't Ignore Testing In Maintenance"
  R  Requirements ....... gather security needs: confidentiality, integrity, auth, compliance
  S  Specifications ..... write them as TESTABLE rules ("passwords hashed", "lock after 5 fails")
  D  Design ............. threat model (STRIDE), trust boundaries, choose controls (MFA, RBAC, encryption)
  D  Development ........ secure coding: validate input, parameterised queries, salted-hash passwords
  I  Integration ........ verify controls still work when components are joined
  T  Testing & debugging  security testing: injection, auth bypass, authorisation checks  (-> 18-01)
  I  Installation ....... harden deployment: enforce HTTPS, lock config, restrict DB access
  M  Maintenance ........ patch vulns, monitor, update dependencies  (supply chain -> case_the_xz_backdoor)

Shift left  = move security effort EARLIER. Fixing in production ≈ 63× the design-phase cost.
Traps: "bolt security on at the end"  ·  "testing = security" (testing is ONE of eight phases).
```

### Listing 3 — Secure-login design in NESA pseudocode (built-in at design/development)

```text
BEGIN AuthenticateUser
    GET username, password FROM request
    VALIDATE username, password        // never trust input

    user ← LookupUser(username)
    IF user EXISTS AND user.lockedUntil > now THEN
        RETURN "Account locked"        // DoS / brute-force countermeasure
    ENDIF

    // Compare against the SALTED HASH, never a stored plaintext password.
    IF user EXISTS AND VerifyHash(password, user.salt, user.passwordHash) THEN
        user.failedAttempts ← 0
        LOG "login success", user.id    // accountability / non-repudiation
        RETURN StartSession(user)
    ELSE
        user.failedAttempts ← user.failedAttempts + 1
        IF user.failedAttempts ≥ 5 THEN LockAccount(user) ENDIF
        LOG "login failure", username    // do NOT reveal whether user or password was wrong
        RETURN "Invalid credentials"
    ENDIF
END AuthenticateUser
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| DB | Database | An organised, queryable store of persistent data |
| HTTPS | HyperText Transfer Protocol Secure | HTTP encrypted with TLS for confidentiality and integrity in transit |
| MFA | Multi-Factor Authentication | Requiring two or more independent factors to verify identity |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| RBAC | Role-Based Access Control | Granting permissions to roles, then assigning users to those roles |
| SDLC | Software Development Life Cycle | The staged process (requirements → design → build → test → maintain) for building software |
| STRIDE | Spoofing · Tampering · Repudiation · Information disclosure · Denial of service · Elevation of privilege | The six threat categories used in threat modelling |
| TLS | Transport Layer Security | The protocol that encrypts and authenticates data in transit (secures HTTPS) |
