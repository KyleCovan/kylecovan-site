---
title: "All clouds are not equal"
date: 2026-08-11
build: personal-ai-os
draft: true
---

I set up a cloud environment for Onesimus, my AI operating system, and then spent a while confused about something that should have been simple. Where does the work actually get saved, and what can reach it?

The confusion came from one word doing two jobs. In Cursor, "cloud" means two different things, and they are not the same thing at all.

The first one is a brain. When I type a request, the thinking happens on Cursor's servers. That is the model, and the machinery around it that decides what to do next. It is not a computer I can open a file on. It has no folder, no terminal, no copy of my repo. It reasons, and that is all it does.

The second one is a machine. A cloud VM is a temporary Linux computer that Cursor spins up somewhere in a data center to do the physical work: clone the repo, run commands, open a browser. Those are hands.

Once I saw it as a brain and a pair of hands, the rest fell into place.

There are two ways to run an agent, and the only real difference between them is whose hands it uses.

Remote Control points the brain at my Mac. The thinking still happens in Cursor's cloud, but the file edits and the terminal commands land on my own machine. That means my Mac has to be awake. If the lid is shut, there are no hands.

A Cloud Agent points the brain at the VM instead. Same thinking, different hands. My Mac can be off and closed, because the work is happening on a machine that isn't mine.

Same brain both times. The only question is whose hands you want it to use.

That reframing also answered the question I had actually gotten stuck on, which was where things get saved.

GitHub is the shelf they both reach for. My Mac pushes to it. The VM clones from it. Neither one is reading the other's hard drive. If I want work I did on my laptop to be visible to a cloud agent later, I have to push it. Nothing gets there by being nearby.

It explains something about my phone that I had backwards, too. My phone can't work a repo on its own, because it has no machine attached to it. What it can do is talk to the brain and tell it which hands to use, either the VM or my Mac through Remote Control. The phone is a remote control, not a workstation.

The last piece was the saved environment. I had assumed that setting one up would make Onesimus available everywhere, including in the chat on my desktop. It doesn't work that way. A saved environment is a pre-warmed set of hands for cloud agents. It's the VM with the setup already done, so the agent doesn't sit there installing things before it can start. My desktop chat never touches it, because my desktop already has hands.

For Onesimus specifically, that made the day to day simple.

Push often, so the phone and the cloud are always looking at current files. Rebuild the environment only when the dependencies or the config actually change, not because time has passed. And since Onesimus is a folder of plain markdown files, there is nothing heavy to pre-warm in the first place, so letting it build fresh every time costs nothing.

None of this was difficult once I had words for it. It was difficult while one word was doing two jobs.
