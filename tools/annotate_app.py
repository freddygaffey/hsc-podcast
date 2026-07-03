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
from pathlib import Path

from flask import Flask, jsonify, request, send_file

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

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
    return jsonify({"pages": [p["image"] for p in info["pages"]], "annotations": ann})


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
 .keys b{border:1px solid #ccd;border-radius:4px;padding:0 5px;background:#fff}
</style>
<header>
 <select id=paper></select>
 <select id=kind>
  <option value="question">question box</option>
  <option value="lines">lines box</option>
 </select>
 <label>Q <input class=small id=qn value="1"></label>
 <label>part <input class=small id=part placeholder="a"></label>
 <label>marks <input class=small id=marks placeholder="?"></label>
 <label><input type=checkbox id=autoq checked> next Q after box</label>
 <span id=count></span><span id=status></span>
 <span class=keys style="margin-left:auto">drag = new box · drag a box = move · corner = resize · <b>l</b> lines mode · <b>⌫</b> delete</span>
</header>
<main id=pages></main>
<script>
const $=s=>document.querySelector(s);
let PID=null, BOXES=[], sel=-1, saveT=null;
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
 BOXES=r.annotations.boxes||[];
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
 document.querySelectorAll(".box,.ghost").forEach(e=>e.remove());
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
loadPapers();
</script>"""


@app.route("/")
def home():
    return PAGE


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5090)
    args = ap.parse_args()
    app.run(port=args.port, debug=False)
