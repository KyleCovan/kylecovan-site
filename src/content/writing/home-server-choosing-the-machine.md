---
title: "Making an old iMac always on"
date: 2026-08-06
draft: true
---

<!--
DRAFT — HELD BACK ON PURPOSE. Do not publish as written.

This entry concludes the iMac is the server. Kyle reversed that on August 5 in a
later session: the 2021 M1 Pro becomes the clamshell server instead.

The two reasons this entry gives for rejecting the M1 Pro (see "The machine I was
tempted to use instead") are both now false. Kyle does not edit video by hand and
does not make music on it anymore — he wants AI pipelines for the video work. The
argument that survived is different and stronger, and is not in this draft at all:
he already has scheduled jobs that never fire because he closes the lid.

The reversal is on-genre, not a problem. This entry already opens by promising the
parts where he was wrong, and already contains one reversal. Rewrite it as a piece
with two, not as if the iMac section never happened.

What survives unchanged: the iPad-cannot-be-a-server reasoning, the stale-facts
lesson, sync-is-not-backup, and the priority note at the end.
-->

I have a 2019 iMac sitting in my house doing very little. I want to turn it into an always on server so my Obsidian vault stays in sync across my iPhone, my laptop and my iPad, and so my AI operating system can keep working when I am not at my desk.

This is the first entry in that build. I am writing these as I go, including the parts where I was wrong, because the parts where I was wrong turned out to be the useful parts.

## The question I started with

I own a few machines. I wanted to know which one should be the always on box.

I had two candidates in mind: the 2019 iMac, and a fifth generation iPad Air.

The iPad was out immediately, and not because it is slow. iPadOS does not allow background processes. Apps get suspended the moment they lose focus. There is no way to run a database, a sync service, a git remote or a scheduled job on it. It is a very good client and it cannot be a server. That is a hard limitation, not a tradeoff I could work around.

So it came down to the iMac.

## What the iMac actually is

I pulled the real numbers instead of guessing:

- iMac Retina 4K, 21.5 inch, 2019
- 3.0 GHz 6 core Intel i5
- 8 GB of DDR4 memory
- 256 GB internal SSD with about 206 GB free
- Radeon Pro 560X

Six cores and a real SSD. For the work I am actually asking it to do, which is mostly waiting around and occasionally calling an API, that is plenty.

## The part where I found out I had already decided this

Here is the honest bit.

Partway through working this out, I went looking through my own vault and found a decision log entry dated July 23. In it I had already chosen the iMac. I had already compared it against a spare MacBook. I had already decided the OS should live on the internal drive, that the external SSD gets demoted to backup duty, and that I would reach the machine over Tailscale.

I had made this decision two weeks ago, written down my reasoning, and then forgotten I did it.

That is worth sitting with. I keep a decision log specifically so I do not redo work. It only helps if I read it. Writing something down is not the same as remembering it, and a second brain you do not consult is just a folder.

The good news is I arrived at nearly the same answer the second time, which suggests the reasoning was sound. The bad news is I spent the time twice.

## What my own record got wrong

The July 23 entry said the iMac was a better choice than the spare MacBook partly because the iMac was "still getting security updates."

That was true when I wrote it. It is not true now.

The iMac is running Ventura 13.7.2. Apple only patches the current version of macOS and the two before it. Right now that means Tahoe 26, Sequoia 15 and Sonoma 14. Ventura fell off that list some time around late 2025. So my always on box, the one that is going to sit on the internet holding my entire vault, is currently running an operating system that stops receiving security patches.

The conclusion still holds. The iMac is still the right machine. But it is only the right machine after it gets upgraded, and until then it is in the same category as the old MacBook I rejected for exactly that reason.

This is the real lesson from the whole session. A decision log is not a set of facts. It is a set of facts *as of a date*. Some of those facts have a shelf life, and the ones about software support have a short one. I am going to start dating the assumptions inside my decisions, not just the decisions.

For the record: this iMac can run Sequoia, which is currently at 15.7.8. It cannot run Tahoe. macOS 27 drops Intel support entirely. So Sequoia is the end of the line, and it should keep getting security patches until roughly autumn 2027. That gives me about a year of runway, which matches the twelve to eighteen months I estimated in July.

## The machine I was tempted to use instead

Halfway through I had a better idea, or what felt like one. I also own a 2021 MacBook Pro with an M1 Pro chip and 32 GB of memory. On paper it is a far better server. It idles at around 5 watts instead of 47. It has a battery, which is a built in backup power supply. It is silent. It is Apple silicon, so it will keep getting macOS updates for years after the iMac stops. And 32 GB of memory means it can actually run open weight models locally, which is something I want to do.

It wins every category. I still did not use it.

Two reasons. First, it is my working machine. I edit video on it and I make music on it. A server lives in a closet with the lid closed, so making it the server means giving that up, and then pulling my "always on" machine off the shelf every time I want to work would defeat the point.

Second, the fallback would have been an older MacBook Pro from around 2015, which cannot run a supported version of macOS. I would have been fixing a small security problem on a machine that sits in my closet by creating a bigger one on the machine I use every day and browse the web on.

## The thing that made the decision easy

The only reason I was tempted by the M1 Pro was that I want to run local models. Then it occurred to me that local models do not belong on an always on machine at all.

Running a model is interactive. You want it fast and in front of you while you are working. It is not a background service waiting for something to happen. So it belongs on the machine I am sitting at, which is already the M1 Pro, and it has the memory for it today.

That collapsed the whole problem. The iMac takes the boring always on work: sync, scheduled jobs, backups, holding the repo. The M1 Pro stays my laptop and becomes the local model machine. Nothing competes with anything.

It also settled a conflict I did not realize I had. I have a project on local and open weight models that I archived a couple of weeks ago, and part of my reason for archiving it was that it "competes for the same iMac." It never did. The iMac cannot meaningfully run local models at all: 8 GB of memory, and AMD graphics on an Intel Mac are a dead end for inference. Those two projects were never fighting over anything.

## What it costs

The software is mostly free. Tailscale covers this on its free tier, which allows six users and unlimited devices. The macOS upgrade is free. Git and GitHub are free.

The one thing I pay for is Obsidian Sync at four dollars a month, which I already had.

The surprise is electricity. Apple rates this iMac at 47 watts idle. Running that continuously is about 412 kilowatt hours a year, which lands somewhere around twelve to fourteen dollars a month here in California.

The power costs three times more than the software. That is the actual argument for eventually replacing this with a Mac mini, which idles around 5 watts. Not speed. Not features. The power bill.

## What I am actually building

The order matters more than the list:

1. Upgrade to Sequoia. Nothing else starts until this is done.
2. Energy settings. The important one is "start up automatically after a power failure." A server that needs a human to walk over and press a button after a power blip is not a server.
3. Decide about FileVault. If it is on, the machine will not finish booting after an outage until someone types the password, which quietly defeats the whole thing.
4. Tailscale on all four devices, with key expiry disabled so the server does not silently drop off the network in six months.
5. Obsidian Sync, set up on the laptop first, because that is the machine holding the good copy of the vault.
6. Git and the AI OS repo on the internal drive.
7. Time Machine to an external drive.

Then one scheduled job, and only one.

## Two things I nearly got wrong

**Sync is not backup.** I was treating "my notes are on four devices" as safety. It is not. If I delete a folder on my phone, sync will faithfully and immediately delete it on all four. Four copies of a mistake is still one mistake. The iMac is the perfect machine to run Time Machine precisely because it is the one that is always on and always plugged in.

**Put it in the house, not the garage.** My original plan was the garage. This iMac has a display glued on with adhesive and an Intel processor that runs warm. Heat cycling through a California summer in an uninsulated garage is how these machines die, and any repair means cutting the screen off. Since Tailscale means I can reach it from anywhere, there is no reason for it to be somewhere hot.

## Where this sits against everything else

One more honest note.

I keep a ranked list of what I am supposed to be working on. Building this machine is on it, but it is second. First is revenue: ship the site, publish the videos, follow up with the lead, open the business bank account. I have about ten weeks against a deadline of one to three paying clients by mid October.

My own notes from late July flag the exact failure mode I need to watch: a tooling block that "consumed a focus block and produced nothing shippable." Thirty five commits and eleven skills in one week, against zero published videos and zero clients.

So I am being deliberate. This build is about half a day of work and it closes four separate things I have been circling. That is real leverage, which is why it ranks second instead of last. But it does rank second, and a build log is not a client.

Next entry: the upgrade, and the one scheduled job.
