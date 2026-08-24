/**
 * RSS feed for Upon the Waters.
 *
 * The feed URL stays /rss.xml. Existing subscribers are pointed here and a
 * feed that 404s is a subscriber lost silently, with no error anyone sees.
 *
 * August 24, 2026: Unless the Lord renamed Upon the Waters.
 */
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const entries = (await getCollection('writing', ({ data }) => !data.draft))
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
    title: 'Kyle Covan — Upon the Waters',
    description:
      'Writing by Kyle Covan on faith, technology, and the daily striving.',
    site: context.site,
    items,
    customData: '<language>en-us</language>',
  });
}
