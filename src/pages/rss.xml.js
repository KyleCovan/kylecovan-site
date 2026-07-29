/**
 * RSS feed for the build log.
 *
 * Added because the site previously had no way to follow it — the only actions
 * were an email address and a link to Tapo Canyon. A feed costs nothing, needs
 * no third party, and means someone who likes an entry can get the next one
 * without Kyle running a mailing list.
 */
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import projects from '../data/projects.json';

export async function GET(context) {
  const entries = (await getCollection('log', ({ data }) => !data.draft))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: 'Kyle Covan — Building in public',
    description:
      'Build logs for two systems Kyle Covan is building for himself first: ' +
      'a personal AI OS that ranks and tracks ideas, and an AI-powered second brain.',
    site: context.site,
    items: entries.map((e) => ({
      title: e.data.title,
      pubDate: e.data.date,
      description: projects.find(p => p.id === e.data.project)?.name ?? '',
      link: `/building/#${e.data.project}`,
    })),
    customData: '<language>en-us</language>',
  });
}
