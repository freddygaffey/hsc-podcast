# Physics textbook ingestion (Year 11 + Year 12)

Drop each textbook PDF here so questions can be generated **from the book** and cite real
pages. **The whole book never enters git** — only the single page a question cites is exposed.

## What to add

```
content/physics/textbook/y11/source.pdf     # ← place the Year 11 PDF here (LOCAL ONLY)
content/physics/textbook/y12/source.pdf      # ← place the Year 12 PDF here (LOCAL ONLY)
```

`source.pdf` and the extracted `pages.jsonl` are **gitignored** — they stay on your machine.
Then edit each `book.json` (title, edition, and `pageOffset`).

`pageOffset` maps a printed page to the PDF page: `pdf_page = printed_page + pageOffset`.
Open the PDF, find printed page 1, note which PDF page it is; `pageOffset = (that pdf page) − 1`.

## Then (I run these)

```bash
python3 tools/ingest_textbook.py extract content/physics/textbook/y11   # PDF → local pages.jsonl
python3 tools/ingest_textbook.py extract content/physics/textbook/y12
# …generate textbook-sourced quizzes (each cites a real page)…
python3 tools/ingest_textbook.py pages-for-quiz content/physics/<EP>/quiz.json content/physics/textbook/y11
```

`pages-for-quiz` renders **only the pages actually cited** into
`content/physics/sources/<slug>/p<NN>.jpg` — those single pages are committed + deployed
(login-gated per `content/_template-subject/sources/README.md`), and "View source ↗" opens them.

## How honesty is enforced

`tools/validate_quiz.py` (the pre-commit gate) cross-checks every `textbook` citation against
the digitized `pages.jsonl`: the cited page must exist and the question text must actually
overlap that page. A fabricated or wrong page reference fails the gate and cannot be committed.
