---
name: LLM Wiki
order: 2
oneLiner: An AI-powered knowledge base that centralizes internal documentation and unstructured data so hard-won knowledge is never lost.
# Sitemap <lastmod>. Seeded from this file's last commit date, not invented.
updated: 2026-08-03
# Renamed from "Second Brain" on July 30. Kyle's answer to "is this yours, or is
# it something other people use?" was: both. The private thing is a second brain;
# the public thing is a curated slice of it, published as a wiki people can query.
# The page is named for what a visitor actually gets. The second brain belongs in
# the first line of the prose, which also keeps that searchable phrase on the page
# without making it the name.
inspiration: Andrej Karpathy
# NOT RENDERED. Writing prompts for the prose below — see content.config.ts.
prompts:
  - lead: The problem
    rest: ANSWERED Aug 3, dictated. The strongest material on the page.
  - lead: How it's structured
    rest: ANSWERED Aug 3 — but he described the MANUAL workflow, not a built system.
  - lead: Retrieval in practice
    rest: ANSWERED Aug 3 as manual retrieval. No LLM question-and-answer exists yet.
  - lead: What I'd do differently
    rest: ANSWERED Aug 3 as what he WANTS, not lessons from a shipped architecture.
  - lead: Where it goes next
    rest: ANSWERED Aug 3 — Substack and Medium, a newsletter.
---

<!--
DRAFT, August 3 — shaped from Kyle's dictated answers to the five prompts.

He asked for this explicitly: he dictates, and the job is to turn what he says
into finished, readable prose in his voice. That is a standing instruction for
this page, not the usual "ask, don't draft" rule — but it licenses SHAPING what
he said, never adding what he didn't. Every claim below traces to the dictation.

The analogies (lighting it on fire, paper thrown into the wind, the desk of
stacked Post-its) are verbatim his and should survive any edit — they are the
best writing on the page.

TENSE IS DELIBERATE AND LOAD-BEARING. Kyle answered prompts 2 and 3 by
describing how he works in Obsidian by hand, and prompt 4 by describing what he
WANTS a model to do. Nothing he said describes a working LLM layer: there is no
real question-and-answer example because none exists yet. So the problem and the
workflow are past tense, and the model is written as intent, not capability.

That is the same trap the `prompts` array was pulled out of the template for —
publishing a list of promises on a page with nothing behind it. This page must
not become that in prose form. If the retrieval layer gets built, this page gets
rewritten in the present tense and gains a real worked example.

OPEN, and only Kyle can settle them:
  - The Andrej Karpathy credit in the frontmatter still has no sentence. The
    dictation garbled where it belonged.
  - "The book of Ezekiel" appeared in the same garbled clause and looked like a
    sixth example question. Left out rather than guessed at.
  - The password note he mentioned is deliberately omitted; see the note in the
    session, not worth publishing either way.
-->

## The problem

I was losing track of everything I wrote.

I'd write a note and it would get filed away into oblivion. The next day I'd
write something else, and the circle would continue. I wrote and wrote and never
referenced any of it.

It was the equivalent of writing something and then lighting it on fire and
never seeing it again. Like writing on a piece of paper and throwing it into the
wind — if I ever saw it again, that would be pretty amazing. That was my habit
with everything I wrote.

I didn't post it anywhere. I didn't refine it. Just notes, journal entries,
thoughts, ideas, and all the Bible verses that stood out to me. If it were on a
desk it would be a desk full of random papers and Post-its of different sizes,
stacked on top of each other in no particular order.

I moved to Obsidian in the first place because I had file management fatigue.
Knowing it was all in there was comforting enough. But there was no file system
— just a pile of notes loosely connected by a few tags, with no semblance of
order to them at all.

I wasn't using any of it to create new notes or to build knowledge out of. I was
literally just writing.

## How I was working

Click new note, title it, and get the idea out in simple markdown — headers,
subheaders, bullets or numbered lists. That was the whole system.

Getting anything back out relied on my memory. I'd search a hashtag, or search
for a note by name if I remembered the name. So the only notes I ever recalled
were the ones I already knew I had, and those were usually the most recent ones,
still fresh in my mind. Eventually those got lost too. There was plenty in there
I never kept at the forefront of my mind.

Otherwise I'd pull up a to-do list, search for a word I knew was in there
somewhere, or just leave tabs open on what I was working on and click back to
them. Very rudimentary, very basic. I knew the tools were far more advanced than
the way I was using them.

One file that kept growing was called "names" — names for bands, names for
projects, just names. I like words, so I'd keep adding to it.

## What I want it to do

I want a large language model to connect my notes in a strategic way: file them
by category and link them in ways that actually mean something.

Then I want to ask the collection questions.

- What are some of the ideas I've had for apps?
- What are some cool names I've come up with that start with the letter C?
- What have I written about my family that I've had issues with in the past?
- What have I written on the topic of X that would make a good newsletter or
  post?

Right now the notes only flow one direction. I put ideas in. What I want is to
put questions in too, and pull back out the thinking I already did and forgot —
so the writing I've already done starts working for me instead of just
accumulating.

## Where it goes next

The next thing to wire in is a way to push out to Substack and Medium, and to
start a newsletter built around the things that interest me and the places they
converge — for anybody who wants to follow along with the way I think about
things.
