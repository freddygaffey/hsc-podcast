#!/usr/bin/env python3
"""Ground-truth annotation UI: draw question boxes on the ORIGINAL paper pages.

Shows a paper's rendered pages (papers/_work/<paperId>/pNN.png) blank — no machine
boxes — and lets a human drag rectangles marking each question/part region, with
question number, part label and marks. Saves to papers/_work/<paperId>/annotations.json
in the same normalised-bbox shape as boundaries.json, so the machine's segmentation can
be scored against it (IoU per question) and the locate policy iterated until they agree.

    python3 tools/annotate_app.py [--port 5090]
    open http://localhost:5090

Controls: pick the paper top-left · set Q/part/marks in the toolbar · drag on a page to
add a box · click a box to select (then Delete key or ✕ to remove) · everything
auto-saves. "next Q" bumps the question number after each box if ticked.
"""
import argparse
import json
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_file

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vision_seg as vs  # noqa: E402

app = Flask(__name__)


@app.route("/api/papers")
def api_papers():
    out = []
    for d in sorted(WORK.iterdir()):
        if d.is_dir() and (d / "info.json").exists() and list(d.glob("p*.png")):
            try:
                info = json.loads((d / "info.json").read_text())
            except Exception:
                continue
            out.append({"paperId": d.name, "subject": info.get("subject"),
                        "pages": info.get("pageCount"),
                        "annotated": (d / "annotations.json").exists()})
    return jsonify({"papers": out})


@app.route("/api/paper/<pid>")
def api_paper(pid):
    wd = WORK / pid
    info = json.loads((wd / "info.json").read_text())
    ann = {"paperId": pid, "boxes": []}
    ap = wd / "annotations.json"
    if ap.exists():
        try:
            ann = json.loads(ap.read_text())
        except Exception:
            pass
    vision = []
    vp = wd / "vision-boxes.json"
    if vp.exists():
        try:
            vision = json.loads(vp.read_text()).get("boxes", [])
        except Exception:
            pass
    return jsonify({"pages": [p["image"] for p in info["pages"]],
                    "annotations": ann, "vision": vision})


@app.route("/api/paper/<pid>/save", methods=["POST"])
def api_save(pid):
    data = request.get_json()
    (WORK / pid / "annotations.json").write_text(json.dumps(
        {"paperId": pid, "boxes": data.get("boxes", [])}, indent=1))
    return jsonify({"ok": True, "n": len(data.get("boxes", []))})


@app.route("/page/<pid>/<name>")
def page_img(pid, name):
    p = WORK / pid / name
    if not p.exists() or not name.endswith(".png"):
        return "not found", 404
    return send_file(p, mimetype="image/png")


# ── compare view: papers rerun through the gen-3 pipeline (have split.json).
# Shows each content page twice, parallel: unannotated | machine split boxes.
# Question units come from split.json; writing-space "lines" bands (which the
# splitter never emits) are pulled dimmed from the frozen gold set for context.
GOLDSET = ROOT / "papers" / "_goldset"


@app.route("/api/compare/papers")
def api_compare_papers():
    out = []
    for d in sorted(WORK.iterdir()):
        if not (d.is_dir() and (d / "split.json").exists() and list(d.glob("p*.png"))):
            continue
        try:
            split = json.loads((d / "split.json").read_text())
        except Exception:
            continue
        out.append({"paperId": d.name, "subject": split.get("subject"),
                    "units": len(split.get("units", []))})
    return jsonify({"papers": out})


@app.route("/api/compare/paper/<pid>")
def api_compare_paper(pid):
    wd = WORK / pid
    info = json.loads((wd / "info.json").read_text())
    split = json.loads((wd / "split.json").read_text())
    lines = []
    gp = GOLDSET / pid / "gold.json"
    if gp.exists():
        try:
            gold = json.loads(gp.read_text())
            lines = [b for b in gold.get("boxes", []) if b.get("kind") == "lines"]
        except Exception:
            pass
    return jsonify({"pages": [p["image"] for p in info["pages"]],
                    "units": split.get("units", []), "lines": lines,
                    "source": split.get("source", "?")})


