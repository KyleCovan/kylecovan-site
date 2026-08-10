# kylecovan.com

Personal site. Astro, deployed static to Cloudflare Pages.

**Hardware concept (not the site):** open root [`PIGEON.md`](PIGEON.md) → `docs/concepts/pigeon/` (Level B pigeon ornithopter).

**Read `docs/handoff.md` before changing anything.** It holds the hard
constraints, the design tokens, and — most importantly — the copy rules.
Section 6 lists every correction Kyle has made to his own words. Several of them
have been undone once already by a well-meaning rewrite.

## Publishing anything you write

One file, and one optional field decides where it lands.

```bash
# create src/content/writing/what-broke.md
---
title: "The version I threw away"
date: 2026-08-15
build: personal-ai-os     # OPTIONAL. Omit it and this is just a post.
---

Your words here. Plain Markdown paragraphs.

npm run build && npm run verify
git add -A && git commit -m "writing: what broke" && git push
```

- **With `build:`** → renders in full on that build's page at
  `/builds/<build>/#<filename>`, and is listed on `/writing/`.
- **Without it** → gets its own page at `/writing/<filename>/`.

Either way it lands in the JSON-LD, `sitemap-0.xml` and `rss.xml` with no other
edit. The filename is the URL, so name it for the URL you want and skip the date
prefix. You can add or remove `build:` later without rewriting anything.

**There is only ever one full copy of any text**, which is why a tagged post has
no second URL under `/writing/`. Don't "fix" that by giving it one.

Set `draft: true` to write ahead without publishing.

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
│   ├── writing/index.astro   the writing index — "Unless the Lord"
│   ├── writing/[post].astro  one page per UNTAGGED post
│   └── rss.xml.js            feed
├── content/builds/*.md       ← a build: frontmatter + prose
├── content/writing/*.md      ← everything dated goes here
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
