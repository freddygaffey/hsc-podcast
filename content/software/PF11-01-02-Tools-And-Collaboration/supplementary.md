---
title: "Supplementary Materials — Tools and Collaboration"
module: PF11
year: 11
lesson: "1.2"
script: script.md
---

# Supplementary Materials

Read-along reference for this episode. Nothing here is spoken — the narration points at
each listing by label. These are Git and shell commands; run them in a terminal opened at
your project folder.

### Listing 1 — Set up the Grade Calculator repo with two focused commits
```bash
# Create the project folder and start version control.
mkdir grade-calculator
cd grade-calculator
git init

# Snapshot 1: documentation only.
echo "# Grade Calculator" > README.md
echo "Averages three test scores. Run with: python main.py" >> README.md
git add README.md
git commit -m "Initial project setup"

# Snapshot 2: the actual feature, committed separately.
# (main.py holds the validate_grade / calculate_average functions from lesson 1.1.)
git add main.py
git commit -m "Add grade calculation function"

# Read the history back: two small, focused commits.
git log --oneline
# e.g.
#   a1b2c3d Add grade calculation function
#   f4e5d6c Initial project setup
```

### Listing 2 — A minimal `.gitignore` for a Python project
```gitignore
# Python bytecode / compiled cache — generated noise, never track it.
__pycache__/
*.pyc

# Virtual environment folders.
.venv/
venv/

# Secrets — credentials must NEVER enter version control.
.env

# Editor / OS clutter.
.vscode/
.idea/
.DS_Store
```

### Listing 3 — The trap: stop tracking a file you already committed
```bash
# Problem: .env was committed BEFORE it was added to .gitignore,
# so Git keeps tracking it — the ignore rule alone does nothing.

# Fix: remove it from Git's tracking but KEEP it on disk (--cached),
# then commit the removal. Now the .gitignore rule takes effect.
git rm --cached .env
git commit -m "Stop tracking .env (now ignored)"

# Verify the rule now applies and names the matching pattern.
git check-ignore -v .env
# .gitignore:10:.env    .env
```
