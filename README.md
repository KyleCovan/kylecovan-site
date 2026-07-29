# kylecovan.com

Two-page personal site. Astro, deployed static to Cloudflare Pages.

**Read `claude/kylecovan-handoff.md` in the Claude project before changing anything.**
It holds the hard constraints, the design tokens, and — most importantly — the
copy rules. Section 6 lists every correction Kyle has made to his own words.
Several of them have been undone once already by a well-meaning rewrite.

## Publishing a build-log entry

One file. That is the whole workflow.

```bash
# 1. create src/content/log/2026-08-15-what-broke.md
---
title: "The version I threw away"
date: 2026-08-15
project: personal-ai-os     # or second-brain
---

Your words here. Plain Markdown paragraphs.

# 2. check it
npm run build && npm run verify

# 3. ship
git add -A && git commit -m "log: what broke" && git push
```

The entry automatically appears on `/building/`, in the JSON-LD, in
`sitemap-0.xml`, and in `rss.xml`. Nothing else needs editing.

Set `draft: true` in the frontmatter to write ahead without publishing.

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
│   ├── building/index.astro  build log, both projects
│   └── rss.xml.js            feed
├── content/log/*.md          ← build-log entries go here
├── content.config.ts         entry frontmatter schema
├── data/
│   ├── projects.json         project names, one-liners, outlines
│   ├── videos.json           the 32 approved YouTube titles
│   ├── portrait.txt          headshot, WebP data URI
│   └── favicon.txt           favicon, PNG data URI
└── styles/site.css           all CSS, inlined into every page at build
public/                       og.png, robots.txt — copied verbatim
scripts/                      verify.py, verify_site.py
```

## Non-obvious things

- **`build.inlineStylesheets: 'always'`** keeps the promise that each deployed
  page is one file with zero external requests. Don't remove it.
- **`smartypants: false`** stops Markdown curling apostrophes. The rest of the
  site uses straight ones; mixing them is visible. See the note in the config.
- **`.project-title` / `.entry-title` are classes, not tag selectors.** The same
  markup renders at different heading levels on different pages.
- **The video rotator is the only executing JavaScript on the site**, and it runs
  during parse so there is no flash of the fallback entry. The `<script>` in the
  head is `application/ld+json`, which is inert data, not code.
- Both pages were verified **pixel-identical** to the hand-built originals Kyle
  approved. If you change the CSS, re-run the comparison before shipping.
