#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Minimal OpenRouter client for the HSC solution pipeline.

Two stages, two models (both via OpenRouter's one OpenAI-compatible endpoint):
  - VISION   read a question image -> clean text        (default qwen/qwen3-vl-235b-a22b-instruct)
  - REASONING generate a worked solution from text      (default deepseek/deepseek-v4-pro)

Key is read from $OPENROUTER_API_KEY or ~/.config/hsc/openrouter.key (never printed).

    python3 tools/or_client.py --smoke                 # cheap end-to-end sanity check
    python3 tools/or_client.py --text  MODEL "prompt"
    python3 tools/or_client.py --image MODEL img.png "prompt"
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
KEY_FILE = Path.home() / ".config" / "hsc" / "openrouter.key"
VISION_MODEL = "qwen/qwen3-vl-235b-a22b-instruct"
REASON_MODEL = "deepseek/deepseek-v4-flash"


def load_key():
    k = os.environ.get("OPENROUTER_API_KEY")
    if not k and KEY_FILE.exists():
        k = KEY_FILE.read_text().strip()
    if not k:
        sys.exit("no OpenRouter key ($OPENROUTER_API_KEY or ~/.config/hsc/openrouter.key)")
    return k


def _data_uri(path):
    b = Path(path).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode()


def chat(model, messages, max_tokens=4000, temperature=0.2, timeout=180,
         reasoning=None, response_format=None):
    """One chat completion. Returns (text, usage_dict). Raises on HTTP/JSON error.
    max_tokens caps TOTAL completion (reasoning + content) on thinking models, so pass
    `reasoning={"max_tokens": N}` (or {"effort":"low"}) to leave room for the answer, and
    `response_format={"type":"json_object"}` to force valid JSON."""
    payload = {"model": model, "messages": messages,
               "max_tokens": max_tokens, "temperature": temperature}
    if reasoning is not None:
        payload["reasoning"] = reasoning
    if response_format is not None:
        payload["response_format"] = response_format
    body = json.dumps(payload).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Authorization": "Bearer " + load_key(),
        "Content-Type": "application/json",
        "HTTP-Referer": "https://papers.hsc.pebnum.com",
        "X-Title": "HSC solution pipeline",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    if "choices" not in d:
        raise RuntimeError("OpenRouter error: " + json.dumps(d)[:400])
    return d["choices"][0]["message"]["content"], d.get("usage", {})


def ask_text(model, prompt, **kw):
    return chat(model, [{"role": "user", "content": prompt}], **kw)


def ask_image(model, image_path, prompt, **kw):
    content = [{"type": "text", "text": prompt},
               {"type": "image_url", "image_url": {"url": _data_uri(image_path)}}]
    return chat(model, [{"role": "user", "content": content}], **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--text", nargs=2, metavar=("MODEL", "PROMPT"))
    ap.add_argument("--image", nargs=3, metavar=("MODEL", "IMG", "PROMPT"))
    a = ap.parse_args()
    if a.smoke:
        print(f"[reasoning] {REASON_MODEL}")
        t, u = ask_text(REASON_MODEL, "In one line, integrate 5/(2+x^2) dx. Reply with just the result.",
                        max_tokens=800)
        print("  ->", (t or "").strip()[:200], "| cost $%.5f" % u.get("cost", 0))
    elif a.text:
        t, u = ask_text(a.text[0], a.text[1])
        print(t, "\n--- usage:", u)
    elif a.image:
        t, u = ask_image(a.image[0], a.image[1], a.image[2])
        print(t, "\n--- usage:", u)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
