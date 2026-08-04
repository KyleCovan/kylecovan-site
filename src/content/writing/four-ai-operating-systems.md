---
title: "Four AI operating systems in one vault, and I only knew about one"
date: 2026-08-03
build: llm-wiki
---

<!--
Dictated by Kyle on August 3 and shaped, not invented. Same method as every
other entry: his account, his words where they were good, tightened.

THE SPINE IS THE QUESTION, NOT THE CLEANUP. He could have opened by asking for
a tidy-up and got one. He asked whether the idea was sound first, and gave
permission to say no. That is what surfaced the four roots. His own CLAUDE.md
lists "check the premise, not just the request" as a lesson that keeps proving
itself here, and this is the same lesson arriving from his side of the desk.
Any edit that reorders this into a cleanup checklist loses the only reason the
post is worth reading.

WHAT WAS LEFT OUT, deliberately:
  - The Onesimus name story (Philemon, useless to useful). Kyle raised it and
    suggested it might be its own post. It should be. Buried at the bottom of a
    maintenance entry it would be a footnote; it is the best story he told all
    day. Logged in docs/post-ideas.md.
  - The full configuration list: attachment defaults, link updating, excluded
    folders, git fsck. True, his, and unreadable in a post. The specifics that
    survived are the ones a reader can feel: 255 duplicates, 54 files to 9.
  - Backup codes were in one of the folders. Left out on purpose. Saying where
    credentials sat in a vault, even fixed, is not something to publish.

NUMBERS ARE HIS AND SHOULD NOT BE ROUNDED for rhythm: 15+ commits, 6 near
identical skills, 255 deduped, 1 triplicated, 19 sync conflicts, 1150 notes,
54 loose files to 9 hub notes, more than 5 files as the blast radius trigger.

THE LESSON IS STATED, second to last, on purpose. Kyle asked whether it should
be spelled out at the end. It should: it is the one line a person or a model
can lift out of the post whole, which is what makes it worth quoting. But it
sits BEFORE the closing paragraph, not after, so the entry still ends on him
rather than on a moral. Don't move it to last.

"Hub notes" is his source's phrase and he said he didn't know what it meant, so
the post now explains it in the same sentence rather than assuming. If a term
in here needs a footnote, it needs a clause instead.
-->

I've been building an AI operating system inside my LLM wiki (my Obsidian
vault), which is also where a good portion of what I've written lives. I'd
already had a first go at building it, but before I changed anything else in
there, I stopped and asked a different question: is keeping my AI OS inside my
LLM wiki a good idea? And if it isn't, why not?

The answer was yes, and the reasoning stuck with me. The whole point of a second
brain is that the context sits next to the thing it's about. My operating system
is mostly instructions: how my projects run, how I write, how I like things
done. All of that already lives in the vault. Split them up and one search index
becomes two, one backlink graph becomes two, and every tool that wants file
access needs two paths instead of one.

Then it gave me three ways that goes wrong.

- Blast radius. Point an agent at the operating system folder and what it
  usually gets is the whole vault root. One bad loop can write two hundred
  files, or start a sync conflict cascade across every device I own.
- Version control. Notes want to sync continuously. Agent instructions want
  commits and diffs, so that when a prompt gets worse I can find out why and
  roll it back. Those two wants fight each other.
- Noise. Run logs, transcripts, scratch files. They pollute search and the graph
  until the vault stops feeling like my thinking and starts feeling like a build
  directory.

The fix for all three is a boundary. One folder for the durable things, system
prompts and skills and style guides. A scratch directory outside the vault for
everything an agent generates. Write access scoped to that folder rather than
the vault root, while read access to the whole vault stays open, because reading
is where most of the value is anyway.

The test of whether the boundary is drawn right is whether that folder still
works somewhere else. The operating system should read the vault, not depend on
it.

So I handed over the actual folder and asked it to stop describing and start
fixing.

It found that I had four.

Not four folders. Four things that all looked like an operating system. The real
one was fine: fifteen or more commits, an instruction file that genuinely knows
about the business I'm starting, decision logs, priority stacks. A working
system, not a folder of prompts.

The other three were the problem. One was an unversioned shadow copy holding six
skills nearly identical to the real ones, with no way to tell which was current.
One was a blank template. One was a note quietly writing itself into a fourth.

Four roots means no roots.

What came out of it: one root. A policy file that splits the vault into zones
and halts any run that would touch more than five files outside the boundary,
showing me the list before it proceeds. A vault map, so an agent reads two
folders instead of grepping eleven hundred and fifty notes. A runtime folder
Obsidian ignores completely, where agents can write at no cost to my search.

And the cleanup underneath all that: two hundred and fifty-five duplicate files,
one of them triplicated, nineteen sync conflicts buried in scripture notes and a
journal from 2023. My root went from fifty-four loose files down to nine hub
notes, which are just entry points: notes whose whole job is to point at other
notes rather than hold anything themselves.

If there's one thing worth taking from this, it isn't the cleanup. It's that I
asked whether the idea was any good before I asked for more of it to be built,
and I left room for the answer to be no. That question is what turned up the
other three roots I didn't know I had.

I don't understand all of it yet. I know what the vault map is doing and I'm
still catching up on the rest. I'm not going to let that slow me down. I'd
rather keep going and learn the parts I'm missing when something breaks.