PAGE = """<!doctype html><meta charset=utf-8><title>Paper annotator</title>
<style>
 body{font:14px/1.4 system-ui;margin:0;background:#eef1f5;color:#1a1d24}
 header{display:flex;gap:10px;align-items:center;padding:8px 14px;background:#fff;
  border-bottom:1px solid #dde;position:sticky;top:0;z-index:50;flex-wrap:wrap}
 select,input,button{font:inherit;padding:5px 8px;border:1px solid #ccd;border-radius:6px;background:#fff}
 input.small{width:48px}
 #status{color:#697;font-size:12px}
 main{max-width:960px;margin:12px auto;padding:0 12px}
 .pg{position:relative;margin:0 auto 16px;box-shadow:0 1px 6px rgba(0,0,0,.15);user-select:none}
 .pg img{display:block;width:100%;height:auto;pointer-events:none}
 .pg .num{position:absolute;top:4px;left:-34px;color:#99a;font-size:12px}
 .box{position:absolute;border:2px solid rgba(200,40,40,.85);background:rgba(230,60,60,.08);cursor:move}
 .box.lines{border-color:rgba(20,140,60,.85);background:rgba(30,170,80,.10)}
 .box.lines .tag{background:rgba(20,140,60,.9)}
 .box.sel{border-color:#1450d0;background:rgba(40,90,220,.12)}
 .box .tag{position:absolute;top:-18px;left:-2px;background:rgba(200,40,40,.9);color:#fff;
  font-size:11px;padding:0 6px;border-radius:3px;white-space:nowrap}
 .box.sel .tag{background:#1450d0}
 .box .x{position:absolute;top:-18px;right:-2px;background:#333;color:#fff;font-size:11px;
  padding:0 5px;border-radius:3px;cursor:pointer}
 .box .rs{position:absolute;right:-6px;bottom:-6px;width:12px;height:12px;background:#1450d0;
  border-radius:3px;cursor:nwse-resize;display:none}
 .box.sel .rs{display:block}
 .ghost{position:absolute;border:2px dashed #1450d0;background:rgba(40,90,220,.08);pointer-events:none}
 .vbox{position:absolute;border:2px solid rgba(30,90,220,.75);pointer-events:none}
 .vbox.vlines{border-color:rgba(0,150,140,.75);border-style:dashed}
 .vbox .vtag{position:absolute;bottom:-16px;right:-2px;background:rgba(30,90,220,.85);color:#fff;
  font-size:10px;padding:0 5px;border-radius:3px;white-space:nowrap}
 .vbox.vlines .vtag{background:rgba(0,150,140,.85)}
 .keys b{border:1px solid #ccd;border-radius:4px;padding:0 5px;background:#fff}
</style>
<header>
 <a href="/compare" style="color:#1450d0;text-decoration:none">compare ›</a>
 <select id=paper></select>
 <select id=kind>
  <option value="question">question box</option>
  <option value="lines">lines box</option>
 </select>
 <label>Q <input class=small id=qn value="1"></label>
 <label>part <input class=small id=part placeholder="a"></label>
 <label>marks <input class=small id=marks placeholder="?"></label>
 <label><input type=checkbox id=autoq checked> next Q after box</label>
 <label><input type=checkbox id=showai checked> show AI boxes</label>
 <span id=count></span><span id=status></span>
 <span class=keys style="margin-left:auto">drag = new box · drag a box = move · corner = resize · <b>l</b> lines mode · <b>⌫</b> delete</span>
</header>
<main id=pages></main>
<script>
const $=s=>document.querySelector(s);
let PID=null, BOXES=[], VISION=[], sel=-1, saveT=null;
async function loadPapers(){
 const r=await fetch("/api/papers").then(r=>r.json());
 $("#paper").innerHTML=r.papers.map(p=>`<option value="${p.paperId}">${p.annotated?"✓ ":""}${p.subject} — ${p.paperId.slice(-40)}</option>`).join("");
 const q=new URLSearchParams(location.search).get("paper");
 if(q)$("#paper").value=q;
 loadPaper($("#paper").value);
}
async function loadPaper(pid){
 PID=pid; sel=-1;
 const r=await fetch(`/api/paper/${pid}`).then(r=>r.json());
 BOXES=r.annotations.boxes||[]; VISION=r.vision||[];
 const main=$("#pages"); main.innerHTML="";
 r.pages.forEach((img,i)=>{
  const d=document.createElement("div"); d.className="pg"; d.dataset.pg=i;
  d.innerHTML=`<span class=num>p${i+1}</span><img src="/page/${pid}/${img}">`;
  main.appendChild(d);
  hookDraw(d,i);
 });
 renderBoxes(); updateCount();
}
function renderBoxes(){
 document.querySelectorAll(".box,.ghost,.vbox").forEach(e=>e.remove());
 if($("#showai").checked)VISION.forEach(b=>{
  const pg=document.querySelector(`.pg[data-pg="${b.page}"]`); if(!pg)return;
  const el=document.createElement("div");
  el.className="vbox"+(b.kind==="lines"?" vlines":"");
  el.style.left=(b.bbox[0]*100)+"%"; el.style.top=(b.bbox[1]*100)+"%";
  el.style.width=((b.bbox[2]-b.bbox[0])*100)+"%"; el.style.height=((b.bbox[3]-b.bbox[1])*100)+"%";
  const lab=(b.kind==="lines"?"AI lines":"AI Q"+(b.number||"?")+(b.part||""))+(b.marks?" · "+b.marks+"m":"");
  el.innerHTML=`<span class=vtag>${lab}</span>`;
  pg.appendChild(el);
 });
 BOXES.forEach((b,idx)=>{
  const pg=document.querySelector(`.pg[data-pg="${b.page}"]`); if(!pg)return;
  const el=document.createElement("div");
  el.className="box"+(b.kind==="lines"?" lines":"")+(idx===sel?" sel":"");
  el.style.left=(b.bbox[0]*100)+"%"; el.style.top=(b.bbox[1]*100)+"%";
  el.style.width=((b.bbox[2]-b.bbox[0])*100)+"%"; el.style.height=((b.bbox[3]-b.bbox[1])*100)+"%";
  const lab=b.kind==="lines"?`lines${b.number?" Q"+b.number:""}`:`Q${b.number||"?"}${b.part||""}${b.marks?" · "+b.marks+"m":""}`;
  el.innerHTML=`<span class=tag>${lab}</span><span class=x title=delete>✕</span><span class=rs></span>`;
  el.onmousedown=e=>{
   e.stopPropagation();e.preventDefault();
   if(e.target.className==="x")return;
   sel=idx;
   if(b.kind!=="lines"){$("#qn").value=b.number||"";$("#part").value=b.part||"";$("#marks").value=b.marks||"";}
   renderBoxes();
   startDrag(e,pg,idx,e.target.className==="rs"?"resize":"move");
  };
  el.onclick=e=>{e.stopPropagation();
   if(e.target.className==="x"){BOXES.splice(idx,1);sel=-1;renderBoxes();save();}};
  pg.appendChild(el);
 });
 updateCount();
}
function startDrag(e,pg,idx,mode){
 const b=BOXES[idx], r=pg.getBoundingClientRect();
 const sx=(e.clientX-r.left)/r.width, sy=(e.clientY-r.top)/r.height;
 const orig=[...b.bbox];
 let moved=false;
 function mm(ev){
  const cx=(ev.clientX-r.left)/r.width, cy=(ev.clientY-r.top)/r.height;
  const dx=cx-sx, dy=cy-sy;
  if(Math.abs(dx)+Math.abs(dy)>0.002)moved=true;
  if(!moved)return;
  if(mode==="move"){
   const w=orig[2]-orig[0], h=orig[3]-orig[1];
   let x0=Math.min(Math.max(orig[0]+dx,0),1-w), y0=Math.min(Math.max(orig[1]+dy,0),1-h);
   b.bbox=[x0,y0,x0+w,y0+h].map(v=>Math.round(v*1e4)/1e4);
  }else{
   b.bbox=[orig[0],orig[1],
    Math.min(Math.max(orig[2]+dx,orig[0]+0.02),1),
    Math.min(Math.max(orig[3]+dy,orig[1]+0.005),1)].map(v=>Math.round(v*1e4)/1e4);
  }
  renderBoxes();
 }
 function mu(){document.removeEventListener("mousemove",mm);document.removeEventListener("mouseup",mu);
  if(moved)save();}
 document.addEventListener("mousemove",mm);
 document.addEventListener("mouseup",mu);
}
function hookDraw(pg,pageIdx){
 let start=null, ghost=null;
 pg.onmousedown=e=>{
  const r=pg.getBoundingClientRect();
  start=[(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height];
  ghost=document.createElement("div");ghost.className="ghost";pg.appendChild(ghost);
  e.preventDefault();
 };
 pg.onmousemove=e=>{
  if(!start||!ghost)return;
  const r=pg.getBoundingClientRect();
  const cur=[(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height];
  const x0=Math.min(start[0],cur[0]),y0=Math.min(start[1],cur[1]),
        x1=Math.max(start[0],cur[0]),y1=Math.max(start[1],cur[1]);
  ghost.style.left=(x0*100)+"%";ghost.style.top=(y0*100)+"%";
  ghost.style.width=((x1-x0)*100)+"%";ghost.style.height=((y1-y0)*100)+"%";
  ghost.dataset.b=JSON.stringify([x0,y0,x1,y1]);
 };
 pg.onmouseup=e=>{
  if(!start)return;
  const b=ghost&&ghost.dataset.b?JSON.parse(ghost.dataset.b):null;
  if(ghost)ghost.remove(); ghost=null; start=null;
  if(!b||(b[2]-b[0])<0.02||(b[3]-b[1])<0.005)return;   // ignore tiny accidental drags
  const kind=$("#kind").value;
  BOXES.push({page:pageIdx,bbox:b.map(v=>Math.round(v*1e4)/1e4),kind:kind,
   number:$("#qn").value.trim()||null,part:$("#part").value.trim()||null,
   marks:kind==="lines"?null:(parseInt($("#marks").value)||null)});
  if(kind==="question"&&$("#autoq").checked&&!$("#part").value.trim()){
   $("#qn").value=(parseInt($("#qn").value)||0)+1; $("#marks").value="";
  }
  sel=BOXES.length-1; renderBoxes(); save();
 };
}
function updateCount(){$("#count").textContent=BOXES.length+" boxes";}
function save(){
 clearTimeout(saveT);
 saveT=setTimeout(async()=>{
  const r=await fetch(`/api/paper/${PID}/save`,{method:"POST",
   headers:{"Content-Type":"application/json"},body:JSON.stringify({boxes:BOXES})}).then(r=>r.json());
  $("#status").textContent="saved ✓ "+new Date().toLocaleTimeString();
 },400);
}
document.addEventListener("keydown",e=>{
 if(document.activeElement.tagName==="INPUT")return;
 if((e.key==="Backspace"||e.key==="Delete")&&sel>=0){
  BOXES.splice(sel,1);sel=-1;renderBoxes();save();e.preventDefault();
 }
 if(e.key==="l"){const k=$("#kind");k.value=k.value==="lines"?"question":"lines";}
});
$("#paper").onchange=()=>loadPaper($("#paper").value);
$("#showai").onchange=renderBoxes;
loadPapers();
</script>"""


@app.route("/")
def home():
    return PAGE


# ── dashboard: one row per split paper — counts, marks-to-90, invariant status, confidence.
def _is_ii(u):
    return "II" in (u.get("section") or "").replace(" ", "").upper()


@app.route("/api/dashboard")
def api_dashboard():
    try:
        import invariants as inv
    except Exception:
        inv = None
    rows = []
    for d in sorted(WORK.iterdir()):
        if not (d.is_dir() and (d / "split.json").exists() and list(d.glob("p*.png"))):
            continue
        try:
            s = json.loads((d / "split.json").read_text())
        except Exception:
            continue
        info = {}
        if (d / "info.json").exists():
            try:
                info = json.loads((d / "info.json").read_text())
            except Exception:
                pass
        units = s.get("units", [])
        mc = {str(u.get("number")) for u in units if u.get("section") and not _is_ii(u)}
        ii_marks = {}
        for u in units:
            if _is_ii(u):
                ii_marks.setdefault(str(u.get("number")), u.get("marks"))
        confs = [u.get("confidence") for u in units if isinstance(u.get("confidence"), (int, float))]
        status, reasons = "ok", []
        if inv:
            try:
                vs, _ = inv.check(d.name)
                errs = [v for v in vs if v.level == "error"]
                status = "FAIL" if errs else ("warn" if any(v.level == "warn" for v in vs) else "ok")
                reasons = [f"{v.code}: {v.msg}" for v in vs if v.level in ("error", "warn")]
            except Exception as e:
                status, reasons = "?", [str(e)]
        # pending rule-exceptions the AI flagged: mandatory human approval, even if invariants pass
        pending = [dict(unit=str(u.get("number")), **(u.get("ruleException") or {}))
                   for u in units if u.get("ruleException")]
        if pending and status != "FAIL":
            status = "review"
        reasons = [f"⚑ Q{p['unit']} broke '{p.get('rule','?')}': {p.get('reason','')}" for p in pending] + reasons
        # solution coverage: gaps/missing need human review; 'none' is queued for AI-fill
        sol = s.get("solutions") or {}
        if sol.get("status") in ("gaps", "missing") and status != "FAIL":
            status = "review"
            reasons = [f"⚑ solutions {sol['status']}"
                       + (f": gaps {sol.get('gaps')}" if sol.get("gaps") else "")] + reasons
        rows.append({
            "paperId": d.name, "subject": s.get("subject"), "source": s.get("source", "?"),
            "pages": info.get("pageCount"), "mc": len(mc),
            "ii": len(ii_marks), "iiMarks": sum(m for m in ii_marks.values() if m),
            "sol": sol,
            "avgConf": round(sum(confs) / len(confs), 2) if confs else None,
            "lowConf": sum(1 for c in confs if c < 0.7),
            "status": status, "reasons": reasons,
        })
    return jsonify({"papers": rows})


