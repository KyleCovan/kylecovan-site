---
description: Add a post — tagged to a build, or standalone
argument-hint: [build slug or "none"] [what it is about]
---

Add a new post: $ARGUMENTS

Steps:

1. Read `src/content.config.ts` for the `writing` schema and an existing file in
   `src/content/writing/` for the frontmatter shape. Match them exactly.
2. Create `src/content/writing/<slug>.md`. **The filename is the URL** — name it
   for the URL, and no date prefix.
   - Tagged to a build: set `build:` to a filename in `src/content/builds/`. The
     post renders in full on that build's page and is not listed on Unless the
     Lord. It is a `reference()`, so a wrong value fails the build rather than
     passing quietly.
   - Standalone: omit `build:` entirely and it gets its own `/writing/` page.
   - If it isn't obvious which, ask. Don't guess — the tag decides the URL.
3. **Write from Kyle's own words only.** If I haven't given you the content, ask
   me for it — do not draft prose on my behalf and do not invent details. An
   invented failure story in a build log is the worst possible outcome. See
   `docs/handoff.md` §6.
4. Run `/verify`.
5. Show me the rendered post before committing.

Nothing else needs touching: Astro regenerates the build page (if tagged) or
the writing index, per-post page, home recent-posts list, JSON-LD and RSS (if
not) from the one Markdown file. If this is a build's first entry, its "first
entry coming soon" placeholder disappears on its own.
