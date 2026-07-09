#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Build the Software Engineering *Memorisation* deck.

Emits card-only "episodes" under content/software/MEM-* — each a quiz.json of
type:"recall" flashcards (front question -> revealed key points) plus a short
stub script.md so tools/generate_manifest.py picks the folder up.

Two sources, both already in the repo:
  1. Hand-authored syllabus-list cards (SYLLABUS below), taken from the NESA
     Software Engineering syllabus dot points (the "memorisation" doc), one card
     per list, with the course mnemonic as a recall hook.
  2. The acronym table in content/software/GLOSSARY.md, parsed straight into
     "What does X stand for, and what is it?" cards.

Re-run any time; it overwrites the MEM-* quiz.json/script.md in place. Then run
tools/generate_manifest.py to fold the new episodes into manifest.json.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SW = ROOT / "content" / "software"
GLOSSARY = SW / "GLOSSARY.md"
SOURCE = {"origin": "syllabus", "ref": "NESA Software Engineering 11–12 syllabus"}

# --- 1. Hand-authored syllabus-list cards -----------------------------------
# Each entry: (front question, [key points...], mnemonic-hook or "").
SYLLABUS = {
    "MEM-01-Secure-Software-Architecture": ("Secure Software Architecture", [
        ("Name the two benefits of developing secure software.",
         ["Data protection", "Minimising cyber attacks and vulnerabilities"], ""),
        ("List the eight fundamental software development steps, in order.",
         ["Requirements definition", "Determining specifications", "Design", "Development",
          "Integration", "Testing and debugging", "Installation", "Maintenance"],
         "Hook: R-S-D-D-I-T-I-M."),
        ("Name the six fundamental software security concepts.",
         ["Confidentiality", "Integrity", "Availability", "Authentication", "Authorisation",
          "Accountability"], "Hook: the CIA triad + AAA (C-I-A-A-A-A)."),
        ("What four security features are incorporated into software?",
         ["Data protection", "Security", "Privacy", "Regulatory compliance"], ""),
        ("State the three 'privacy by design' principles.",
         ["Proactive, not reactive", "Embed privacy into the design", "Respect for user privacy"],
         "Hook: PER — Proactive, Embed, Respect."),
        ("List the five activities that test and maintain a system's security and resilience.",
         ["Determine vulnerabilities", "Harden systems", "Handle breaches",
          "Maintain business continuity", "Conduct disaster recovery"], ""),
        ("Name the five strategies developers use to manage the security of code.",
         ["Code review", "Static application security testing (SAST)",
          "Dynamic application security testing (DAST)", "Vulnerability assessment",
          "Penetration testing"], ""),
        ("State the three defensive data-input handling practices.",
         ["Input validation", "Input sanitisation", "Error handling"],
         "Hook: VSE — Validate, Sanitise, handle Errors."),
        ("Name the three resource-management concerns for efficient, secure execution.",
         ["Memory management", "Session management", "Exception management"],
         "Hook: M-S-E."),
        ("List the four categories of vulnerability in user action controls.",
         ["Broken authentication and session management",
          "Cross-site scripting (XSS) and cross-site request forgery (CSRF)",
          "Invalid forwarding and redirecting", "Race conditions"],
         "Hook: B-X-I-R."),
        ("What two user file and hardware vulnerabilities must secure code protect against?",
         ["File attacks", "Side channel attacks"], ""),
        ("Give the three benefits of collaborating to build secure software.",
         ["Considering various points of view", "Delegating tasks based on expertise",
          "Quality of the solution"], "Hook: V-D-Q."),
        ("List the five benefits to an enterprise of safe and secure development practices.",
         ["Improved products or services", "Influence on future software development",
          "Improved work practices", "Productivity", "Business interactivity"],
         "Hook: PIP-PB."),
        ("Name the six social, ethical and legal issues raised by software.",
         ["Employment", "Data security", "Privacy", "Copyright", "Intellectual property",
          "Digital disruption"], "Hook: 'Ed Picid' — E-D-P-C-I-D."),
    ]),
    "MEM-02-Programming-For-The-Web": ("Programming for the Web", [
        ("Name the three applications of web programming.",
         ["Interactive websites / webpages", "E-commerce", "Progressive web apps (PWAs)"],
         "Hook: I-E-P."),
        ("How is data transferred on the internet? (three things)",
         ["Data packets", "Internet Protocol (IP) addresses, including IPv4",
          "Domain Name System (DNS)"], ""),
        ("List the web protocols (grouped) you must know.",
         ["HTTP, HTTPS", "TCP/IP", "DNS", "FTP, SFTP", "SSL, TLS", "SMTP, POP3, IMAP"], ""),
        ("Name the seven processes/elements for securing the web.",
         ["SSL certificates", "Encryption algorithms", "Encryption keys",
          "Plain text and cipher text", "Authentication and authorisation", "Hash values",
          "Digital signatures"], ""),
        ("What three big-data concepts affect web architecture?",
         ["Data mining", "Metadata", "Streaming service management"], "Hook: M-M-S."),
        ("List the five roles of the W3C in web development.",
         ["Web Accessibility Initiative (WAI)", "Internationalisation", "Web security",
          "Privacy", "Machine-readable data"], ""),
        ("Name the three elements that form a web development system.",
         ["Client-side (front-end) programming", "Server-side (back-end) programming",
          "Interfacing with SQL or non-SQL databases"], ""),
        ("State the three impacts of CSS on web application design.",
         ["Consistency of appearance", "Flexibility across browsers / display devices",
          "CSS maintenance tools"], ""),
        ("What three types of code library support front-end development?",
         ["Frameworks (control complex web apps)", "Template engines",
          "Predesigned CSS classes"], "Hook: F-T-C."),
        ("List the five parts of the back-end process that manages a web request.",
         ["Webserver software", "Web framework", "Objects", "Libraries", "Databases"], ""),
        ("Name the SQL query building blocks you must be able to script.",
         ["Selecting fields", "GROUP BY", "Common queries", "Constraints using WHERE",
          "Table joins"], ""),
        ("What must a PWA consider in its design?",
         ["UI/UX principles of font, colour, audio, video and navigation",
          "A UI that considers accessibility and inclusivity"], ""),
    ]),
    "MEM-03-Software-Automation": ("Software Automation", [
        ("How does machine learning support automation? (three ways)",
         ["DevOps", "Robotic process automation (RPA)", "Business process automation (BPA)"], ""),
        ("Name the four models of training machine learning.",
         ["Supervised learning", "Unsupervised learning", "Semi-supervised learning",
          "Reinforcement learning"], "Hook: S-U-S-R."),
        ("List three common applications of key ML algorithms.",
         ["Data analysis and forecasting", "Virtual personal assistants", "Image recognition"],
         "Hook: F-A-I — Forecasting, Assistants, Image recognition."),
        ("What two models do engineers use to design and analyse ML?",
         ["Decision trees", "Neural networks"], ""),
        ("Name the three types of algorithm associated with ML.",
         ["Linear regression", "Logistic regression", "K-nearest neighbour"], "Hook: L-L-K."),
        ("List the three regression models built with an OOP approach.",
         ["Linear regression", "Polynomial regression", "Logistic regression"], ""),
        ("Name the five areas where automation's impact is assessed.",
         ["Safety of workers", "People with disability",
          "The nature and skills required for employment",
          "Production efficiency, waste and the environment",
          "The economy and distribution of wealth"], "Hook: S-P-E-E."),
        ("What four human-behaviour patterns influence ML and AI development?",
         ["Psychological responses", "Patterns related to acute stress response",
          "Cultural protocols", "Belief systems"], "Hook: P-S-C-B."),
        ("What two sources of bias affect ML/AI solutions?",
         ["Human source bias", "Dataset source bias"], ""),
    ]),
    "MEM-04-Software-Engineering-Project": ("Software Engineering Project", [
        ("What five things define and analyse the requirements of a problem?",
         ["Demonstrate needs or opportunities", "Assess scheduling and financial feasibility",
          "Generate requirements (functionality and performance)",
          "Define data structures and data types", "Define boundaries"], ""),
        ("Name the tools used to develop ideas and generate solutions.",
         ["Brainstorming, mind-mapping, storyboards", "Data dictionaries", "Algorithm design",
          "Code generation", "Testing and debugging", "Installation", "Maintenance"], ""),
        ("List the four software implementation (changeover) methods.",
         ["Direct", "Phased", "Parallel", "Pilot"], "Hook: DiP-PP."),
        ("What are the key aspects of the Waterfall approach?",
         ["Logical progression of life-cycle steps", "The 'falling water' stages",
          "Advantages and disadvantages", "Scale and types of development"], ""),
        ("What are the key aspects of the Agile approach?",
         ["Rate of developing a final solution", "Method tailoring", "Iteration workflow",
          "Scale and types of development"], ""),
        ("What are the key aspects of the WAgile approach?",
         ["It is a hybrid model", "Analysis of when and how intervention is applied in the life cycle",
          "Scale and types of development"], ""),
        ("What project-management tools plan and track a project?",
         ["Scheduling and tracking with a software tool, including Gantt charts",
          "Collaboration tools"], ""),
        ("Name the three communication issues in project work.",
         ["Involving and empowering the client", "Enabling feedback", "Negotiating"],
         "Hook: I-F-N."),
        ("How is a software engineering solution quality assured? (three things)",
         ["Define the criteria on which quality is judged",
          "Ensure requirements are met with continual checking",
          "Address compliance and legislative requirements"], ""),
        ("List the four contributions of back-end engineering.",
         ["Technology used", "Error handling", "Interfacing with the front end",
          "Security engineering"], "Hook: T-E-I-S."),
        ("Name the three strategies for responding to development difficulties.",
         ["Looking for a solution online", "Collaboration with peers", "Outsourcing"],
         "Hook: S-P-O — Self-search, Peers, Outsource."),
        ("How do you evaluate the effectiveness of a solution?",
         ["Develop a report to synthesise feedback", "Develop a test plan",
          "Test data based on path and boundary testing", "Compare actual vs expected output"], ""),
    ]),
}