DASH = """<!doctype html><meta charset=utf-8><title>Segmentation dashboard</title>
<style>
 body{font:14px/1.4 system-ui;margin:0;background:#eef1f5;color:#1a1d24}
 header{display:flex;gap:12px;align-items:center;padding:10px 16px;background:#fff;border-bottom:1px solid #dde}
 h1{font-size:16px;margin:0}
 a{color:#1450d0;text-decoration:none}
 main{padding:16px;max-width:1200px;margin:0 auto}
 table{width:100%;border-collapse:collapse;background:#fff;box-shadow:0 1px 5px rgba(0,0,0,.08);border-radius:8px;overflow:hidden}
 th,td{padding:8px 10px;text-align:left;border-bottom:1px solid #eef}
 th{background:#f6f8fb;font-size:12px;color:#678;cursor:pointer;user-select:none}
 td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
 tr:hover{background:#f9fbff}
 .pill{font-size:11px;padding:1px 7px;border-radius:10px;font-weight:600}
 .ok{background:#e3f6e8;color:#1a7f37}.FAIL{background:#fde8e8;color:#c22}.warn{background:#fdf3e0;color:#a56a00}
 .review{background:#e7ecfd;color:#3b4cc0}
 .src{font-size:11px;color:#789;background:#eef2f7;padding:1px 6px;border-radius:4px}
 .bad{color:#c22;font-weight:600}.good{color:#1a7f37}
 .sub{color:#8494ab;font-size:12px}
 .reasons{font-size:11px;color:#a56a00;max-width:340px}
</style>
<header><h1>Segmentation dashboard</h1><span id=meta class=sub></span>
 <span style="margin-left:auto"><a href="/pipeline">pipeline ›</a> · <a href="/solution">solution style ›</a> · <a href="/compare">compare view ›</a> · <a href="/">annotator ›</a></span></header>
<main><table id=t><thead><tr>
 <th data-k=paperId>paper</th><th data-k=source>src</th><th class=num data-k=pages>pp</th>
 <th class=num data-k=mc>MC</th><th class=num data-k=ii>Sec II</th><th class=num data-k=iiMarks>II marks</th>
 <th>sol</th><th class=num data-k=avgConf>conf</th><th data-k=status>status</th><th>flags</th>
</tr></thead><tbody></tbody></table></main>
<script>
const $=s=>document.querySelector(s);
let ROWS=[], sortK='status', asc=true;
function render(){
 ROWS.sort((a,b)=>{let x=a[sortK],y=b[sortK];if(x==null)x=-1;if(y==null)y=-1;return (x>y?1:x<y?-1:0)*(asc?1:-1);});
 const ok=ROWS.filter(r=>r.status==='ok').length;
 $('#meta').textContent=`${ROWS.length} papers · ${ok} passing invariants`;
 $('#t tbody').innerHTML=ROWS.map(r=>{
  const marks=r.iiMarks?`<span class="${r.iiMarks===90?'good':'bad'}">${r.iiMarks}</span>/90`:'—';
  const mc=`<span class="${r.mc===10?'good':'bad'}">${r.mc}</span>`;
  const s=r.sol||{};
  const sol=!s.status?'—':s.status==='complete'?`<span class=good>${s.matched}/${s.total}</span>`
    :s.status==='none'?`<span class=sub>AI-fill</span>`:`<span class=bad>${s.status}</span>`;
  return `<tr>
   <td><a href="/compare?paper=${encodeURIComponent(r.paperId)}">${r.paperId.slice(-46)}</a></td>
   <td><span class=src>${r.source||'?'}</span></td>
   <td class=num>${r.pages??'—'}</td>
   <td class=num>${mc}</td><td class=num>${r.ii}</td><td class=num>${marks}</td>
   <td>${sol}</td>
   <td class=num>${r.avgConf??'—'}${r.lowConf?` <span class=bad>(${r.lowConf}?)</span>`:''}</td>
   <td><span class="pill ${r.status}">${r.status}</span></td>
   <td class=reasons>${(r.reasons||[]).join(' · ')}</td>
  </tr>`;}).join('');
}
document.querySelectorAll('th[data-k]').forEach(th=>th.onclick=()=>{
 const k=th.dataset.k; asc=(sortK===k)?!asc:true; sortK=k; render();});
fetch('/api/dashboard').then(r=>r.json()).then(d=>{ROWS=d.papers;render();});
</script>"""


@app.route("/dashboard")
def dashboard():
    return DASH


@app.route("/solution")
def solution_preview():
    p = ROOT / "tools" / "solution_preview.html"
    if not p.exists():
        return "solution preview not generated yet", 404
    return p.read_text()


@app.route("/pipeline")
def pipeline_view():
    p = ROOT / "tools" / "pipeline_view.html"
    if not p.exists():
        return "pipeline view not generated yet", 404
    return p.read_text()


