---
title: "The brain that couldn't see the rest of the work"
date: 2026-08-08
kind: log
project: Personal AI OS
draft: true
---

The morning briefing worked fine inside Onesimus. It pulled my priorities, checked the decisions log, looked at what I'd planned to do the day before. That part worked.

Then I'd spend the next six hours in a different repo, and when nightcap ran it couldn't see any of it. The morning didn't know what I'd been building. The night didn't know either. Each session in another project was invisible to the brain that was supposed to keep track.

That's an honest gap and it's worth naming. The brain knows what's in its own folder. It doesn't automatically know what's happening anywhere else.

## How the gap shows up

My personal site lives in one repo. Tapo Canyon lives in another. If I spend a day rebuilding the site, Onesimus sees none of it. The nightcap pulls nothing about what I actually did. The morning briefing the next day has no sense of where yesterday went.

The information exists. It's just in a different folder, and the brain has no way to reach it.

## The synapse

The solution we're wiring is called the synapse. The idea is straightforward: connection is automatic, stack placement is intentional.

Three pieces.

The first is a workspace registry. A file in Onesimus that lists every project folder Cursor should know about, each one tagged with a path, a stack letter, and a status. Projects that land without a stack letter show up as unplaced and nightcap can ask about them. The registry is live now.

The second is a pulse script. Session start registers the folder if it's new. The pulse line itself writes at session end and at the close of each agent turn: just a timestamp and which repo was active. No elaborate summarizing. Morning coffee reads those lines and knows where the work happened. That script is live too.

The third is the synthesis layer: `synapse-status.sh` reads the pulse files, checks the registry, and hands morning coffee and nightcap an actual picture of the day across all repos. That's wired now.

## What this is solving

The goal isn't to make Onesimus aware of every detail in every repo. It's to know which ones I touched, in which order, and how they map to the stack. Everything else the brain already knows from context.

Once this is running, the morning briefing can say "you were in kylecovan-astro most of yesterday" without me telling it. Nightcap can ask about a repo it's never seen before and decide whether it belongs in a workstream or gets parked.

The brain stays in one place. The work happens everywhere. The synapse is what connects them.
