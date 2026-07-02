---
title: "Supplementary Materials — The Shai-Hulud npm Worm"
module: SSA
year: 12
lesson: "case-study"
script: script.md
---

# Supplementary Materials

Read-along reference for the case study. Nothing here is spoken in the audio. The
code listings are deliberately minimal and illustrative — they show the *shape* of
each mechanism, not the real attackers' code.

### Listing 1 — Timeline of the 2025 npm worm wave
```text
2025-09-08  The "Qix" phishing attack (the curtain-raiser)
   ~13:00 UTC  Maintainer "Qix" (Josh Junon) gets a fake 2FA-reset email from a
               look-alike domain (npmjs.help) and enters his username, password,
               and a live one-time code on a fake login page.
   13:16 UTC  ~18 packages published with malware: chalk, debug, ansi-styles,
               strip-ansi, color-convert, supports-color, and more.
               Combined reach: 2B+ downloads/week. Payload = browser crypto-clipper.
   ~within 2h  Community raises the alarm; maintainer reverts to clean versions.
               Actual theft: a few hundred USD. Reach was historic; damage was tiny
               only because a human drove it and was caught fast.

2025-09-15  "Shai-Hulud" — the first self-replicating supply-chain worm
               Patient zero: @ctrl/tinycolor. A postinstall script runs on install:
               scans the machine for secrets (TruffleHog), exfiltrates npm/GitHub/
               cloud tokens, dumps them into a PUBLIC GitHub repo named "Shai-Hulud",
               then uses the stolen npm token to auto-publish itself into every
               package the victim can publish. No human, no command-and-control.
               ~200 packages at first; counts later climbed past 500.
               2025-09-23  CISA issues a formal alert.

2025-11-24  "Shai-Hulud: The Second Coming" (2.0)
               Same self-propagating idea, sharpened. ~796 packages backdoored in a
               single morning, 20M+ downloads/week. Hides payload in innocuously
               named files; reuses tokens stolen from earlier victims to exfiltrate.
               ~500 developers had secrets stolen.
```

### Listing 2 — A normal feature (`postinstall`) abused to run code on install
```json
// package.json — "postinstall" is a legitimate npm hook for honest setup work.
// The hook is normal; the abuse is what the script it runs actually does.
{
  "name": "some-popular-utility",
  "version": "4.1.1",
  "scripts": {
    "postinstall": "node ./bundle.js"
  }
}
```

### Listing 3 — The self-propagation loop, in plain terms (illustrative)
```text
// bundle.js, described — NOT the real payload. This is what makes it a WORM
// rather than a one-shot theft: step 4 turns every victim into a launch pad.
//   1. Scan THIS machine for secrets — use a credential scanner (e.g. TruffleHog)
//      to sweep files, environment variables, and cloud metadata services.
//   2. Collect npm tokens, code-host (GitHub) tokens, and cloud keys (AWS/Azure/GCP).
//   3. Exfiltrate them — e.g. create a PUBLIC repo on the victim's own GitHub and
//      dump the stolen secrets there (theft + public exposure in one act).
//   4. With the stolen npm token, authenticate AS the victim, list every package
//      they may publish, inject a copy of this script into each, and publish them.
// Each new install of an infected package re-runs steps 1-4 → exponential spread.
```

### Listing 4 — One human attacker vs. a self-replicating worm
```text
                    Sep 8 "Qix" phishing        Shai-Hulud worm
  Driver            a human, in real time       automatic, self-running
  Reach             2B+ downloads/week           fewer packages...
  Damage            ~a few hundred USD           ...but far worse: mass secret theft
  How it ended      human spotted + caught (2h)  must revoke tokens on every machine
  Core danger       big reach                    NO HUMAN TO CATCH; spreads on its own
```

### Listing 5 — A "safe dependency update" / integrity check, in NESA pseudocode
```text
BEGIN SafeDependencyUpdate
    FOR EACH dependency IN project
        candidate ← latest available version
        IF candidate ≠ pinned_version THEN
            expected_hash ← integrity hash recorded in the lock file
            actual_hash ← compute hash of candidate package contents
            IF actual_hash ≠ expected_hash THEN
                REJECT candidate                  // contents do not match the lock
                RAISE alert "integrity check failed"
            ELSE IF install_scripts_enabled AND NOT scripts_reviewed THEN
                HOLD candidate                    // do not let postinstall run unseen
            ELSE IF provenance NOT verified THEN
                HOLD candidate FOR manual code review
            ELSE
                pinned_version ← candidate         // accept, then re-lock
                UPDATE lock file WITH candidate, actual_hash
            ENDIF
        ENDIF
    NEXT dependency
END SafeDependencyUpdate
```

### Key terms
```text
software supply chain  the chain of trust from a code author, through every package
                       that depends on another, down to the machine that runs it.
worm                   malware that reproduces and spreads on its own, with no human
                       driving each step (contrast: a one-shot, human-aimed attack).
postinstall script     an npm hook that runs code automatically when a package is
                       installed — legitimate, but abused here to run on every victim.
crypto-clipper         malware that silently rewrites a cryptocurrency transaction's
                       destination address while the screen still shows the right one.
phishing-resistant MFA second-factor login (e.g. passkeys) that a fake login page
                       cannot capture and replay — defeats a Qix-style con.
pinning + integrity    locking dependencies to specific versions, with cryptographic
                       fingerprints that reject any package whose contents changed.
provenance             verifiable proof of where a package was really built/published.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| 2FA | Two-Factor Authentication | Requiring two independent pieces of evidence to log in (e.g. password plus a code) |
| MFA | Multi-Factor Authentication | Requiring two or more independent factors to verify identity |
| NESA | NSW Education Standards Authority | The body that sets the HSC syllabus and exams in New South Wales |
| USD | United States Dollars | The currency unit used in cost/impact figures |
| UTC | Coordinated Universal Time | The primary global time standard, used for unambiguous timestamps |
