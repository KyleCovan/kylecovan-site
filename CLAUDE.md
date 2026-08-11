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
| Local | `~/1. Projects/kylecovan-site` — quote it, the folder name has a space |
| Repo | https://github.com/KyleCovan/kylecovan-site (public, branch `main`) |
| Host | Cloudflare Pages project `kylecovan-site` — auto-deploys on push to `main` |
| Live | **https://kylecovan.com** (also `kylecovan-site.pages.dev`) |
| `www` | 301 redirect rule → apex, path and query preserved |

An **Astro** project, not hand-written HTML. Nav: **Kyle Covan · Builds ·
Unless the L**ORD** · Contact**. Pages are `/` (Story, Builds summary, Writing
summary, Contact), `/builds/`, `/builds/<id>/`, `/writing/`, `/writing/<id>/`.

```
src/
  layouts/Base.astro          head, top bar, footer, the one inline script
  pages/index.astro           home
  pages/builds/index.astro    the builds directory
  pages/builds/[build].astro  one page per build
  pages/writing/index.astro   the writing index — "Unless the Lord"
  pages/writing/[post].astro  one page per UNTAGGED post
  pages/rss.xml.js            RSS feed
  styles/site.css             ALL the CSS, once
  data/videos.json            the video titles + urls
  data/portrait.txt           WebP data URI, 340px
  data/favicon.txt            PNG data URI, 64px
  content/builds/*.md         one file per build — frontmatter + prose
  content/writing/*.md        everything dated — posts and build-log entries
  content.config.ts           both collection schemas
public/                       og-2.png, robots.txt, _redirects
scripts/verify.py             home-page suite
scripts/verify_site.py        site-level suite
```

- **All CSS lives once in `src/styles/site.css`.** Never duplicate it.
- **One `writing` collection, not two.** A post with a `build:` field renders in
  full on that build's page; a post without one gets its own URL under
  `/writing/`. That is why Kyle never has to decide "log entry or blog post?" —
  he writes, and one optional field decides where it lands. **There is only ever
  one full copy of any text**, so nothing is duplicate content.
- **Build pages are pillar pages.** Description plus every post about that build,
  in one document. Splitting build writing onto separate URLs was considered on
  July 30 and rejected — see handoff §7.
- **`build:` is a `reference('builds')`.** A typo fails the build instead of
  silently orphaning the entry.
- **Substantively rewriting a post body means bumping its `date` / `updated`
  frontmatter.** The sitemap's `<lastmod>` is derived from frontmatter, not from
  build time (handoff §51), so an edited body with an unchanged date tells Google
  nothing changed and delays the recrawl. Typo and whitespace fixes don't count.
  **No test catches this** — `verify_site.py` checks each date against the
  frontmatter it describes, which catches a *wrong* date but never a *stale* one,
  because "did the body change since this date?" is a git-history question.
- **Never render a build's `prompts` array.** Those were the old "What the log
  will cover" bullets — a list of promises on a page with nothing behind it.
  They are now writing prompts for the prose body.
- **`.epigraph` is not the `h1`.** Each section page opens with a verse above
  its heading. The verse must never become the heading; see the note in the CSS.
- **`public/_redirects` keeps `/building/` alive.** That URL was indexed. Never
  delete a rule from that file without checking what still links to it.
- **Never hand-edit `dist/`.** It is build output.
- Nothing is generated into the source tree. Both files under
  `src/pages/builds/` **are** edited by hand.
- **Images are rebuilt, never hand-edited.** `build_assets.py` regenerates the
  portrait, the favicon and the share card from `headshot.jpg` and
  `headshot-favicon.jpg`:
  `source .venv/bin/activate && python3 build_assets.py`.
  The favicon has its own tighter crop of the same photo on purpose; read the
  note in that script before merging the two sources.
- **The share card's filename is versioned (`og-2.png`) and must change every
  time the image does.** iMessage, Slack, X and LinkedIn cache share cards by
  image URL, so reusing a filename means nobody ever sees the new card. Update
  **all five** references: `Base.astro` (×2), `index.astro` (×2), and
  `writing/[post].astro` (×1, the `BlogPosting.image`, added August 6).
  `verify_site.py` asserts the `og:image` URL resolves to a file that ships —
  but only the `og:image`, so the other four can go stale silently. Five
  hardcoded copies of one filename is the actual defect; a single shared
  constant is the fix, and it is a deliberate refactor rather than a drive-by.
- **The card's typography cannot be regenerated.** `build_assets.py` only
  replaces the photo inside it. Changing its *words* needs a design source that
  is still missing from this repo.

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
inert data, not a second script. (`og-2.png` is the documented exception: crawlers
fetch it, no visitor's browser ever does.)

WCAG AA contrast on every text/background pair, verified programmatically.

## Scope

This site is **personal**. **Services and pricing live on tapocanyon.com and
never appear here** — nothing on this site sells anything. The only connection is
a single closing line at the bottom of the home page.

**The work itself is a different question, and Kyle narrowed this rule on
August 4.** `/builds/` is his portfolio of things made, and it may include client
projects and projects outside Tapo Canyon's scope. Showing the work is allowed;
offering the service is not. If a build page starts reading like a pitch — rates,
packages, "hire me", a call to action — it has crossed back over the line.

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
