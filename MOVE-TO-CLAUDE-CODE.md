# Moving kylecovan.com to Claude Code in VS Code

**The short version: the code has already moved. Only the context needs to.**

The site stopped being "a Claude project" on July 29 — it became a git repo
(then named `kylecovan-astro`). **Live local path as of 2026-08-11:**
`~/1. Projects/kylecovan-site` (quote it — spaces in the folder name). Repo on
GitHub, auto-deploying from Cloudflare Pages. Open that folder and work it
directly, with a real terminal, so you can run `npm run build`, both verify
suites, and push.

What has *not* moved is everything the claude.ai project was carrying in its head:
the instructions prepended to every chat, and the four project docs. Claude Code
can't see any of that — it reads files in the repo. That's what this bundle is.

There's a bonus: **the project instructions are currently wrong** in three ways
(they describe the pre-Astro five-file site, `build_site.py`, and the creed as
"keep"). A session following them literally would undo real work. The `CLAUDE.md`
in this bundle is the corrected replacement, so the move fixes that at the same
time.

---

## Step 1 — Get Claude Code into VS Code

You already run Claude Code, so you may be done here. If not:

- VS Code → Extensions → search **Claude Code** → Install.
- Open the folder `~/1. Projects/kylecovan-site` (quote paths in the shell).
- Or open `/Users/kylecovan/1. Projects/Onesimus-with-sites.code-workspace`.

The extension runs Claude Code inside the folder you have open, so **open the
repo folder, not your home folder or a parent.** Same reasoning as the `git init`
trap in `docs/deploy-status.md`.

---

## Step 2 — Drop this bundle into the repo

Unzip it and copy the contents into `~/1. Projects/kylecovan-site`, preserving the
folder structure. You should end up with:

```
kylecovan-site/
├── CLAUDE.md              ← loaded automatically at the start of every session
├── docs/
│   ├── handoff.md          the full source of truth
│   ├── deploy-status.md    where the deploy and DNS stand
│   └── dns-records.md      the verified DNS inventory
├── .claude/
│   ├── settings.json       what Claude can run without asking
│   └── commands/
│       ├── verify.md       → /verify
│       ├── log-entry.md    → /log-entry
│       └── ship.md         → /ship
├── src/ …                  (already there)
└── scripts/ …              (already there)
```

Nothing here overwrites site code. If a `CLAUDE.md` already exists in the repo,
open both and merge rather than clobbering.

Then commit it:

```bash
git add CLAUDE.md docs .claude
git commit -m "docs: port project context into the repo for Claude Code"
```

You can push it or not — it changes nothing about the built site, so Cloudflare
will just rebuild identically.

---

## Step 3 — Check it took

Start a session in the repo and ask:

> What does the creed line read, and what's the one rule about my bio paragraphs?

If it answers **"Striving to put Jesus Christ first"** and *don't reword them*
without you pasting anything, `CLAUDE.md` is loading. Then try `/verify` — it
should run the build and both suites and report back.

---

## Step 4 — What to do about the claude.ai project

Your call, but the honest recommendation:

**Leave the project instructions alone but stop trusting them, or replace their
whole body with a pointer.** Something like:

```text
This site is maintained in Claude Code, not here.
Repo: github.com/KyleCovan/kylecovan-site — local ~/1. Projects/kylecovan-site
CLAUDE.md at the repo root plus docs/ are the source of truth.
Do not make site changes from a chat in this project; they cannot be built,
verified or deployed from here.
```

That kills the failure mode where a future chat helpfully "fixes" the site back
to a single page.

**The four project docs:**

| Doc | What to do |
|---|---|
| `claude/kylecovan-handoff.md` | Superseded by `docs/handoff.md`. Keep as an archive or delete. |
| `claude/astro-next-steps.md` | Superseded by `docs/deploy-status.md`. Same. |
| `claude/kylecovan-dns-records.md` | Superseded by `docs/dns-records.md`. Same. |
| `claude/kylecovan-cleanup-checklist.md` | **Obsolete.** It describes the pre-Astro five-file site and tells you to paste the now-wrong instructions. Delete it. |

Also still sitting in the project, per the old handoff: `claude/index.html`,
`claude/building.html`, `claude/scripts/*` — the pre-Astro hand-built site.
Editing them changes nothing. They were kept as a verification reference for the
Astro migration, which is long done. Safe to delete.

---

## What changes about how you work

| Before (Cowork / project chat) | After (Claude Code in VS Code) |
|---|---|
| Describe a change, get files back, place them yourself | Claude edits the repo in place; you review the diff |
| Couldn't run the verify suites | `/verify` actually runs them and reads the failures |
| Couldn't push | `/ship` verifies, commits and pushes (deploying) |
| Context lived in project instructions | Context lives in `CLAUDE.md` + `docs/`, versioned with the code |
| Rules could silently go stale | A rule change and its test change land in the same commit |

The three commands are starting points — edit the `.md` files in
`.claude/commands/` any time, they're just prompts.

## One thing that gets slightly worse

`npm run verify` needs `source .venv/bin/activate` first, in every new shell.
Claude Code opens its own shells, so the `/verify` and `/ship` commands both do
the `source` inline. If you ever see `ModuleNotFoundError: No module named
'playwright'`, that's what's missing — not a broken install.
