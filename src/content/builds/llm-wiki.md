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
    rest: ANSWERED Aug 3, dictated, then edited by Kyle four times.
  - lead: How it's structured
    rest: ANSWERED Aug 3 as the MANUAL workflow. There is no built system yet.
  - lead: Retrieval in practice
    rest: ANSWERED Aug 3 as manual retrieval. No LLM question-and-answer exists.
  - lead: What I'd do differently
    rest: ANSWERED Aug 3 as what he WANTS. The LEAD section, by his call.
  - lead: Where it goes next
    rest: ANSWERED Aug 3 — Substack or Medium, a newsletter. Aspirational tense.
---

<!--
DRAFT 5, August 3 — dictated by Kyle, shaped, then edited by him four times.

He dictates and the job is to turn what he says into finished prose in his
voice. That is a standing instruction for this page, not the usual "ask, don't
draft" rule. It licenses SHAPING what he said, never adding what he didn't.

VOICE. Contractions throughout, at his request in draft 5, without forcing one
into every clause. This agrees with handoff §6, which already required "don't"
over "do not" page-wide. Plain words over precise ones: he rejected the draft 4
paragraph about plain markdown files and lock-in as reading like an instruction
manual, and rejected the backlinks/tags/graph paragraph as jargon a newcomer
would bounce off. Both were rewritten in plain language rather than deleted,
because the next section depends on them: "the things that drew me to Obsidian,
I wasn't even doing" only lands if the reader knows what those things were.

TWO IMAGES, NOT THREE. Kyle cut "lighting it on fire" in draft 4 and kept the
wind and the desk. Do not put the fire line back.

WRITTEN FOR HIM TO CHECK, not dictated: the Obsidian passages. He said he knew
what he was trying to say and couldn't articulate it, and asked for it filled in
from what is actually true of Obsidian. Everything traces to something he said
(file management fatigue, it grouped notes without any AI in it, the gardener
framing, the tools were more advanced than his use of them) plus real Obsidian
behaviour. NO INVENTED SPECIFICS about how often he used a feature.

THE ENDING IS A LOOP, by his design. "How I was working" now closes by naming
the LLM Wiki as the thing that changes the story, and restates in one sentence
what the lead section promised. That hands the reader to "Where it goes next"
instead of stopping dead. Keep the loop if you edit the ending.

EM DASHES. None in the prose. Kyle doesn't write with them, so they stay out of
anything published in his voice. STRUCTURAL em dashes are fine and were left
alone (the `.log-status` line, the one-liners). handoff §6 banned them in the
home-page paragraphs and noted he had not asked for a sweep; this is the sweep,
prose only.

NOT BUILT. Asked directly on August 3, Kyle confirmed LLM Wiki does not exist
yet: he is building it. Everything except the lead section is past tense and the
model is written as intent. That is not a style choice to be tidied away later.
Present tense here would put promises on a page with nothing behind them, the
exact trap the `prompts` array was pulled out of the rendered template to avoid
on July 30. When retrieval works, this page earns the present tense and a real
worked example.

CUTS, all his, which should not creep back:
  - the "names" file, names for bands and projects. His call in draft 5: nice
    personal flair, but out of place.
  - "But now things have changed" as a standalone line, replaced by the loop.
  - "cool names starting with C" and the family question, from the bullets.
  - the fire image; "there was no file system"; "I wasn't using any of it to
    create new notes"; the to-do list and word-search retrieval examples;
    "Very rudimentary"; "never referenced" softened to "hardly referenced";
    "everything I wrote" softened to "a lot of things I wrote".
  - the password note, dropped before he ever saw it: not worth publishing.
-->

## What I want it to do

I want a large language model to connect my notes in a strategic way. File them
by category. Link them in ways that actually mean something.

I also want it working on what's already in there.

A lot of my notes are one long dump. I wrote them in a single sitting, so three
or four unrelated ideas can end up in the same file just because they showed up
on the same day. I want it to break those apart, and pull an idea out of the
middle of a long note into a place of its own where it can be linked to and
found instead of buried.

Then I want to ask the collection questions.

- What Bible study notes do I have on the book of Matthew?
- Show me a collection of quotes I've saved from pastors I respect.
- What have I written on the topic of X that would make a good newsletter or
  post?
- What are the ideas I've had for apps?
- What have I written and never looked at again?

Right now the notes only flow one direction. I put ideas in. I want to put
questions in too, and pull back out the thinking I already did and forgot, so
the writing starts working for me instead of just accumulating.

## The problem

I was losing track of things I wrote.

I'd write a note and it would get filed away into oblivion. The next day I'd
write something else, and the circle would continue. I wrote and wrote and
hardly referenced any of it.

It was the equivalent of writing on a piece of paper and throwing it into the
wind. If I did ever see it again, that would be pretty amazing.

That was my habit with a lot of things I wrote. I didn't post it anywhere, I
didn't refine it. Just notes, journal entries, thoughts, ideas, Bible verses,
and other things I thought were noteworthy.

If it were on a desk it would have been a desk full of random papers and
Post-its of different sizes, stacked on top of each other in no particular
order.

I moved to Obsidian because I had file management fatigue. I didn't want to
think about folders anymore, and I liked that everything I write stays on my own
computer instead of living inside somebody else's app.

What appealed to me past that was that Obsidian can connect notes on its own,
with no AI in it at all. You link two notes together and both ends know about
it, so over time those connections build into something you can follow.

The other thing was how it was explained to me. Obsidian is a gardener's way of
taking notes. You don't finish a note. You start one, then you come back and add
to it, and it grows.

Other apps let you do that too, but that framing is what made it click for me.
Knowing it was all there was comforting enough.

## How I was working

Create a new note, title it, get the idea out in simple markdown. Headers,
subheaders, bullets. That was the whole system.

The things that drew me to Obsidian in the first place, I wasn't even doing. I
wasn't linking notes together. My tags were loose, and not something I could
count on later.

The gardener style of making notes appealed to me, but I just went back to
creating fresh notes every time instead of tending to the ones I already had.

Getting anything back out relied on my memory. I'd search a hashtag, or search
for a note by name if I remembered the name. So the only notes I ever recalled
were the ones I already knew I had, usually the most recent ones. Eventually a
lot of those got lost too.

Mostly I just left tabs open on what I was working on and clicked back to them.
I knew the tools were far more advanced than the way I was using them.

But now things are starting to change, thanks to the LLM Wiki I'm beginning to
implement: something that reads back through what I've already written, breaks
it up where it should be broken up, connects it, and answers questions about it.

## Where it goes next

Next, I'm hoping to add a way to push out to Substack or Medium, or both, and to
start a newsletter built around the things that interest me and the places they
converge.

If the way I think is interesting to anyone else, I'd like to give them a place
to follow along.
