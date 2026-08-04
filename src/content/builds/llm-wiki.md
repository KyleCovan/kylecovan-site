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
    rest: ANSWERED Aug 3, dictated, then edited by Kyle line by line.
  - lead: How it's structured
    rest: ANSWERED Aug 3 as the MANUAL workflow. There is no built system yet.
  - lead: Retrieval in practice
    rest: ANSWERED Aug 3 as manual retrieval. No LLM question-and-answer exists.
  - lead: What I'd do differently
    rest: ANSWERED Aug 3 as what he WANTS. Folded into "What I want it to do".
  - lead: Where it goes next
    rest: ANSWERED Aug 3 — Substack or Medium, a newsletter. Folded in by Kyle.
---

<!--
DRAFT, August 3 — shaped from Kyle's dictated answers, then edited by Kyle,
then cut down at his request.

He asked for this explicitly: he dictates, and the job is to turn what he says
into finished, readable prose in his voice. That is a standing instruction for
this page, not the usual "ask, don't draft" rule. It licenses SHAPING what he
said, never adding what he didn't.

NO EM DASHES IN THIS PROSE. Kyle asked for them out on August 3. handoff §6
already banned them in the home-page paragraphs and recorded that he had been
told and had not asked for a sweep; this is him asking, at least here. Do not
reintroduce them, and do not "fix" a comma splice by reaching for one.

NOT BUILT. Asked directly on August 3 whether LLM Wiki exists, Kyle said no: he
is building it now. That is why the problem and the workflow are past tense and
the model is written as intent, and it is not a style choice to be tidied away
later. Writing this page in the present tense would put promises on a page with
nothing behind them, the exact trap the `prompts` array was pulled out of the
rendered template to avoid on July 30. When the retrieval layer works, this page
gets rewritten in the present tense and earns a real worked example.

His analogies (lighting it on fire, paper thrown into the wind, the desk of
stacked Post-its) are verbatim and should survive any future edit. They are the
best writing on the page.

Kyle cut these, and they should not creep back:
  - "there was no file system, just a pile of notes loosely connected by tags"
  - "I wasn't using any of it to create new notes or to build knowledge out of"
  - the to-do list and word-search examples of manual retrieval
  - "everything I wrote" became "a lot of things I wrote", a smaller, truer claim
  - the password note, dropped before he ever saw it: not worth publishing
-->

## The problem

I was losing track of everything I wrote.

I'd write a note and it would get filed away into oblivion. The next day I'd
write something else, and the circle would continue. I wrote and wrote and never
referenced any of it. It was the equivalent of writing something, lighting it on
fire, and never seeing it again. Or writing on a piece of paper and throwing it
into the wind. If I ever saw it again, that would be pretty amazing.

That was my habit with a lot of things I wrote. I didn't post it anywhere. I
didn't refine it. Just notes, journal entries, thoughts, ideas, Bible verses,
and other things I thought were noteworthy. If it were on a desk it would have
been a desk full of random papers and Post-its of different sizes, stacked on
top of each other in no particular order.

I moved to Obsidian because I had file management fatigue. Knowing it was all
there was comforting.

## How I was working

Click new note, title it, get the idea out in simple markdown. Headers,
subheaders, bullets. That was the whole system.

Getting anything back out relied on my memory. I'd search a hashtag, or search
for a note by name if I remembered the name. So the only notes I ever recalled
were the ones I already knew I had, usually the most recent ones. Eventually a
lot of those got lost too.

Mostly I just left tabs open on what I was working on and clicked back to them.
Very rudimentary. I knew the tools were far more advanced than the way I was
using them.

One file kept growing. It was called "names": names for bands, names for
projects, just names. I like words, so I'd keep adding to it.

## What I want it to do

I want a large language model to connect my notes in a strategic way. File them
by category. Link them in ways that actually mean something.

Then I want to ask the collection questions.

- What are some of the ideas I've had for apps?
- What are some cool names I've come up with that start with the letter C?
- What have I written about my family that I've had issues with in the past?
- What have I written on the topic of X that would make a good newsletter or
  post?

Right now the notes only flow one direction. I put ideas in. I want to put
questions in too, and pull back out the thinking I already did and forgot, so
the writing starts working for me instead of just accumulating.

Next is a way to push out to Substack or Medium, and a newsletter built around
the things that interest me and the places they converge. If the way I think is
interesting to anyone else, that gives them a place to follow along.