COMPARE = """<!doctype html><meta charset=utf-8><title>Pipeline compare</title>
<style>
 body{font:14px/1.4 system-ui;margin:0;background:#eef1f5;color:#1a1d24}
 header{display:flex;gap:12px;align-items:center;padding:8px 14px;background:#fff;
  border-bottom:1px solid #dde;position:sticky;top:0;z-index:50;flex-wrap:wrap}
 select,button{font:inherit;padding:5px 8px;border:1px solid #ccd;border-radius:6px;background:#fff}
 a{color:#1450d0;text-decoration:none}
 #meta{color:#697;font-size:12px}
 .leg{margin-left:auto;font-size:12px;color:#89a;display:flex;gap:12px;align-items:center}
 .leg i{display:inline-block;width:22px;height:0;vertical-align:middle;margin-right:4px}
 .leg .q{border-top:2px solid rgba(30,90,220,.85)}
 .leg .l{border-top:1px dashed rgba(120,130,150,.7)}
 main{padding:14px 12px;margin:0 auto}
 main.compact{max-width:1180px}
 .row{display:flex;gap:14px;margin:0 0 12px;align-items:flex-start}
 .col{flex:1 1 0;min-width:0}
 .cap{font-size:11px;color:#8494ab;margin:0 0 3px}
 .pg{position:relative;box-shadow:0 1px 5px rgba(0,0,0,.15);background:#fff;line-height:0}
 .pg img{display:block;width:100%;height:auto}
 .qbox{position:absolute;border:2px solid rgba(30,90,220,.85);background:rgba(40,90,220,.06);box-sizing:border-box}
 .qbox .t{position:absolute;top:-15px;left:-2px;background:rgba(30,90,220,.9);color:#fff;
  font-size:10px;line-height:1.4;padding:0 5px;border-radius:3px;white-space:nowrap}
 .lbox{position:absolute;border:1px dashed rgba(120,130,150,.55);background:rgba(120,130,150,.05);box-sizing:border-box}
 .lbox .t{position:absolute;bottom:-13px;right:-2px;background:rgba(120,130,150,.55);color:#fff;
  font-size:9px;line-height:1.4;padding:0 4px;border-radius:3px;white-space:nowrap}
 .empty{color:#89a;padding:40px;text-align:center}
</style>
<header>
 <a href="/dashboard">‹ dashboard</a>
 <select id=paper></select>
 <label><input type=checkbox id=lines checked> dim lines</label>
 <label>width
  <select id=width>
   <option value="1180" selected>compact</option>
   <option value="1500">wide</option>
   <option value="2000">full</option>
  </select></label>
 <span id=meta></span>
 <span class=leg><span><i class=q></i>machine question</span><span><i class=l></i>writing lines</span></span>
</header>
<main id=view class=compact></main>
<script>
const $=s=>document.querySelector(s);
let DATA=null;
async function loadPapers(){
 const r=await fetch('/api/compare/papers').then(r=>r.json());
 if(!r.papers.length){$('#view').innerHTML='<div class=empty>No papers have been run through the gen-3 pipeline yet (none have split.json).</div>';return;}
 $('#paper').innerHTML=r.papers.map(p=>`<option value="${p.paperId}">${p.subject||''} — ${p.paperId.slice(-42)} (${p.units}u)</option>`).join('');
 const q=new URLSearchParams(location.search).get('paper');
 if(q)$('#paper').value=q;
 load($('#paper').value);
}
async function load(pid){
 PID=pid;
 DATA=await fetch(`/api/compare/paper/${pid}`).then(r=>r.json());
 render();
}
function box(cls,bb,label){
 const el=document.createElement('div'); el.className=cls;
 el.style.left=(bb[0]*100)+'%'; el.style.top=(bb[1]*100)+'%';
 el.style.width=((bb[2]-bb[0])*100)+'%'; el.style.height=((bb[3]-bb[1])*100)+'%';
 el.innerHTML=`<span class=t>${label}</span>`;
 return el;
}
function render(){
 if(!DATA)return;
 const showLines=$('#lines').checked;
 const byPage={}, linesByPage={}, wsByPage={};
 DATA.units.forEach(u=>u.regions.forEach(rg=>{(byPage[rg.page]=byPage[rg.page]||[]).push({bb:rg.bbox,u});}));
 DATA.units.forEach(u=>(u.writingSpace||[]).forEach(w=>{(wsByPage[w.page]=wsByPage[w.page]||[]).push(w);}));
 DATA.lines.forEach(b=>{(linesByPage[b.page]=linesByPage[b.page]||[]).push(b);});
 const pages=[...new Set([...Object.keys(byPage),...Object.keys(linesByPage),...Object.keys(wsByPage)].map(Number))].sort((a,b)=>a-b);
 const nws=DATA.units.reduce((s,u)=>s+((u.writingSpace||[]).length),0);
 $('#meta').textContent=`${DATA.units.length} units · ${pages.length} content pages`+(nws?` · ${nws} writing-space bands`:` · no writing-space yet`);
 const view=$('#view'); view.innerHTML='';
 pages.forEach(pn=>{
  const img='/page/'+PID+'/'+(DATA.pages[pn-1]||('p'+String(pn).padStart(2,'0')+'.png'));
  const row=document.createElement('div'); row.className='row';
  row.innerHTML=`<div class=col><div class=cap>p${pn} · unannotated</div><div class=pg><img src="${img}"></div></div>`+
   `<div class=col><div class=cap>p${pn} · ${DATA.source} split</div><div class="pg" data-ann></div></div>`;
  const ann=row.querySelector('[data-ann]');
  ann.innerHTML=`<img src="${img}">`;
  if(showLines)(linesByPage[pn]||[]).forEach(b=>ann.appendChild(box('lbox',b.bbox,'lines'+(b.number?' Q'+b.number:''))));
  if(showLines)(wsByPage[pn]||[]).forEach(w=>ann.appendChild(box('lbox',w.bbox,'write')));
  (byPage[pn]||[]).forEach(rg=>{const u=rg.u;
   ann.appendChild(box('qbox',rg.bb,'Q'+(u.number||'?')+(u.part||'')+(u.marks?' · '+u.marks+'m':'')));});
  view.appendChild(row);
 });
}
let PID=null;
$('#paper').onchange=()=>{PID=$('#paper').value;load(PID);};
$('#lines').onchange=render;
$('#width').onchange=()=>{const w=$('#width').value;$('#view').style.maxWidth=w+'px';};
(async()=>{await loadPapers();PID=$('#paper').value;})();
</script>"""


@app.route("/compare")
def compare():
    return COMPARE


# ── eval view: question|answer per-question evaluation for one subject's run.
# Left = each question's crop (from split.json regions), right = its answer
# (real solution crop from answers.json, or AI-rendered, or pending). Crops are
# rendered client-side from the page PNGs — nothing is baked here.
def _grouped_units(split):
    """split.json units are already grouped (persist_one merges regions); pass through,
    tolerating either the grouped shape (regions[]) or a flat page/bbox shape."""
    out = []
    for u in split.get("units", []):
        regions = u.get("regions")
        if not regions and u.get("page") is not None:
            regions = [{"page": u["page"], "bbox": u.get("bbox")}]
        out.append({
            "id": u.get("id") or ("q" + str(u.get("number")) + (u.get("part") or "")),
            "number": u.get("number"), "part": u.get("part"),
            "section": u.get("section"), "marks": u.get("marks"),
            "confidence": u.get("confidence"),
            "ruleException": u.get("ruleException"),
            "note": u.get("note", ""),
            "regions": regions or [],
        })
    return out


@app.route("/api/eval/papers")
def api_eval_papers():
    subject = request.args.get("subject")
    out = []
    for d in sorted(WORK.iterdir()):
        if not (d.is_dir() and (d / "split.json").exists() and list(d.glob("p*.png"))):
            continue
        try:
            split = json.loads((d / "split.json").read_text())
        except Exception:
            continue
        if subject and split.get("subject") != subject:
            continue
        units = split.get("units", [])
        out.append({"paperId": d.name, "subject": split.get("subject"),
                    "units": len(units),
                    "source": split.get("source", "?"),
                    "hasAnswers": (d / "answers.json").exists()})
    return jsonify({"papers": out,
                    "subjects": sorted({p["subject"] for p in out if p["subject"]})})


@app.route("/api/eval/paper/<pid>")
def api_eval_paper(pid):
    wd = WORK / pid
    info = json.loads((wd / "info.json").read_text())
    split = json.loads((wd / "split.json").read_text())
    # answers: a rendered solution image per unit, auto-discovered from solutions/<id>.png
    # (transcribed from the paper's marking solutions, re-set in the house style). An
    # answers.json can still override/extend.
    answers = {}
    soldir = wd / "solutions"
    if soldir.is_dir():
        for u in split.get("units", []):
            uid = u.get("id") or ("q" + str(u.get("number")) + (u.get("part") or ""))
            img = soldir / (uid + ".png")
            if img.exists():
                note = ""
                sj = soldir / (uid + ".json")
                if sj.exists():
                    try:
                        note = json.loads(sj.read_text()).get("answerNote", "")
                    except Exception:
                        pass
                answers[uid] = {"kind": "img", "src": f"/solimg/{pid}/{uid}.png", "note": note}
    ap = wd / "answers.json"
    if ap.exists():
        try:
            answers.update(json.loads(ap.read_text()).get("answers", {}))
        except Exception:
            pass
    return jsonify({
        "paperId": pid, "subject": split.get("subject"),
        "source": split.get("source", "?"),
        "solutionsStartPage": split.get("solutionsStartPage"),
        "pages": [p["image"] for p in info["pages"]],
        "units": _grouped_units(split),
        "answers": answers,
    })


@app.route("/solimg/<pid>/<name>")
def sol_img(pid, name):
    p = WORK / pid / "solutions" / name
    if not p.exists() or not name.endswith(".png"):
        return "not found", 404
    return send_file(p, mimetype="image/png")


@app.route("/aimg/<pid>/<name>")
def annotated_img(pid, name):
    p = WORK / pid / "annotated" / name
    if not p.exists() or not name.endswith(".png"):
        return "not found", 404
    return send_file(p, mimetype="image/png")


@app.route("/gimg/<pid>/<name>")
def green_only_img(pid, name):
    """The clean page with ONLY the final (green) boxes. Recomputed LIVE from the cached vision
    responses with the buffer values passed as ?buf=&pad= (fractions of page height), so the
    'green only' toggle doubles as a buffer-tuning preview. Falls back to split.json regions if
    the live recompute isn't available."""
    import io
    from PIL import Image, ImageDraw
    if not name.endswith(".png"):
        return "not found", 404
    page = WORK / pid / name                                  # the clean (unannotated) page
    if not page.exists():
        return "not found", 404
    try:
        pn = int(name[1:-4])
    except ValueError:
        return "bad page", 400
    img = Image.open(page).convert("RGB")
    W, H = img.size
    dr = ImageDraw.Draw(img)

    def _rect(bbox, label):
        x0, y0, x1, y1 = bbox[0] * W, bbox[1] * H, bbox[2] * W, bbox[3] * H
        dr.rectangle([x0, y0, x1, y1], outline=(15, 160, 60), width=2)
        dr.rectangle([x0 - 1, y0, x0 + 42, y0 + 12], fill=(15, 160, 60))
        dr.text((x0 + 2, y0 + 1), label, fill=(255, 255, 255))

    buf = _qfloat("buf", vs.BUF_FRAC)
    pad = _qfloat("pad", vs.PAD_FRAC)
    boxes = None
    try:                                                      # live recompute with tuned buffers
        boxes = vs.page_boxes(pid, pn, buf_frac=buf, pad_frac=pad)
    except Exception:
        boxes = None
    if boxes:
        for label, bbox in boxes:
            _rect(bbox, label)
    else:                                                     # fallback: whatever is in split.json
        sp = WORK / pid / "split.json"
        split = json.loads(sp.read_text()) if sp.exists() else {}
        for u in split.get("units", []):
            for r in u.get("regions", []):
                if r.get("page") == pn and r.get("bbox"):
                    _rect(r["bbox"], u.get("id", ""))
    out = io.BytesIO()
    img.save(out, "PNG")
    out.seek(0)
    return send_file(out, mimetype="image/png")


