#!/usr/bin/env python3
"""Round-robin downloader for thsconline HSC/Prelim papers.

Key insight: each listing page serves all its papers through ONE aggregate
"base" id via a Google Apps Script. That base has a per-base rate limit that
refills over ~an hour; hammering a single base returns a placeholder PDF.
So we ROUND-ROBIN across bases (never hit one rapidly) and put a base on
cooldown when it throttles, working other bases meanwhile.

Papers that have a direct source URL (index/<base>.json, e.g. NESA-hosted HSC
papers) are fetched straight from the source with no rate limit at all.

Covers Physics + all NSW Maths courses, Y12 (HSC + Trial) and Y11 (Yearly),
saved by subject under this folder. Fully resumable. Optional subject filter:
    python3 _downloader.py Physics      # only Physics
    python3 _downloader.py Maths        # only Maths courses
Logs to _download.log next to this file.
"""
import re, os, sys, time, html, json, base64, hashlib, urllib.parse, urllib.request
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
APPS = "https://script.google.com/macros/s/AKfycbx69GPoJtf9sSevsUbWtPr46vpa01u4oNkHjFmkkWxmj62AZ0q-/exec"
SITE = "https://thsconline.github.io/s"

PAGES = [
    # Maths Advanced + Extension 1 first (HSC before trials) — current priority.
    ("Maths Advanced",    "Y12-HSC",    "yr12/Maths/hscpapers_advanced.html"),
    ("Maths Extension 1", "Y12-HSC",    "yr12/Maths/hscpapers_extension1.html"),
    ("Maths Advanced",    "Y12-Trial",  "yr12/Maths/trialpapers_advanced.html"),
    ("Maths Extension 1", "Y12-Trial",  "yr12/Maths/trialpapers_extension1.html"),
    ("Maths Advanced",    "Y11-Yearly", "yr11/Maths/prelimpapers_advanced.html"),
    ("Maths Extension 1", "Y11-Yearly", "yr11/Maths/prelimpapers_extension1.html"),
    # Physics
    ("Physics",           "Y12-HSC",    "yr12/Physics/hscpapers.html"),
    ("Physics",           "Y12-Trial",  "yr12/Physics/trialpapers.html"),
    ("Physics",           "Y11-Yearly", "yr11/Physics/prelimpapers.html"),
    # English (Advanced/Standard share one folder; Ext 1 is separate)
    ("English",           "Y12-HSC",       "yr12/English/hscpapers.html"),
    ("English",           "Y12-Trial-P1",  "yr12/English/trialpapers_paper1.html"),
    ("English",           "Y12-Trial-P2-Adv", "yr12/English/trialpapers_paper2_advanced.html"),
    ("English",           "Y12-Trial-P2-Std", "yr12/English/trialpapers_paper2_standard.html"),
    ("English Extension 1","Y12-Trial",    "yr12/English Ext 1/trialpapers_extension1.html"),
    # Remaining Maths courses
    ("Maths Standard 2",  "Y12-HSC",    "yr12/Maths/hscpapers_general.html"),
    ("Maths Standard 2",  "Y12-Trial",  "yr12/Maths/trialpapers_general.html"),
    ("Maths Standard 2",  "Y11-Yearly", "yr11/Maths/prelimpapers_general.html"),
    ("Maths Extension 2", "Y12-HSC",    "yr12/Maths/hscpapers_extension2.html"),
    ("Maths Extension 2", "Y12-Trial",  "yr12/Maths/trialpapers_extension2.html"),
    ("Maths Accelerated", "Y11-Yearly", "yr11/Maths/prelimpapers_accelerated.html"),
    # --- Full-site sweep: every remaining THSC subject (yr12 HSC/Trial + yr11 Yearly) ---
    ("Ancient History",               "Y12-HSC",    "yr12/Ancient History/hscpapers.html"),
    ("Ancient History",               "Y12-Trial",  "yr12/Ancient History/trialpapers.html"),
    ("Biology",                       "Y12-HSC",    "yr12/Biology/hscpapers.html"),
    ("Biology",                       "Y12-Trial",  "yr12/Biology/trialpapers.html"),
    ("Business Studies",              "Y12-HSC",    "yr12/Business Studies/hscpapers.html"),
    ("Business Studies",              "Y12-Trial",  "yr12/Business Studies/trialpapers.html"),
    ("Chemistry",                     "Y12-HSC",    "yr12/Chemistry/hscpapers.html"),
    ("Chemistry",                     "Y12-Trial",  "yr12/Chemistry/trialpapers.html"),
    ("Earth & Environmental Science", "Y12-HSC",    "yr12/Earth & Environmental Science/hscpapers.html"),
    ("Earth & Environmental Science", "Y12-Trial",  "yr12/Earth & Environmental Science/trialpapers.html"),
    ("Economics",                     "Y12-HSC",    "yr12/Economics/hscpapers.html"),
    ("Economics",                     "Y12-Trial",  "yr12/Economics/trialpapers.html"),
    ("Engineering Studies",           "Y12-HSC",    "yr12/Engineering Studies/hscpapers.html"),
    ("Engineering Studies",           "Y12-Trial",  "yr12/Engineering Studies/trialpapers.html"),
    ("Legal Studies",                 "Y12-HSC",    "yr12/Legal Studies/hscpapers.html"),
    ("Legal Studies",                 "Y12-Trial",  "yr12/Legal Studies/trialpapers.html"),
    ("Modern History",                "Y12-HSC",    "yr12/Modern History/hscpapers.html"),
    ("Modern History",                "Y12-Trial",  "yr12/Modern History/trialpapers.html"),
    ("Agriculture",                   "Y12-Trial",  "yr12/Agriculture/trialpapers.html"),
    ("History Extension",             "Y12-Trial",  "yr12/History Extension/trialpapers.html"),
    ("IPT",                           "Y12-Trial",  "yr12/IPT/trialpapers.html"),
    ("Investigating Science",         "Y12-Trial",  "yr12/Investigating Science/trialpapers.html"),
    ("PDHPE",                         "Y12-Trial",  "yr12/PDHPE/trialpapers.html"),
    ("Society & Culture",             "Y12-Trial",  "yr12/Society & Culture/trialpapers.html"),
    ("Software",                      "Y12-Trial",  "yr12/Software/trialpapers.html"),
    ("Visual Arts",                   "Y12-Trial",  "yr12/Visual Arts/trialpapers.html"),
    ("Studies of Religion 1",         "Y12-Trial",  "yr12/Studies of Religion/trialpapers_sor1.html"),
    ("Studies of Religion 2",         "Y12-Trial",  "yr12/Studies of Religion/trialpapers_sor2.html"),
    ("Japanese Continuers",           "Y12-HSC",    "yr12/LOTE/Japanese/hscpapers_continuers.html"),
    ("Japanese Extension",            "Y12-HSC",    "yr12/LOTE/Japanese/hscpapers_extension.html"),
    ("Japanese Beginners",            "Y12-Trial",  "yr12/LOTE/Japanese/trialpapers_beginners.html"),
    ("Japanese Continuers",           "Y12-Trial",  "yr12/LOTE/Japanese/trialpapers_continuers.html"),
    ("Latin Continuers",              "Y12-Trial",  "yr12/LOTE/Latin/trialpapers_continuers.html"),
    ("Latin Extension",               "Y12-Trial",  "yr12/LOTE/Latin/trialpapers_extension.html"),
    ("Biology",                       "Y11-Yearly", "yr11/Biology/prelimpapers.html"),
    ("Business Studies",              "Y11-Yearly", "yr11/Business Studies/prelimpapers.html"),
    ("Chemistry",                     "Y11-Yearly", "yr11/Chemistry/prelimpapers.html"),
    ("Earth & Environmental Science", "Y11-Yearly", "yr11/Earth & Environmental Science/prelimpapers.html"),
    ("Economics",                     "Y11-Yearly", "yr11/Economics/prelimpapers.html"),
    ("Engineering Studies",           "Y11-Yearly", "yr11/Engineering Studies/prelimpapers.html"),
    ("IPT",                           "Y11-Yearly", "yr11/IPT/prelimpapers.html"),
    ("Legal Studies",                 "Y11-Yearly", "yr11/Legal Studies/prelimpapers.html"),
    ("Modern History",                "Y11-Yearly", "yr11/Modern History/prelimpapers.html"),
]

