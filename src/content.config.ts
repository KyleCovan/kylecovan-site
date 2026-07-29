/**
 * Build-log entries are Markdown files in src/content/log/.
 *
 * This is the single biggest practical win of the Astro migration: adding an
 * entry means adding one .md file. The Building page, the project's entry list,
 * the JSON-LD, the sitemap and the RSS feed all pick it up with no other edit.
 * Posting friction is the thing most likely to kill a build log, so the whole
 * pipeline is built to make one file the entire cost of publishing.
 */
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const log = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/log' }),
  schema: z.object({
    title: z.string(),
    // Kyle's dates render as "July 28, 2026" but are authored as ISO so they
    // sort correctly and land in JSON-LD without a parsing step.
    date: z.coerce.date(),
    // Must match an id in src/data/projects.json. A typo here is caught by
    // scripts/verify_site.py rather than silently producing an orphan entry.
    project: z.enum(['personal-ai-os', 'second-brain']),
    draft: z.boolean().default(false),
  }),
});

export const collections = { log };