def _qfloat(name, default):
    try:
        v = float(request.args.get(name, ""))
        return v if v > 0 else default
    except (TypeError, ValueError):
        return default


def _view_pages(pid):
    """Pages to show for a paper. Prefer the debug-annotated PNGs; otherwise (segmentation-only
    papers) derive the QUESTION pages from split.json so they're still viewable green-only."""
    d = WORK / pid / "annotated"
    if d.is_dir():
        pgs = sorted(f.name for f in d.glob("p*.png"))
        if pgs:
            return pgs, True
    sp = WORK / pid / "split.json"
    if not sp.exists():
        return [], False
    last = (json.loads(sp.read_text()).get("solutionsStartPage") or 999) - 1
    pgs = [f.name for f in sorted((WORK / pid).glob("p*.png"))
           if f.stem[1:].isdigit() and 2 <= int(f.stem[1:]) <= last]
    return pgs, False


@app.route("/annotated")
def annotated_view():
    # every paper with a segmentation (split.json) is viewable; those with a debug annotation
    # show the full overlay, the rest show green-only (computed live from split.json).
    papers = sorted(x.name for x in WORK.iterdir()
                    if (x / "split.json").exists() and any(x.glob("p*.png")))
    pid = request.args.get("paper", "")
    if pid not in papers and papers:
        pid = papers[0]
    pages, has_ann = _view_pages(pid)
    opts = "".join(f'<option value="{p}"{" selected" if p == pid else ""}>{p[18:]}</option>'
                   for p in papers)
    imgs = "".join(
        f'<figure><figcaption>{n}</figcaption>'
        f'<img class=pageimg src="/{"aimg" if has_ann else "gimg"}/{pid}/{n}" '
        f'data-a="/{"aimg" if has_ann else "gimg"}/{pid}/{n}" '
        f'data-g="/gimg/{pid}/{n}" loading="lazy"></figure>' for n in pages)
    return f"""<!doctype html><meta charset=utf-8><title>Box annotations</title>
<style>body{{font:14px system-ui;margin:0;background:#eef1f5;color:#1a1d24}}
header{{position:sticky;top:0;background:#fff;padding:10px 16px;border-bottom:1px solid #dde;
 display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
select{{font:inherit;padding:5px 8px;border:1px solid #ccd;border-radius:6px}}
.legend span{{display:inline-block;margin-right:12px;font-size:12px}}
.legend i{{display:inline-block;width:14px;height:3px;vertical-align:middle;margin-right:4px}}
main{{max-width:960px;margin:14px auto;padding:0 12px}}
figure{{margin:0 0 20px;background:#fff;box-shadow:0 1px 5px rgba(0,0,0,.12)}}
figcaption{{font-size:12px;color:#889;padding:4px 8px}}
img{{display:block;width:100%;height:auto}}</style>
<header><b>Box annotations</b>
 <select onchange="location.search='?paper='+this.value">{opts}</select>
 <label style="font-size:13px;user-select:none"><input type=checkbox id=greenonly
  onchange="apply()"> green only</label>
 <label style="font-size:12px;color:#556">buffer <input id=bufin type=number step=0.1 min=0.1
  style="width:4em;font:inherit" onchange="apply()">%</label>
 <label style="font-size:12px;color:#556">pad <input id=padin type=number step=0.1 min=0
  style="width:4em;font:inherit" onchange="apply()">%</label>
 <span class=legend><span><i style="background:#1e5adc"></i>Qwen raw</span>
 <span><i style="background:#0fa03c"></i>final</span>
 <span><i style="background:#e67800"></i>DeepSeek</span>
 <span><i style="background:#963cc8"></i>content blocks</span>
 <span><i style="background:#dc1e1e"></i>rules</span></span></header>
<main>{imgs or '<p style=padding:20px>No annotated pages — run tools/dual_annotate.py &lt;paperId&gt;.</p>'}</main>
<script>
function gurl(im){{
  const b = document.getElementById('bufin').value, p = document.getElementById('padin').value;
  return im.dataset.g + '?buf=' + (b/100) + '&pad=' + (p/100) + '&_=' + Date.now();
}}
function apply(){{
  const on = document.getElementById('greenonly').checked;
  localStorage.setItem('greenOnly', on ? '1' : '');
  localStorage.setItem('bufPct', document.getElementById('bufin').value);
  localStorage.setItem('padPct', document.getElementById('padin').value);
  for(const im of document.querySelectorAll('.pageimg'))
    im.src = on ? gurl(im) : im.dataset.a;
}}
(function(){{
  document.getElementById('greenonly').checked = localStorage.getItem('greenOnly') === '1';
  document.getElementById('bufin').value = localStorage.getItem('bufPct') || '2.0';
  document.getElementById('padin').value = localStorage.getItem('padPct') || '0.6';
  apply();
}})();
</script>"""


REVIEW_FILE = WORK / "_review.json"


def _review_load():
    try:
        return json.loads(REVIEW_FILE.read_text())
    except Exception:
        return {}


def _paper_stats(pid):
    sp = WORK / pid / "split.json"
    if not sp.exists():
        return {"mc": 0, "s2": 0}
    s = json.loads(sp.read_text())
    mc = sum(1 for u in s.get("units", []) if not vs._is_ii(u.get("section")))
    s2 = sum(1 for u in s.get("units", []) if vs._is_ii(u.get("section")))
    return {"mc": mc, "s2": s2}


@app.route("/review/mark")
def review_mark():
    pid = request.args.get("paper", "")
    page = request.args.get("page", "")
    status = request.args.get("status", "")
    key = f"{pid}#{page}" if page else pid
    d = _review_load()
    if status in ("good", "fail", "solution"):
        d[key] = {"status": status}
    elif status == "clear":
        d.pop(key, None)
    REVIEW_FILE.write_text(json.dumps(d, indent=2))
    return jsonify(ok=True, reviewed=len(d))


@app.route("/review/pagedata")
def review_pagedata():
    """Clean page image + the current boxes on it (from split.json) for the inline editor."""
    pid = request.args.get("paper", "")
    page = int(request.args.get("page", "0"))
    sp = WORK / pid / "split.json"
    split = json.loads(sp.read_text()) if sp.exists() else {"units": []}
    boxes = []
    for u in split.get("units", []):
        for r in u.get("regions", []):
            if r.get("page") == page and r.get("bbox"):
                b = r["bbox"]
                boxes.append({"id": u["id"], "x0": b[0], "y0": b[1], "x1": b[2], "y1": b[3]})
    boxes.sort(key=lambda z: z["y0"])
    return jsonify({"img": f"/page/{pid}/p{page:02d}.png", "boxes": boxes})


def _apply_page_boxes(split, page, boxes):
    """Replace the boxes on ONE page: update kept units' bbox, drop units whose box was removed,
    create a unit for any new label. Shared by savebox and revert."""
    sub = {b["id"]: b for b in boxes}
    for u in split.get("units", []):
        regs = []
        for r in u.get("regions", []):
            if r.get("page") != page:
                regs.append(r)
                continue
            if u["id"] in sub:
                b = sub[u["id"]]
                r = dict(r)
                r["bbox"] = [round(b["x0"], 4), round(b["y0"], 4),
                             round(b["x1"], 4), round(b["y1"], 4)]
                regs.append(r)
        u["regions"] = regs
    existing = {u["id"] for u in split.get("units", [])}
    for bid, b in sub.items():
        if bid in existing:
            continue
        s = bid[1:] if bid[:1].lower() == "q" else bid
        num = "".join(c for c in s if c.isdigit())
        part = "".join(c for c in s if c.isalpha()).lower() or None
        sec = "II" if (part or (num.isdigit() and int(num) >= 11)) else "I"
        split.setdefault("units", []).append({
            "id": bid, "number": num or bid, "part": part, "section": sec,
            "marks": None, "marksPrinted": False, "type": None, "ruleId": "manual",
            "confidence": 1.0, "ruleException": None, "writingSpace": [], "note": "added in review",
            "regions": [{"page": page, "bbox": [round(b["x0"], 4), round(b["y0"], 4),
                                                round(b["x1"], 4), round(b["y1"], 4)]}]})
    split["units"] = [u for u in split.get("units", []) if u.get("regions")]