def parse_acronyms():
    """Rows of the '## Acronyms & abbreviations' table -> {term: [meanings...]}."""
    text = GLOSSARY.read_text(encoding="utf-8")
    section = text.split("## Acronyms & abbreviations", 1)[1]
    rows = {}
    order = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("Term", "") or set(cells[0]) <= set("-: "):
            continue
        term, expansion, meaning = cells[0], cells[1], cells[2]
        if term not in rows:
            rows[term] = []
            order.append(term)
        rows[term].append((expansion, meaning))
    return [(t, rows[t]) for t in order]


def acronym_cards():
    cards = []
    for i, (term, meanings) in enumerate(parse_acronyms(), 1):
        clean = term.replace("*", "")
        if len(meanings) == 1:
            exp, mean = meanings[0]
            front = f"What does **{clean}** stand for, and what is it?"
            key = [exp, mean]
        else:
            front = f"What does **{clean}** stand for? (it has {len(meanings)} meanings in this course)"
            key = [f"{exp} — {mean}" for exp, mean in meanings]
        cards.append({
            "id": f"mem-acr-{i:03d}", "type": "recall", "q": front,
            "keyPoints": key, "source": SOURCE,
        })
    return cards


def recall_card(cid, front, key_points, hook):
    card = {"id": cid, "type": "recall", "q": front, "keyPoints": key_points, "source": SOURCE}
    if hook:
        card["explanation"] = hook
    return card