# --- pacing (deliberately gentle: this is a shared free resource for HSC
# students, so we trickle and back off hard the moment the site signals a
# limit, leaving plenty of quota headroom for real users) ---
GLOBAL_GAP   = 25     # seconds between ANY two Apps-Script requests
PER_BASE_GAP = 150    # min seconds between hits on the SAME base
COOLDOWN     = 1800   # base rests 30 min after returning the placeholder
IDLE_ABORT   = 6*3600 # give up if every base is cooling down this long (safety)
MAX_THROTTLES = 8     # after this many placeholder hits, treat an item as
                      # genuinely unavailable and drop it (a real base-throttle
                      # clears within a cycle or two; only permanently-missing
                      # papers ever reach this and they otherwise stall the run)

BLOCK_FILEREFS = {"12TrRtJ9xfV4mo9O34MJ5_1YrHzjvirBR"}
BLOCK_MD5S     = {"a15ea5c8538acccf0c83ce0314390524"}

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
LINK_RE = re.compile(r'pdf\(this,\s*(\d+)\)["\'][^>]*>(.*?)</a>', re.I | re.S)

def log(msg):
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {msg}"
    with open(os.path.join(HERE, "_download.log"), "a") as f:
        f.write(line + "\n")

def fetch(url, timeout=90):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def sanitize(name):
    name = html.unescape(name).strip()
    name = re.sub(r'\s+', ' ', name)
    return re.sub(r'[/\\:*?"<>|]', '-', name)[:180]

