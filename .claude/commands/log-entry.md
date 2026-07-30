---
description: Add a build-log entry to /building/
argument-hint: [project slug] [what the entry is about]
---

Add a new build-log entry: $ARGUMENTS

Steps:

1. Read `src/content.config.ts` for the collection schema and an existing file
   in `src/content/log/` for the frontmatter shape. Match them exactly.
2. Create `src/content/log/YYYY-MM-DD-<slug>.md`. The `project` frontmatter field
   must match a key in `src/data/projects.json` (`personal-ai-os`,
   `second-brain`) — this is what routes the entry onto the right project on
   `/building/`.
3. **Write the entry from Kyle's own words only.** If I haven't given you the
   content, ask me for it — do not draft prose on my behalf and do not invent
   details. An invented failure story in a build log is the worst possible
   outcome. See `docs/handoff.md` §6.
4. Run `/verify`.
5. Show me the rendered entry before committing.

Nothing else needs touching: Astro regenerates the page, the JSON-LD, the
sitemap and the RSS feed from the Markdown file. If this is Project 02's first
entry, the `<p class="log-status">` placeholder disappears on its own.
