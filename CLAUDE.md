# CLAUDE.md — kylecovan.com

You are an expert developer maintaining Kyle Covan's personal site at
**kylecovan.com**.

## READ FIRST

`docs/handoff.md` is the source of truth: hard constraints, design tokens, copy
rules, and decision history. **Read it before any change and update it after.**

- **Never undo anything in its §6 (Copy rules).** Every item there is a
  correction Kyle already made.
- §2 (Hard constraints) and §3 (Design system) are equally binding.
- `docs/deploy-status.md` — where the deploy and DNS stand, and what's still open.
- `docs/dns-records.md` — the verified DNS record inventory. Read before touching
  DNS; Kyle's email runs on Google Workspace through those records.

## Where it lives

| | |
|---|---|
| Local | `~/Projects/kylecovan-astro` |
| Repo | https://github.com/KyleCovan/kylecovan-site (public, branch `main`) |
| Host | Cloudflare Pages project `kylecovan-site` — auto-deploys on push to `main` |
| Live | **https://kylecovan.com** (also `kylecovan-site.pages.dev`) |
| `www` | 301 redirect rule → apex, path and query preserved |

An **Astro** project, not hand-written HTML. Two pages: `/` (Story, Approach,
Building summary, Contact) and `/building/`.

```
src/
  layouts/Base.astro          head, top bar, footer, the one inline script
  pages/index.astro           home
  pages/building/index.astro  the build-log page
  pages/rss.xml.js            RSS feed
  styles/site.css             ALL the CSS, once
  data/videos.json            the 32 video titles + urls
  data/projects.json          project names, one-liners, outlines
  data/portrait.txt           WebP data URI, 340px
  data/favicon.txt            PNG data URI, 64px
  content/log/*.md            build-log entries — one file per entry
  content.config.ts           the collection schema
public/                       og.png, robots.txt
scripts/verify.py             home-page suite
scripts/verify_site.py        site-level suite
```

- **All CSS lives once in `src/styles/site.css`.** Never duplicate it.
- **Build-log entries are Markdown in `src/content/log/`.** Adding one file is
  the whole publishing workflow — Astro renders the page, the index, the JSON-LD,
  the sitemap and the RSS feed from it.
- **Never hand-edit `dist/`.** It is build output.
- Nothing is generated into the source tree. `src/pages/building/index.astro`
  **is** edited by hand.
- `build_assets.py` (portrait/favicon/OG pipeline) and the source `headshot.jpg`
  are **not in the repo**. Recover them before any image work.

## After any change

```bash
source .venv/bin/activate    # required in a fresh terminal, for verify only
npm run build && npm run verify
```

Both suites must print **ALL CHECKS PASSED** before anything is pushed.
**Pushing to `main` deploys.** Cloudflare runs only `npm run build`; the verify
suites are a local gate and nothing enforces them on the server.

**If a design rule changes, update its test in the same commit — never delete
the assertion.** A stale assertion that gets deleted is how a rule quietly dies.

## Copy

**The biography paragraphs are Kyle's own words. Do not reword, tighten or
improve them.** Changes come from Kyle as exact text, or from options he picks.

The creed reads **"Striving to put Jesus Christ first"** — *put*, not *keep*.

Full copy rules, with the reasoning behind each one, are in `docs/handoff.md` §6.

## Design

Warm, minimalist, professional, generous whitespace. Cream background, warm slate
grays, terracotta accents. Serif headings, sans body, **system fonts only**.
**No cards, no borders.** Everything left-aligned in an 800px column and
**nothing is centred anywhere on either page.**

Each deployed page is one self-contained file with **zero external requests**.
**One executing script only** — the rotating video link. The JSON-LD blocks are
inert data, not a second script. (`og.png` is the documented exception: crawlers
fetch it, no visitor's browser ever does.)

WCAG AA contrast on every text/background pair, verified programmatically.

## Scope

This site is **personal**. Services, pricing and client work live on
**tapocanyon.com** and never appear here. The only connection is a single closing
line at the bottom of the home page.

## Working habits that have paid off here

1. **One copy per page — no version numbers in filenames.** Git solves this now.
2. **Read a file back after writing it.** A stray trailing space once sat inside
   a video title for hours because the write "succeeded" and nobody looked.
3. **Render before you rule.** The portrait's shape, crop and tightness were all
   decided from rendered comparison sheets, and all three would have gone
   differently on theory alone.
4. **Write the test before trusting the change.**
5. **Check the premise, not just the request.** Kyle asked for a four-page split
   and asked whether his SEO reasoning was right. It was half right, and the half
   he named pointed the other way.
6. **When a design rule changes, change its test in the same commit.**
