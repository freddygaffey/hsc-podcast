#!/usr/bin/env python3
"""Visual review tool for baked question crops (the spec's first-class review gate, §4.1).

Shows each baked q_/a_ PDF as an image; one keypress approves or rejects it with a reason.
Verdicts append to papers/_work/_review.jsonl (append-only, re-runnable — latest verdict
per question wins). Questions whose part labels look like mis-split roman numerals
(an 'i'/'v'/'x' the alphabet never reached) are pre-flagged with a ⚠ badge.

    python3 tools/review_app.py [--port 5089]
    open http://localhost:5089            # ?subject=maths-advanced&only=unreviewed|flagged

Keys:  g = good   c = cut off   w = wrong split   o = other-bad   ← → = navigate
"""
import argparse
import json
import time
from pathlib import Path

import fitz
from flask import Flask, Response, jsonify, request

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
REVIEW = WORK / "_review.jsonl"
ROMAN = {"i", "v", "x"}

app = Flask(__name__)
ITEMS = []          # [{paperId, subject, paperSlug, assetKey, answerKey, q, part, marks, flagged}]
INDEX = {}          # (paperId, assetKey) -> item


def load_items():
    for qj in sorted(WORK.glob("*/questions.json")):
        try:
            data = json.loads(qj.read_text())
        except Exception:
            continue
        pid = qj.parent.name
        flagged_qs = set()
        bpath = qj.parent / "boundaries.json"
        if bpath.exists():
            try:
                for q in json.loads(bpath.read_text()).get("questions", []):
                    letters = [p.get("label") for p in (q.get("parts") or [])
                               if p.get("label") and len(p["label"]) == 1]
                    for r in ROMAN & set(letters):
                        if len(letters) <= ord(r) - ord("a"):
                            flagged_qs.add(str(q.get("number")))
            except Exception:
                pass
        for r in data.get("questions", []):
            if not r.get("assetKey"):
                continue
            item = {
                "paperId": pid, "subject": data.get("subject") or "misc",
                "paperSlug": data.get("paperSlug") or "?",
                "assetKey": r["assetKey"], "answerKey": r.get("answerKey"),
                "q": r.get("questionNumber"), "part": r.get("partLabel"),
                "marks": r.get("marks"), "type": r.get("type"), "topic": r.get("topic"),
                "flagged": str(r.get("questionNumber")) in flagged_qs,
            }
            ITEMS.append(item)
            INDEX[(pid, r["assetKey"])] = item


def verdicts():
    out = {}
    if REVIEW.exists():
        for line in REVIEW.read_text().splitlines():
            try:
                v = json.loads(line)
                out[(v["paperId"], v["assetKey"])] = v["verdict"]
            except Exception:
                continue
    return out


@app.route("/api/items")
def api_items():
    subj = request.args.get("subject")
    only = request.args.get("only")
    vs = verdicts()
    rows = []
    for it in ITEMS:
        if subj and it["subject"] != subj:
            continue
        v = vs.get((it["paperId"], it["assetKey"]))
        if only == "unreviewed" and v:
            continue
        if only == "flagged" and not it["flagged"]:
            continue
        rows.append({**it, "verdict": v})
    return jsonify({"items": rows,
                    "subjects": sorted({i["subject"] for i in ITEMS}),
                    "reviewed": len(vs), "total": len(ITEMS)})


@app.route("/api/verdict", methods=["POST"])
def api_verdict():
    v = request.get_json()
    rec = {"paperId": v["paperId"], "assetKey": v["assetKey"],
           "verdict": v["verdict"], "ts": int(time.time() * 1000)}
    with REVIEW.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    return jsonify({"ok": True})


@app.route("/img/<pid>/<name>")
def img(pid, name):
    pdf = WORK / pid / "baked" / name
    if not pdf.exists():
        return "not found", 404
    doc = fitz.open(pdf)
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2))
    return Response(pix.tobytes("png"), mimetype="image/png")


@app.route("/api/stats")
def api_stats():
    vs = verdicts()
    by = {}
    for (pid, ak), verdict in vs.items():
        it = INDEX.get((pid, ak))
        if not it:
            continue
        d = by.setdefault(it["subject"], {})
        d[verdict] = d.get(verdict, 0) + 1
    return jsonify({"bySubject": by, "reviewed": len(vs), "total": len(ITEMS)})


