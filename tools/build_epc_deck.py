#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Build the Software Engineering *Episode Content* deck (EPC-*).

Reads four staging JSON files (arrays of {q, keyPoints, explanation?} authored by
distilling each topic's episode scripts) and writes card-only "episodes" under
content/software/EPC-* — one per SENG topic. Each becomes a quiz.json of
type:"recall" cards plus a stub script.md so generate_manifest.py picks it up.

Staging files live in a scratch dir passed as argv[1] (default: alongside this
note). Re-run to overwrite. Then run tools/generate_manifest.py.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SW = ROOT / "content" / "software"
STAGE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tools" / "_epc_staging"

# folder -> (title, staging filename, id slug)
TOPICS = [
    ("EPC-01-Secure-Software-Architecture", "Secure Software Architecture", "epc_ssa.json", "ssa"),
    ("EPC-02-Programming-For-The-Web",      "Programming for the Web",      "epc_pfw.json", "pfw"),
    ("EPC-03-Software-Automation",          "Software Automation",          "epc_sa.json",  "sa"),
    ("EPC-04-Software-Engineering-Project", "Software Engineering Project", "epc_see.json", "see"),
]

STUB = ("---\ntitle: \"{title} — Episode Content\"\n---\n\n# {title} — Episode Content\n\n"
        "Concept-recall flashcards drawn from the **{title}** episodes — the ideas, "
        "definitions and comparisons taught in the audio. No audio here; open the "
        "**Quiz** tab to drill the cards.\n")


def build(folder_name, title, stage_file, slug):
    raw = json.loads((STAGE / stage_file).read_text(encoding="utf-8"))
    cards = []
    for i, c in enumerate(raw, 1):
        card = {
            "id": f"{slug}-content-{i:02d}",
            "type": "recall",
            "q": c["q"],
            "keyPoints": c["keyPoints"],
        }
        if c.get("explanation"):
            card["explanation"] = c["explanation"]
        card["source"] = {"origin": "ai", "ref": f"Generated from {title} episode scripts"}
        cards.append(card)
    folder = SW / folder_name
    folder.mkdir(exist_ok=True)
    (folder / "quiz.json").write_text(
        json.dumps({"questions": cards}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "script.md").write_text(STUB.format(title=title), encoding="utf-8")
    return len(cards)


def main():
    total = 0
    for folder_name, title, stage_file, slug in TOPICS:
        n = build(folder_name, title, stage_file, slug)
        print(f"  {folder_name}: {n} cards")
        total += n
    print(f"Wrote {total} content cards across {len(TOPICS)} EPC episodes.")


if __name__ == "__main__":
    main()