def extract(page_html):
    out, seen = [], set()
    for m in LINK_RE.finditer(page_html):
        base, raw = m.group(1), m.group(2).strip()
        if raw and (base, raw) not in seen:
            seen.add((base, raw)); out.append((base, raw))
    return out

def load_index(base):
    """Return {title: direct_url} from index/<base>.json, or {} if none."""
    try:
        data = json.loads(fetch(f"{SITE}/index/{base}.json").decode("utf-8-sig", "replace"))
    except Exception:
        return {}
    out = {}
    for title, arr in data.items():
        if not isinstance(arr, list): arr = [arr]
        url = next((r.get("url") for r in arr if isinstance(r, dict) and r.get("url")), None)
        if url: out[title] = url
    return out

def resolve_apps(base, raw_title):
    """('ok', bytes) | ('ratelimit', None) | ('fail', reason)."""
    h = hashlib.sha256(base.encode()).hexdigest()
    url = f"{APPS}?export=data&field={urllib.parse.quote(raw_title)}&base={base}&hash={h}"
    body = fetch(url).decode("utf-8", "replace")
    m = re.search(r'downloadfile\((\{.*\})\)', body, re.S)
    if not m: return ("fail", "no-jsonp")
    d = json.loads(m.group(1))
    if not d.get("data"): return ("fail", "no-data")
    pdf = base64.b64decode(d["data"])
    if d.get("fileref") in BLOCK_FILEREFS or hashlib.md5(pdf).hexdigest() in BLOCK_MD5S:
        return ("ratelimit", None)
    if not pdf.startswith(b"%PDF"): return ("fail", "not-pdf")
    return ("ok", pdf)

def valid_existing(path):
    try:
        if os.path.getsize(path) < 500: return False
        d = open(path, "rb").read()
        return d[:5].startswith(b"%PDF") and hashlib.md5(d).hexdigest() not in BLOCK_MD5S
    except OSError:
        return False

