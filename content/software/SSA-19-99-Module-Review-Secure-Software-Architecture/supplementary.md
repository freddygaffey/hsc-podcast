---
title: "Supplementary Materials — Module Review: Secure Software Architecture (Chapters 14–19)"
module: SSA
year: 12
lesson: "14–19"
script: script.md
---

# Supplementary Materials

Read-along reference for the whole-module review. Nothing here is spoken. No new content — these
listings consolidate the entire module: the mnemonic master list, the eight marker distinctions,
the integrated CIA-AAA stimulus walk-through, and the three case studies mapped across chapters.

### Listing 1 — The SSA mnemonic master list (dump CIA-AAA in second one of the exam) (text)

```text
CH14 MINDSET
  D-A                          protect Data, prevent Attacks (benefits); security = ENABLER not cost
  "Really Smart Developers Don't Ignore Testing In Maintenance"  = 8 SDLC steps
  shift left · STRIDE          (Spoofing/Tampering/Repudiation/Info-disclosure/DoS/Elevation)
  "secure default, easy right path" · "Risk = Likelihood x Impact"
CH15 PRINCIPLES
  CIA-AAA   ★MARQUEE★          Confidentiality/Integrity/Availability + Authentication/Authorisation/Accountability
                              CIA = what we protect; AAA = how. (secrecy / accuracy / access · who / what / what-you-did)
  "Hash is one-way, Encrypt is two-way" · "hash it, salt it, slow it" · "salt stops the rainbow"
  "Symmetric = Same key; Asymmetric = A pair" · "sign with private, verify with public"
  "Good Spies Rotate Disguises" (Generate/Store/Rotate/Destroy) · sandbox = playpen code can't climb out of
CH16 DATA
  VSE (Validate/Sanitise/handle Errors) · "allow-list beats block-list" · "validation rejects, sanitisation cleans"
  "injection and XSS are the same disease" · "log it private, show it generic"
  PER (Proactive/Embed/Respect) · "collect less, keep less" · "privacy ≠ security"
CH17 SYSTEMS
  A-A-R-T (Authenticate/Authorise/Rate-limit/Transport-secure) · "authenticated is NOT authorised"
  S-A-F-E sessions (Strong/Attributes/Fixed-lifetime/regen-on-Escalation) · "CORS is not access control"
  M-S-E (Memory/Session/Exception) · "../ climbs out" · "compare in constant time"
CH18 TEST + VULNS
  CR-SAST-DAST-VA-PEN · "Static = Source; Dynamic = Doing" · H-B-D (Harden/Breach-handle/Disaster-recover)
  B-X-I-R (Broken-auth/Cross-site/Invalid-redirect/Race) · "XSS injects a Script; CSRF rides a Session" · TOCTOU
CH19 CONTEXT
  V-D-Q (Views/Delegate-by-expertise/Quality) · PIP-PB (Products/Influence/Practices/Productivity/Business-interactivity)
  E-D-P-C-I-D "Ed Picid" (Employment/Data-security/Privacy/Copyright/IP/Digital-disruption) · M-A-I (Measure/Audit/Improve)
```

### Listing 2 — The eight marker distinctions (the traps) (text)

```text
1 Authentication vs Authorisation   who you are        vs  what you may do (authenticate THEN authorise)
2 Confidentiality vs Integrity      reading            vs  changing (fail independently)
3 Hashing vs Encryption             one-way (integrity) vs two-way (confidentiality) — passwords are HASHED
4 Validation vs Sanitisation        reject             vs  clean
5 SAST vs DAST                      source, not running vs  app, running
6 XSS vs CSRF                       inject a script    vs  forge a request (ride a session)
7 Privacy vs Security               should you collect? vs  is what you hold protected?
8 Copyright vs IP                   one TYPE of IP     vs  the whole category (also patents/trademarks/secrets)
```

### Listing 3 — Integrated stimulus: the vulnerable health portal, every CIA-AAA violation (text)

```text
FLAW                              SYLLABUS TERM              PROPERTY BROKEN     FIX (mnemonic)
plain HTTP login                  no transport security     Confidentiality     TLS/HTTPS:443 (A-A-R-T, 15-02)
unsalted fast MD5 passwords       weak password storage     Confidentiality     hash+salt+slow (15-02)
input concatenated into SQL       SQL injection             Integrity+Conf.     parameterise (VSE, 16-01)
search echoed unencoded           reflected XSS             Integrity+Conf.     output encode + CSP (18-02)
change URL id → any record        broken access control     Authorisation       authz + ownership check (17-01)
password-only login               weak authentication       Authentication      MFA (15-01)
over-collect DOB/address/Medicare privacy / over-collection (privacy)           data minimisation (PER, 16-02) + legal (19-03)
stack trace shown to user         information disclosure    Confidentiality     log private/show generic (16-01, M-S-E 17-02)
no access logging                 no audit trail            Accountability      audit logging (15-01)

ANSWER PATTERN (band 6): flaw → exact term → CIA-AAA property → named fix. Repeat for each.
```

### Listing 4 — The three case studies mapped across the module (text)