STUB = ("---\ntitle: \"{title} — Memorisation Deck\"\n---\n\n# {title} — Memorisation Deck\n\n"
        "A rote-recall flashcard set for the **{title}** syllabus dot points. "
        "There's no audio here — open the **Quiz** tab and drill the cards.\n")


def write_episode(folder_name, title, cards):
    folder = SW / folder_name
    folder.mkdir(exist_ok=True)
    (folder / "quiz.json").write_text(
        json.dumps({"questions": cards}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "script.md").write_text(STUB.format(title=title), encoding="utf-8")
    return len(cards)


def main():
    total = 0
    slug = {"MEM-01": "ssa", "MEM-02": "pfw", "MEM-03": "sa", "MEM-04": "see"}
    for folder_name, (title, lists) in SYLLABUS.items():
        pfx = slug[folder_name[:6]]
        cards = [recall_card(f"mem-{pfx}-{i:02d}", front, kp, hook)
                 for i, (front, kp, hook) in enumerate(lists, 1)]
        total += write_episode(folder_name, title, cards)

    # All acronyms in one set, alphabetical (the confirmed layout has a single
    # "Acronyms & Abbreviations" item under Memorisation).
    total += write_episode("MEM-05-Acronyms-And-Abbreviations",
                           "Acronyms & Abbreviations", acronym_cards())

    print(f"Wrote {total} cards across {len(SYLLABUS) + 1} MEM episodes.")


if __name__ == "__main__":
    main()
