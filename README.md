# kylecovan.com

Personal site. Astro, deployed static to Cloudflare Pages.

**Read `docs/handoff.md` before changing anything.** It holds the hard
constraints, the design tokens, and — most importantly — the copy rules.
Section 6 lists every correction Kyle has made to his own words. Several of them
have been undone once already by a well-meaning rewrite.

## Publishing anything you write

One file. The house is **Unless the Lord** at `/writing/`. Essays and logs live
in one stream; a log is a kind inside that house, not a second blog.

```bash
# create src/content/writing/what-broke.md
---
title: "The version I threw away"
date: 2026-08-15
kind: log                 # OPTIONAL. Omit it (or essay) for a scarce essay.
project: Personal AI OS   # OPTIONAL free-text label. Not a second door.
---

Your words here. Plain Markdown paragraphs.

npm run build && npm run verify
git add -A && git commit -m "writing: what broke" && git push
```

- Every published post gets its own page at `/writing/<filename>/`.
- `kind: log` marks it on the index so a reader can skip logs without leaving.
- Unset `kind` means essay. Do not invent a new filename scheme for kinds.
- `draft: true` stays off public lists, the sitemap and the RSS feed.

**There is only ever one full copy of any text.** Old `/builds/` URLs redirect
into the house; they are not a second place to put the same post.

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
│   ├── writing/index.astro   Unless the Lord — essays and logs
│   ├── writing/[post].astro  one page per published post
│   └── rss.xml.js            feed
├── content/builds/*.md       ← names + one-liners for the home summary
├── content/writing/*.md      ← everything dated goes here
├── content.config.ts         both collection schemas
├── data/
│   ├── videos.json           the approved YouTube titles
│   ├── portrait.txt          headshot, WebP data URI
│   └── favicon.txt           favicon, PNG data URI
└── styles/site.css           all CSS, inlined into every page at build
public/                       og-2.png, robots.txt, _redirects — copied verbatim
scripts/                      verify.py, verify_site.py
```

## Non-obvious things

- **`build.inlineStylesheets: 'always'`** keeps the promise that each deployed
  page is one file with zero external requests. Don't remove it.
- **`smartypants: false`** stops Markdown curling apostrophes. The rest of the
  site uses straight ones; mixing them is visible. See the note in the config.
- **RSS item links must be absolute.** `@astrojs/rss` runs a relative link
  through the site's `trailingSlash: 'always'` and appends a slash after the
  fragment, quietly breaking every anchor. `verify_site.py` checks for this.
- **`public/_redirects`** keeps retired `/building/` and `/builds/` URLs alive.
  They were indexed; the file is not decoration. Destinations are `/writing/`.
- **The video rotator is the only executing JavaScript on the site**, and it runs
  during parse so there is no flash of the fallback entry. The `<script>` in the
  head is `application/ld+json`, which is inert data, not code.
- Nav is three pillars: **Kyle Covan · Unless the Lord · Contact.** Privacy is
  in the footer. Builds is not a nav destination.