```text
CASE              STORY                                         CASHES INTO (chapters)
xz backdoor       2-yr social-eng maintainer takeover →         14-02 supply chain · 18-01 code review caught it ·
(2024)            backdoor in Linux; caught by 0.5s slowdown    19-01 trust/collaboration · 19-03 OSS ethics/disclosure
Equifax           1 unpatched framework vuln → 147M records;    14-01 business case · 18-01 missed VA/patch ·
(2017)            hundreds of millions in settlements           19-02 enterprise cost (lost PIP-PB) · 19-03 legal/Privacy Act
Heartbleed        TLS memory over-read leaked private keys;     15-02 TLS · 17-02 memory mgmt · 18-01 testing
(2014)            sound maths, buggy implementation
```

### Listing 5 — The bridge to Software Automation (text)

```text
SSA = make software TRUSTWORTHY  →  SA = make software SMART (AI/ML + automation). Security travels with you:
- DATA:           ML trains on (often personal) data → PER / data minimisation / Privacy Act return as AI data ethics;
                  CIA confidentiality now also protects training data.
- ETHICS (Ed Picid): employment + digital disruption get SHARPER when AI does the displacing; + new issue = bias/fairness.
- ACCOUNTABILITY: CIA-AAA's "who did what" becomes "who is responsible when the algorithm gets it wrong".
NEXT EPISODE: SA-20-01 — what AI actually is, vs ML, and where RPA/BPA fit. New hooks; CIA-AAA/PER/Ed-Picid persist.
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| A-A-R-T | Authenticate · Authorise · Rate-limit · Transport-secure | Four rules for securing an API endpoint |
| AAA | Authentication · Authorisation · Accountability | The three access-security pillars: prove who you are, check what you may do, and keep a traceable record |
| AI | Artificial Intelligence | Software that performs tasks normally needing human intelligence |
| B-X-I-R | Broken authentication/session · Cross-site (XSS/CSRF) · Invalid redirect · Race condition | Common web-application vulnerabilities |
| BPA | Business Process Automation | Automating whole multi-step business workflows, not just single tasks |
| CIA | Confidentiality · Integrity · Availability | The three core information-security properties (the security triad) |
| CORS | Cross-Origin Resource Sharing | Browser rules controlling when a page may request resources from another origin |
| CR | Code Review | Manual inspection of source code by other developers to catch defects |
| CSRF | Cross-Site Request Forgery | An attack that tricks a logged-in user's browser into sending an unwanted request |
| DAST | Dynamic Application Security Testing | Testing a running application from the outside for security flaws ("doing") |
| E-D-P-C-I-D | Employment · Data security · Privacy · Copyright · Intellectual property · Digital disruption | Checklist ("Ed Picid") of the social, ethical and legal issues raised by software |
| H-B-D | Harden · Breach-handle · Disaster-recover | Layered approach to security resilience and business continuity |
| HTTP | HyperText Transfer Protocol | The request/response protocol used to transfer web resources |
| HTTPS | HyperText Transfer Protocol Secure | HTTP encrypted with TLS for confidentiality and integrity in transit |
| IP | Intellectual Property | Creations of the mind (code, designs, content) protected by copyright, patents and trademarks |
| M-A-I | Measure · Audit · Improve | The continuous, outcome-based security-evaluation loop |
| M-S-E | Memory · Session · Exception management | Resource-management concerns in secure execution |
| MFA | Multi-Factor Authentication | Requiring two or more independent factors to verify identity |
| ML | Machine Learning | AI systems that learn patterns from data rather than being explicitly programmed |
| OSS | Open-Source Software | Software whose source code is publicly available and licensed for reuse |
| PEN | Penetration test | An authorised simulated attack that chains real exploits to prove impact |
| PER | Proactive · Embed · Respect | The privacy-by-design principles (act ahead of harm, build privacy in, respect the user) |
| PIP-PB | Products/services · Influence on future development · Practices · Productivity · Business | The organisational benefits an enterprise gains from a strong security program |
| RPA | Robotic Process Automation | Software 'bots' that automate repetitive, rule-based user tasks |
| S-A-F-E | Status · Abort · Feedback · Errors | Design principles for a safe control interface |
| SAST | Static Application Security Testing | Analysing source code for security flaws without running it ("source") |
| SDLC | Software Development Life Cycle | The staged process (requirements → design → build → test → maintain) for building software |
| SQL | Structured Query Language | The standard language for querying and manipulating relational databases |
| STRIDE | Spoofing · Tampering · Repudiation · Information disclosure · Denial of service · Elevation of privilege | The six threat categories used in threat modelling |
| TLS | Transport Layer Security | The protocol that encrypts and authenticates data in transit (secures HTTPS) |
| TOCTOU | Time-Of-Check to Time-Of-Use | A race-condition flaw where state changes between validating and using it |
| URL | Uniform Resource Locator | The address that identifies and locates a resource on the web |
| V-D-Q | Various Views · Delegate by expertise · Quality | The benefits of collaborating in a development team rather than working solo |
| VA | Vulnerability Assessment | Systematically scanning and cataloguing known weaknesses (breadth over depth) |
| VSE | Validate · Sanitise · handle Errors | How to treat untrusted input at a trust boundary (server-side) |
| XSS | Cross-Site Scripting | An attack injecting malicious scripts into pages viewed by other users |
