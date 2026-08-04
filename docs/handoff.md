# kylecovan.com — the source of truth

**Status:** Astro project, live at **https://kylecovan.com** on Cloudflare Pages.
DNS moved to Cloudflare July 29, 2026 and Google Workspace email survived intact.
**Handoff date:** July 29, 2026.

Ported into the repo from the claude.ai project on July 29, 2026 so that Claude
Code reads it directly. `CLAUDE.md` at the repo root is the short version and is
loaded automatically; this document is the long one. **When they disagree, fix
both.**

---

## Lessons that keep proving themselves

1. **One copy per page — no version numbers in filenames.** Once there were
   `index_1.html` through `index_10.html` and the newer-looking number held the
   older content. Git now solves this properly.

2. **Read a file back after writing it.** A stray trailing space sat inside
   video title #22 for hours because the write "succeeded" and nobody looked.

3. **Render before you rule.** The portrait's shape, its crop, and its
   tightness were all decided from rendered comparison sheets, and all three
   would have gone differently on theory alone. This held again on July 29:
   the favicon was *described* as fine and *looked* wrong the moment it was
   rendered at 16/32/64px beside a replacement.

4. **Write the test before trusting the change.** The two-page split shipped
   with three defects and the suite caught all three.

5. **Check the premise, not just the request.** Kyle asked for a four-page
   split and asked whether his SEO reasoning was right. It was half right, and
   the half he named pointed the other way.

6. **When a design rule changes, change its test in the same commit.**
   July 29: the mobile video line moved above the nav, which broke `verify.py`'s
   flush-left assertion *by design*. The assertion was rewritten, not deleted.
   Hours later the line was centred and then un-centred; the test tracked both
   moves. A stale assertion that gets deleted is how a rule quietly dies.

---

## 1. What this site is

Kyle Covan's personal site: who he is, what he believes, and what he's building
in the open.

**Scope boundary — important.** Commercial services, pricing, and the client FAQ
live on **tapocanyon.com**. kylecovan.com is personal. The only connection is a
single closing line at the bottom of the home page.

