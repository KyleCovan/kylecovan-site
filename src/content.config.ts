/**
 * Two collections.
 *
 * `writing` — everything dated, one house. Unless the Lord at /writing/ is
 * the door. A post is a full page at /writing/<id>/ whether it is an essay
 * or a log. `kind: log` marks the frequent dated notes so a reader can skip
 * them without leaving the house. `kind` defaults to essay when unset, so
 * existing essays need no new field and no new filename scheme.
 *
 * `project` is a free-text label for "this log is about a named thing." It is
 * not a second door and it does not hide a post from the house.
 *
 * August 21, 2026: the July 30 lock that sent any post with `build:` off
 * /writing/ and onto a product page is reversed. That field is gone. Logs
 * live in the house. Old /builds/ URLs redirect; they are not a blog.
 *
 * `builds` — structured facts for the three things named on the home page
 * (name, one-liner, order). The Markdown bodies stay in the repo. They are
 * not rendered as product pages; that was the second door.
 */
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const builds = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/builds' }),
  schema: z.object({
    name: z.string(),
    // Drives display order and the "Project 01" label, which is derived rather
    // than stored — storing it meant renumbering by hand on every insert.
    order: z.number().int().positive(),
    // RENDERED on the home page as the `.one-liner`. Section 6 of
    // docs/handoff.md puts it out of reach — changes come from Kyle as exact
    // text, or from options he picks.
    oneLiner: z.string(),
    // NOT rendered. Was the /builds/<id>/ meta/og override. Those pages
    // redirect now. Kept so the files do not fail the schema.
    description: z.string().optional(),
    // Not rendered. Still ages the home page's sitemap <lastmod> when the
    // home summary lists these names. Optional on purpose: a missing date
    // costs nothing, a wrong one costs the file's credibility.
    updated: z.coerce.date().optional(),
    // Where the idea came from. Not rendered — see the note in the build files.
    inspiration: z.string().optional(),
    // NOT RENDERED. These were the old "What the log will cover" outline, which
    // published a list of promises on a page with nothing behind it. They are
    // now writing prompts for the Markdown body. Never render this array.
    prompts: z.array(z.object({ lead: z.string(), rest: z.string() })),
  }),
});

const writing = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/writing' }),
  schema: z.object({
    title: z.string(),
    // Authored as ISO so it sorts correctly and lands in JSON-LD without a
    // parsing step; rendered as "July 28, 2026".
    date: z.coerce.date(),
    // essay (default) or log. A log is a kind inside Unless the Lord, not a
    // second blog. Unset means essay — do not make Kyle add a field to every
    // scarce piece.
    kind: z.enum(['essay', 'log']).default('essay'),
    // Free text, NOT a reference. A label for a named thing. It does not
    // hide the post and it does not mint a product page.
    project: z.string().optional(),
    // Free text, not an enum. These come from Kyle's chat-to-obsidian skill,
    // which writes them when a note is captured out of a conversation. An enum
    // here would reject a valid vault file over a value this repo hasn't seen
    // yet, turning a publish into a debugging session.
    voice: z.string().optional(),
    audience: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { builds, writing };
