#!/usr/bin/env python3
"""Visual review tool for baked question crops (the spec's first-class review gate, §4.1).

Shows each baked q_/a_ PDF as an image; one keypress approves or rejects it with a reason.
Verdicts append to papers/_work/_review.jsonl (append-only, re-runnable — latest verdict
per question wins). Questions whose part labels look like mis-split roman numerals
(an 'i'/'v'/'x' the alphabet never reached) are pre-flagged with a ⚠ badge.

    python3 tools/review_app.py [--port 5089]
    open http://localhost:5089            # ?subject=maths-advanced&only=unreviewed|flagged

Keys:  g = good   c = cut off   w = wrong split   o = other-bad   f = flag tag   ← → = navigate

Metadata: shows lineCount / type / module / syllabus outcomes (AI-tagged values get a chip,
outcome codes get description tooltips). Type and outcomes can be reassigned from dropdowns
fed by content/<subject>/syllabus.json; corrections append to papers/_work/_corrections.jsonl
(latest per (paperId, assetKey, field) wins) and are applied by build_manifest.py — human
always beats the AI tag.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import fitz
from flask import Flask, Response, jsonify, request

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _subjects import load_syllabus, outcome_codes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
REVIEW = WORK / "_review.jsonl"
CORRECTIONS = WORK / "_corrections.jsonl"
ROMAN = {"i", "v", "x"}
TAG_FIELDS = ("type", "topic", "module", "syllabusRefs")

app = Flask(__name__)
ITEMS = []          # [{paperId, subject, paperSlug, assetKey, answerKey, q, part, marks, flagged}]
INDEX = {}          # (paperId, assetKey) -> item
CONFIGS = {}        # subject -> {types, outcomes}


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
        tags = {}
        tpath = qj.parent / "tags.json"
        if tpath.exists():
            try:
                tags = json.loads(tpath.read_text()).get("tags", {})
            except Exception:
                pass
        for r in data.get("questions", []):
            if not r.get("assetKey"):
                continue
            subj = data.get("subject") or "misc"
            if subj not in CONFIGS:
                syl = load_syllabus(subj)
                CONFIGS[subj] = {
                    "types": (syl or {}).get("types", []),
                    "outcomes": [{"code": o["code"], "description": o.get("description", "")}
                                 for o in (syl or {}).get("outcomes", [])] or
                                [{"code": c, "description": ""} for c in outcome_codes(syl)],
                } if syl else {"types": [], "outcomes": []}
            item = {
                "paperId": pid, "subject": subj,
                "paperSlug": data.get("paperSlug") or "?",
                "assetKey": r["assetKey"], "answerKey": r.get("answerKey"),
                "q": r.get("questionNumber"), "part": r.get("partLabel"),
                "marks": r.get("marks"), "type": r.get("type"), "topic": r.get("topic"),
                "module": r.get("module"), "syllabusRefs": r.get("syllabusRefs") or [],
                "lineCount": r.get("lineCount"), "spaceHeight": r.get("spaceHeight"),
                "unit": r.get("unit"),
                "flagged": str(r.get("questionNumber")) in flagged_qs,
            }
            # AI tags fill gaps the locate step left (same rule build_manifest.py applies)
            t = tags.get(r["assetKey"]) or {}
            ai_fields = []
            for f in TAG_FIELDS:
                if t.get(f) and not item.get(f):
                    item[f] = t[f]
                    ai_fields.append(f)
            item["aiTagged"] = ai_fields
            item["confidence"] = t.get("confidence")
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


def corrections():
    """Latest correction per (paperId, assetKey) -> {field: value}."""
    out = {}
    if CORRECTIONS.exists():
        for line in CORRECTIONS.read_text().splitlines():
            try:
                c = json.loads(line)
                out.setdefault((c["paperId"], c["assetKey"]), {})[c["field"]] = c["value"]
            except Exception:
                continue
    return out


@app.route("/api/items")
def api_items():
    subj = request.args.get("subject")
    paper = request.args.get("paper")
    only = request.args.get("only")
    vs = verdicts()
    cs = corrections()
    rows = []
    for it in ITEMS:
        if subj and it["subject"] != subj:
            continue
        if paper and it["paperSlug"] != paper:
            continue
        v = vs.get((it["paperId"], it["assetKey"]))
        c = cs.get((it["paperId"], it["assetKey"]), {})
        if only == "unreviewed" and v:
            continue
        if only == "flagged" and not it["flagged"]:
            continue
        if only == "tag-flagged" and not c.get("tagFlag"):
            continue
        if only == "low-confidence" and not (it.get("confidence") is not None
                                             and it["confidence"] < 0.7):
            continue
        row = {**it, "verdict": v}
        for f, val in c.items():        # human corrections win over base + AI
            if f != "tagFlag":
                row[f] = val
        row["corrected"] = [f for f in c if f != "tagFlag"]
        row["tagFlag"] = c.get("tagFlag")
        rows.append(row)
    return jsonify({"items": rows,
                    "subjects": sorted({i["subject"] for i in ITEMS}),
                    "papers": sorted({i["paperSlug"] for i in ITEMS if not subj or i["subject"] == subj}),
                    "configs": CONFIGS,
                    "reviewed": len(vs), "total": len(ITEMS)})


@app.route("/api/verdict", methods=["POST"])
def api_verdict():
    v = request.get_json()
    rec = {"paperId": v["paperId"], "assetKey": v["assetKey"],
           "verdict": v["verdict"], "ts": int(time.time() * 1000)}
    with REVIEW.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    return jsonify({"ok": True})


@app.route("/api/correction", methods=["POST"])
def api_correction():
    c = request.get_json()
    if c.get("field") not in ("type", "syllabusRefs", "topic", "module",
                              "marks", "lineCount", "tagFlag"):
        return jsonify({"ok": False, "error": "bad field"}), 400
    rec = {"paperId": c["paperId"], "assetKey": c["assetKey"],
           "field": c["field"], "value": c["value"], "ts": int(time.time() * 1000)}
    with CORRECTIONS.open("a") as f:
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
 .ai{background:#eef2ff;color:#4353c7;padding:2px 8px;border-radius:12px;font-weight:600}
 .fix{background:#e6f6ee;color:#1f9d63;padding:2px 8px;border-radius:12px;font-weight:600}
 .tflag{background:#fdeaea;color:#c0392b;padding:2px 8px;border-radius:12px;font-weight:600}
 .ref{border:1px solid #d6dbe4;border-radius:10px;padding:1px 7px;background:#fff;cursor:help}
 .editor{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:#fff;border:1px solid #e4e8ef;border-radius:12px;padding:10px;margin:12px 0}
 .editor select[multiple]{min-width:180px;height:88px}
 .editor .save{border-color:#4353c7;color:#4353c7;font-weight:600}
</style>
<header>
 <select id=subj></select>
 <select id=paper></select>
 <select id=only>
  <option value="">everything</option>
  <option value="unreviewed" selected>unreviewed only</option>
  <option value="flagged">⚠ flagged (roman-split suspects)</option>
  <option value="tag-flagged">⚑ tag-flagged</option>
  <option value="low-confidence">low-confidence tags</option>
 </select>
 <span id=pos></span>
 <span class=keys style="margin-left:auto"><b>r</b>ight <b>n</b>ot-right · <b>g</b>ood <b>c</b>ut-off <b>w</b>rong-split <b>o</b>ther <b>f</b>lag-tag <b>←</b><b>→</b></span>
 <a href="#" id=statlink>stats</a>
</header>
<main>
 <div class=meta id=meta></div>
 <div class=crop><img id=im alt="question crop"></div>
 <div class=ansrow><label><input type=checkbox id=showans> show answer crop</label></div>
 <div class=crop id=anscrop style="display:none"><img id=ansim alt="answer crop"></div>
 <div class=editor id=editor style="display:none">
  <label>type <select id=edtype></select></label>
  <label>outcomes <select id=edrefs multiple></select></label>
  <button class=save id=edsave>save corrections</button>
  <span id=edmsg></span>
 </div>
 <div class=btns>
  <button class=good data-v=right style="font-size:16px">✓ RIGHT (r)</button>
  <button class=bad data-v=not-right style="font-size:16px">✗ NOT RIGHT (n)</button>
  <button class=good data-v=good>good (g)</button>
  <button class=bad data-v=cut-off>cut off (c)</button>
  <button class=bad data-v=wrong-split>wrong split (w)</button>
  <button class=bad data-v=other-bad>other (o)</button>
 </div>
</main>
<script>
let items=[],i=0,subjects=[],configs={};
const $=s=>document.querySelector(s);
async function load(){
 const s=$("#subj").value,o=$("#only").value,p=$("#paper").value;
 const r=await fetch(`/api/items?subject=${s}&only=${o}&paper=${encodeURIComponent(p)}`).then(r=>r.json());
 items=r.items; subjects=r.subjects; configs=r.configs||{}; i=0;
 if(!$("#subj").options.length){
  const q=new URLSearchParams(location.search);
  $("#subj").innerHTML='<option value="">all subjects</option>'+subjects.map(x=>`<option>${x}</option>`).join('');
  if(q.get("subject")){$("#subj").value=q.get("subject");return load();}
 }
 const papers=r.papers||[];
 const cur=$("#paper").value;
 $("#paper").innerHTML='<option value="">all papers</option>'+papers.map(x=>`<option>${x}</option>`).join('');
 if(papers.includes(cur))$("#paper").value=cur;
 const q2=new URLSearchParams(location.search);
 if(q2.get("paper")&&papers.includes(q2.get("paper"))&&!cur){$("#paper").value=q2.get("paper");history.replaceState(null,"",location.pathname+"?subject="+$("#subj").value);return load();}
 show();
}
function refChips(it,cfg){
 const desc=Object.fromEntries((cfg.outcomes||[]).map(o=>[o.code,o.description]));
 return (it.syllabusRefs||[]).map(c=>`<span class=ref title="${(desc[c]||'').replace(/"/g,'&quot;')}">${c}</span>`).join(' ');
}
function show(){
 const it=items[i];
 $("#pos").textContent=items.length?`${i+1} / ${items.length}`:"nothing matches";
 if(!it){$("#im").src="";$("#meta").textContent="";$("#editor").style.display="none";return}
 const cfg=configs[it.subject]||{types:[],outcomes:[]};
 $("#im").src=`/img/${it.paperId}/${it.assetKey}`;
 $("#meta").innerHTML=`<span><b>${it.subject}</b> · ${it.paperSlug}</span>
  <span>Q${it.q??"?"}${it.part??""}</span><span>${it.marks?it.marks+" marks":"no marks"}</span>
  <span>${it.lineCount?it.lineCount+" lines"+(it.spaceHeight?" · "+Math.round(it.spaceHeight)+"pt space":""):""}</span>
  <span>${it.type??""}</span><span>${it.module??it.topic??""}</span>
  <span>${refChips(it,cfg)}</span>
  ${it.aiTagged&&it.aiTagged.length?`<span class=ai title="AI-tagged: ${it.aiTagged.join(", ")}${it.confidence!=null?" · confidence "+it.confidence:""}">AI</span>`:''}
  ${it.corrected&&it.corrected.length?`<span class=fix>corrected: ${it.corrected.join(", ")}</span>`:''}
  ${it.tagFlag?`<span class=tflag>⚑ ${it.tagFlag}</span>`:''}
  ${it.flagged?'<span class=flag>⚠ roman-split suspect</span>':''}
  ${it.verdict?`<span class="verdict ${(it.verdict==='good'||it.verdict==='right')?'v-good':'v-bad'}">${it.verdict}</span>`:''}`;
 const hasCfg=cfg.types.length||cfg.outcomes.length;
 $("#editor").style.display=hasCfg?"":"none";
 if(hasCfg){
  $("#edtype").innerHTML='<option value="">(unset)</option>'+cfg.types.map(t=>`<option ${t===it.type?"selected":""}>${t}</option>`).join('');
  $("#edrefs").innerHTML=cfg.outcomes.map(o=>`<option value="${o.code}" title="${(o.description||'').replace(/"/g,'&quot;')}" ${(it.syllabusRefs||[]).includes(o.code)?"selected":""}>${o.code}</option>`).join('');
  $("#edmsg").textContent="";
 }
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
async function correct(field,value){
 const it=items[i]; if(!it)return;
 await fetch("/api/correction",{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({paperId:it.paperId,assetKey:it.assetKey,field,value})});
}
$("#edsave").onclick=async()=>{
 const it=items[i]; if(!it)return;
 const t=$("#edtype").value||null;
 const refs=[...$("#edrefs").selectedOptions].map(o=>o.value);
 if(t!==it.type){await correct("type",t); it.type=t; (it.corrected??=[]).push("type");}
 if(JSON.stringify(refs)!==JSON.stringify(it.syllabusRefs||[])){
  await correct("syllabusRefs",refs); it.syllabusRefs=refs; (it.corrected??=[]).push("syllabusRefs");}
 $("#edmsg").textContent="saved ✓"; show();
};
document.addEventListener("keydown",e=>{
 if(e.target.tagName==="SELECT"||e.target.tagName==="INPUT")return;
 if(e.key==="ArrowRight"&&i<items.length-1){i++;show()}
 if(e.key==="ArrowLeft"&&i>0){i--;show()}
 if(e.key==="f"){const it=items[i];if(it){correct("tagFlag","wrong-tag");it.tagFlag="wrong-tag";show()}return}
 const map={g:"good",c:"cut-off",w:"wrong-split",o:"other-bad",r:"right",n:"not-right"};
 if(map[e.key])verdict(map[e.key]);
});
document.querySelectorAll(".btns button").forEach(b=>b.onclick=()=>verdict(b.dataset.v));
$("#subj").onchange=()=>{$("#paper").value="";load()}; $("#paper").onchange=load;
$("#only").onchange=load; $("#showans").onchange=show;
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