**The design reference is [andrewng.org](https://www.andrewng.org/).** What was
taken: a horizontal nav of short section labels, and a hero with the photo left
of the name. What was *not*: its multi-company structure, its density, or its
centred layout. The 800px left-aligned column stays.

### The architecture decision — settled, don't relitigate

Kyle asked to split all four nav pillars onto separate pages for SEO/AEO/GEO.
**He was half right, and the half he named pointed the other way.**

- **Classic SEO:** separate URLs let you target separate queries, but the
  guidance names portfolios and personal brands as the case where one page is
  *right*.
- **AEO/GEO:** the premise is backwards. Generative engines work at the passage
  level; the recommended pattern is a **pillar page answering sub-questions
  inside one document**, not one-topic-per-URL silos.
- **Measured word counts** turned opinion into arithmetic:

  | Section | Words | As its own URL |
  |---|---|---|
  | Story | 276 | thin |
  | Approach | 109 | very thin |
  | Building | 462 | healthy |
  | Contact | 23 | very thin |

**Outcome: a hybrid.** Story, Approach and Contact on the home page; Building on
its own page. Splitting the remaining three is a decision to re-make
deliberately with fresh word counts, not a correction of an oversight.

---

## 1b. The Astro migration — DONE

Completed July 29, 2026. What it bought, all of it now real:

- **File-based routing.** `/building/` is an extensionless URL for free.
- **Content collections.** A build-log entry is a Markdown file in
  `src/content/writing/` (it was `src/content/log/` until July 30). Astro
  renders the page, the index, the JSON-LD and the RSS feed from it. Posting friction was the thing most likely to kill the
  build log; it is now one file plus `git push`.
- **One layout.** The CSS exists once. `build_site.py`, the duplicated
  stylesheet, and the byte-identical drift check are gone as *concepts* —
  though `verify_site.py` still asserts the two pages' inlined CSS matches,
  which is now a free tautology rather than a real risk.
- **Zero JS by default**, which matches the scoped-JS constraint instead of
  fighting it.
- **`build.inlineStylesheets: 'always'`** preserves zero-external-requests in
  the built output.

**What it cost, stated honestly.** "No build step" is formally dead — it was
already bent by `build_site.py`. The constraint is now *"each **deployed** page
is one self-contained file"*, which is the property Kyle actually cares about.
The site is also no longer readable as a single file; source is spread across a
layout, two pages, a stylesheet and four data files. Real legibility traded for
real maintainability.

**What ported over unchanged:** every design token in §3, every copy rule in §6,
the JSON-LD graph, the OG image, the favicon and portrait pipeline's *output*,
and both verify suites — they check built HTML, so they now run against `dist/`.

---

## 2. Hard constraints

| Constraint | Why |
|---|---|
| **Each deployed page is one self-contained file.** All CSS inlined into a style tag, the one script inline. | Reworded from "one file per page, no build step" — Astro builds, but what a visitor receives is still exactly one request. |
| **Zero external requests at page load.** No web fonts, no CDN, no analytics. Portrait and favicon are data URIs. | "Load instantly." Cloudflare's analytics is server-side, so traffic data costs nothing on the page. |
| **JavaScript is limited to one thing.** The single inline script that rotates the video link. | The nav is plain anchors; `scroll-behavior: smooth` does the easing in CSS. |
| **No cards, no borders, no complex graphics.** | Structure comes from whitespace and typographic hierarchy. The portrait's 3px radius is the outer limit. |
| **System fonts only.** | Zero-latency text rendering. |
| **Left-aligned content in an 800px centred container.** | Exceptions are bounded and enumerated in §3/§5. There is currently **nothing centred anywhere on either page** — see the July 29 revert in §5. |
| **WCAG AA contrast on every text/background pair.** | Verified programmatically on every page. **Zero failures is the assertion; the node count is not.** The old suite hardcoded "46 nodes and 60 nodes", which meant adding a paragraph failed the test for a legitimate reason and trained you to edit the assertion. Rewritten July 30 — see §8. |

### `og-2.png` — the documented exception

Fetched by crawlers when the link is pasted into Slack, iMessage, X or LinkedIn.
**No visitor's browser ever requests it.** The absolute URL in the meta tag is
required — crawlers won't resolve a relative path or read a data URI.

### JSON-LD is not a second script

Both pages carry `<script type="application/ld+json">`. **It is inert data.**
Browsers never execute it and the page renders identically with JS disabled. It
is flagged here rather than slipped in, because it *looks* like a violation on a
grep. A second genuinely **executing** script remains a deliberate decision to
make — which is exactly why the dark-mode toggle was declined (§7).

**Building-page structured data is derived from the content collection**, so the
markup physically cannot claim a headline or date the page doesn't show.
`verify_site.py` enforces the same rule from the other side.

The `@id` `https://kylecovan.com/#kyle` is a stable identifier;
`/building/` carries a stub `Person` referencing it rather than redefining Kyle.

---

## 3. Design system

### Palette

| Token | Value | Use | Contrast on cream |
|---|---|---|---|
| `--cream` | `#FBF8F2` | Page background | — |
| `--ink` | `#302D28` | Headings, bold lead-ins, email | 12.93:1 |
| `--ink-soft` | `#5C574E` | Body copy | 6.77:1 |
| `--ink-faint` | `#6E675C` | Eyebrows, nav, watching line, log labels, colophon | 5.27:1 |
| `--terracotta` | `#9E4A28` | Creed, project numbers, entry dates, hover, separators | 5.72:1 |
| `--terracotta-light` | `#B2673F` | Decorative marks only | decorative |
| `--underline` | `rgba(178,103,63,0.24)` | Link underlines | decorative by design |
| `--wash` | `rgba(178,103,63,0.15)` | `::selection` | — |

`--underline` is the single control for all *prose* link underlines. Retune
every link at once by changing that alpha; never set `text-decoration-color` on
individual link rules.

**One documented exception:** `.topnav a` carries `text-decoration: none` at
rest. Hover and focus restore the full terracotta underline. Don't let it spread.

`--terracotta` was deliberately darkened from a lighter orange that failed AA at
small sizes (4.35:1). Keep `--terracotta-light` for marks only, never for text.

**July 29 — the video link stays `--ink-faint`, same as the nav.** Kyle asked
whether colouring it would help it stand out. It was declined and he agreed.
Three reasons, recorded so it isn't reopened casually: the nav and the video
line are deliberately the same size and colour so they read as peers rather than
one outranking the other; terracotta is the only palette-legal option and **the
creed is the only terracotta text on the home page** — a second, louder
terracotta *above* it would make a YouTube link the first coloured thing a
visitor sees; and the two are already differentiated, because nav links drop
their resting underline and the video link keeps it.

### Type

- `--serif`: `ui-serif, "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, "Times New Roman", serif` — headings, entry titles, email, closing line.
- `--sans`: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Helvetica, Arial, sans-serif` — everything else.
- Body: `clamp(1.0125rem, 0.97rem + 0.22vw, 1.125rem)` / line-height `1.75`.
- All headings are `font-weight: 400`. Weight contrast comes from size and colour.
- Eyebrows: `0.7rem`, weight 600, `letter-spacing: 0.22em`, uppercase.
- **Nav and the watching line are both `0.85rem` sans in `--ink-faint`** — see above.
- h1: `clamp(2.6rem, 9vw, 3.9rem)`, reduced when the portrait moved beside it.

### The portrait

- **Square, 3px radius — not a circle.** Layout decision, not taste: the
  square's left edge sits exactly on the 800px column edge that every heading
  below uses. A circle touches that edge at one tangent point and reads as
  floating inboard. Both were rendered side by side before deciding.
- Slot is `clamp(104px, 17vw, 156px)`.
- **The source ships at 340px, rebuilt from `headshot.jpg` by
  `build_assets.py`.** ~~Crop B, cut down from a 360px crop because the original
  was lost.~~ **Superseded August 3, 2026:** Kyle supplied a new photograph, a
  381px square, and it is in the repo. The old warning not to scale the CSS box
  past ~170px without a fresh export no longer binds the same way — a genuine
  re-export is possible again, and a bigger slot only needs `PORTRAIT_PX` raised
  in the script.
- **The July 29 photo was a grey studio headshot; this one is outdoors.** That
  is why the favicon now has its own source; see below.
- Format is WebP, quality 80, no JPEG fallback. The source is **not** pre-masked;
  the shape lives entirely in CSS.
- Below `34rem` the hero stacks to a single flush-left column.

### The favicon

**Square, re-cut from the same portrait crop, July 29.** It had been a circle
with cream corners — a leftover from before the portrait was squared — which on
iOS read as a circle sitting inside a white-cornered box. Rendered old-vs-new at
16/32/64px before changing it. Keeping it cut from the *same* crop as the
portrait was deliberate: two separately-tuned crops of one face drift.

**Amended August 3, 2026 — the favicon now has its own source file.** The new
portrait is outdoors, and at 16px the fence and foliage swallowed the face
entirely; rendered at 16/32/64 again before deciding, exactly as on July 29.
`headshot-favicon.jpg` is a **tighter crop of the same photograph**, which is
what keeps the original rule's intent: one photograph framed twice on purpose,
not two photographs drifting apart unattended. **Replace both together or not at
all.** `build_assets.py` falls back to the portrait crop if the favicon source
is missing, and says so on stdout rather than silently.

Honest limitation, unchanged: legible at 32px, mush at 16px. The "K" monogram
alternative is preserved commented-out.

### Heading classes — not tag selectors

`.project-title` and `.entry-title` carry the styling for project and log-entry
headings. They are **classes rather than `.project h3`** because the same markup
renders at different heading levels on the two pages — `h3`/`h4` on the home
page under a section `h2`, `h2`/`h3` on `/building/` where the page's own `h1`
replaces that `h2`. Tag selectors produced an `h1 → h3` skip, which screen
readers and crawlers both read as a structural error.

`.masthead-page h1` takes the **h2 scale**. `.topnav a[aria-current="page"]`
darkens to `--ink` rather than terracotta — terracotta there would compete with
the creed.

### Rhythm

- `--measure: 800px` — `.page` max-width, border-box, centred.
- `--gap-section: clamp(5rem, 13vh, 9rem)`.
- Page padding: `clamp(4.5rem, 15vh, 9rem)` top, `clamp(1.5rem, 7vw, 2.5rem)` sides.
- **Below 34rem the top padding drops to `clamp(2.25rem, 6vh, 3.25rem)`.**
  Added July 29: `15vh` on an 844px-tall phone is ~127px of empty cream above
  the nav, which Kyle correctly read as a bug rather than as whitespace.
- `section[id], article[id] { scroll-margin-top: 2.5rem }`.
- No horizontal overflow down to 320px, including with the longest video title.

---

## 4. Page structure

### Home page

```
topbar        nav left, video line immediately after it
masthead      portrait left, name / creed / role right
#story        eyebrow "Story"      h2 Laying music down            (5 paragraphs)
#approach     eyebrow "Approach"   h2 Startup operations, now AI orchestration
#building     eyebrow "Building in public" — summary + two projects, each
                                   deep-linking to its anchor on /building/
#contact      eyebrow "Contact"    h2 Reach out anytime
colophon
```

### `/writing/` — nav label "Unless the L**ORD**", URL `/writing/`

```
topbar        nav only, Unless the Lord marked aria-current, no video line
masthead-page epigraph Psalm 127:1a + cite + h1 + list of posts
follow        "Follow along" + RSS · YouTube · X · LinkedIn
more          back to kylecovan.com
```

The label is expressive and the URL is plain **on purpose**: URLs are functional
and someone typing one guesses "writing", not a psalm. The name does its work on
the page.

**One `writing` collection, not two.** A post with a `build:` field renders in
full on that build's page and is *listed* here. A post without one gets its own
page at `/writing/<id>/`. Kyle never decides "log entry or blog post?" when he
sits down — he writes, and one optional field decides where it lands. The tag
can be added or removed later without rewriting anything.

**There is exactly one full copy of any text on the site.** That is why
`/writing/[post].astro` skips tagged posts in `getStaticPaths`. Giving them a
second URL would be duplicate content, which §1 is unambiguous about.

### The epigraphs — the verse is never the `h1`

Both section pages open with a verse above the heading: Ecclesiastes 11:1 on
`/builds/`, Psalm 127:1a (ESV, first clause only, at Kyle's instruction) on
`/writing/`. **The verse is a `<p class="epigraph">`, not the `h1`, and must
never become one.** Kyle asked for the verse on top; this gives that layout with
the semantics intact. An `h1` reading "Cast your bread upon the waters" on a page
about software is a mismatch Google punishes, and a screen-reader user
navigating by heading would hear a verse instead of a page name.

**LORD is small-capped** — how every major English translation sets the divine
name, so it is correct typesetting rather than decoration. Only `ord` is
wrapped in `.sc`, so the underlying text stays "Lord" for copy/paste and screen
readers. Kyle asked for it in the nav *and* the verse, after being told fonts
without true small-cap glyphs synthesise them and read slightly light. Verified
in a render at nav size: correct on macOS.

### `/builds/` — the directory

```
topbar        nav only, Builds marked aria-current, no video line
masthead-page epigraph Ecclesiastes 11:1 + cite + h1 + lede
project 01    Personal AI OS — one-liner, entry count, "Read more"
project 02    Second Brain — one-liner, "first entry coming soon", "Read more"
follow        "Follow along" + RSS · YouTube · X · LinkedIn
more          back to kylecovan.com
colophon
```

**This page deliberately does not repeat each build's outline or its log.** Those
live on the build's own page. Duplicating them would put identical paragraphs on
two URLs, which is the one thing §1's SEO reasoning is unambiguous about.

**Each `<article>` keeps `id="<build-id>"`.** `/building/#personal-ai-os` was a
real published URL. A server redirect cannot preserve a fragment — browsers never
send it — so the id is what makes the old deep link land on the right build
rather than the top of the page. Don't remove them.

### `/builds/<id>/` — one page per build

```
topbar        nav only, Builds marked aria-current, no video line
masthead-page eyebrow "Project 01" + h1 build name + lede one-liner
prose         the Markdown body — the thing itself. EMPTY on both builds today.
outline       "What the log covers" / "will cover"
build log     .log-label + dated entries, newest first, each with an id
follow        "Follow along" + RSS · YouTube · X · LinkedIn
more          all builds
colophon
```

**Prose first, log second.** That order is the point of the July 30 restructure:
someone who has never heard of the project reads what it *is* before they read a
changelog about it. The body is empty on both builds until Kyle writes it, and an
empty body renders nothing, so the pages read as they did on `/building/`.

**IDs are on the sections; `aria-labelledby` points at `*-heading` ids on the
h2s.** Don't collapse these into one id per heading — the nav would then scroll
to the heading rather than the section, losing the eyebrow.

**Each project carries its own "Read the build log" link**, deep-linking to that
project's anchor. A single trailing link used to sit after both articles where
it read as belonging only to Project 02. Kyle caught that. Keep them symmetric.

**The Building page deliberately carries no portrait and no video line.** The
rotating link is the home page's signature.

### ~~When each project gets its own URL~~ — DONE July 30, trigger retired

The old rule was: **each project page needs two log entries before it earns its
own URL**, on the same thin-page test as §1. That rule was **retired rather than
met**, and the reasoning is recorded here so it isn't reinstated by accident.

The trigger assumed a project page is *an outline plus whatever entries have
accumulated*. On that model the page genuinely does stay thin until entries pile
up, and the rule was correct. The July 30 restructure changed the model: a build
page is now **prose about the thing itself, written once** — what it is, why it
exists, how it's built, a decision worth explaining, what broke. That is
substantial from the day it is written, and it does not depend on entry count.

**The old rule was measuring the wrong thing.** It is not a rule that was broken;
it is a rule whose premise stopped being true. What has *not* changed is the
principle underneath it — **tooling getting easier does not make a thin page less
thin.** That still applies, and it is why the build pages carry prose rather than
just being an outline moved to its own URL.

The shape §4 predicted was right: `getStaticPaths` over the collection, one new
file. It landed as `src/pages/builds/[build].astro`.

**The honest caveat:** the prose is empty on both builds today, so until Kyle
writes it those two pages are exactly as thin as the old rule feared. The
structure exists so he has somewhere to write into. **This is the reason commit A
was not pushed on its own** — see §7.

---

## 5. The top bar

### The nav

Four pillars: **Kyle Covan · Builds · Unless the L**ORD** · Contact.**
Rebuilt July 30 from Story · Approach · Building · Contact. Still four.

**Every pillar is now a real destination.** Contact is the one remaining
in-page anchor, and off the home page it becomes `/#contact`.

**"Building" became "Builds".** Kyle caught the tense problem: a finished
project sitting under a present-progressive verb is a contradiction, and it gets
worse as more things finish. "Builds" is a noun that commits to neither state.
The old URL redirects; see `public/_redirects`.

**Story left the nav.** Kyle spotted that it pointed at an anchor on the page you
are already standing on — a scroll-to-here rather than a destination — while
**nothing in the nav said "home" at all**; the only way back was a text link at
the very bottom of the page. His name now does that job and the site gets the
wordmark it never had. `#story` stays in the HTML, so `/#story` still resolves.

**Approach left the nav**, and its 109 words were **moved, not deleted** — see §6.

Considered and rejected: five pillars. The original reason (five would promote
two barely-started build logs) no longer applied, but four still reads better and
Story and Approach both had somewhere better to be.

### The rotating video link

31 `{title, url}` objects in `src/data/videos.json`, serialised into an inline
`<script>` placed immediately after the `.topbar` markup. **Placement is
deliberate: the script runs during parse, before first paint**, so the random
pick is swapped in with no flash of the default. Moving it to the end of
`<body>` or wrapping it in `DOMContentLoaded` reintroduces the flash.

**Graceful degradation:** entry 01 ships hardcoded as a real, valid link, so the
page works with JS disabled.

**The link opens in a new tab** — `target="_blank" rel="noopener noreferrer"`.
The `noopener` matters: it stops the opened tab getting a handle on the page.

### Layout — rewritten July 29, twice. Read this before touching it.

**Desktop: `justify-content: flex-start`, `gap: 0.8rem 1.4rem`.** The video line
sits **directly after "Contact"**, on the same column gap the nav uses between
its own items.

It was `space-between` until July 29, which pinned the line to the column's far
right edge. On a 1440px laptop that left a wide gap between "Contact" and the
line, and Kyle read the two as unrelated rather than as one utility row. Tuned
by eye: 2.2rem read as detached, 1.8rem was closer, **1.4rem is what he chose.**
What keeps it from reading as a fifth nav pillar is everything other than
spacing — it is a `<p>` not a nav `<a>`, it keeps the resting underline the nav
links drop, and it is the only link in the row that leaves the site.

**Phones (below 34rem): the top bar becomes a column and the video line moves
ABOVE the nav, still flush left.** Below 34rem the two cannot share a row; the
line used to wrap *underneath* the nav, where it read as an orphaned tail of it.

**It was centred for a few hours on July 29 and then reverted, at Kyle's
choice.** Recorded because the reasoning matters: moving it above the nav was
the fix; centring was a separate change solving nothing, and it made the video
line the only element on either page not sitting on the column's left edge.
Wrapping settled it — 8 of 32 titles wrap at 320px, and centred two-line text
goes ragged on both sides while left-aligned wraps break cleanly against the
same edge the nav uses. **`verify.py` now asserts above-nav *and* flush-left on
phones**, so a drift back to centred fails the suite rather than passing quietly.

### `flex: 0 0 auto` on `.watching` — still load-bearing

```css
.watching { flex: 0 0 auto; max-width: 100%; }
```

The box is content-width and **refuses to shrink**. A title that fits sits on
the nav's line; a title that doesn't **can't shrink, so it wraps to its own flex
line** — and under `flex-start` that lands it flush left, on the same edge as
the nav and every heading below.

`flex: 0 1 auto` with a `min-width` looks equivalent and isn't: the box then
stays min-width wide even for a three-word title, so short titles float
mid-row. That bug shipped briefly and was caught in a render. Don't go back.

`max-width: 100%` is *containment*, not the 46ch cap that was removed. Without
it a long title on a narrow screen pushes past the column and scrolls the page
sideways.

### What survives from the old §5

- **No width cap.** The 46ch cap was the sole cause of desktop wrapping.
- **No `::before` hairline.** It indented the first line by 36px while wrapped
  lines started flush left, reading as a broken hang.
- **Speaker attributions stay stripped.** Trailing credits (`| John MacArthur`,
  `| Paul Washer`, `: R.C. Sproul`, `| @WesHuff`, `| Costi Hinn`,
  `- Tim Keller on the Resurrection`) were removed from 9 titles with Kyle's
  approval. **Apply the same rule to any video added later: keep the subject,
  drop the credit.**

**Measured wrapping:** 0/32 at 1440 and 768, 2/32 at 430, 4/32 at 390, 8/32 at
320. If Kyle later wants zero wrapping on phones, the next lever is trimming the
~6 longest titles to roughly 38 characters; the Psalm 1 quote is the hardest
case and should be raised with him rather than cut unilaterally.

**Normalizations applied to the source list**, all flagged to Kyle:
`?si=…` share-tracking tokens stripped from all 32 URLs; the straight/curly
quote mismatch in the "I feel more like myself" title fixed; the non-breaking
space in `My testimony is Galatians 2:20...` preserved from the source.

**July 29 title edits, both at Kyle's request:**

- **The 🥹 emoji removed** from `"I feel more like myself."` There are now zero
  emoji in the list.
- **`Can I Trust the Bible - Episode 3: The Council of Nicaea` →
  `Can I Trust the Bible: The Council of Nicaea`.** Episode label dropped and
  the hyphen with it; the colon was kept because it reads as *title, then
  subject*, which is what the two halves are. Also 12 characters shorter, so one
  fewer title wraps on a phone.

`verify.py` reads the titles out of the **built HTML**, so title edits need no
test update.

---

## 6. Copy rules

**The bio paragraphs are Kyle's own words. Do not reword, tighten, or "improve"
them.** Any future copy change should come from Kyle as exact text, or from
options he explicitly picks.

### The creed line

**"Striving to put Jesus Christ first."** Changed from "keep" to "put" on
July 28 at Kyle's request, matching his YouTube channel description and echoing
the bio line "more time, energy, and desire to **put** Jesus Christ first in my
life" exactly. Changed in three places: `.creed`, the `og:image:alt` meta, and
the share-card source.

### "Laying music down" — four paragraphs

Roughly ten passes with Kyle on July 28. **Every one of the following was a
specific correction Kyle made. Do not undo any of them.**

- **"My prayer is that I approach this new work…" is a petition, not a claim.**
  The most important line in the section. A draft read "I approach this new work
  with reverence…"; Kyle changed it because the declarative asserts he *has* the
  posture. The prayer framing asks for it. Never tighten this back to a
  statement — the humility is the entire point.
- **"For me the benefit came immediately. I had more time, energy, and desire to
  put Jesus Christ first in my life."** Three corrections converged here. Kyle
  insisted the change was literally immediate, not "almost." He objected that
  opening with "Immediately" implies anyone who lays something down gets the
  same result — "For me" guards the claim without deleting the fact, so keep
  both halves. He replaced the abstract "more space" with the three things he
  actually gained. Note the deliberate echo: he "poured my energy into music" in
  the first sentence and gets energy back here. Don't break that pairing to
  avoid repetition.
- **"aim to help others" — not "help others."** Kyle hasn't started doing this
  yet. The hedge is factual, not modesty. Same reason "Today I build AI agents
  and automations" describes what he actually builds rather than claiming
  clients.
- **"the appetite for creating music" — not just "the appetite."** The bare
  version implied he wants nothing to do with music at all; what left him was
  the appetite to *make* it. Narrow and keep it narrow.
- **"So I gladly (and gratefully) laid music down."** Parentheses are his,
  verbatim. So is "music" — he replaced "laid it down" because paragraph one
  leaned on "it" too heavily. There is now exactly one standalone "it" in the
  section ("how much it pulled my focus"). Keep it that way.
- **The nine-month gap is load-bearing.** An earlier draft implied the new
  direction arrived right after he quit. It took about nine months, and the
  not-knowing in between is the point of paragraph two. "Other changes were
  underway too" is deliberately unspecific; don't fill it in. It's "long-term
  work" and "wasn't sure" rather than "didn't know."
- **"In God's timing, the desire and drive to learn and build AI surfaced."**
  Previously began "Then the desire…". Kyle rejected that: following "We had
  recently moved across the country," *then* read as *therefore* and handed the
  credit to the move. Any transition implying circumstances caused the change is
  wrong here.
- **It is "Jesus Christ," not "Christ."** Used everywhere on the page.
- **No em dashes in these paragraphs.** The em dashes elsewhere (project
  one-liners, outline items, `.log-status`) were deliberately left, since those
  are structural rather than prose. He was told this and did not ask for a sweep.
- **Contractions.** "don't," not "do not," page-wide.
- **The word "space" is gone from the page entirely.** Don't reintroduce it, or
  "In that quiet."
- **Paragraph breaks are Kyle's.** Do not merge them.

### The Anna paragraph

> I am deeply grateful for my wife, Anna. She has been my constant partner,
> supporter, and helper since long before we even started dating, standing by me
> in every step of this journey.

**Kyle's exact words, verbatim.** Note "I am," not "I'm" — the page-wide
contraction sweep does *not* apply to text Kyle supplied directly.

**It sits last in the Story section on purpose.** "Every step of this journey"
looks back over the whole section, so it only lands correctly once all three
beats have been read. Placing it earlier reads more naturally sentence-to-
sentence but breaks the three-beat arc and makes the closing line about AI the
section's last word instead of gratitude. **Don't move it and don't reword it.**

### "Startup operations, now AI orchestration" — MOVED July 30, not deleted

**These two paragraphs now live at
`src/content/writing/startup-operations-now-ai-orchestration.md`**, verbatim,
as the first post. Not a word changed. The Approach section and its nav pillar
were retired; the words were promoted to a post with room to breathe rather than
being cut. **Every rule below still governs them and travelled with them as a
comment at the top of that file.** If the post is ever edited, read them first.

1. **No governing-metaphor language for the professional experience.** A draft
   read "That is the lens I bring to everything I build now." Kyle cut it: for
   him the lens is Jesus Christ. Avoid "lens," "worldview," "my philosophy,"
   "what guides me." Watch "everything" too — it totalizes.
2. **No second person.** A previous version read "I partner with your team…".
   That is client-facing sales copy and belongs on tapocanyon.com.
3. **No claims Kyle can't personally vouch for.** A draft read "It's rarely the
   big decisions." Kyle cut it: it asserts something about businesses in general
   that he has no basis to know. Is it a fact about the world, or a report of
   Kyle's experience? Only the second is allowed.
4. **"Managers of agents" is Kyle's idea and the heart of the paragraph.** It
   states what automation is *for* — the person isn't removed, they move up a
   level. Keep the human on the page.

Also: "automate only where it earns its place" — don't soften "only." "Done
well, a business gets more out of what it already has" is his ROI point stated
deliberately without the vocabulary; "ROI," "efficiency," and "returns more on
what it spends" were all drafted and set aside as too tapocanyon-flavoured.
"Done well" is a conditional, not a promise.

**Open thread — the concrete version.** Kyle considered naming three real
examples of friction from his startup years and kept it abstract because the
specifics have to be things he actually witnessed. Two drafts already died this
way. **Don't invent them on his behalf.**

### The closing tapocanyon.com line

> Tapo Canyon is where I work with clients.
> *This page is personal. That one is for business.*

**The note line is untouchable.** Dry, self-aware, and it explains the entire
two-site architecture in eight words. Kyle asked for it back verbatim after a
draft replaced it. Never rewrite it.

The line above it is deliberately plain — a straight setup so the dry note lands
as the punchline. Declarative and first person: imperatives ("visit," "head over
to") smuggle a *you* back in and were rejected on exactly that ground.

**July 29: "Tapo Canyon" is no longer a hyperlink.** tapocanyon.com does not
resolve — the link was a dead end for readers and a broken outbound link for
crawlers. **Kyle's sentence is untouched, word for word; only the `<a>` was
removed**, and a comment in `src/pages/index.astro` says to restore it the day
that site goes live.

**The line must fit on one line, and that is a font-metrics problem, not a
copy-length problem.** `ui-serif` resolves differently on every OS. Keep the
sentence at ~90% or less of the measure in a wide serif; it currently sits at
**49%**. `.closing` carries `text-wrap: balance` as the backstop; don't swap it
for `pretty`.

### "Follow along" — /building/, added July 29

> **FOLLOW ALONG**
> RSS · YouTube · X · LinkedIn

**A label and four links. No sentence, on purpose.** The July 28 handoff flagged
the old version of this block as *the only prose on the site not written by
Kyle*, and left it for him to approve or rewrite. The cleanest resolution wasn't
a better sentence — it was no sentence. Every word on both pages is now his.

RSS is first because it is the only one of the four that is *this log* rather
than Kyle generally. **Left-aligned**, like everything else in the column; Kyle
asked whether it should be centred and agreed it shouldn't.

### The masthead

Name / creed / role, beside the portrait. Kyle considered adding four capability
areas under his title and decided they belong on tapocanyon.com. Three reasons
still valid: a four-phase process arc is methodology and methodology is the
business side; a fourth line means the creed is no longer the last thing read
before scrolling; and Kyle described these as areas he *wants to excel in*,
which a masthead would render as an accomplished claim. **Don't reopen.**

### The build log — Project 01, entry one

Written from Kyle's dictated answers, shaped but not invented. Covers four of
the five outline beats. **"What broke" is deliberately uncovered** — Kyle didn't
answer that one, and an invented failure story would be the worst possible thing
to put in a build log.

---

## 7. Open TODOs

1. ~~**Google Search Console + sitemap submission.**~~ **Done August 3, 2026.**
   `https://kylecovan.com/sitemap-index.xml` is submitted and accepted; seven
   URLs, every one verified 200 beforehand. **The field wants the full URL, not
   a path** — this is a **Domain** property, so entering `sitemap-index.xml`
   alone returns *"Invalid sitemap address"*. That error is client-side
   validation firing **before** Google fetches anything, so it says nothing
   about the sitemap itself; it reads like a broken file and isn't one.
   `public/robots.txt` also declares the sitemap, so discovery never depended
   on this submission — what it buys is the coverage reporting.
   See `docs/deploy-status.md` Step 5.
2. **A DMARC record.** There is currently none. See `docs/deploy-status.md`.
3. ~~**"What broke" for Project 01.**~~ **Done August 3, 2026.** Dictated by
   Kyle. He answered it with his own understanding breaking down and his working
   habits, not with software failures, and the section is ordered to keep it
   that way. See the note in `src/content/builds/personal-ai-os.md`.
4. ~~**Project 02's first entry.**~~ **Done August 3, 2026** —
   "Four AI operating systems in one vault, and I only knew about one". The
   `log-status` line on `/builds/llm-wiki/` disappeared on its own the moment
   the file existed. (Note the stale references this entry used to carry: the
   field is `build:`, the value is `llm-wiki` not `second-brain`, and entries
   live in `src/content/writing/`, not `src/content/log/`.)
5. **Restore the Tapo Canyon link** when that site resolves.
6. **Dark mode — decided, deferred.** **Automatic via `prefers-color-scheme`,
   no toggle.** A toggle needs a second executing script plus persistence,
   breaking the one-script rule, and needs a visible control on a page built with
   no chrome; avoiding a flash of the wrong theme would need a render-blocking
   script in the `<head>`, which is worse. The honest counterpoint Kyle accepted:
   automatic gives the visitor no way to override. It is a real design pass —
   every token needs a dark counterpart, terracotta most of all since it was
   darkened specifically to pass AA on cream, and the portrait backdrop and
   `og.png` are both light.
7. ~~**`build_assets.py` and `headshot.jpg` are not in the repo.**~~
   **Resolved August 3, 2026.** Both are in the repo now. One command rebuilds
   every image on the site from one source file:
   `source .venv/bin/activate && python3 build_assets.py`. Pillow was added to
   the venv for it. The script deliberately does **not** redraw `og.png`: it
   paints out the photo box and composites the new portrait in, leaving every
   text pixel alone, because the card's typography was set in a design tool
   that is still not in this repo. **If the card's WORDS ever need to change,
   that source is still missing.** Note also that the July 29 warning about not
   scaling the CSS box past ~170px no longer applies the same way: the portrait
   now comes from a fresh 381px square export rather than crop B of a lost
   original, so a genuine re-export is possible again.
8. ~~**Cloudflare rewrites `robots.txt`.**~~ **Resolved July 30, 2026** — Kyle
   disabled Managed robots.txt in Cloudflare's AI Crawl Control and set AI-bot
   blocking to "Do not block." Training crawlers are now allowed by choice.
   History and the settings map: `docs/dns-records.md`.

**Optional, not requested:** a current-section highlight *within* the home
page's nav (needs JS and an IntersectionObserver, so a deliberate decision
against the scoped-JS rule, not a drive-by addition).

### The July 30 restructure — where it stands

Agreed with Kyle in full; being built in three commits, each shippable alone.

| | State |
|---|---|
| **A — `/builds/`** | **Built, both suites green, NOT pushed.** Collection, per-build URLs, redirect, RSS fixed, verify rewritten. |
| **B — `/writing/`** | **Built, both suites green, NOT pushed.** One `writing` collection with an optional `build:` tag, `/writing/` + per-post pages, epigraphs, small-caps LORD, nav rebuilt, Approach moved to a post, `second-brain` renamed `llm-wiki`, `prompts` no longer rendered. |
| **C — copy** | **In progress.** Lede deleted. Personal AI OS has prose for "what it is" and "how it's built", dictated by Kyle and shaped. `kylecovan.com` added as build 03 with a full draft assembled from this document. |

**Exactly what is left, July 30:**

1. **Kyle reviews two drafts.** `src/content/builds/personal-ai-os.md` and
   `src/content/builds/kylecovan-com.md`. Both carry a DRAFT comment naming
   their source. Neither is his final voice until he says so.
2. **Personal AI OS — "what broke".** Still unanswered after three sessions.
   **Nothing in this repo records it**; the failures documented here are the
   *website's*, not that system's. Do not borrow them across.
3. **kylecovan.com — "where it goes next".** The only prompt left blank on it.
4. **LLM Wiki — all prose.** Opens with the second-brain line: a slice of his
   second brain, published so people can poke around in it.
5. **The `.qualifier` nod.** Each build's `inspiration` frontmatter still holds
   a credit ("Nate Herk", "Andrej Karpathy") waiting to be worked into prose.
6. **Then push.** Nothing has been pushed. Everything is on branch
   `restructure-builds`.

**Why neither was pushed:** the build pages carry no prose yet, so shipping puts
genuinely thin pages on a live indexed site. The structure is right; it is
waiting on content, not on code. Everything sits on branch `restructure-builds`.

**The vocabulary, settled — three internal words, two kinds of content.**
*Portfolio* = the index of things made. *Blog* = the index of things written.
*Build log* = the dated entries under a build. **None of those three words appear
on the site.** They are for talking about it, not labels for visitors.

**Only Kyle can supply, and it blocks C:**

1. A heading and lede for the builds section — "Two systems, built for myself
   first" is wrong on both count and framing once client websites are included.
2. The prose body for each build. §6 forbids drafting it on his behalf, and
   two drafts of the concrete Approach examples already died this way.
3. Whether the Second Brain / LLM wiki entry links to the live thing, and if so
   what is safe to expose.

**"Upon the Waters" was NOT used and is deliberately unspent.** Kyle proposed it
as the `/builds/` page title. It was set aside because two allusive scripture
names in one nav ("Upon the Waters" and "Unless the Lord" — both three words,
both prepositional, both starting with U) stop functioning as names. Quoting the
verse instead means the phrase still appears, inside its own source text. The
name is held for a future series, section or newsletter.

**"Not by chariots" (Psalm 20:7) is reserved by Kyle for a post title.** It was
the `Unless the Lord` vault folder's tagline and is no longer used on the site.
Don't spend it elsewhere.

**`second-brain` was renamed `llm-wiki` on July 30.** Kyle's answer to "is this
yours, or something other people use?" was *both*: the private thing is a second
brain, the public thing is a curated slice of it published as a wiki people can
query. The page is named for **what a visitor actually gets**, and "second brain"
belongs in the first line of the prose — which also keeps that far more
searchable phrase on the page without making it the name. Renaming was free
because `/builds/second-brain/` had never been deployed.

---

## 8. How to verify changes

```bash
cd ~/Projects/kylecovan-astro
source .venv/bin/activate      # REQUIRED in a fresh Terminal, for verify only
npm run build                  # writes dist/
npm run verify                 # both suites — ALL CHECKS PASSED twice
```

Both suites run against **`dist/`, not the source** — what matters is the HTML a
visitor receives, and Astro minifies the CSS and serialises the video array on
the way through. Headless Chromium via Playwright, launched with
`--disable-lcd-text` so subpixel fringing doesn't pollute contrast sampling.

Cloudflare runs **only** `npm run build`. The verify suites are a local gate.
Nothing enforces them on the server — that discipline is Kyle's.

### `verify.py` — the home page

1. **Contrast** — every text node against `#FBF8F2`, correct threshold per size.
   **46 nodes, 0 failures.**
2. **Overflow** — `scrollWidth === 320` at 320px **with the longest video title
   forced in**. A short random pick hides a real overflow.
3. **Top bar** — every title at 5 viewports: never escapes the column, never
   collides with the nav, lands flush left when on its own row (desktop), and
   sits **above the nav and flush left** below 544px.
4. **Nav** — every `href="#…"` resolves; nav's left edge equals the column's.
5. **Randomness** — ~400 reloads, asserts every distinct pair appears; every
   URL regex-validated as `https://youtu.be/<11 chars>`.
6. **No-JS** — loads with JS disabled, asserts the fallback link still works.
7. **Closing line** — forces a wide serif, fails above 90% of the measure.
   Currently 49%.
8. **Visual** — screenshots at 1440×1000 and 390×844 at 2× DPR.

### `verify_site.py` — the site-level checks

**Rewritten July 30 for a growing site.** Every check that used to name
`building/index.html` now runs over **every page discovered in `dist/`**, so a
new build is covered the day its Markdown file exists. Nothing was deleted in the
rewrite — each assertion was regeneralised. Two changes are worth knowing:

- **Pages are discovered, not enumerated.** `PAGES` was a hand-maintained list of
  two paths. A hand-maintained list silently stops covering new pages, which is
  the exact failure mode a growing site produces.
- **The hardcoded contrast counts are gone.** "46 nodes and 60 nodes" failed
  whenever a paragraph was added — a legitimate change — so the only way forward
  was to edit the assertion, which teaches you to edit assertions. **Zero
  failures** is now the claim; the count is printed, not asserted.

1. CSS identical across **all** pages (a tautology under one layout, kept as a
   backstop against Astro tree-shaking one page differently).
2. **Metadata uniqueness** — title, description and canonical must differ, and
   duplicates are named in the failure output.
3. **Link integrity, both directions** — every relative href resolves; every
   fragment exists *in the file it points at*.
4. Contrast on every page — **0 failures asserted**, node count reported.
5. Exactly one `h1` per page, no skipped levels.
6. Overflow at 320px on **every** page, not just one.
7. Sitemap completeness — count must equal the discovered page count.
8. **Structured data** — one JSON-LD block per page; it parses; `Person` carries
   name/url/jobTitle/sameAs; **every `sameAs` URL is a real `href` on the
   page**; **every** non-home page's stub `@id` resolves to the home page's
   definition; **every `BlogPosting` headline, date and anchor appears in the
   rendered HTML** of the page declaring it; **every `ItemList` name is a real
   heading and every `ItemList` url is a page that exists.** These enforce
   schema.org's "don't claim more than the page shows" rule mechanically
   instead of on trust.
9. **Redirects** — `public/_redirects` survives into `dist/`, every target is a
   page that exists, no source shadows a live page, and the retired
   `/building/#<id>` deep links still have targets on `/builds/`.
10. **RSS integrity — new, and it caught a real bug immediately.** Every item
    link must resolve to a real page and its fragment must exist on that page.
    The first version of the per-entry links rendered as
    `.../#2026-07-28-too-many-ideas/` because `@astrojs/rss` runs a *relative*
    link through the site's `trailingSlash: 'always'` and appends the slash to
    the end of the whole string, fragment included. The feed was valid XML, the
    build passed, every other check passed, and every link in the feed was
    broken. **Item links must be absolute** — `isValidURL` passes those through
    untouched.

---

## 9. Revision log

| # | Change |
|---|---|
| 1–17 | Pre-split work: 800px measure, Kyle's copy, rotating video link, muted underlines, closing-line rewrites, trailing-space fix in title #22. |
| 18 | OG share image; `twitter:card` upgraded to `summary_large_image`. |
| 19 | Social URLs filled in with `rel="me"`. |
| 20 | Portrait added, then replaced with the studio headshot across page, share card and favicon. |
| 21 | Portrait crop widened — 300px of synthesised backdrop above the frame. |
| 22 | Build log shipped — Project 01, entry one. |
| 23 | Creed changed "keep" → "put". |
| 24 | Anna paragraph added, verbatim. |
| 25 | Restructured after andrewng.org — four-pillar top nav, portrait-left hero. |
| 26 | Portrait squared, chosen from a rendered comparison. |
| 27 | Top-bar flex bug fixed — `flex: 0 0 auto` + `max-width: 100%`. |
| 28 | Portrait crop tightened to `D=720`. |
| 29 | Site split to two pages — hybrid, not the four Kyle asked for. |
| 30–32 | `build_site.py`, class-based heading selectors, `verify_site.py`. |
| 33 | Em dash removed from Project 01's one-liner. |
| 34 | Per-project build-log links, deep-linking to anchors. |
| 35 | Project docs renamed to stable names. |
| 36 | JSON-LD structured data on both pages, generated from page content. |
| 37 | **Rebuilt on Astro.** One layout, one stylesheet, content collections for the build log, RSS feed, `/building/` as an extensionless URL. `build_site.py` retired. Both suites re-pointed at `dist/`. |
| 38 | **Shipped.** GitHub repo `KyleCovan/kylecovan-site`, Cloudflare Pages, auto-deploy on push. Live at `kylecovan-site.pages.dev`. |
| 39 | **Favicon squared**, re-cut from the portrait crop. |
| 40 | **Mobile top bar rebuilt.** Below 34rem it becomes a column and the video line moves above the nav. Centred at Kyle's request, then reverted the same day. `verify.py` tracked both moves. |
| 41 | **Mobile top padding cut** from `15vh` (~127px on a phone) to `clamp(2.25rem, 6vh, 3.25rem)`. |
| 42 | **"Follow along" restored** to the foot of `/building/` — a label and four links, no prose. Every word on the site is now Kyle's. |
| 43 | **Tapo Canyon unlinked** while that domain doesn't resolve. Sentence untouched. |
| 44 | **Portrait crop B** — 20px of backdrop trimmed off the top, source now 340px. Favicon re-cut from the same crop. |
| 45 | **Desktop top bar: `space-between` → `flex-start`, gap 1.4rem.** Tuned by eye: 2.2 → 1.8 → 1.4rem. |
| 46 | **Video titles:** 🥹 emoji removed; `Can I Trust the Bible - Episode 3: The Council of Nicaea` → `Can I Trust the Bible: The Council of Nicaea`. |
| **47** | **DNS moved to Cloudflare and kylecovan.com went live.** Google Workspace email verified intact end to end. `www` 301s to the apex. |
| **48** | **Context ported into the repo.** `CLAUDE.md` plus `docs/` replace the claude.ai project instructions as the source of truth; maintenance moved to Claude Code in VS Code. |
| **50** | **The writing section.** One `writing` collection replaces `log`, with an optional `build:` tag deciding whether a post renders on a build page or gets its own URL — so there is never a "log entry or blog post?" decision, and never two copies of one text. `/writing/` added, nav rebuilt to **Kyle Covan · Builds · Unless the L**ORD** · Contact** (Story and Approach both left, Approach's words moved verbatim to a post). Epigraphs added above the h1 on both section pages, with small-caps LORD. `second-brain` → `llm-wiki`. The `outline` array stopped rendering and became writing `prompts` — it was publishing five bullets of promises on a page with nothing behind them. Both suites green, **not pushed**. |
| **49** | **`/building/` → `/builds/`, one page per build.** `projects.json` became the `builds` content collection; `log` entries now use `build: reference('builds')` so a typo fails the build. Nav pillar renamed (Kyle caught the tense contradiction). `.qualifier` subtitles removed, the credit kept in `inspiration` frontmatter. `public/_redirects` added — `/building/` was indexed. **RSS item links fixed**: they were relative, so `@astrojs/rss` appended a trailing slash *after* the fragment and every anchor was broken. **`verify_site.py` rewritten** to discover pages instead of enumerating two, to assert zero contrast failures instead of two hardcoded node counts, and to cover redirects and the RSS feed. Both suites green. **Not pushed** — the build pages have no prose yet. |
| **51** | **Sitemap `<lastmod>`, derived from content.** Every URL now carries a date that traces to a file Kyle actually edited: a build page takes the later of its new `updated` frontmatter and the newest post tagged to it (the page renders both); `/writing/<id>/` takes the post's own date; `/`, `/builds/` and `/writing/` are generated from the collections, so each takes its newest member. **`<priority>` removed** — Google's sitemap documentation says it ignores both `priority` and `changefreq`, so the 1.0/0.8 split was steering nothing while looking like a ranking knob, which invites tuning. The stamp-deploy-time shortcut was rejected: a sitemap claiming all seven pages changed on every push is one Google learns to ignore, and then the page that really did change gets no signal either. `verify_site.py` gained five assertions, including two that cross-check each date against the frontmatter it claims to describe — both were confirmed to FAIL when deliberately broken before being trusted. A build with no `updated` simply gets no `<lastmod>`; a missing date costs nothing, a wrong one costs the file's credibility. Also corrected a comment in `astro.config.mjs` that claimed the sitemap filter excluded `rss.xml` — it never did, and never needed to. Both suites green. **Pushed to `restructure-builds`; 49, 50 and 51 are all on that branch and none of them are merged or deployed** — kylecovan.com still serves the old two-URL structure until `main` moves. |
| **52** | **All three build pages written, and the first LLM Wiki entry.** Dictated by Kyle over a long session and shaped; his edits win over every draft, including the cuts. **LLM Wiki** went 47 words to ~970 across six drafts, leading with "What I want it to do" at his call because a visitor arrived not knowing what an LLM Wiki was and had to read 250 words of history to find out. **It is written in past tense and as intent on purpose: he confirmed the retrieval layer does not exist yet.** Present tense there would put promises on a page with nothing behind them, which is the exact trap the `prompts` array was pulled out of the template to avoid (§49). **Personal AI OS** gained "What broke", "What I actually use" and "Where I'm trying to get to", 526 words to ~1140. He answered "what broke" with his own understanding and his own working habits rather than software failures, and the section is ordered to keep it that way; the one technical failure (scheduled tasks need the laptop open, so the AI coach got deleted) sits in the middle deliberately. **kylecovan.com** gained "Where it goes next", written from §7's open TODOs rather than invented — dark mode leads because it was already decided there in full. **First LLM Wiki log entry**, "Four AI operating systems in one vault, and I only knew about one": he asked whether keeping his AI OS inside the vault was sound *and gave permission to say no*, which is what surfaced four roots where he thought he had one. That is §"check the premise" arriving from his side of the desk. **Both `inspiration` credits finally landed in prose** (Karpathy, Nate Herk with his video linked), where the July 30 note said they belonged. **New copy rule: no em dashes in anything published in Kyle's voice.** §6 had banned them in the home-page paragraphs and recorded that he had not asked for a sweep; on August 3 he asked. Structural em dashes are untouched. `docs/post-ideas.md` added — five posts worth writing, chief among them the Onesimus name story, which was too good to bury in a maintenance log. |
| **53** | **New photograph everywhere, and the image pipeline recovered.** Closes §7 item 7, open since July 30. `build_assets.py` and `headshot.jpg` are both in the repo now; one command rebuilds the portrait, the favicon and the share card from source, and Pillow was added to the venv for it. **The favicon has its own tighter crop** of the same photograph, a documented exception to §3 — the new outdoor background swallowed the face at 16px. **`og.png` renamed to `og-2.png`, and this is the important part:** the new card was going out at the old URL, and iMessage, Slack, X and LinkedIn all cache share images keyed on that URL in caches this site cannot reach. The deploy would have shipped a card nobody ever saw. **The filename must now change every time the image does.** `verify_site.py` gained an assertion that the `og:image` URL resolves to a file that ships, confirmed to fail before being trusted. **Video list:** title 01 became "Psalms 1 & 2" (plural: two psalms), "Religious But Not Saved" removed at Kyle's request, and the top bar now reads "*Title*, from my liked videos on YouTube" — the bare title let any entry read as Kyle's own words rather than a video he saved. **The label had to follow the link, not precede it**: written as a prefix first, `verify.py` rejected it at all five widths because it pushed the anchor 145px off the column edge. The test was right. Removing a video also broke `verify.py`'s `len(TITLES) == 32`, so **the video count is now derived** — the same trap the contrast counts were pulled out of on July 30. No assertion was weakened. |

---

## 10. Starting a session

Open `~/Projects/kylecovan-astro` in VS Code and run Claude Code there.
`CLAUDE.md` loads automatically; read this document when the change touches
design, copy, or the top bar.

**Highest-value next steps, in order:**

1. **Search Console** (`docs/deploy-status.md` Step 5), so the SEO work becomes
   measurable. Add the DMARC record in the same sitting.
2. Get Kyle's "what broke" answer for Project 01, and Project 02's first entry.
3. Once each project has ~2 entries, split them to their own URLs (§4).
4. Dark mode, as its own focused pass (§7).
