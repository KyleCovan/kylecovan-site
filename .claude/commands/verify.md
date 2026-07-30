---
description: Build the site and run both verify suites
allowed-tools: Bash(source .venv/bin/activate && npm run build && npm run verify), Bash(npm run build), Bash(npm run verify), Read, Glob, Grep
---

Build the site and run both verification suites, then report the result.

```bash
source .venv/bin/activate && npm run build && npm run verify
```

Notes:

- `source .venv/bin/activate` is required in a fresh shell; `npm run verify`
  needs Playwright from that virtualenv. `npm run build` alone does not need it.
- Both suites must print **ALL CHECKS PASSED** — that's twice, once for
  `verify.py` (home page) and once for `verify_site.py` (site-level).
- The suites run against `dist/`, not the source, so the build has to happen
  first.

If anything fails, show me the failing assertion verbatim and tell me which rule
in `docs/handoff.md` it protects before proposing a fix. Do not weaken or delete
an assertion to make it pass — if the underlying design rule genuinely changed,
update the assertion and say so explicitly.
