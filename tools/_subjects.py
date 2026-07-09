#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Shared subject-config helpers for the paper pipeline.

Each subject that goes through the crop pipeline carries a committed config at
content/<slug>/syllabus.json holding what makes its papers different: the closed
vocabulary of syllabus outcome codes (for syllabusRefs), the question-type taxonomy,
module/topic lists and exam section structure. Tools degrade gracefully when the
file is missing (tagging refuses to run, review UI shows no dropdowns).

The papers/ source tree slugs subjects from folder names ("Design & Technology" →
"design-technology") but committed content lives under short slugs (content/dt/).
SUBJECT_ALIASES maps tree slugs → content slugs; apply with content_slug().
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# papers/-tree slug -> content/ directory slug
SUBJECT_ALIASES = {
    "design-technology": "dt",
    "design-and-technology": "dt",
}


def content_slug(subject):
    """Resolve a subject slug (as stamped by the pipeline) to its content/ dir slug."""
    return SUBJECT_ALIASES.get(subject, subject)


def load_syllabus(subject):
    """Load content/<subject>/syllabus.json (alias-aware). Returns dict or None."""
    p = CONTENT / content_slug(subject) / "syllabus.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def outcome_codes(syllabus):
    """The closed vocabulary of syllabusRefs codes for a loaded syllabus config.

    Two shapes exist: the pipeline shape (top-level outcomes[].code) and the older
    classifier shape used by maths-standard-2 (modules[].code + modules[].topics[].code).
    Harvest codes from both so either validates the corpus.
    """
    if not syllabus:
        return []
    codes = [o["code"] for o in syllabus.get("outcomes", []) if isinstance(o, dict) and o.get("code")]
    for m in syllabus.get("modules", []):
        if isinstance(m, dict):
            if m.get("code"):
                codes.append(m["code"])
            for t in m.get("topics", []):
                if isinstance(t, dict) and t.get("code"):
                    codes.append(t["code"])
    return codes


def code_maps(syllabus):
    """(code -> topic name, code -> module name) for topic/module normalisation.

    Topics must be a CLOSED vocabulary (10-15 per subject, ~textbook chapters), not
    free text — the primary syllabusRefs code determines the topic/module label.
    Works for both config shapes; entries without the info map to None."""
    topics, modules = {}, {}
    if not syllabus:
        return topics, modules
    for o in syllabus.get("outcomes", []):
        if isinstance(o, dict) and o.get("code"):
            topics[o["code"]] = o.get("topic")
            modules[o["code"]] = o.get("module")
    for m in syllabus.get("modules", []):
        if isinstance(m, dict):
            mname = m.get("module")
            if m.get("code"):
                topics.setdefault(m["code"], mname)
                modules[m["code"]] = mname
            for t in m.get("topics", []):
                if isinstance(t, dict) and t.get("code"):
                    topics[t["code"]] = t.get("topic")
                    modules[t["code"]] = mname
    return topics, modules
