/**
 * Two collections.
 *
 * `builds` — one Markdown file per thing Kyle has made. The frontmatter carries
 * the structured parts (name, one-liner, the outline); the body carries the
 * prose. Adding a build is adding one file: it appears on /builds/, gets its own
 * URL at /builds/<id>/, and lands in the sitemap with no other edit.
 *
 * `log` — dated entries that hang underneath a build. Adding an entry is also
 * one file. The build page, the JSON-LD and the RSS feed all pick it up.
 *
 * Posting friction is the thing most likely to kill both of these, so the whole
 * pipeline is built to make one file the entire cost of publishing.
 */
import { defineCollection, reference, z } from 'astro:content';
import { glob } from 'astro/loaders';

const builds = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/builds' }),
  schema: z.object({
    name: z.string(),
    // Drives display order and the "Project 01" index label, which is derived
    // rather than stored. Storing the label meant renumbering by hand every
    // time a build was inserted anywhere but the end.
    order: z.number().int().positive(),
    oneLiner: z.string(),
    // Where the idea came from. Deliberately not rendered — see the note in
    // src/content/builds/personal-ai-os.md.
    inspiration: z.string().optional(),
    outline: z.array(z.object({ lead: z.string(), rest: z.string() })),
  }),
});

const log = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/log' }),
  schema: z.object({
    title: z.string(),
    // Kyle's dates render as "July 28, 2026" but are authored as ISO so they
    // sort correctly and land in JSON-LD without a parsing step.
    date: z.coerce.date(),
    // `reference` instead of the old hardcoded z.enum: Astro now fails the
    // BUILD if this points at a build that doesn't exist, and the valid set
    // updates itself when a build is added. The enum had to be hand-edited
    // every time, which is exactly the kind of step that gets forgotten.
    build: reference('builds'),
    draft: z.boolean().default(false),
  }),
});

export const collections = { builds, log };
