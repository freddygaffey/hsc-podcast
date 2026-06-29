# `sources/` — traceability assets for quiz questions

This folder holds the **original material** a quiz question links back to, so a student can
verify any question against its source (`source.url` in `quiz.json`).

```
content/{subject}/sources/{book-slug}/p{NN}.jpg     # textbook page scans
content/{subject}/papers/{year}/{paper}.pdf         # past papers (see papers/, public)
```

A question references one like this:

```json
"source": { "origin": "textbook", "ref": "Jacaranda Physics 12", "page": 388,
            "url": "sources/jac-phy12/p388.jpg" }
```

## Copyright — read before adding scans

- **Past papers** are public NESA documents — host and link them freely (use `papers/`, and
  `#page=N` anchors in the PDF URL to jump to the right page).
- **Textbook pages are copyright.** Only add scans you have the right to use, and serve this
  `sources/` tree **behind login**, not on the public origin — it's a personal-study aid, not
  a public textbook mirror.

### Gating `sources/` behind login

The app's `auth-worker` is a sync/auth API; it does **not** proxy static files. To require a
signed-in session for these assets, add a **Cloudflare Access** policy on the deploy (one-time,
in the dashboard or `wrangler`/Terraform), scoping a self-hosted application to the path:

```
{your-pages-domain}/content/*/sources/*
```

with a policy allowing your authenticated users (e.g. an email/OTP or identity-provider rule).
Until that policy exists, **omit `source.url` for textbook items** and let the badge show the
citation (`ref` + `page`) as plain text — the student looks the page up themselves. The app
already does the right thing when `url` is absent.