PAGE = """<!doctype html><meta charset=utf-8><title>Crop review</title>
<style>
 body{font:15px/1.5 system-ui;margin:0;background:#f5f7fa;color:#1a1d24}
 header{display:flex;gap:12px;align-items:center;padding:10px 16px;background:#fff;border-bottom:1px solid #e4e8ef;position:sticky;top:0}
 select,button{font:inherit;padding:6px 10px;border-radius:8px;border:1px solid #d6dbe4;background:#fff;cursor:pointer}
 .keys b{display:inline-block;border:1px solid #ccd;border-radius:4px;padding:0 6px;margin:0 2px;background:#fff}
 main{max-width:980px;margin:16px auto;padding:0 16px}
 .meta{display:flex;gap:14px;color:#697386;font-size:13px;margin:8px 2px;flex-wrap:wrap;align-items:center}
 .flag{background:#fff3cd;color:#8a6d00;padding:2px 8px;border-radius:12px;font-weight:600}
 .verdict{padding:2px 8px;border-radius:12px;font-weight:600}
 .v-good{background:#e6f6ee;color:#1f9d63}.v-bad{background:#fdeaea;color:#c0392b}
 .crop{background:#fff;border:1px solid #e4e8ef;border-radius:12px;padding:10px;text-align:center}
 .crop img{max-width:100%;height:auto}
 .btns{display:flex;gap:8px;margin:14px 0}
 .btns button{padding:10px 16px;font-weight:600}
 .good{border-color:#1f9d63;color:#1f9d63}.bad{border-color:#c0392b;color:#c0392b}
 .ansrow{margin:8px 0}
</style>
<header>
 <select id=subj></select>
 <select id=only>
  <option value="">everything</option>
  <option value="unreviewed" selected>unreviewed only</option>
  <option value="flagged">⚠ flagged (roman-split suspects)</option>
 </select>
 <span id=pos></span>
 <span class=keys style="margin-left:auto"><b>g</b>ood <b>c</b>ut-off <b>w</b>rong-split <b>o</b>ther <b>←</b><b>→</b></span>
 <a href="#" id=statlink>stats</a>
</header>
<main>
 <div class=meta id=meta></div>
 <div class=crop><img id=im alt="question crop"></div>
 <div class=ansrow><label><input type=checkbox id=showans> show answer crop</label></div>
 <div class=crop id=anscrop style="display:none"><img id=ansim alt="answer crop"></div>
 <div class=btns>
  <button class=good data-v=good>✓ good (g)</button>
  <button class=bad data-v=cut-off>✗ cut off (c)</button>
  <button class=bad data-v=wrong-split>✗ wrong split (w)</button>
  <button class=bad data-v=other-bad>✗ other (o)</button>
 </div>
</main>
<script>
let items=[],i=0,subjects=[];
const $=s=>document.querySelector(s);
async function load(){
 const s=$("#subj").value,o=$("#only").value;
 const r=await fetch(`/api/items?subject=${s}&only=${o}`).then(r=>r.json());
 items=r.items; subjects=r.subjects; i=0;
 if(!$("#subj").options.length)
  $("#subj").innerHTML='<option value="">all subjects</option>'+subjects.map(x=>`<option>${x}</option>`).join('');
 show();
}
function show(){
 const it=items[i];
 $("#pos").textContent=items.length?`${i+1} / ${items.length}`:"nothing matches";
 if(!it){$("#im").src="";$("#meta").textContent="";return}
 $("#im").src=`/img/${it.paperId}/${it.assetKey}`;
 $("#meta").innerHTML=`<span><b>${it.subject}</b> · ${it.paperSlug}</span>
  <span>Q${it.q??"?"}${it.part??""}</span><span>${it.marks?it.marks+" marks":"no marks"}</span>
  <span>${it.topic??""}</span>
  ${it.flagged?'<span class=flag>⚠ roman-split suspect</span>':''}
  ${it.verdict?`<span class="verdict ${it.verdict==='good'?'v-good':'v-bad'}">${it.verdict}</span>`:''}`;
 const on=$("#showans").checked&&it.answerKey;
 $("#anscrop").style.display=on?"":"none";
 if(on)$("#ansim").src=`/img/${it.paperId}/${it.answerKey}`;
}
async function verdict(v){
 const it=items[i]; if(!it)return;
 await fetch("/api/verdict",{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({paperId:it.paperId,assetKey:it.assetKey,verdict:v})});
 it.verdict=v; if(i<items.length-1)i++; show();
}
document.addEventListener("keydown",e=>{
 if(e.key==="ArrowRight"&&i<items.length-1){i++;show()}
 if(e.key==="ArrowLeft"&&i>0){i--;show()}
 const map={g:"good",c:"cut-off",w:"wrong-split",o:"other-bad"};
 if(map[e.key])verdict(map[e.key]);
});
document.querySelectorAll(".btns button").forEach(b=>b.onclick=()=>verdict(b.dataset.v));
$("#subj").onchange=load; $("#only").onchange=load; $("#showans").onchange=show;
$("#statlink").onclick=async e=>{e.preventDefault();
 const s=await fetch("/api/stats").then(r=>r.json());
 alert(`reviewed ${s.reviewed} of ${s.total}\\n`+Object.entries(s.bySubject)
  .map(([k,v])=>`${k}: `+Object.entries(v).map(([a,b])=>`${a} ${b}`).join(", ")).join("\\n"));};
load();
</script>"""


@app.route("/")
def home():
    return PAGE


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5089)
    args = ap.parse_args()
    load_items()
    print(f"{len(ITEMS)} crops loaded · flagged: {sum(1 for i in ITEMS if i['flagged'])}")
    app.run(port=args.port, debug=False)
