# AGENTS.md

Read `CLAUDE.md` and `docs/handoff.md` first — they are the source of truth for
this repo's constraints, design rules, and copy rules. This file only adds
environment/run notes for automated agents.

## Cursor Cloud specific instructions

This is a static **Astro** site. Standard commands live in `README.md` (§Commands)
and `package.json` (`dev`, `build`, `preview`, `verify`). Notes below are only the
non-obvious things.

- **Two toolchains.** Node (npm) builds/serves the site; a Python `.venv` with
  Playwright + Chromium runs the two verify suites (`scripts/verify.py`,
  `scripts/verify_site.py`). The startup update script keeps both installed, so
  you should not need to reinstall anything.
- **`npm run verify` runs against `dist/`, not the source.** Always
  `npm run build` first, or verify will test a stale/absent build. The suites
  print `ALL CHECKS PASSED` / `SITE RESULT: ALL CHECKS PASSED` on success.
- **`npm run verify` does not need `source .venv/bin/activate`.** `package.json`
  calls `./.venv/bin/python3` directly. You only need to activate the venv when
  running a Python script yourself (e.g. `build_assets.py`).
- **Dev server:** `npm run dev` → http://localhost:4321/ (live reload). This is
  what to run and browse to exercise the site (home, `/builds/`, `/builds/<id>/`,
  `/writing/`, `/writing/<id>/`; the only interactive JS is the rotating
  "What I'm watching" video link on the home page).
- **`build_assets.py` (image regeneration) is optional and needs Pillow**, which
  the update script does not install (`./.venv/bin/pip install Pillow`). It also
  needs `headshot.jpg` / `headshot-favicon.jpg`, which are not always in the repo.
  You almost never need this for code work.
- **`npm install` reports vulnerabilities** — ignore them and never run
  `npm audit fix --force` (build-time tooling only; output is static HTML).
