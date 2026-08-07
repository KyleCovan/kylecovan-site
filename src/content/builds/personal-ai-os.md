---
name: Personal AI OS
order: 1
# A colon inside an unquoted YAML scalar starts a mapping, which fails the
# build. Quoted so the one-liner can use one. This is not a style preference.
oneLiner: "An AI operating system that runs quietly in the background like a digital assistant: keeping me on track, strategizing with me, flagging opportunities, and spotting bottlenecks before they become real problems."
# NOT rendered — overrides oneLiner for <meta name="description"> and the
# og:description share card only. Kyle picked this wording on August 6.
# The one-liner above is 210 characters and was being cut mid-clause in search
# results and on LinkedIn/X cards, which print it verbatim to someone who has
# not clicked yet. This keeps all four verbs — they are the substance — and
# drops the simile and the closing qualifier to land at 152. The page itself
# still says exactly what Kyle wrote.
description: "An AI operating system that runs quietly in the background: keeping me on track, strategizing with me, flagging opportunities, and spotting bottlenecks."
# Sitemap <lastmod>. Seeded from this file's last commit date, not invented.
updated: 2026-08-03
# Held, not displayed. Kyle added "Nate Herk style" as a subtitle to credit where
# the inspiration came from. As a qualifier under the name it read as a borrowed
# credential, so it was removed from the heading on July 30. The nod itself was
# worth keeping and now lives in a sentence of the prose, with a link to the
# video he actually followed along with.
inspiration: Nate Herk
# NOT RENDERED. Writing prompts for the prose below — see content.config.ts.
# These used to publish as "What the log will cover", which put a list of
# promises on a page that had nothing behind them yet.
prompts:
  - lead: The friction that started it
    rest: COVERED by the "Too many ideas" entry. Don't repeat it in the prose.
  - lead: How it works today
    rest: ANSWERED Aug 3. The three skills he actually uses, and the loop.
  - lead: What it caught
    rest: COVERED by the "Too many ideas" entry. Don't repeat it in the prose.
  - lead: What broke
    rest: ANSWERED Aug 3, dictated. The best material on the page.
  - lead: Where it goes next
    rest: the video pipeline is in the entry. The prose covers the longer arc.
---

<!--
Shaped from Kyle's dictated answers, NOT invented. Every claim traces to
something he said; nothing was added to make it read better. Same method as the
"Too many ideas" entry (handoff §6). He asked for a draft to edit rather than a
blank page, a deliberate waiver of the usual "ask, don't draft" rule.

August 3 — "What broke" answered at last, and it is the most valuable writing on
the page. Read this before editing it:

  He did not answer with software failures, and the section must not be quietly
  rewritten into a list of them. What he said broke was his own understanding,
  then his own working habits. The one genuine technical failure (scheduled
  tasks needing the laptop open, and the AI coach he deleted because of it) sits
  in the middle rather than at the top on purpose. Leading with the technical
  problem would make it a debugging note; leading with "my understanding broke
  down" is what makes the page an account rather than a brochure, which is
  exactly what he asked for.

  "I got it built. I couldn't always have told you why it worked" is his, in
  substance and in tone. Do not soften it. It is the most credible line here.

WHERE IT GOES NEXT, and why the heading is "Where I'm trying to get to": the
"Too many ideas" entry, which renders IN FULL on this page, already ends with
"next is a pipeline for making YouTube videos". Two sections both called what
comes next, at different horizons, would read as a contradiction. The heading
separates the long arc from the immediate next thing rather than competing with
it. If that entry is ever retitled or removed, revisit this.

THE AGENT AMBITION IS DELIBERATELY UNDERSOLD. Kyle was explicit that the point
is not the number of agents and not looking impressive for running many. It is
fluency, so that an idea reaches something instead of sitting. Any edit that
turns this into a bigger-is-better passage gets it backwards.

EM DASHES. None in this prose, under the rule Kyle set on August 3 for anything
published in his voice. Structural em dashes elsewhere are fine.

EXTERNAL LINK. The Nate Herk video is the one he followed to build this. The
share tracking parameter was stripped from the URL. verify_site.py skips
external links, so nothing checks it: if that video ever comes down, no test
will catch it.

NOT COVERED HERE, by his instruction: the things he built inside Claude Code.
He said that work is separate and doesn't belong on this page.
-->

## What it is

An AI operating system has the tools you already use linked into it, so you're
not clicking around a browser all day. Gmail, Google Calendar, Granola, Slack,
Instagram. Instead of going to each one, you work from a single place.

It remembers me. It keeps track of who I am and learns as it goes, so it gets
better at helping me organize what I already do, and at surfacing things I don't
do yet. It takes a rough idea and turns it into a working project, and it helps
me get projects out the door instead of piling ideas up.

The structure of it came from Nate Herk. He'd put a repo out publicly and made
[a video walking through it](https://youtu.be/bCljOfCH8Ms), so instead of
starting from a blank page I followed along with him. It gave me the scaffolding
and, more than that, a direction to build in. I've shaped it around how I work
since then, but the foundation is his, and I wouldn't have gotten off the ground
without it.

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

## What I actually use

Three skills, and they run as a loop.

Morning coffee doesn't recap the day, it pre-caps it. It tells me what I'm doing
today and why, built off what I did yesterday.

Plan Tomorrow works the other end, planning the next day out of what I've
actually been doing and the goals I've set.

Nightcap closes the circle. It sums up what I got done and what I didn't, and
feeds straight into Plan Tomorrow.

Those three I use constantly. There are other skills sitting in there I've never
touched, and a few I'd have to go and look up to tell you what they even do.

## What broke

The first thing that broke was my understanding of what I was doing.

Some of it I'm still wrapping my head around. Sometimes it was the terminology.
Sometimes it was just slow going and I took it in baby steps, leaning on Nate
Herk's video to hold the road map while I caught up. I got it built. I couldn't always
have told you why it worked.

Then there are the scheduled tasks, and the reason those break is boring: they
only run if my laptop is open and on. I built an AI coach that was meant to
nudge me when I drifted off task, set it to run every morning, and it simply
didn't. I deleted it. The idea is still a good one. I just haven't worked out
how to run something on a schedule on a machine that spends half its time shut.

I've also built features I've never gone back to, and skills I still haven't
implemented. All of that was time spent.

The honest version, though, is that most of what broke was already broken before
any of this existed.

I worked impulsively. Whatever came to mind was what I'd start, instead of
finishing what was already open, and by the end of a day I'd have a pile of
loose threads and no idea which of them mattered most.

I'm still coming off that. The old way was scattered and it was a habit, and a
habit doesn't leave because you installed something. What this is really doing
is teaching me to work differently, and some days that's harder than building it
was.

## Where I'm trying to get to

I started out running one task at a time and watching it work.

Now I'm learning to let things run on a schedule, or in the background while I'm
doing something else, so I'm not sitting there watching the whole time. Where
it's going is several agents running at once, all working together, with me
conducting instead of doing.

One person doing a job turns into ten. Then ten turns into a hundred.

The point isn't the number, though. Nobody needs to run a hundred agents to
prove anything. The point is getting fluent enough that an idea actually goes
somewhere. Right now most ideas don't. They show up, and then they sit. What I
want is for every idea to get a direction: either it's a bad one and I drop it
and stop thinking about it, or it's a good one and I can put real work behind it
and see it through.
