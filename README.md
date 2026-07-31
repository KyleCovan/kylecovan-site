# kylecovan.com

Personal site. Astro, deployed static to Cloudflare Pages.

**Read `docs/handoff.md` before changing anything.** It holds the hard
constraints, the design tokens, and — most importantly — the copy rules.
Section 6 lists every correction Kyle has made to his own words. Several of them
have been undone once already by a well-meaning rewrite.

## Publishing a build-log entry

One file. That is the whole workflow.

```bash
# 1. create src/content/log/2026-08-15-what-broke.md
---
title: "The version I threw away"
date: 2026-08-15
build: personal-ai-os     # must match a filename in src/content/builds/
---

Your words here. Plain Markdown paragraphs.

# 2. check it
npm run build && npm run verify

# 3. ship
git add -A && git commit -m "log: what broke" && git push
```

The entry automatically appears on that build's page, in the JSON-LD, in
`sitemap-0.xml`, and in `rss.xml`. Nothing else needs editing.

Set `draft: true` in the frontmatter to write ahead without publishing.

## Adding a build

Also one file — `src/content/builds/<id>.md`. The filename becomes the URL, so
`llm-wiki.md` is served at `/builds/llm-wiki/`. Frontmatter carries `name`,
`order`, `oneLiner` and the `outline`; the Markdown body is the prose about the
thing itself, which renders above the build log.

`order` drives both the sort and the displayed "Project 01" label, so inserting
a build in the middle renumbers the rest automatically.

## Commands

| Command | Does |
|---|---|
| `npm run dev` | local server at localhost:4321, live reload |
| `npm run build` | static build into `dist/` |
| `npm run preview` | serve `dist/` exactly as Cloudflare will |
| `npm run verify` | both test suites against `dist/` — run after every build |

## Layout

```
src/
├── layouts/Base.astro        head, top bar, footer. The only layout.
├── pages/
│   ├── index.astro           home. Kyle's prose lives here — see §6.
│   ├── builds/index.astro    the builds directory
│   ├── builds/[build].astro  one page per build
│   └── rss.xml.js            feed
├── content/builds/*.md       ← a build: frontmatter + prose
├── content/log/*.md          ← build-log entries go here
├── content.config.ts         both collection schemas
├── data/
│   ├── videos.json           the 32 approved YouTube titles
│   ├── portrait.txt          headshot, WebP data URI
│   └── favicon.txt           favicon, PNG data URI
└── styles/site.css           all CSS, inlined into every page at build
public/                       og.png, robots.txt, _redirects — copied verbatim
scripts/                      verify.py, verify_site.py
```

## Non-obvious things

- **`build.inlineStylesheets: 'always'`** keeps the promise that each deployed
  page is one file with zero external requests. Don't remove it.
- **`smartypants: false`** stops Markdown curling apostrophes. The rest of the
  site uses straight ones; mixing them is visible. See the note in the config.
- **`.project-title` / `.entry-title` are classes, not tag selectors.** The same
  markup renders at different heading levels on different pages.
- **RSS item links must be absolute.** `@astrojs/rss` runs a relative link
  through the site's `trailingSlash: 'always'` and appends a slash after the
  fragment, quietly breaking every anchor. `verify_site.py` checks for this.
- **`public/_redirects`** keeps the retired `/building/` URL alive. It was
  indexed; the file is not decoration.
- **The video rotator is the only executing JavaScript on the site**, and it runs
  during parse so there is no flash of the fallback entry. The `<script>` in the
  head is `application/ld+json`, which is inert data, not code.
- Both pages were verified **pixel-identical** to the hand-built originals Kyle
  approved. If you change the CSS, re-run the comparison before shipping.
