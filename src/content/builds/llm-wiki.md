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
    rest: ANSWERED Aug 3, dictated, then edited by Kyle three times.
  - lead: How it's structured
    rest: ANSWERED Aug 3 as the MANUAL workflow. There is no built system yet.
  - lead: Retrieval in practice
    rest: ANSWERED Aug 3 as manual retrieval. No LLM question-and-answer exists.
  - lead: What I'd do differently
    rest: ANSWERED Aug 3 as what he WANTS. Now the LEAD section, by his call.
  - lead: Where it goes next
    rest: ANSWERED Aug 3 — Substack or Medium, a newsletter. Aspirational tense.
---

<!--
DRAFT 4, August 3 — dictated by Kyle, shaped, then edited by him three times.

He dictates and the job is to turn what he says into finished prose in his
voice. That is a standing instruction for this page, not the usual "ask, don't
draft" rule. It licenses SHAPING what he said, never adding what he didn't.

TWO IMAGES, NOT THREE. Kyle cut the "lighting it on fire" line in draft 4 and
restored the desk of Post-its, on the grounds that three images in one post was
too many. Wind and desk survive. Do not put the fire line back.

WRITTEN FOR HIM TO CHECK, not dictated: the Obsidian passages in "The problem"
and the second paragraph of "How I was working". He said he knew what he was
trying to say and could not articulate it, and asked for it filled in from what
is actually true of Obsidian. Everything there traces to something he said (file
management fatigue, it grouped notes without any AI in it, the gardener framing,
the tools were more advanced than his use of them) plus factual Obsidian
behaviour: plain local markdown, links that both ends know about, tags, a graph
view. NO INVENTED SPECIFICS about how often he used a feature. If any of it
misstates him, it is the first thing to cut.

ORDER IS DELIBERATE. "What I want it to do" leads because Kyle asked for it: a
visitor arrives not knowing what an LLM Wiki is, and that section answers it
better than the backstory does.

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

BULLETS, settled in draft 4. Kyle named the three he wanted kept and their
order, then asked for a fourth about cleanup. Dropped: "cool names starting with
C" (his call) and "what have I written about my family that I've had issues
with" (dropped by omission when he re-listed the set, and worth leaving out of a
public page anyway). The Ezekiel question comes from his very first dictation,
where it was garbled and was left out of drafts 1 to 3 rather than guessed at.

Earlier cuts, all his, which should not creep back:
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

I also want it working on what is already in there. Most of my notes came out in
one piece because that is how the thought arrived, not because everything in
them belonged together. So I want it to take a long note and break it into
smaller ones, and pull an idea sitting three paragraphs down out into a note of
its own, where it can be linked to and found instead of buried.

Then I want to ask the collection questions.

- What have I written about the book of Ezekiel?
- What have I written on the topic of X that would make a good newsletter or
  post?
- What are the ideas I've had for apps?
- What have I written and never looked at again?

Right now the notes only flow one direction. I put ideas in. I want to put
questions in too, and pull back out the thinking I already did and forgot, so
the writing starts working for me instead of just accumulating.

## The problem

I was losing track of everything I wrote.

I'd write a note and it would get filed away into oblivion. The next day I'd
write something else, and the circle would continue. I wrote and wrote and
hardly referenced any of it. It was the equivalent of writing on a piece of
paper and throwing it into the wind. If I did ever see it again, that would be
pretty amazing.

That was my habit with a lot of things I wrote. I didn't post it anywhere, I
didn't refine it. Just notes, journal entries, thoughts, ideas, Bible verses,
and other things I thought were noteworthy. If it were on a desk it would have
been a desk full of random papers and Post-its of different sizes, stacked on
top of each other in no particular order.

I moved to Obsidian because I had file management fatigue. I didn't want to
think about folders anymore. Everything stays a plain markdown file on my own
computer, so there is no format to get locked into and nothing to migrate later.

What appealed to me past that was that it could connect notes on its own, with
no AI in it at all. Link one note to another and both ends know about it, so a
note can show you what points back at it. Tags and the graph give you groupings
without having to build them by hand.

The other thing was how it was explained to me. Obsidian is a gardener's way of
taking notes. You don't finish a note, you start one, and you come back and add
to it, and it grows. Other apps let you do that too, but that framing is what
made it click for me. Knowing it was all there was comforting enough.

## How I was working

Create new note, title it, get the idea out in simple markdown. Headers,
subheaders, bullets. That was the whole system.

Almost none of what drew me to Obsidian is what I actually did in it. I wasn't
linking notes together. My tags were loose, and not something I could count on
later. The gardener idea appealed to me and then I went back to starting a fresh
note every time instead of tending the ones I already had.

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

Next, I'm hoping to add a way to push out to Substack or Medium, or both, and to
start a newsletter built around the things that interest me and the places they
converge. If the way I think is interesting to anyone else, I'd like to give
them a place to follow along.
