// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

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
      // og.png and rss.xml are assets, not pages. Left in, they tell crawlers
      // to index a picture and a feed as if they were content.
      filter: (page) => !page.includes('/og.png'),
      serialize: (item) => ({
        ...item,
        priority: item.url === 'https://kylecovan.com/' ? 1.0 : 0.8,
      }),
    }),
  ],
});
