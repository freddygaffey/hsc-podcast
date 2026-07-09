#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Render a structured solution -> PNG via KaTeX (real LaTeX) in headless Chrome.

Robust replacement for the matplotlib renderer: DeepSeek emits ordinary FULL LaTeX,
KaTeX (bundled offline at tools/katex) renders it in the browser, headless Chrome
screenshots the page, PIL trims to content. No mathtext subset, no hand-written
sanitizers, no fragile fallbacks — the browser is the LaTeX engine.

    python3 tools/render_solution_html.py <solution.json> -o out.png
"""
import argparse
import html as _html
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageChops


def _wrap_math(s):
    """Safety net: if the model emitted a bare LaTeX line without $...$, wrap it so KaTeX
    still renders it (instead of showing raw \\frac{...} source)."""
    if s and "$" not in s and ("\\" in s or re.search(r"[\^_]", s)):
        return "$" + s + "$"
    return s

HERE = Path(__file__).resolve().parent
KATEX = HERE / "katex"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
 *{box-sizing:border-box}
 body{margin:0;background:#fff;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;color:#1c1e24}
 .card{position:relative;width:780px;padding:26px 30px 30px;overflow:hidden}
 .hdr{display:flex;align-items:baseline;justify-content:space-between;
   border-bottom:1px solid #e6e8ee;padding-bottom:8px;margin-bottom:4px}
 .qn{font-size:21px;font-weight:700}
 .kind{font-size:12px;color:#8a93a3;letter-spacing:.02em}
 .note{color:#b45309;font-style:italic;font-size:13px;margin:8px 0 4px}
 .part{margin:18px 0 0}
 .plabel{display:flex;align-items:baseline;justify-content:space-between;
   font-weight:700;font-size:15px;margin-bottom:6px}
 .marks{font-weight:500;font-size:12px;color:#6b7482}
 .step{margin:5px 0 5px 6px}
 .answer{display:inline-block;margin:9px 0 2px 6px;padding:6px 12px;
   border:1.4px solid #3b4cc0;background:#eef0fb;border-radius:8px;color:#2733a8}
 .katex{font-size:1.02em}
 .wm{position:absolute;top:46%;left:50%;transform:translate(-50%,-50%) rotate(-18deg);
   font-size:44px;font-weight:800;color:#b45309;opacity:.11;white-space:nowrap;
   pointer-events:none;letter-spacing:.04em}
"""


def esc(s):
    return _html.escape(s or "", quote=False)


def build_html(sol):
    num = esc(str(sol.get("number", "?")))
    sec = sol.get("section", "")
    blocks = []
    for p in sol.get("parts", []):
        lab = esc(p.get("label") or "")
        mk = p.get("marks")
        marks = f'<span class="marks">{mk} mark{"" if mk == 1 else "s"}</span>' if mk is not None else ""
        head = f'<div class="plabel"><span>{lab}</span>{marks}</div>' if lab else ""
        steps = "".join(f'<div class="step">{esc(_wrap_math(s))}</div>' for s in p.get("steps", []))
        ans = f'<div class="answer">{esc(_wrap_math(p.get("answer")))}</div>' if p.get("answer") else ""
        blocks.append(f'<div class="part">{head}{steps}{ans}</div>')
    note = f'<div class="note">{esc(sol.get("answerNote"))}</div>' if sol.get("answerNote") else ""
    wm = '<div class="wm">AI-GENERATED SOLUTION</div>' if sol.get("aiGenerated") else ""
    kind = "Multiple choice" if sec == "I" else "Worked solution"
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{KATEX}/katex.min.css">
<style>{CSS}</style></head><body>
<div class="card">{wm}
 <div class="hdr"><span class="qn">Question {num}</span><span class="kind">{kind}</span></div>
 {note}{''.join(blocks)}
</div>
<script src="file://{KATEX}/katex.min.js"></script>
<script src="file://{KATEX}/contrib/auto-render.min.js"></script>
<script>
renderMathInElement(document.body,{{delimiters:[
 {{left:'$',right:'$',display:false}},
 {{left:'\\\\(',right:'\\\\)',display:false}},
 {{left:'\\\\[',right:'\\\\]',display:true}}],throwOnError:false}});
</script></body></html>"""


def render_png(sol, out_png, scale=2):
    with tempfile.TemporaryDirectory() as td:
        hp = Path(td) / "s.html"
        hp.write_text(build_html(sol))
        shot = Path(td) / "shot.png"
        # Chrome headless writes the screenshot quickly but often doesn't exit (its updater/
        # crash-handler child lingers), so run async, poll for the PNG, then kill it.
        proc = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
             "--no-default-browser-check", "--hide-scrollbars",
             "--disable-background-networking", "--disable-component-update",
             "--disable-default-apps", "--disable-sync", "--disable-extensions",
             "--metrics-recording-only", "--mute-audio",
             f"--user-data-dir={td}/ud", f"--force-device-scale-factor={scale}",
             "--default-background-color=FFFFFFFF",
             "--window-size=820,3600", f"--screenshot={shot}", f"file://{hp}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.time() + 40
        while time.time() < deadline:
            if shot.exists() and shot.stat().st_size > 0:
                time.sleep(0.4)                       # let the write finish
                break
            if proc.poll() is not None:
                break
            time.sleep(0.2)
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        if not (shot.exists() and shot.stat().st_size > 0):
            raise RuntimeError("Chrome produced no screenshot")
        img = Image.open(shot).convert("RGB")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bbox = ImageChops.difference(img, bg).getbbox()      # trim to content
        if bbox:
            pad = 12 * scale
            img = img.crop((0, 0, img.width, min(img.height, bbox[3] + pad)))
        img.save(out_png)
    return out_png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("solution")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    render_png(json.loads(Path(a.solution).read_text()), a.out)
    print(f"rendered -> {a.out}")


if __name__ == "__main__":
    main()
