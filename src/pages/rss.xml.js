/**
 * RSS feed for the build log.
 *
 * Added because the site previously had no way to follow it — the only actions
 * were an email address and a link to Tapo Canyon. A feed costs nothing, needs
 * no third party, and means someone who likes an entry can get the next one
 * without Kyle running a mailing list.
 *
 * July 30: every item used to link to `/building/#<project>`, so two entries
 * about the same build produced two feed items pointing at the same place. A
 * reader clicking the newest one landed at the top of a project they may have
 * already read. Items now link to the entry itself.
 *
 * The feed URL does NOT move with the /building/ -> /builds/ rename. Existing
 * subscribers are pointed at /rss.xml and a feed that 404s is a subscriber lost
 * silently, with no error anyone sees.
 */
import rss from '@astrojs/rss';
import { getCollection, getEntry } from 'astro:content';

export async function GET(context) {
  const entries = (await getCollection('writing', ({ data }) => !data.draft))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  // Resolve each entry's build once, up front — `reference()` gives us an id,
  // not the record. `build` is optional, so an untagged essay resolves to null
  // and links to its own page instead.
  const items = await Promise.all(
    entries.map(async (e) => {
      const build = e.data.build ? await getEntry(e.data.build) : null;
      return {
        title: e.data.title,
        pubDate: e.data.date,
        description: build?.data.name ?? 'Writing',
        /* ABSOLUTE, deliberately. @astrojs/rss runs a relative link through
           createCanonicalURL, which honours the site's `trailingSlash: always`
           and appends a slash to the END OF THE WHOLE STRING — producing
           ".../#2026-07-28-too-many-ideas/", a fragment that matches no id on
           the page. An already-valid URL is passed through untouched instead
           (see isValidURL in @astrojs/rss/dist/index.js). Caught by the RSS
           check in verify_site.py, which exists because of this bug. */
        link: new URL(
          build ? `builds/${build.id}/#${e.id}` : `writing/${e.id}/`,
          context.site
        ).href,
      };
    })
  );

  return rss({
    title: 'Kyle Covan — Building in public',
    description:
      'Build logs for two systems Kyle Covan is building for himself first: ' +
      'a personal AI OS that ranks and tracks ideas, and an AI-powered second brain.',
    site: context.site,
    items,
    customData: '<language>en-us</language>',
  });
}
