/**
 * Two collections.
 *
 * `builds` — one Markdown file per thing Kyle has made. Frontmatter carries the
 * structured parts; the body carries the prose about the thing itself.
 *
 * `writing` — everything dated. One collection, not two, and this is the July 30
 * decision worth understanding before changing it:
 *
 *   A post with a `build:` field renders IN FULL on that build's page and is
 *   listed (not duplicated) in the writing index. A post without one gets its
 *   own page at /writing/<id>/.
 *
 * That means Kyle never has to decide "is this a log entry or a blog post?" when
 * he sits down — he just writes, and one optional field decides where it lands.
 * The tag can be added or removed later without rewriting anything.
 *
 * It also keeps each build page a PILLAR PAGE: description plus every dated
 * entry about it, in one document. handoff §1 settled that generative engines
 * work at the passage level and reward exactly that shape. Splitting build
 * writing onto separate URLs was considered and rejected for this reason — see
 * §7. There is only ever ONE full copy of any text, so nothing is duplicate
 * content.
 */
import { defineCollection, reference, z } from 'astro:content';
import { glob } from 'astro/loaders';

const builds = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/builds' }),
  schema: z.object({
    name: z.string(),
    // Drives display order and the "Project 01" label, which is derived rather
    // than stored — storing it meant renumbering by hand on every insert.
    order: z.number().int().positive(),
    oneLiner: z.string(),
    // Not rendered. Feeds <lastmod> in the sitemap, which is the one hint in
    // that file Google actually reads — it ignores <priority> and <changefreq>
    // outright. A build page's real lastmod is the LATER of this date and the
    // newest post tagged to the build, because the page renders both; see the
    // note in astro.config.mjs. Bump it when the prose here changes and no new
    // post lands, otherwise an edited page keeps advertising a stale date.
    // Optional on purpose: a build with no date simply gets no <lastmod>, which
    // is honest. A wrong date is worse than a missing one — Google learns to
    // distrust the whole file when lastmod stops matching what actually changed.
    updated: z.coerce.date().optional(),
    // Where the idea came from. Not rendered — see the note in the build files.
    inspiration: z.string().optional(),
    // NOT RENDERED. These were the old "What the log will cover" outline, which
    // published a list of promises on a page with nothing behind it. They are
    // now writing prompts for the Markdown body: Kyle answers them in prose and
    // the answers become the page. Never render this array again.
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
    // Optional. Set it and the post lands on that build's page; leave it off
    // and the post gets its own URL. `reference` means a typo fails the BUILD
    // rather than silently orphaning the post.
    build: reference('builds').optional(),
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
