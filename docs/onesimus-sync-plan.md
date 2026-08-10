# Onesimus sync plan — do this at the desktop

**For Kyle.** Agreed August 10, 2026 on a Cursor iPhone / cloud session.
Parked here so the site repo can remind you; **move or copy the lasting version
into Onesimus itself** once the drive is mounted (this file in kylecovan-site
is only a sticky note until then).

`docs/` never publishes.

---

## The rule (agreed)

**One source of truth: the private GitHub repo for Onesimus.**

| Place | Role |
|---|---|
| **Private GitHub (Onesimus)** | Canonical. Everything syncs to/from this. |
| **Desktop folder** (SSD / Obsidian vault path) | Working copy. Pull when you open; push when you finish real changes. |
| **Cursor cloud / iPhone** | Temporary checkout of that same repo when a session needs it. Not a permanent third twin. |

Do **not** keep three syncing copies (desktop + GitHub + "Cursor cloud version")
with auto-update in every direction.

Do **not** put Onesimus inside kylecovan-site.

---

## Why cloud agents could not see it (August 10)

This session could only list two GitHub repos under `KyleCovan`
(`kylecovan-site`, `needs-based-selling`). Your Onesimus repo is **private**;
the cloud agent's GitHub token apparently cannot see it (or the remote name /
owner differs from what we searched).

**Desktop checklist item:** confirm the private remote exists and that Cursor
Cloud / the GitHub integration is allowed to access that private repo.

---

## Desktop checklist (next time you sit down)

Do these in order.

### 1. Confirm the private remote

```bash
cd "/Volumes/Acasis Samsung SSD 990 PRO 4TB/kernel journal/Onesimus"
# or wherever the real Onesimus root is
git remote -v
git status
```

- If there is already a private GitHub remote and it matches what you expect:
  note the exact URL (e.g. `git@github.com:KyleCovan/<name>.git`).
- If there is no remote: create a **private** GitHub repo and `git push -u`.
- Fix ownership / repo name confusion if the remote is not under `KyleCovan`
  or is not named what you think.

### 2. Fix "cloud cannot see private Onesimus"

On the machine where Cursor is logged in as you:

- Confirm GitHub → Settings → Applications / Cursor (or the integration used by
  Cloud Agents) has access to **private** repos, and to **this** Onesimus repo
  (org access / "All repositories" vs selected).
- Open Onesimus as its **own** Cursor project (separate from kylecovan-site).
- Optionally add that private repo to a Cursor Cloud environment so phone /
  cloud agents can clone it when the SSD is off.

### 3. Habit (not a three-way sync engine)

- **On open (desktop):** `git pull` in Onesimus before trusting it.
- **After real changes:** `git add` / `git commit` / `git push` to the private
  remote. Prefer deliberate pushes over "commit everything on session end."
- **Phone / cloud:** work in a checkout of the same private repo; push when
  done so the desktop can pull next time.

### 4. Land the lasting note inside Onesimus

Copy the substance of this plan into Onesimus (e.g. under its own docs /
HOW-TO / decisions), then you can delete or shrink this sticky note in
kylecovan-site so the brain owns its sync rules.

---

## Anti-patterns

- A permanent "Cursor cloud copy" kept in sync as a peer of GitHub.
- Auto-commit-all on every session close (half-finished thoughts, secrets).
- Forking Onesimus into kylecovan-site "so the agent can see it."
- Editing Onesimus only on the SSD with no push, then expecting the phone to
  have it.
