<!-- Source: src/content/writing/all-clouds-are-not-equal.md · UNPOSTED · queued 2026-08-11 -->

I spent an afternoon confused by a word.

I set up a cloud environment for my AI operating system, and then couldn't answer a simple question: where does the work actually get saved, and what can reach it?

The problem was that "cloud" was doing two jobs at once.

One of them is a brain. When you send a request, the thinking happens on the provider's servers. That's the model. It has no folder, no terminal, no copy of your repo. It reasons, and that's all it does.

The other is a machine. A cloud VM is a temporary Linux computer spun up in a data center to do the physical work: clone the repo, run commands, open a browser. Those are hands.

Once I saw it as a brain and a pair of hands, everything else fell into place.

Running an agent on your own laptop and running one in the cloud use the same brain. The only difference is whose hands it uses. Your laptop has to be awake for its hands to work. The cloud VM doesn't care whether your laptop exists.

That also answered the saving question. GitHub is the shelf they both reach for. Neither machine reads the other's hard drive. If you want yesterday's work visible to a cloud agent, you push it. Nothing gets there by being nearby.

And my phone, which I'd had backwards: it can't work a repo on its own, because there's no machine attached to it. It talks to the brain and tells it which hands to use. It's a remote control, not a workstation.

Most of what felt hard about this was vocabulary. Two very different things were wearing the same word.
