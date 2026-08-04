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
    rest: ANSWERED Aug 3, dictated, then edited twice by Kyle.
  - lead: How it's structured
    rest: ANSWERED Aug 3 as the MANUAL workflow. There is no built system yet.
  - lead: Retrieval in practice
    rest: ANSWERED Aug 3 as manual retrieval. No LLM question-and-answer exists.
  - lead: What I'd do differently
    rest: ANSWERED Aug 3 as what he WANTS. Now the LEAD section, by his call.
  - lead: Where it goes next
    rest: ANSWERED Aug 3 — Substack or Medium, a newsletter.
---

<!--
DRAFT 3, August 3 — dictated by Kyle, shaped, then edited by him twice.

He dictates and the job is to turn what he says into finished prose in his
voice. That is a standing instruction for this page, not the usual "ask, don't
draft" rule. It licenses SHAPING what he said, never adding what he didn't.

ORDER IS DELIBERATE. "What I want it to do" leads because Kyle asked for it: a
visitor arrives not knowing what an LLM Wiki is, and that section answers it
better than the backstory does. Before the reorder the page spent 250 words on
history before saying what the thing is for. The past-tense sections now read as
the reason rather than the setup, which is why "But now things have changed"
moved to the end of "How I was working" — it is the hinge into the future, and
sitting mid-narrative it pointed the wrong way.

EM DASHES. None in the prose. Kyle clarified August 3: he doesn't write with
them, so they stay out of anything published under his name. STRUCTURAL em
dashes are fine and were explicitly left alone (the `.log-status` line, the
one-liners). handoff §6 banned them in the home-page paragraphs and noted he had
not asked for a sweep; this is the sweep, for prose only.

NOT BUILT. Asked directly on August 3, Kyle confirmed LLM Wiki does not exist
yet: he is building it. That is why everything except the lead section is past
tense and the model is written as intent. It is not a style choice to be tidied
away later. Present tense here would put promises on a page with nothing behind
them, the exact trap the `prompts` array was pulled out of the rendered template
to avoid on July 30. When retrieval works, this page earns the present tense and
a real worked example.

CUT BY KYLE in draft 3, flagged to him rather than restored:
  - the desk of random papers and Post-its stacked in no particular order. It
    was the strongest image on the page and he dropped it on a re-read. If that
    was a dictation skip rather than a cut, it goes back in paragraph three of
    "The problem".
Earlier cuts, also his, which should not creep back:
  - "there was no file system, just a pile of notes loosely connected by tags"
  - "I wasn't using any of it to create new notes or to build knowledge out of"
  - the to-do list and word-search examples of manual retrieval
  - "Very rudimentary"
  - "never referenced any of it" became "hardly referenced any of it"
  - "everything I wrote" became "a lot of things I wrote", a smaller, truer claim
  - the password note, dropped before he ever saw it: not worth publishing
-->

## What I want it to do

I want a large language model to connect my notes in a strategic way. File them
by category. Link them in ways that actually mean something.

Then I want to ask the collection questions.

- What are the ideas I've had for apps?
- What are some cool names I've come up with that start with the letter C?
- What have I written about my family that I've had issues with in the past?
- What have I written on the topic of X that would make a good newsletter or
  post?

Right now the notes only flow one direction. I put ideas in. I want to put
questions in too, and pull back out the thinking I already did and forgot, so
the writing starts working for me instead of just accumulating.

## The problem

I was losing track of everything I wrote.

I'd write a note and it would get filed away into oblivion. The next day I'd
write something else, and the circle would continue. I wrote and wrote and
hardly referenced any of it. It was the equivalent of writing something,
lighting it on fire and never seeing it again, or writing on a piece of paper
and throwing it into the wind. If I ever saw it again, that would be pretty
amazing.

That was my habit with a lot of things I wrote. I didn't post it anywhere, I
didn't refine it. Just notes, journal entries, thoughts, ideas, Bible verses,
and other things I thought were noteworthy.

I moved to Obsidian because I had file management fatigue. Knowing it was all
there was comforting enough for me.

## How I was working

Create new note, title it, get the idea out in simple markdown. Headers,
subheaders, bullets. That was the whole system.

Getting anything back out relied on my memory. I'd search a hashtag, or search
for a note by name if I remembered the name. So the only notes I ever recalled
were the ones I already knew I had, usually the most recent ones. Eventually a
lot of those got lost too.

Mostly I just left tabs open on what I was working on and clicked back to them.
I knew the tools were far more advanced than the way I was using them.

One file kept growing. It was called "names": names for bands, names for
projects, just names. I like words, so I keep adding to it.

But now things have changed.

## Where it goes next

Next is a way to push out to Substack or Medium, and a newsletter built around
the things that interest me and the places they converge. If the way I think is
interesting to anyone else, that gives them a place to follow along.
