/**
 * RSS feed for Unless the Lord — the blog.
 *
 * Build-log posts (anything with `build:`) are not in this feed. They render
 * on their build page and are not blog posts. Kyle locked that on August 21,
 * 2026. Drafts stay out.
 *
 * Added because the site previously had no way to follow the writing — the
 * only actions were an email address and a link to Tapo Canyon. A feed costs
 * nothing, needs no third party, and means someone who likes a post can get
 * the next one without Kyle running a mailing list.
 *
 * The feed URL does NOT move with any rename. Existing subscribers are pointed
 * at /rss.xml and a feed that 404s is a subscriber lost silently, with no
 * error anyone sees.
 */
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const entries = (await getCollection('writing', ({ data }) => !data.draft && !data.build))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  const items = entries.map((e) => ({
    title: e.data.title,
    pubDate: e.data.date,
    description: 'Writing',
    /* ABSOLUTE, deliberately. @astrojs/rss runs a relative link through
       createCanonicalURL, which honours the site's `trailingSlash: always`
       and appends a slash to the END OF THE WHOLE STRING — producing
       ".../#2026-07-28-too-many-ideas/", a fragment that matches no id on
       the page. An already-valid URL is passed through untouched instead
       (see isValidURL in @astrojs/rss/dist/index.js). Caught by the RSS
       check in verify_site.py, which exists because of this bug. */
    link: new URL(`writing/${e.id}/`, context.site).href,
  }));

  return rss({
    title: 'Unless the Lord — Kyle Covan',
    description:
      'Writing by Kyle Covan on faith, technology, and the daily striving.',
    site: context.site,
    items,
    customData: '<language>en-us</language>',
  });
}