@app.route("/review/savebox", methods=["POST"])
def review_savebox():
    """Persist edited/deleted boxes for one page back into split.json."""
    d = request.get_json(force=True)
    pid, page = d.get("paper", ""), int(d.get("page", 0))
    sp = WORK / pid / "split.json"
    split = json.loads(sp.read_text())
    _apply_page_boxes(split, page, d.get("boxes", []))
    split["_edited"] = True
    sp.write_text(json.dumps(split, indent=2))
    return jsonify(ok=True, units=len(split["units"]))


@app.route("/review/revert")
def review_revert():
    """Undo edits on ONE page: recompute the boxes from the cached vision responses and write
    them back. If the page can't be recomputed alone (e.g. its units were deleted), fall back to
    regenerating the WHOLE paper with vision_seg (also from cache, free)."""
    pid = request.args.get("paper", "")
    page = int(request.args.get("page", "0"))
    sp = WORK / pid / "split.json"
    if not sp.exists():
        return jsonify(ok=False, error="no split.json")
    auto = []
    try:
        auto = vs.page_boxes(pid, page)
    except Exception:
        auto = []
    if auto:
        split = json.loads(sp.read_text())
        _apply_page_boxes(split, page,
                          [{"id": l, "x0": b[0], "y0": b[1], "x1": b[2], "y1": b[3]} for l, b in auto])
        split["_edited"] = True
        sp.write_text(json.dumps(split, indent=2))
        return jsonify(ok=True, scope="page", n=len(auto))
    import subprocess                                       # fallback: rebuild the whole paper
    subprocess.run([sys.executable, str(ROOT / "tools" / "vision_seg.py"), pid],
                   capture_output=True, timeout=600)
    return jsonify(ok=True, scope="paper")


def _review_queue():
    """One entry PER QUESTION PAGE (blank/reference pages are excluded — the triage only lists
    pages that hold units). Each carries the paper's auto-issues so the reviewer knows where to
    look. Falls back to live stats if no triage file exists yet."""
    tf = WORK / "_triage.json"
    tri = json.loads(tf.read_text()) if tf.exists() else {}
    rev = _review_load()
    q = []
    for pid in sorted(tri):
        t = tri[pid]
        pages = t.get("pages") or {}
        for pg in sorted(pages, key=int):
            info = pages[pg]
            issues = list(info.get("issues", [])) + list(t.get("paperIssues", []))
            q.append({"pid": pid, "name": pid[18:], "page": int(pg),
                      "img": f"/gimg/{pid}/p{int(pg):02d}.png",
                      "units": info.get("units", []), "issues": issues,
                      "auto": "fail" if issues else "pass",
                      "verdict": rev.get(f"{pid}#{pg}", {}).get("status", "")})
    return q


@app.route("/review")
def review_view():
    """Per-PAGE review. The parser pre-sorts every page into pass / needs-attention; you A=approve
    or F=fail each page, then filter to the failed pile for a second pass. Blank pages excluded."""
    q = _review_queue()
    if not q:
        return "No triage yet — run: python3 tools/triage.py"
    return REVIEW_HTML.replace("__QUEUE__", json.dumps(q))


