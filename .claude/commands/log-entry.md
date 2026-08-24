---
description: Add a post — essay or log — in In Your Sight
argument-hint: [essay|log] [what it is about]
---

Add a new post: $ARGUMENTS

Steps:

1. Read `src/content.config.ts` for the `writing` schema and an existing file in
   `src/content/writing/` for the frontmatter shape. Match them exactly.
2. Create `src/content/writing/<slug>.md`. **The filename is the URL** — name it
   for the URL, and no date prefix.
   - Essay (default): omit `kind`, or set `kind: essay`. Scarce pieces.
   - Log: set `kind: log`. Dated notes inside the same house. Optional
     `project: "Personal AI OS"` (free text) if it is about a named thing.
   - Do **not** use `build:` — that field is gone. It used to hide posts from
     /writing/; that lock is reversed.
3. **Write from Kyle's own words only.** If I haven't given you the content, ask
   me for it — do not draft prose on my behalf and do not invent details. See
   `docs/handoff.md` §6.
4. Run `/verify`.
5. Show me the rendered post before committing.

Nothing else needs touching: Astro regenerates the writing index, the home
page's recent-posts list, the JSON-LD, the sitemap and the RSS feed from the
one Markdown file. Every published post is a full page at `/writing/<slug>/`.
