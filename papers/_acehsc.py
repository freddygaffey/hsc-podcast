#!/usr/bin/env python3
"""Download HSC past papers from acehsc.net.

acehsc embeds its whole catalogue as a JSON blob (`var aceobj = {"libdat": ...}`)
on the library pages. Each entry links to a /resource/<slug>/ page that contains
a direct BunnyCDN PDF link (aceh.b-cdn.net) — no Google Drive, effectively no
rate limit. We parse the catalogue, filter to paper-type resources, then pull
the CDN PDF for each. Saves to papers/<Subject>/ACE-<tag>/. Fully resumable.

Usage:
    python3 _acehsc.py                     # all subjects, paper types
    python3 _acehsc.py Physics Chemistry   # subject filter (substring match)
    python3 _acehsc.py --all-types Physics # include Notes/Essays/etc. too
"""
import re, os, sys, json, time, html, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
LIB_PAGES = ["https://www.acehsc.net/library/",            # HSC
             "https://www.acehsc.net/preliminary-library/"] # Preliminary

# rtype -> category tag (papers only, by default)
PAPER_TAGS = {
    "Trial Paper": "ACE-Trial",
    "HSC Exam Paper": "ACE-HSC",
    "Half Yearly Paper": "ACE-HalfYearly",
    "Yearly Paper": "ACE-Yearly",
    "HSC Questions": "ACE-HSC-Questions",
}
# extra tags when --all-types is passed (any rtype not listed here still gets
# included under an auto-generated "ACE-<rtype>" folder)
EXTRA_TAGS = {
    "Notes": "ACE-Notes", "Essay": "ACE-Essay", "Assessment Task": "ACE-Assessment",
    "Case Study": "ACE-CaseStudy", "Syllabus": "ACE-Syllabus", "Other": "ACE-Other",
    "Essay and Notes": "ACE-Notes", "Quiz": "ACE-Quiz", "Video": "ACE-Video",
}
# normalise acehsc subject names to our existing folders
SUBJ_MAP = {
    "Mathematics Advanced": "Maths Advanced",
    "Mathematics Extension 1": "Maths Extension 1",
    "Mathematics Extension 2": "Maths Extension 2",
    "Mathematics Standard": "Maths Standard 2",
}

def log(msg):
    print(msg, flush=True)
    with open(os.path.join(HERE, "_acehsc.log"), "a") as f:
        f.write(msg + "\n")

def fetch(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def sanitize(name):
    name = html.unescape(name).strip()
    return re.sub(r'[/\\:*?"<>|]', '-', name)[:180]

def catalogue():
    seen, out = set(), []
    for page in LIB_PAGES:
        try:
            h = fetch(page).decode("utf-8", "replace")
        except Exception as e:
            log(f"lib page fail {page}: {e}"); continue
        m = re.search(r'var aceobj\s*=\s*(\{.*?\});', h, re.S)
        if not m:
            log(f"no aceobj on {page}"); continue
        for d in json.loads(json.loads(m.group(1))["libdat"]):
            hm = re.search(r'href=\\?"([^"\\]+)', d.get("title", ""))
            if not hm:
                continue
            page_url = hm.group(1)
            if page_url in seen:
                continue
            seen.add(page_url)
            out.append({"url": page_url, "subject": d.get("subject", "Misc"),
                        "rtype": d.get("rtype", ""), "year": d.get("year", "")})
    return out

def cdn_pdf(resource_html):
    m = re.search(r'https://aceh\.b-cdn\.net/[^\s"\'<>]+\.pdf', resource_html, re.I)
    return m.group(0) if m else None

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    all_types = "--all-types" in sys.argv
    tags = dict(PAPER_TAGS)
    if all_types:
        tags.update(EXTRA_TAGS)
    filt = [a.lower() for a in args]
    want_subj = lambda s: not filt or any(f in s.lower() for f in filt)

    def tag_for(rtype):
        # explicit mapping, else an auto folder for any other type
        return tags.get(rtype) or ("ACE-" + sanitize(rtype).replace(" ", "-") if rtype else "ACE-Misc")

    log(f"=== acehsc start (types={'ALL' if all_types else 'papers'} filter={filt or 'ALL'}) ===")
    # papers-only: restrict to PAPER_TAGS rtypes; all-types: include every rtype
    items = [r for r in catalogue()
             if want_subj(r["subject"]) and (all_types or r["rtype"] in PAPER_TAGS)]
    log(f"{len(items)} resources in scope")

    ok = skip = fail = 0
    for i, r in enumerate(items, 1):
        subj = SUBJ_MAP.get(r["subject"], r["subject"])
        tag = tag_for(r["rtype"])
        outdir = os.path.join(HERE, sanitize(subj), tag)
        os.makedirs(outdir, exist_ok=True)
        try:
            page = fetch(r["url"]).decode("utf-8", "replace")
        except Exception as e:
            fail += 1; log(f"[{i}/{len(items)}] page fail {r['url']}: {e}"); continue
        pdf_url = cdn_pdf(page)
        if not pdf_url:
            fail += 1; log(f"[{i}/{len(items)}] no CDN pdf: {r['url']}"); continue
        name = sanitize(urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(pdf_url).path)))
        path = os.path.join(outdir, name)
        if os.path.exists(path) and os.path.getsize(path) > 500:
            skip += 1; continue
        try:
            pdf = fetch(pdf_url)
            if not pdf[:5].startswith(b"%PDF"):
                fail += 1; log(f"[{i}/{len(items)}] not-pdf {name}"); continue
            with open(path, "wb") as f:
                f.write(pdf)
            ok += 1
            log(f"[{i}/{len(items)}] OK {subj}/{tag}/{name} ({len(pdf)//1024} KB)")
        except Exception as e:
            fail += 1; log(f"[{i}/{len(items)}] dl fail {name}: {e}")
        time.sleep(0.35)   # gentle; acehsc CDN is not tightly rate-limited
    log(f"=== acehsc done: ok={ok} skip={skip} fail={fail} ===")

if __name__ == "__main__":
    main()