def main():
    filters = [a.lower() for a in sys.argv[1:] if not a.startswith("-")]
    wanted = lambda s: not filters or any(f in s.lower() for f in filters)
    log(f"=== round-robin downloader start (filter={filters or 'ALL'}) ===")

    queues = {}         # base -> list of pending item dicts
    index_cache = {}    # base -> {title: url}
    order = []          # base order for round-robin
    ok = skip = fail = gaveup = 0

    for subject, tag, path in PAGES:
        if not wanted(subject): continue
        try:
            page = fetch(f"{SITE}/{urllib.parse.quote(path, safe='/')}").decode("utf-8", "replace")
        except Exception as e:
            log(f"page fetch failed {path}: {e}"); continue
        outdir = os.path.join(HERE, subject, tag); os.makedirs(outdir, exist_ok=True)
        for base, raw in extract(page):
            fpath = os.path.join(outdir, sanitize(raw) + ".pdf")
            if valid_existing(fpath): skip += 1; continue
            if base not in index_cache:
                index_cache[base] = load_index(base)
            queues.setdefault(base, [])
            if base not in order: order.append(base)
            queues[base].append({"subject": subject, "tag": tag, "raw": raw,
                                  "path": fpath, "url": index_cache[base].get(raw)})

    # First pass: grab everything with a direct source URL (no rate limit).
    for base in list(queues):
        remaining = []
        for it in queues[base]:
            if not it["url"]:
                remaining.append(it); continue
            try:
                pdf = fetch(it["url"])
                if pdf[:5].startswith(b"%PDF"):
                    open(it["path"], "wb").write(pdf); ok += 1
                    log(f"DIRECT {it['subject']}/{it['tag']}/{os.path.basename(it['path'])} ({len(pdf)//1024} KB)")
                else:
                    remaining.append(it)
            except Exception:
                remaining.append(it)
        queues[base] = remaining

    total = sum(len(q) for q in queues.values())
    log(f"resume: {skip} already on disk, {ok} direct. {total} to fetch via {len(order)} bases.")

    cooldown = {b: 0.0 for b in order}     # base -> ready-at monotonic ts
    rr = 0
    last_progress = time.monotonic()

    while any(queues[b] for b in order):
        now = time.monotonic()
        ready = [b for b in order if queues[b] and cooldown[b] <= now]
        if not ready:
            soonest = min((cooldown[b] for b in order if queues[b]), default=now + 30)
            wait = max(5, min(soonest - now, 120))
            if now - last_progress > IDLE_ABORT:
                log(f"=== idle {IDLE_ABORT}s, all bases cooling -> abort. ok={ok} left={sum(len(queues[b]) for b in order)} ==="); return
            time.sleep(wait); continue

        base = ready[rr % len(ready)]; rr += 1
        last_progress = now   # reaching any ready base counts as alive; idle-abort
                              # now only fires on a true hang (no base reachable at all)
        it = queues[base][0]
        name = f"{it['subject']}/{it['tag']}/{os.path.basename(it['path'])}"
        try:
            status, payload = resolve_apps(base, it["raw"])
        except Exception as e:
            cooldown[base] = time.monotonic() + 120
            it["throttles"] = it.get("throttles", 0) + 1
            queues[base].pop(0)
            if it["throttles"] >= MAX_THROTTLES:
                gaveup += 1
                log(f"GIVEUP {name}: net-errors ({it['throttles']}), last={e}")
            else:
                # rotate so a persistently-failing item (e.g. a 404) can't block
                # the rest of its base
                queues[base].append(it)
                log(f"net-error base {base}: {e} (cooldown 120s, rotated hit {it['throttles']})")
            time.sleep(GLOBAL_GAP); continue

        if status == "ratelimit":
            cooldown[base] = time.monotonic() + COOLDOWN
            it["throttles"] = it.get("throttles", 0) + 1
            queues[base].pop(0)
            if it["throttles"] >= MAX_THROTTLES:
                gaveup += 1
                log(f"GIVEUP {name}: unavailable ({it['throttles']} placeholder hits)")
            else:
                # rotate to the back so a stuck head item can't starve the base's
                # other papers or drive every base into idle-abort
                queues[base].append(it)
                log(f"base {base} throttled -> cooldown {COOLDOWN}s, rotated ({name}, hit {it['throttles']})")
        elif status == "ok":
            open(it["path"], "wb").write(payload)
            queues[base].pop(0); ok += 1; last_progress = time.monotonic()
            cooldown[base] = time.monotonic() + PER_BASE_GAP
            remain = sum(len(queues[b]) for b in order)
            log(f"OK {name} ({len(payload)//1024} KB)  [done {ok}, left {remain}]")
        else:
            queues[base].pop(0); fail += 1
            cooldown[base] = time.monotonic() + PER_BASE_GAP
            log(f"FAIL {name}: {payload}")
        time.sleep(GLOBAL_GAP)

    log(f"=== done: ok={ok} skip={skip} fail={fail} gaveup={gaveup} ===")

if __name__ == "__main__":
    main()
