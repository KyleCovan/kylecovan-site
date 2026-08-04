---
name: Personal AI OS
order: 1
oneLiner: An AI operating system that runs quietly in the background like a digital assistant, flagging opportunities and spotting bottlenecks before they become real problems.
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

STILL MISSING, and only Kyle can answer:
  - what triggers it: a schedule, or only when he asks?
  - how it reaches Gmail / Calendar / OBS: MCP servers, n8n, scripts?
  - where the Markdown lives: inside the Obsidian vault, or separate?
  - whether it writes back, or only reads and surfaces.
  - what broke. Nothing in any repo record answers this — the failures
    documented in docs/handoff.md are the WEBSITE's, not this system's.
-->

## What it is

An AI operating system has the tools you already use linked into it, so you are
not clicking around a browser all day. Gmail, Google Calendar, Granola, Slack,
Instagram. Instead of going to each one, you work from a single place.

It remembers me. It keeps track of who I am and learns as it goes, so it gets
better at helping me organize what I already do, and at surfacing things I don't
do yet. It takes a rough idea and turns it into a working project, and it helps
me get projects out the door instead of piling ideas up.

I got the idea of building it this way from Nate Herk. What I've made is my own,
but the shape of it is his.

## How it's built

It lives on my own computer. Everything in it is Markdown files, which keeps it
light. An LLM reads it and runs it, in my case Claude. The files sit in my
Obsidian vault.

It reaches Gmail, Calendar and OBS through MCP servers and APIs, and it doesn't
only read them. It writes back.

Right now it runs when I ask it something. Getting it to run on its own, without
me starting it, is the part I haven't unlocked yet.