REVIEW_HTML = r'''<!doctype html><meta charset=utf-8><title>Page review</title>
<style>
:root{color-scheme:light dark}
*{box-sizing:border-box}
body{font:14px system-ui;margin:0;background:#e9edf2;color:#1a1d24}
header{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #dde;
 padding:8px 14px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.name{font-weight:600} .pg{color:#667}
.badge{padding:2px 9px;border-radius:20px;font-size:12px;font-weight:700;color:#fff}
.issue{background:#fdecec;color:#b02a2a;border:1px solid #f3c3c3;padding:1px 8px;border-radius:6px;font-size:12px}
.units{font-size:12px;color:#3a8a5a;font-family:ui-monospace,monospace}
.edited{font-size:12px;color:#0a63d6;font-weight:600}
.filters{display:flex;gap:6px;margin-left:auto}
.filters button{font:inherit;font-size:12px;padding:3px 10px;border:1px solid #ccd;border-radius:16px;background:#f4f6fa;cursor:pointer}
.filters button.on{background:#1a1d24;color:#fff;border-color:#1a1d24}
.keys{font-size:12px;color:#889;width:100%} .keys b{background:#eef;padding:1px 6px;border-radius:4px;color:#334}
main{max-width:860px;margin:12px auto;padding:0 10px 60px}
.done{text-align:center;padding:60px;color:#667;font-size:16px}
.wrap{position:relative;display:block;width:100%;line-height:0}
.wrap img{display:block;width:100%;height:auto;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.15);border-radius:4px;user-select:none}
#boxlayer{position:absolute;inset:0}
#wrap{scroll-margin-top:58px}
.ctx{opacity:.45;filter:saturate(.55);margin:6px 0}
.ctx img{display:block;width:100%;height:auto;border-radius:4px}
.ctxlbl{font-size:12px;color:#7a8390;padding:3px 2px;text-align:center}
.box{position:absolute;border:2px solid rgba(18,161,80,.95);background:rgba(20,180,80,.05);cursor:move}
.box.sel{border-color:#0a63d6;background:rgba(20,120,230,.10);z-index:3}
.box .lbl{position:absolute;top:-15px;left:-2px;background:#12a150;color:#fff;font:600 11px/15px system-ui;padding:0 5px;border-radius:3px 3px 0 0;white-space:nowrap}
.box.sel .lbl{background:#0a63d6}
.box .del{position:absolute;top:-11px;right:-11px;width:20px;height:20px;border-radius:50%;background:#d63636;color:#fff;font:700 13px/20px system-ui;text-align:center;cursor:pointer;display:none;z-index:5}
.box.sel .del{display:block}
.hd{position:absolute;width:12px;height:12px;background:#0a63d6;border:2px solid #fff;border-radius:2px;display:none;z-index:4;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.box.sel .hd{display:block}
.hd-nw{left:-7px;top:-7px;cursor:nwse-resize}.hd-ne{right:-7px;top:-7px;cursor:nesw-resize}
.hd-se{right:-7px;bottom:-7px;cursor:nwse-resize}.hd-sw{left:-7px;bottom:-7px;cursor:nesw-resize}
.hd-n{left:calc(50% - 6px);top:-7px;cursor:ns-resize}.hd-s{left:calc(50% - 6px);bottom:-7px;cursor:ns-resize}
.hd-e{right:-7px;top:calc(50% - 6px);cursor:ew-resize}.hd-w{left:-7px;top:calc(50% - 6px);cursor:ew-resize}
.verdict{position:fixed;inset:0;display:none;align-items:center;justify-content:center;font-size:160px;font-weight:800;pointer-events:none;z-index:9;text-shadow:0 2px 20px rgba(0,0,0,.2)}
.bar{position:fixed;left:0;bottom:0;width:100%;height:4px;background:#dfe3ea}
.bar>i{display:block;height:100%;background:#1a9e4b;transition:width .2s}
</style>
<header>
 <span class=name id=hName></span><span class=pg id=hPage></span>
 <span class=badge id=hAuto></span>
 <span class=units id=hUnits></span>
 <span class=edited id=edited></span>
 <span class=issue id=hIssue style=display:none></span>
 <span class=badge id=hVerdict style=display:none></span>
 <span class=filters id=filters></span>
 <label style="font-size:12px;color:#556;user-select:none"><input type=checkbox id=ctxToggle onchange="toggleCtx()"> context pages</label>
 <span class=keys><b>A</b> approve &nbsp;<b>F</b> fail &nbsp;<b>S</b> solution &nbsp;<b>C</b> clear &nbsp;<b>&larr;/&rarr;</b> nav &nbsp;&middot;&nbsp; drag box=move &middot; corner=resize &middot; drag empty=new box &middot; dbl-click=rename &middot; click + <b>Delete</b>=remove &middot; <b>R</b>=revert page</span>
</header>
<div class=verdict id=vd></div>
<main id=stage></main>
<div class=bar><i id=barfill></i></div>
<script>
const Q = __QUEUE__;
const verd = {};
Q.forEach(e => { if(e.verdict) verd[e.pid+'#'+e.page] = e.verdict; });
const VC = {good:'#1a9e4b', fail:'#d63636', solution:'#6b7280'};
const MODES = [['all','All'],['attention','⚠ Attention'],['todo','Unreviewed'],['failed','✕ Failed'],['solution','§ Solution']];
let i=0;                                                     // pick a NON-EMPTY default view:
let mode = Q.some(e=>!verd[e.pid+'#'+e.page]) ? 'todo'       //  unreviewed left -> keep reviewing
         : Q.some(e=>verd[e.pid+'#'+e.page]==='fail') ? 'failed'  //  else -> the failed fix-list
         : 'all';                                            //  else -> everything
const HAS = new Set(Q.map(e => e.pid+'#'+e.page));           // which (paper,page) pairs exist
let showCtx = localStorage.getItem('showCtx')==='1';         // show prev/next pages? default off
function toggleCtx(){ showCtx=document.getElementById('ctxToggle').checked;
  localStorage.setItem('showCtx', showCtx?'1':''); render(); }
function keyOf(e){ return e.pid+'#'+e.page; }
function vof(e){ return verd[keyOf(e)]; }
function list(){
  if(mode==='attention') return Q.filter(e => e.auto==='fail' && vof(e)!=='solution' && vof(e)!=='good');
  if(mode==='failed')    return Q.filter(e => vof(e)==='fail');
  if(mode==='solution')  return Q.filter(e => vof(e)==='solution');
  if(mode==='todo')      return Q.filter(e => !vof(e));
  return Q;
}
function nCount(m){
  if(m==='all') return Q.length;
  if(m==='attention') return Q.filter(e=>e.auto==='fail'&&vof(e)!=='solution'&&vof(e)!=='good').length;
  if(m==='failed') return Q.filter(e=>vof(e)==='fail').length;
  if(m==='solution') return Q.filter(e=>vof(e)==='solution').length;
  return Q.filter(e=>!vof(e)).length;
}
function renderFilters(){
  document.getElementById('filters').innerHTML = MODES.map(([m,label])=>
    '<button class="'+(m===mode?'on':'')+'" onclick="setMode(\''+m+'\')">'+label+' '+nCount(m)+'</button>').join('');
}
function setMode(m){ mode=m; i=0; render(); }
function flash(txt,col){ const v=document.getElementById('vd'); v.textContent=txt; v.style.color=col;
  v.style.display='flex'; clearTimeout(v._t); v._t=setTimeout(()=>v.style.display='none',150); }
function snapWrap(){ const w=document.getElementById('wrap'); if(w) w.scrollIntoView({block:'start'}); }

/* ---- inline box editor ---- */
let BOXES=[], sel=-1, curPid=null, curPage=null, drag=null, draw=null, saveT=null;
function pimgRect(){ const im=document.getElementById('pimg'); return im?im.getBoundingClientRect():null; }
function evNorm(ev){ const R=pimgRect(); return R?{x:(ev.clientX-R.left)/R.width, y:(ev.clientY-R.top)/R.height, R}:null; }
function parseId(id){ const m=/^q?(\d+)([a-z]?)$/i.exec(id||''); return m?{num:+m[1],letter:(m[2]||'').toLowerCase()}:null; }
function nextL(c){ return c?String.fromCharCode(c.charCodeAt(0)+1):'a'; }
function prevL(c){ return c&&c>'a'?String.fromCharCode(c.charCodeAt(0)-1):'a'; }
function autoLabel(y0){                                     // guess from the boxes above/below
  const s=BOXES.slice().sort((a,b)=>a.y0-b.y0);
  let ab=null, be=null;
  for(const b of s){ if(b.y0<y0) ab=b; else if(!be) be=b; }
  const anyLetter=s.some(b=>{const p=parseId(b.id); return p&&p.letter;});
  const A=ab&&parseId(ab.id), B=be&&parseId(be.id);
  let id;
  if(anyLetter){                                            // Section II: q<num><letter>
    if(A) id='q'+A.num+(A.letter?nextL(A.letter):'a');
    else if(B) id='q'+B.num+(B.letter?prevL(B.letter):'a');
    else id='q11a';
  } else {                                                  // MC: q<num>
    if(A) id='q'+(A.num+1);
    else if(B) id='q'+Math.max(1,B.num-1);
    else id='q1';
  }
  while(BOXES.some(b=>b.id===id)){                          // keep it unique
    const p=parseId(id); if(!p){ id+='_2'; break; }
    id = p.letter ? 'q'+p.num+nextL(p.letter) : 'q'+(p.num+1);
  }
  return id;
}
function renderBoxes(){
  const layer=document.getElementById('boxlayer'); if(!layer) return;
  let html = BOXES.map((b,idx)=>{
    const l=b.x0*100, t=b.y0*100, w=(b.x1-b.x0)*100, h=(b.y1-b.y0)*100;
    const hs=['nw','n','ne','e','se','s','sw','w'].map(p=>'<div class="hd hd-'+p+'" data-edge="'+p+'"></div>').join('');
    return '<div class="box'+(idx===sel?' sel':'')+'" data-i="'+idx+'" style="left:'+l+'%;top:'+t+'%;width:'+w+'%;height:'+h+'%">'
      +'<span class=lbl>'+b.id+'</span>'+hs+'</div>';
  }).join('');
  if(draw){                                                  // dashed preview of the box being drawn
    const l=Math.min(draw.x0,draw.x1)*100, t=Math.min(draw.y0,draw.y1)*100,
          w=Math.abs(draw.x1-draw.x0)*100, h=Math.abs(draw.y1-draw.y0)*100;
    html += '<div class=box style="left:'+l+'%;top:'+t+'%;width:'+w+'%;height:'+h+'%;border-style:dashed;border-color:#0a63d6;background:rgba(20,120,230,.08);pointer-events:none"></div>';
  }
  layer.innerHTML = html;
}
async function loadBoxes(pid,page){
  curPid=pid; curPage=page; sel=-1; BOXES=[];
  try{
    const r=await fetch('/review/pagedata?paper='+encodeURIComponent(pid)+'&page='+page);
    const d=await r.json();
    if(curPid!==pid||curPage!==page) return;              // navigated away
    BOXES=d.boxes.map(b=>({id:b.id,x0:b.x0,y0:b.y0,x1:b.x1,y1:b.y1}));
    renderBoxes();
  }catch(err){}
}
const BUF=0.006, MINH=0.012;                               // gap + minimum box height
function xOver(a,b){ return a.x0 < b.x1-0.02 && b.x0 < a.x1-0.02; }  // share a column?
function resolve(idx){                                     // push only boxes that OVERLAP this one
  const a=BOXES[idx];                                      // horizontally — side-by-side is allowed
  const col=BOXES.map((b,j)=>j).filter(j=>j!==idx && xOver(a,BOXES[j]));
  let bot=a.y1;                                            // push down the ones below (near edge
  for(const j of col.filter(j=>BOXES[j].y0>=a.y0).sort((p,q)=>BOXES[p].y0-BOXES[q].y0)){
    const b=BOXES[j], need=bot+BUF;
    if(b.y0<need){ if(need<=b.y1-MINH){ b.y0=need; } else { b.y0=need; b.y1=Math.min(1,need+MINH); } }
    bot=Math.max(bot,b.y1);
  }
  let top=a.y0;                                            // push up the ones above
  for(const j of col.filter(j=>BOXES[j].y0<a.y0).sort((p,q)=>BOXES[q].y0-BOXES[p].y0)){
    const b=BOXES[j], cap=top-BUF;
    if(b.y1>cap){ if(cap>=b.y0+MINH){ b.y1=cap; } else { b.y1=cap; b.y0=Math.max(0,cap-MINH); } }
    top=Math.min(top,b.y0);
  }
}
function applyDrag(idx,b,isMove,edge){
  const MINW=0.03;
  b.x0=Math.max(0,Math.min(b.x0,1-MINW)); b.x1=Math.min(1,Math.max(b.x1,b.x0+MINW));
  if(isMove){ const h=b.y1-b.y0; b.y0=Math.max(0,Math.min(b.y0,1-h)); b.y1=b.y0+h; }  // page only
  else{
    if(edge.indexOf('n')>=0) b.y0=Math.max(0,Math.min(b.y0,b.y1-MINH));
    if(edge.indexOf('s')>=0) b.y1=Math.min(1,Math.max(b.y1,b.y0+MINH));
  }
  BOXES[idx]=b;
  resolve(idx);                                            // then shove neighbours out of the way
}
function saveBoxes(){
  clearTimeout(saveT);
  const payload={paper:curPid,page:curPage,boxes:BOXES.map(b=>({id:b.id,x0:b.x0,y0:b.y0,x1:b.x1,y1:b.y1}))};
  saveT=setTimeout(()=>{
    fetch('/review/savebox',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const ed=document.getElementById('edited'); if(ed) ed.textContent='edited ✓';
  },350);
}
function delBox(idx){ BOXES.splice(idx,1); sel=-1; renderBoxes(); saveBoxes(); }
document.addEventListener('pointerdown', ev=>{
  const box=ev.target.closest('.box');
  if(!box){                                                  // empty space -> start drawing a new box
    if(ev.target.id==='pimg' || ev.target.id==='boxlayer'){ const n=evNorm(ev); if(n){ draw={x0:n.x,y0:n.y,x1:n.x,y1:n.y}; sel=-1; renderBoxes(); ev.preventDefault(); } }
    else if(ev.target.closest('#wrap')){ sel=-1; renderBoxes(); }
    return;
  }
  sel=+box.dataset.i;
  drag={idx:sel, edge:ev.target.dataset.edge||null, sx:ev.clientX, sy:ev.clientY, b:Object.assign({},BOXES[sel])};
  renderBoxes(); ev.preventDefault();
});
document.addEventListener('pointermove', ev=>{
  if(draw){ const n=evNorm(ev); if(n){ draw.x1=Math.max(0,Math.min(1,n.x)); draw.y1=Math.max(0,Math.min(1,n.y)); renderBoxes(); } return; }
  if(!drag) return; const R=pimgRect(); if(!R) return;
  const dx=(ev.clientX-drag.sx)/R.width, dy=(ev.clientY-drag.sy)/R.height;
  let b=Object.assign({},drag.b);
  if(!drag.edge){ const h=b.y1-b.y0, w=b.x1-b.x0; b.x0=drag.b.x0+dx; b.x1=b.x0+w; b.y0=drag.b.y0+dy; b.y1=b.y0+h; }
  else{
    if(drag.edge.indexOf('n')>=0) b.y0=drag.b.y0+dy;
    if(drag.edge.indexOf('s')>=0) b.y1=drag.b.y1+dy;
    if(drag.edge.indexOf('w')>=0) b.x0=drag.b.x0+dx;
    if(drag.edge.indexOf('e')>=0) b.x1=drag.b.x1+dx;
  }
  applyDrag(drag.idx,b,!drag.edge,drag.edge); renderBoxes();
});
document.addEventListener('pointerup', ()=>{
  if(draw){
    const x0=Math.min(draw.x0,draw.x1), x1=Math.max(draw.x0,draw.x1),
          y0=Math.min(draw.y0,draw.y1), y1=Math.max(draw.y0,draw.y1);
    draw=null;
    if(x1-x0>0.03 && y1-y0>0.012){                          // ignore tiny accidental drags
      const id=autoLabel(y0);                               // label assigned automatically
      BOXES.push({id:id,x0:x0,y0:y0,x1:x1,y1:y1});
      BOXES.sort((a,b)=>a.y0-b.y0); sel=BOXES.findIndex(z=>z.id===id); renderBoxes(); saveBoxes();
    } else renderBoxes();
    return;
  }
  if(drag){ drag=null; saveBoxes(); }
});
document.addEventListener('dblclick', ev=>{                 // double-click a box to rename it
  const box=ev.target.closest('.box'); if(!box) return;
  const idx=+box.dataset.i, cur=BOXES[idx].id;
  const nid=prompt('Rename box:', cur);
  if(nid && nid.trim() && nid.trim()!==cur){ BOXES[idx].id=nid.trim(); renderBoxes(); saveBoxes(); }
});

/* ---- review flow ---- */
function render(){
  renderFilters();
  const F=list();
  const done=Object.keys(verd).length;
  document.getElementById('barfill').style.width=(100*done/Q.length)+'%';
  const stage=document.getElementById('stage');
  const ids=['hName','hPage','hAuto','hUnits','hIssue','hVerdict','edited'];
  if(!F.length){ stage.innerHTML='<div class=done>Nothing in this filter ✓</div>';
    ids.forEach(id=>document.getElementById(id).style.display='none'); return; }
  if(i>=F.length) i=F.length-1; if(i<0) i=0;
  const e=F[i], v=vof(e)||'';
  ids.forEach(id=>document.getElementById(id).style.display='');
  document.getElementById('hName').textContent=e.name;
  document.getElementById('hPage').textContent=' · p'+e.page+'  ('+(i+1)+'/'+F.length+')';
  const ha=document.getElementById('hAuto'); ha.textContent=e.auto==='fail'?'NEEDS LOOK':'clean';
  ha.style.background=e.auto==='fail'?'#e08a1e':'#8a949f';
  document.getElementById('hUnits').textContent=e.units.join(' ');
  document.getElementById('edited').textContent='';
  const hi=document.getElementById('hIssue');
  if(e.issues.length){ hi.textContent='⚠ '+e.issues.join('  ·  '); } else hi.style.display='none';
  const hv=document.getElementById('hVerdict');
  if(v){ hv.textContent=v.toUpperCase(); hv.style.background=VC[v]; } else hv.style.display='none';
  const pnum=p=>String(p).padStart(2,'0');
  const ctx=(pg,pos)=> HAS.has(e.pid+'#'+pg)
    ? '<div class=ctxlbl>'+(pos==='previous'?'▲ ':'▼ ')+'p'+pg+' (context — scroll)</div>'
      +'<div class=ctx><img class=ctxpage src="/gimg/'+e.pid+'/p'+pnum(pg)+'.png" loading=lazy></div>'
    : '';
  const cur='<div class=wrap id=wrap><img id=pimg src="/page/'+e.pid+'/p'+pnum(e.page)+'.png" draggable=false onload="snapWrap()"><div id=boxlayer></div></div>';
  stage.innerHTML = (showCtx?ctx(e.page-1,'previous'):'') + cur + (showCtx?ctx(e.page+1,'next'):'');
  loadBoxes(e.pid,e.page);
  requestAnimationFrame(snapWrap); snapWrap();               // snap now + again once the image lays out
  for(const j of [i+1,i+2,i-1]){ if(F[j]){ const im=new Image(); im.src='/page/'+F[j].pid+'/p'+pnum(F[j].page)+'.png'; } }
}
function advance(){ if(mode==='all') i++; render(); }   // filtered modes: item drops out, keep i
function mark(status){
  const F=list(); if(!F.length) return;
  const e=F[i], k=keyOf(e);
  if(status==='clear') delete verd[k]; else verd[k]=status;
  fetch('/review/mark?paper='+encodeURIComponent(e.pid)+'&page='+e.page+'&status='+status);
  const f={good:['✓','#1a9e4b'],fail:['✕','#d63636'],solution:['§','#6b7280']}[status];
  if(f) flash(f[0],f[1]);
  advance();
}
async function revertPage(){
  const F=list(); if(!F.length) return; const e=F[i];
  if(!confirm('Revert this page to the original auto-detected boxes? Your edits on this page are discarded.')) return;
  flash('↺','#0a63d6');
  const r=await (await fetch('/review/revert?paper='+encodeURIComponent(e.pid)+'&page='+e.page)).json();
  loadBoxes(e.pid, e.page);
  document.getElementById('edited').textContent = r.scope==='paper' ? 'reverted (whole paper)' : 'reverted ✓';
}
addEventListener('keydown', ev=>{
  if(ev.key==='Delete'||ev.key==='Backspace'){ if(sel>=0){ delBox(sel); ev.preventDefault(); } return; }
  const k=ev.key.toLowerCase();
  if(k==='a'){ ev.preventDefault(); mark('good'); }
  else if(k==='f'){ mark('fail'); }
  else if(k==='s'){ mark('solution'); }
  else if(k==='c'){ mark('clear'); }
  else if(k==='r'){ revertPage(); }
  else if(ev.key==='ArrowRight'||k==='j'){ browse(1); }
  else if(ev.key==='ArrowLeft'||k==='k'){ browse(-1); }
});
function browse(dir){                                        // arrows browse EVERY page (so you can
  if(mode!=='all'){                                          // always go back to fix a mis-marked one)
    const F=list(), cur=F.length?F[i]:null;
    mode='all';
    i = cur ? Math.max(0, Q.findIndex(e=>e.pid===cur.pid && e.page===cur.page)) : 0;
  }
  i += dir; render();
}
document.getElementById('ctxToggle').checked = showCtx;
render();
</script>'''


@app.route("/eval")
def eval_view():
    p = ROOT / "tools" / "eval_view.html"
    if not p.exists():
        return "eval view not generated yet", 404
    return p.read_text()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5090)
    args = ap.parse_args()
    app.run(host="127.0.0.1", port=args.port, debug=False)
