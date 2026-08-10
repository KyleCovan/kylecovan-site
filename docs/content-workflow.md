# Content workflow  -  keep one copy, stop the drift

**For Kyle.** Written August 10, 2026 after the first Cursor iPhone session that
parked Unless the Lord drafts on a PR. Read this when you come back cold and
wonder where the files went, or whether to dump them into Obsidian.

`docs/` never publishes. This note is for you and for agents working the site.

---

## The one rule

**One canonical full text.** Everything else is an adaptation, a scratch pad, or
an idea parking lot. Two full copies is how drafts drift apart.

| Kind | Where it lives | Publishes? |
|---|---|---|
| Site blog / build-log entry | `src/content/writing/<slug>.md` | Only when `draft` is false / absent, and the branch is on `main` |
| LinkedIn, Substack, X, etc. | `content-queue/<same-slug>/` | Never from the repo  -  you paste from here |
| Ideas said but not written | `docs/post-ideas.md` | Never |
| Decisions / why we did it | `docs/handoff.md` | Never |

Same slug for the writing file and the queue folder. That is the whole filing
system.

---

## Drafts are already safe in git

When an agent (or you) drafts a post:

1. It lands in `src/content/writing/` with **`draft: true`**.
2. Platform copies land in **`content-queue/<slug>/`**.
3. The idea is logged in **`docs/post-ideas.md`** if it started as a seed.
4. Usually this sits on a **feature branch / PR**, not on `main`.

`draft: true` is filtered in six places (RSS, builds pages, writing index,
writing post pages, home). A draft is genuinely invisible on the live site even
if the branch somehow merged. You still do not merge until you mean to publish.

**You do not need to download these into Obsidian to "save" them.** Git already
has them. Phone Downloads and a second "final" vault note are how drift starts.

---

## Phone (Cursor iPhone app)

Optional. Only useful if you want to **edit words** on the PR.

- Open the PR or the three files. Mark changes. Stop.
- Do **not** merge, deploy, or copy into Obsidian from the phone unless that is
  a deliberate choice for scratch thinking.
- Done for the night? Close the app. The branch keeps the drafts.

---

## Desktop (where publish happens)

1. Open **kylecovan-site** in Cursor (`~/Projects/kylecovan-astro` locally).
2. Check out / pull the PR branch (or continue from the open PR).
3. Edit the **blog file first**  -  that is the canonical copy.
4. Then update `content-queue/<slug>/` so LinkedIn / Substack stay short
   adaptations, not a second full essay.
5. When ready to publish the site post:
   - set `draft: false` (or remove `draft:`)
   - `npm run build && npm run verify`  -  both must say **ALL CHECKS PASSED**
   - commit, merge to `main` (Cloudflare deploys from `main`)
6. Post LinkedIn / Substack from the queue files when you choose. After posting,
   mark them posted or clear them so the queue does not become a junk drawer.

---

## Two paths, not three

Keep the workflow simple:

| Path | Role |
|---|---|
| **Cursor + the site project** | Primary. Edit, verify, publish. Default habit. |
| **GitHub PR** | Backup / phone. Same files, another door  -  not a second home. |
| **Obsidian** | Not required for site content. Skip it for drafts that already live in git. |

You do not need a vault pointer if Cursor and the PR already cover find + edit.

---

## When Obsidian *is* the right tool

Use Obsidian for thinking, jotting, and capturing ideas that are **not yet tied**
to something you are already working on in Cursor or that already has a git
repo  -  or for personal/faith/life notes that will never need to be a site or
code file.

Do **not** use it as the home for kylecovan.com prose, LinkedIn/Substack queue
copy, or anything that already has a branch/PR.

When an Obsidian idea *turns into* a site post, move it into
`src/content/writing/` (and `content-queue/` if needed). Stop polishing a second
full copy in the vault.

If you still want a vault note as a bookmark into the repo, a one-line pointer
to `src/content/writing/<slug>.md` is enough  -  never a duplicate draft. Most of
the time you can skip that entirely.

Faith writing that belongs on Unless the Lord still ends in
`src/content/writing/` with no `build:` field so it gets its own `/writing/` URL.

---

## Quick recovery ("where did that draft go?")

1. Open the site project in Cursor and look under `src/content/writing/` /
   `content-queue/` (or the PR branch).
2. Or GitHub → kylecovan-site → Pull requests (handy on the phone).
3. Or `docs/post-ideas.md` if it was only an idea, not a draft yet.

Not: Obsidian, Downloads, or a third "organized" folder.

---

## Anti-patterns (do not do these)

- Download the PR files into Obsidian *as the new home* for the post.
- Keep a "final" in the vault and a "final" in the repo and edit both.
- Put LinkedIn text only in Obsidian with no queue file and no link back.
- Merge to `main` before clearing `draft: true` and running verify.
- Invent a third folder on the phone for "organized copies."
