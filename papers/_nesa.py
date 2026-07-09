#!/usr/bin/env python3
"""Download official HSC exam papers straight from NESA (nsw.gov.au).

No rate limit: these are hosted on the government CDN. Covers 2014-2025 for
Physics, all Maths courses, and all English courses. Enumerates exam-pack pages
via the site's public Elasticsearch API, then pulls the PDF assets from each
page. Saves to papers/<Subject>/HSC-NESA/. Fully resumable.
"""
import re, os, json, time, html, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.nsw.gov.au"
ES   = f"{BASE}/api/v1/elasticsearch/prod_content/_search"
UA   = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

# NESA slug -> our subject folder. "-archive" slugs are the older-year packs.
SUBJECTS = {
    "physics": "Physics", "physics-archive": "Physics",
    "mathematics-advanced": "Maths Advanced", "mathematics-archive": "Maths Advanced",
    "mathematics-extension-1": "Maths Extension 1", "mathematics-extension-1-archive": "Maths Extension 1",
    "mathematics-extension-2": "Maths Extension 2", "mathematics-extension-2-archive": "Maths Extension 2",
    "mathematics-standard": "Maths Standard 2", "mathematics-general-archive": "Maths Standard 2",
    "english-advanced": "English Advanced", "english-advanced-archive": "English Advanced",
    "english-standard": "English Standard", "english-standard-archive": "English Standard",
    "english-extension-1": "English Extension 1", "english-extension-1-archive": "English Extension 1",
    "english-extension-2": "English Extension 2", "english-extension-2-archive": "English Extension 2",
    "english-eald": "English EAL-D", "english-esl-archive": "English EAL-D",
    "english-studies": "English Studies",
    "design-and-technology": "Design & Technology",
    "software-engineering": "Software",
    "software-design-and-development-archive": "Software",
}

# Small words kept lowercase in a derived folder name (except when first).
STOP = {"of", "the", "to", "in", "on"}
ACRONYMS = {"Pdhpe": "PDHPE", "Eald": "EAL-D"}

def folder_from_slug(slug):
    """Turn an unmapped NESA slug into a tidy subject folder name.
    e.g. earth-and-environmental-science -> 'Earth & Environmental Science',
         studies-of-religion -> 'Studies of Religion', french-continuers -> 'French Continuers'."""
    if slug.endswith("-archive"):
        slug = slug[:-len("-archive")]
    out = []
    for i, w in enumerate(slug.split("-")):
        if w == "and":
            out.append("&")
        elif w in STOP and i > 0:
            out.append(w)
        else:
            word = w[:1].upper() + w[1:]
            out.append(ACRONYMS.get(word, word))
    return " ".join(out)

def log(msg):
    print(msg, flush=True)
    with open(os.path.join(HERE, "_nesa.log"), "a") as f:
        f.write(msg + "\n")

def fetch(url, data=None, timeout=60):
    hdr = dict(UA)
    if data is not None: hdr["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdr)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def enumerate_pages():
    body = json.dumps({"size": 2000, "_source": ["url"],
                       "query": {"wildcard": {"url": "*hsc-exam-papers*"}}}).encode()
    d = json.loads(fetch(ES, body))
    pat = re.compile(r'/hsc-exam-papers/([^/]+)/(\d{4})$')
    pages = []
    for h in d["hits"]["hits"]:
        u = h["_source"].get("url")
        if isinstance(u, list): u = u[0] if u else ""
        m = pat.search(u or "")
        if m:
            slug = m.group(1)
            folder = SUBJECTS.get(slug) or folder_from_slug(slug)
            pages.append((folder, m.group(2), u))
    return sorted(set(pages))

def pdf_links(page_html):
    out = []
    for href in re.findall(r'href="([^"]+\.pdf[^"]*)"', page_html, re.I):
        href = html.unescape(href)
        if href.startswith("/"): href = BASE + href
        out.append(href)
    return sorted(set(out))

def main():
    log(f"=== NESA downloader start ===")
    pages = enumerate_pages()
    log(f"{len(pages)} exam-pack pages across {len(set(p[0] for p in pages))} subjects")
    ok = skip = fail = 0
    for subj, year, url in pages:
        outdir = os.path.join(HERE, subj, "HSC-NESA")
        os.makedirs(outdir, exist_ok=True)
        try:
            page = fetch(BASE + url if url.startswith("/") else url).decode("utf-8", "replace")
        except Exception as e:
            log(f"  page fail {url}: {e}"); continue
        for link in pdf_links(page):
            name = os.path.basename(urllib.parse.urlparse(link).path)
            name = re.sub(r'\.pdf\.pdf$', '.pdf', name, flags=re.I)
            path = os.path.join(outdir, name)
            if os.path.exists(path) and os.path.getsize(path) > 500:
                skip += 1; continue
            try:
                pdf = fetch(link)
                if not pdf[:5].startswith(b"%PDF"):
                    fail += 1; log(f"  not-pdf {subj}/{name}"); continue
                with open(path, "wb") as f: f.write(pdf)
                ok += 1; log(f"  OK {subj}/HSC-NESA/{name} ({len(pdf)//1024} KB)")
            except Exception as e:
                fail += 1; log(f"  FAIL {subj}/{name}: {e}")
            time.sleep(0.4)
    log(f"=== NESA done: ok={ok} skip={skip} fail={fail} ===")

if __name__ == "__main__":
    main()
