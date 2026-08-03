---
name: kylecovan.com
order: 3
oneLiner: The site you are reading. Every page is a single file with no external requests, and a test suite fails the build when the design drifts.
# Sitemap <lastmod>. Seeded from this file's last commit date, not invented.
updated: 2026-07-30
# NOT RENDERED. Writing prompts — see content.config.ts.
prompts:
  - lead: What it is
    rest: drafted below from the record.
  - lead: How it's built
    rest: drafted below from the record.
  - lead: A decision that could have gone the other way
    rest: drafted below — the four-page split.
  - lead: What broke
    rest: drafted below. Every item traces to docs/handoff.md.
  - lead: Where it goes next
    rest: STILL UNANSWERED. Kyle's to write.
---

<!--
DRAFT, July 30 — assembled from docs/handoff.md, which has recorded every
decision and every defect on this site since July 28. Unlike the Personal AI OS
page, nothing here is guesswork: each claim traces to a specific entry in the
handoff, and the failures in "What broke" are quoted from its own lessons and
revision log.

It is still in Kyle's voice and therefore still HIS to approve. He asked for a
draft to edit rather than a blank page. Edit freely; the facts are checkable
against the handoff.

STILL MISSING: "Where it goes next."
-->

## What it is

This site. I wanted it to load instantly and to stay simple enough that I could
understand all of it, so the whole thing is built around one rule: what a
visitor's browser receives is a single file, with nothing fetched from anywhere
else. No web fonts, no CDN, no analytics scripts. My photo and the favicon are
embedded in the page itself.

There is exactly one piece of JavaScript on it, and all it does is pick a random
video from a list and swap it into the link at the top.

## How it's built

It's an Astro project. The CSS exists once, in one stylesheet, and gets inlined
into every page when the site is built. Each thing I've built and everything I
write is a Markdown file — adding one file is the entire publishing workflow,
because the page, the index, the structured data, the sitemap and the RSS feed
are all generated from it.

It deploys to Cloudflare Pages, and pushing to the main branch is what puts it
live.

Two test suites run against the built output rather than the source, because
what matters is the HTML someone actually receives. They check colour contrast
on every piece of text, that nothing overflows the screen at 320 pixels wide,
that every link and anchor resolves, and that the structured data never claims
something the page doesn't show.

## A decision that could have gone the other way

I asked for the site to be split into four pages, one for each section, because
I thought separate pages would rank better. I also asked whether that reasoning
was right, and it turned out to be half right in a way that pointed the other
direction.

Splitting does let you target different searches. But the guidance names
personal sites as the case where one page is the better answer, and AI search
engines work at the level of passages inside a document, so the recommended
shape is one page that answers several questions rather than several thin pages
that each answer one. Then we counted the words: Story was 276, Approach was 109,
Contact was 23. Three of the four pages I wanted would have been too thin to
stand up.

So it became a hybrid instead of the four I asked for. The part worth keeping is
that I asked whether I was right rather than assuming, and the counting settled
it instead of opinion.

## What broke

- There were once ten copies of the home page numbered `index_1` through
  `index_10`, and the newer-looking number held the older content.
- A trailing space sat inside one of the video titles for hours, because the
  file saved successfully and nobody read it back.
- The two-page split shipped with three defects in it. The test suite caught all
  three, which is the only reason I know about them.
- One CSS setting on the top bar looked identical to the correct one and wasn't:
  short video titles floated in the middle of the row instead of sitting on the
  left edge. It shipped before a rendered screenshot caught it.
- The favicon was a circle with cream-coloured corners, left over from when my
  photo was still round. On an iPhone it read as a circle sitting inside a white
  box. It looked fine described in words and wrong the moment it was rendered.
- The top of every page had 15% of the screen height as padding, which on a
  phone is about 127 pixels of empty space above the first line.
- Markdown was quietly turning straight apostrophes into curly ones, so the
  build log had different quote marks from the rest of the site. No test caught
  that. A pixel comparison did.
- The whole RSS feed was broken and looked fine. Every link had a slash sitting
  after the anchor, so none of them landed where they were supposed to. The XML
  was valid, the build passed, and every other check passed too.

Most of these were found by a test or by looking at a picture of the page, not
by reading the code and thinking about it.
