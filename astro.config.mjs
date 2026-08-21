// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { readFileSync, readdirSync } from 'node:fs';

const SITE = 'https://kylecovan.com';

/**
 * <lastmod> for the sitemap, derived from the CONTENT rather than from build
 * time. This is the one element in that file Google documents itself as using;
 * it ignores <priority> and <changefreq> outright, which is why neither is set
 * below any more.
 *
 * The temptation is to stamp every URL with the deploy timestamp. Don't. A
 * sitemap claiming all seven pages changed on every push is a sitemap Google
 * learns to ignore, and then the one page that really did change gets no
 * signal either. Every date here traces to a file Kyle actually edited:
 *
 *   /builds/<id>/   the later of the build's `updated` and the newest post
 *                   tagged to it — the page renders both, so either can age it
 *   /writing/<id>/  that post's own date (untagged posts only)
 *   /builds/        newest of the per-build dates
 *   /writing/       newest untagged post — tagged posts are not listed there
 *   /               newest of /builds/ and /writing/
 *
 * A page with no date gets no <lastmod> at all. That is deliberate: a missing
 * date costs nothing, a wrong one costs the file's credibility.
 *
 * Frontmatter is read here with fs rather than through astro:content because
 * this runs at config load, before the content layer exists.
 */
const frontmatter = (/** @type {string} */ text) => (text.match(/^---\r?\n([\s\S]*?)\r?\n---/) || ['', ''])[1];

// Top-level scalars only. The pattern is anchored and rejects leading spaces,
// so the indented keys inside the `prompts` array can never match by accident.
const field = (/** @type {string} */ fm, /** @type {string} */ key) => {
  const m = fm.match(new RegExp(`^${key}:[ \\t]*['"]?([^'"\\n#]+)`, 'm'));
  return m ? m[1].trim() : null;
};

const collection = (/** @type {string} */ dir) => {
  const base = new URL(`./src/content/${dir}/`, import.meta.url);
  return readdirSync(base)
    .filter((f) => f.endsWith('.md'))
    .map((f) => ({
      id: f.replace(/\.md$/, ''),
      fm: frontmatter(readFileSync(new URL(f, base), 'utf8')),
    }));
};

// ISO dates sort lexically, which is the whole reason the schema authors them
// as ISO in the first place.
const day = (/** @type {string | null} */ d) => (d ? d.slice(0, 10) : null);
const newest = (/** @type {(string | null | undefined)[]} */ ...dates) => dates.filter(Boolean).sort().pop() ?? null;

const posts = collection('writing')
  .map((e) => ({
    id: e.id,
    date: day(field(e.fm, 'date')),
    build: field(e.fm, 'build'),
    draft: field(e.fm, 'draft') === 'true',
  }))
  .filter((p) => p.date && !p.draft);

const builds = collection('builds').map((e) => ({
  id: e.id,
  updated: day(field(e.fm, 'updated')),
}));

/** Keyed by absolute URL, exactly as @astrojs/sitemap emits it. */
/** @type {Record<string, string>} */
const LASTMOD = {};

for (const b of builds) {
  const d = newest(b.updated, ...posts.filter((p) => p.build === b.id).map((p) => p.date));
  if (d) LASTMOD[`${SITE}/builds/${b.id}/`] = d;
}

// Only an UNtagged post gets its own URL. A tagged one renders in full on its
// build page and is not listed on /writing/ — one copy of any text.
for (const p of posts.filter((p) => !p.build)) {
  // `posts` is already filtered to entries that have a date, so this guard
  // never fires. It is written out because a `.filter()` doesn't narrow the
  // type, and the alternative is asserting the invariant instead of checking
  // it — every other write to LASTMOD guards the same way.
  if (p.date) LASTMOD[`${SITE}/writing/${p.id}/`] = p.date;
}

const buildsIndex = newest(...builds.map((b) => LASTMOD[`${SITE}/builds/${b.id}/`]));
// /writing/ lists only untagged posts, so a new build-log entry must not age it.
const writingIndex = newest(...posts.filter((p) => !p.build).map((p) => p.date));
if (buildsIndex) LASTMOD[`${SITE}/builds/`] = buildsIndex;
if (writingIndex) LASTMOD[`${SITE}/writing/`] = writingIndex;

// The home page renders summaries of both collections, so it genuinely ages
// when either does.
const home = newest(buildsIndex, writingIndex);
if (home) LASTMOD[`${SITE}/`] = home;

/* /privacy/ is the one page here that isn't generated from a collection, so it
   has no frontmatter to age it. Its date still isn't invented: a privacy policy
   has to show its effective date to the reader anyway, so that date is real
   content, and it lives in src/data/privacy.json. The page renders it as the
   visible "Last updated" line and this reads the same file for <lastmod>. One
   date, two uses, no second copy to drift.

   Read with fs like everything else in this block: config load happens before
   the content layer exists, and a JSON import here would need an import
   assertion for no benefit. */
const privacyUpdated = day(
  JSON.parse(readFileSync(new URL('./src/data/privacy.json', import.meta.url), 'utf8')).updated
);
if (privacyUpdated) LASTMOD[`${SITE}/privacy/`] = privacyUpdated;

export default defineConfig({
  site: 'https://kylecovan.com',

  // Trailing slashes, consistently. Cloudflare Pages serves /building/ from
  // building/index.html either way, but pinning it keeps canonical URLs, the
  // sitemap and internal links from disagreeing — which is the kind of quiet
  // mismatch that splits ranking signals between two URLs for one page.
  trailingSlash: 'always',

  build: {
    // The constraint that survived from the hand-built site: a visitor's
    // browser fetches exactly one file per page. Astro would normally emit a
    // separate .css and link to it; this inlines it into <head> instead.
    inlineStylesheets: 'always',
    format: 'directory',
  },

  markdown: {
    // OFF, deliberately. Astro's Markdown pipeline turns straight apostrophes
    // into curly ones by default. That is better typography in isolation, but
    // the rest of the site is hand-written HTML using straight quotes, and
    // handoff §5 records a deliberate normalisation TO straight after a source
    // title arrived with one straight and one curly quote. Leaving this on
    // produced a build log with curly apostrophes sitting next to a home page
    // with straight ones — caught only by a pixel diff against the approved
    // pages, not by any test. Consistency wins; if Kyle ever wants curly, it
    // is one flag here plus a sweep of the hand-written copy, not just this.
    smartypants: false,
  },

  integrations: [
    sitemap({
      // og.png is an asset, not a page. Left in, it tells crawlers to index a
      // picture as if it were content. (The old comment here also claimed to
      // filter rss.xml — it never did, and never needed to: the feed is an
      // endpoint and has never appeared in the built sitemap. Checked against
      // dist/sitemap-0.xml, not assumed.)
      filter: (page) => !page.includes('/og.png'),
      // <lastmod> only. The <priority> values that used to live here were a
      // no-op — Google's own sitemap documentation says it ignores the element
      // — and a knob that looks like it steers ranking but doesn't is worse
      // than no knob, because it invites tuning. See the LASTMOD note above.
      serialize: (item) => {
        const lastmod = LASTMOD[item.url];
        return lastmod ? { ...item, lastmod } : item;
      },
    }),
  ],
});
