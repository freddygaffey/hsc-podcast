# Infra scripts (archived at wind-down, 2026-07-09)

Scripts that lived outside the repo, archived here so the repo is the complete record.

- `hsc-resume.sh` — lived at `~/hsc-resume.sh`. Restarts the whole paper-pulling
  pipeline: the three downloaders on the server (`root@api.plane.pebnums.com:/root/hsc-papers`),
  the textbook grabber, and the two local sync loops below.
- `hsc-sync.sh` — lived at `~/.hsc-sync.sh`. Loop: rsync server papers → local `papers/`
  every 5 min.
- `hsc-textbook-sync.sh` — lived at `~/.hsc-textbook-sync.sh`. Loop: rsync server
  textbooks → `~/hsc-textbooks` every 3 min.
- `grab_textbooks.py` — lived at `root@api.plane.pebnums.com:/root/_grab.py`. Google
  Drive textbook grabber.

The downloader scripts themselves (`_downloader.py` THSC, `_nesa.py` NESA,
`_acehsc.py` acehsc) are in `papers/`.
