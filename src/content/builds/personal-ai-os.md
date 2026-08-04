---
name: Personal AI OS
order: 1
# A colon inside an unquoted YAML scalar starts a mapping, which fails the
# build. Quoted so the one-liner can use one. This is not a style preference.
oneLiner: "An AI operating system that runs quietly in the background like a digital assistant: keeping me on track, strategizing with me, flagging opportunities, and spotting bottlenecks before they become real problems."
# Sitemap <lastmod>. Seeded from this file's last commit date, not invented.
updated: 2026-07-30
# Held, not displayed. Kyle added "Nate Herk style" as a subtitle to credit where
# the inspiration came from. As a qualifier under the name it read as a borrowed
# credential, so it was removed from the heading on July 30 — but the nod itself
# was worth keeping, and belongs in a sentence of the prose below rather than in
# the title. Kept here so the fact survives until that prose is written.
inspiration: Nate Herk
# NOT RENDERED. Writing prompts for the prose below — see content.config.ts.
# These used to publish as "What the log will cover", which put a list of
# promises on a page that had nothing behind them yet.
prompts:
  - lead: The friction that started it
    rest: COVERED by the "Too many ideas" entry. Don't repeat it in the prose.
  - lead: How it works today
    rest: partly covered by the entry (what it watches). The build is not.
  - lead: What it caught
    rest: COVERED by the "Too many ideas" entry. Don't repeat it in the prose.
  - lead: What broke
    rest: the versions that failed and what I changed. STILL UNANSWERED.
  - lead: Where it goes next
    rest: COVERED by the "Too many ideas" entry (the video pipeline).
---

<!--
DRAFT, July 30 — shaped from Kyle's dictated answers, NOT invented. Every claim
below traces to something he said in conversation; nothing was added to make it
read better. Same method as the "Too many ideas" entry (handoff §6).

He asked for a draft to edit rather than a blank page, which is a deliberate
waiver of the usual "ask, don't draft" rule and applies to THIS page only. It
does not license inventing anything he hasn't said.

ANSWERED since, and now in the prose: what triggers it (only when he asks), how
it reaches Gmail, Calendar and OBS (MCP servers and APIs), where the Markdown
lives (his Obsidian vault), and that it writes back rather than only reading.

STILL MISSING, and only Kyle can answer:
  - what broke. Nothing in any repo record answers this. The failures written up
    in docs/handoff.md are the WEBSITE's, not this system's, and must never be
    borrowed to fill this section.

August 3: the Nate Herk credit landed in the prose, where the July 30 note said
it belonged. Em dashes struck from this page's prose under the rule Kyle set
that day for anything published in his voice.
-->

## What it is

An AI operating system has the tools you already use linked into it, so you're
not clicking around a browser all day. Gmail, Google Calendar, Granola, Slack,
Instagram. Instead of going to each one, you work from a single place.

It remembers me. It keeps track of who I am and learns as it goes, so it gets
better at helping me organize what I already do, and at surfacing things I don't
do yet. It takes a rough idea and turns it into a working project, and it helps
me get projects out the door instead of piling ideas up.

The structure of it came from Nate Herk. He'd put a repo out publicly, so
instead of starting from a blank page I started from his. It gave me the
scaffolding and, more than that, a direction to build in. I've shaped it around
how I work since then, but the foundation is his, and I wouldn't have gotten off
the ground without it.

## How it's built

It lives on my own computer. Everything in it is Markdown files, which are just
plain text with a little formatting on top.

That's what keeps it light. There's no database underneath it and no app it has
to run inside. I can open any piece of it in any text editor, read it myself,
and change it by hand if I want to.

An LLM reads it and runs it, in my case Claude. The files sit in my Obsidian
vault.

It reaches Gmail, Calendar and OBS through MCP servers and APIs, and it doesn't
only read them. It writes back.

Right now it runs when I ask it something. Getting it to run on its own, without
me starting it, is the part I haven't unlocked yet.
