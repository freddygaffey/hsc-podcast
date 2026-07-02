---
title: "Supplementary Materials — Module Summary: Programming for the Web"
module: PFW
year: 12
lesson: "11–13"
script: script.md
---

# Supplementary Materials

The one-page revision references for the whole Programming for the Web module. Nothing here is spoken in the audio — it's the read-along sheet. Listing 1 is the master mnemonic table; Listing 2 is the key-terms checklist by topic.

### Listing 1 — Master mnemonic table (every PFW mnemonic + full expansion)
```text
EXAM-DUMP MARQUEE HOOKS (write these first):
  I-E-P · MISO · Dogs Take Tasty Hambones · 80/443/22/21 · Front-Back-Store
  + Ch13 build hooks: R-H-D-R · So Few Workers Go Home On-time · C-C-C-L

CH 11 — TRANSMISSION & TRANSPORT
  I-E-P              = Interactive website / E-commerce / Progressive web app
  MISO               = Manifest, Installable, Service worker, Offline (PWA essentials)
  Dogs Take Tasty Hambones = DNS -> TCP -> TLS -> HTTP (request journey order)
  IPv4               = four numbers, 0-255, dots between
  name/number/translator = domain name / IP address / DNS (the translator)
  80/443/22/21       = 80 plain (HTTP), 443 safe (HTTPS), 22 secure shell (SSH/SFTP),
                       21 file (FTP)  [+ DNS 53]
  Symmetric=Same key; Asymmetric=A pair  (same key fast / key pair solves sharing)
  Authentication = who you are; Authorisation = what you can do
  Hash is one-way, Encrypt is two-way
  3 Vs               = Volume, Velocity, Variety (defines big data)
  M-M-S              = Mining, Metadata, Streaming
  one block / many services / tiny functions = monolith / microservices / serverless

CH 12 — STANDARDS, ARCHITECTURE & DESIGN
  WIPS-M             = WAI accessibility, Internationalisation, Privacy, Security,
                       Machine-readable data (W3C's five concerns)
  POUR               = Perceivable, Operable, Understandable, Robust (WCAG principles)
  i18n vs l10n       = internationalise = prepare; localise = adapt
  Front, Back, Store = client/front-end, server/back-end, database (the 3 tiers)
  SQL=Spreadsheet of tables; NoSQL=Notebook of documents
  E-N-S-P            = Elements, Network, Storage, Performance (dev-tool panels) [+Console]
  4xx/5xx            = 4xx the request/permissions; 5xx the server
  Structure, Style, Behaviour = HTML / CSS / JS (separation of concerns)
  C-FAN-H            = Consistency, Feedback, Accessibility, Navigation, Hierarchy (UI/UX)
  "you call a library; a framework calls you" = inversion of control
  F-T-C              = Frameworks, Template engines, predesigned CSS classes
  BUILD vs BUY       = bespoke/unique/perf/control  vs  standard/tight-timeline/known
  L-C-C              = Licence, Community, Contribution (open-source pillars)
  Permissive=Polite (use freely, attribute); Copyleft=Contagious (share-alike derivatives)

CH 13 — BUILDING THE BACK END, DATA, SPEED & PWA
  R-H-D-R            = Route, Handle, Data, Respond (back-end request lifecycle)
  CRUD               = Create/Read/Update/Delete = INSERT/SELECT/UPDATE/DELETE
                       = POST/GET/PUT/DELETE
  So Few Workers Go Home On-time = SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY
  INNER keeps matches in both; LEFT keeps everything on the left
  "parameterise — pass the value separately so it can never become code"
  C-C-C-L            = Cache, Compress, CDN, Lazy-load (the four speed levers)
  MISO (built here)  = Manifest, Installable, Service worker, Offline
```

### Listing 2 — Key-terms checklist by topic
```text
[ ] 11-01 Applications: interactive (dynamic, no reload) / e-commerce (secure $ + data)
        / PWA (installable + offline); match scenario's driving requirement
[ ] 11-02 Data movement: packets (numbered, reassembled by sequence, out-of-order);
        IP address; IPv4 vs IPv6 (exhaustion); DNS hierarchy (cache->resolver->root
        ->TLD->authoritative) + TTL; request order DNS->TCP->TLS->HTTP
[ ] 11-03 Protocols/ports/transport: protocol=rules; port=service doorway;
        ports 80/443/22/21/53; SSL(old) vs TLS(current); plaintext/ciphertext;
        symmetric vs asymmetric; TLS handshake (cert -> asymmetric -> symmetric);
        authn vs authz; hashing; digital signature (sign private/verify public)
[ ] 11-04 Big data/architecture: 3 Vs; data mining (pattern discovery); metadata;
        streaming mgmt (high-velocity real-time); monolith/microservices/serverless;
        CDN (edge caching)
[ ] 12-01 W3C/standards: recommends NOT enforces; W3C Recommendation; five concerns
        (WIPS-M); WCAG/POUR; contrast >=4.5:1; alt text/labels; keyboard+focus;
        i18n vs l10n; machine-readable (ARIA/microdata/JSON-LD)
[ ] 12-02 Modelling system: Front/Back/Store tiers; client untrusted vs server trusted
        -> validate server-side; SQL/relational + ACID vs NoSQL/documents; middleware;
        API as contract + security boundary
[ ] 12-03 Browser/dev tools: rendering + JS engines; cross-browser compatibility;
        feature detection; progressive enhancement; same-origin policy + CORS;
        panels E-N-S-P + Console; status triage 4xx/5xx
[ ] 12-04 CSS/UI/UX: separation of concerns (Structure/Style/Behaviour); external
        stylesheet + design tokens (maintainability); responsive/media queries/mobile-
        first (NOT a PWA); UI=look vs UX=experience; C-FAN-H; accessibility techniques
[ ] 12-05 Libraries/frameworks: inversion of control; F-T-C three types; SPA;
        server-side rendering (template engine on Back); BUILD vs BUY; adoption
        benefits (speed/tested/consistency/community) + costs (bundle/learning/lock-in)
[ ] 12-06 Open source/CMS: free-as-in-freedom; L-C-C pillars; permissive vs copyleft
        (MIT/Apache/BSD vs GPL); software supply chain (xz); CMS = DB+template+admin;
        hosted vs self-hosted
[ ] 13-01 Server-side Python: R-H-D-R lifecycle; web server (nginx) vs web framework
        (Flask); request/response/session; CRUD<->SQL<->HTTP; untrusted input ->
        injection/XSS; shell scripting
[ ] 13-02 Databases/SQL/ORM: clause order (So Few Workers Go Home On-time);
        WHERE vs HAVING; GROUP BY + aggregate; INNER vs LEFT JOIN; PK<->FK;
        SQL injection -> parameterised query/prepared statement; ORM (fit/predict
        mapping classes<->tables) + trade-offs; hybrid ORM+raw SQL
[ ] 13-03 Performance: measure-before-optimise (profile, no premature optimisation);
        C-C-C-L; Cache-Control; Redis; gzip/Brotli + minify; CDN edge; lazy-load;
        bundling; private vs public cache (no-store)
[ ] 13-04 PWA: MISO; manifest JSON; installable/standalone; service worker = network
        proxy intercepting requests; offline app shell + background sync; HTTPS
        required; apply C-FAN-H + POUR to app shell; PWA != responsive
```

## Glossary
| Term | Expansion | Meaning |
|---|---|---|
| ACID | Atomicity · Consistency · Isolation · Durability | The four properties that guarantee a database transaction is processed reliably |
| API | Application Programming Interface | A defined contract that lets one piece of software request services from another |
| BSD | Berkeley Software Distribution (licence) | A permissive open-source software licence |
| C-C-C-L | Cache · Compress · CDN · Lazy-load | The four levers for faster page loads |
| CDN | Content Delivery Network | Geographically distributed servers that cache and serve content close to the user |
| CMS | Content Management System | Software for creating and managing website content without hand-coding each page |
| CORS | Cross-Origin Resource Sharing | Browser rules controlling when a page may request resources from another origin |
| CRUD | Create · Read · Update · Delete | The four basic operations performed on stored (database) records |
| CSS | Cascading Style Sheets | The language that styles and lays out HTML content |
| DB | Database | An organised, queryable store of persistent data |
| DNS | Domain Name System | The system that translates human-readable domain names into IP addresses |
| E-N-S-P | Elements · Network · Storage · Performance | The browser developer-tool panels (plus Console) |
| F-T-C | Frameworks · Template engines · predesigned CSS Classes | Front-end tools and libraries |
| FK | Foreign Key | A column that references the primary key of another table to link records |
| FTP | File Transfer Protocol | A protocol for transferring files between hosts (insecure unless secured) |
| GPL | GNU General Public License | A copyleft open-source licence requiring derivative works to stay open |
| HTML | HyperText Markup Language | The language that structures the content of web pages |
| HTTP | HyperText Transfer Protocol | The request/response protocol used to transfer web resources |
| HTTPS | HyperText Transfer Protocol Secure | HTTP encrypted with TLS for confidentiality and integrity in transit |
| I-E-P | Interactive website · E-commerce · Progressive web app | Applications of web programming |
| IP | Internet Protocol | The protocol that addresses and routes data packets across networks |
| JS | JavaScript | The programming language that runs in web browsers |
| JSON | JavaScript Object Notation | A lightweight, human-readable text format for exchanging structured data |
| L-C-C | Licence · Community · Contribution | Pillars to weigh when choosing open-source software |
| M-M-S | Mining · Metadata · Streaming | Big-data concepts |
| MISO | Manifest · Installable · Service worker · Offline | The four capabilities that distinguish a Progressive Web App from an ordinary website |
| MIT | Massachusetts Institute of Technology | In licensing, the MIT License — a short, permissive open-source licence; also the US university it is named after |
| ORM | Object-Relational Mapping | A layer that maps database tables to program objects so you write code, not raw SQL |
| PK | Primary Key | The column that uniquely identifies each row in a database table |
| POUR | Perceivable · Operable · Understandable · Robust | The four WCAG accessibility principles for web content |
| PWA | Progressive Web App | A website that can install, work offline and behave like a native app |
| R-H-D-R | Route · Handle · Data · Respond | The back-end request lifecycle |
| SFTP | SSH File Transfer Protocol | A secure, encrypted protocol for transferring files over SSH |
| SPA | Single-Page Application | A web app that loads one page and updates content dynamically via JavaScript |
| SQL | Structured Query Language | The standard language for querying and manipulating relational databases |
| SSH | Secure Shell | An encrypted protocol for remote login and command execution |
| SSL | Secure Sockets Layer | The predecessor to TLS for encrypting network connections |
| TCP | Transmission Control Protocol | The protocol providing reliable, ordered delivery of data over IP |
| TLS | Transport Layer Security | The protocol that encrypts and authenticates data in transit (secures HTTPS) |
| UI | User Interface | The parts of a system a user directly interacts with |
| UX | User Experience | The overall quality of a user's interaction with a product |
| W3C | World Wide Web Consortium | The body that develops open web standards (HTML, CSS, WCAG) |
| WAI | Web Accessibility Initiative | The W3C effort that produces web accessibility guidelines |
| WCAG | Web Content Accessibility Guidelines | The W3C standard defining how to make web content accessible (see POUR) |
| XSS | Cross-Site Scripting | An attack injecting malicious scripts into pages viewed by other users |
