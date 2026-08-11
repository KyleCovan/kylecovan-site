<!-- Source: src/content/writing/all-clouds-are-not-equal.md · UNPOSTED · queued 2026-08-11 -->

Set up a cloud environment for my AI OS this week and immediately got confused about where anything was saved. Posting what untangled it, because I don't think I'm the only one.

The word "cloud" is doing two jobs in Cursor and they're completely different.

One is a brain. When you send a request, the thinking runs on their servers. It has no folder, no terminal, no copy of your repo. It reasons and that's it.

The other is a machine. A cloud VM is a temporary Linux box in a data center that does the physical work: clones the repo, runs commands, opens a browser. Hands.

Once I had brain and hands, the rest was easy.

Remote Control = cloud brain, your Mac's hands. Your Mac has to be awake.
Cloud Agent = cloud brain, the VM's hands. Your Mac can be closed.

Same brain both times. You're only choosing whose hands.

Two things that followed from that:

GitHub is the shelf they both reach for. Neither machine reads the other's hard drive, so if I want laptop work visible to a cloud agent later, I push it. Nothing gets there by being nearby.

A saved environment is a pre-warmed set of hands for cloud agents, not something your desktop chat loads. Your desktop already has hands.

Anyone else set up cloud environments yet? Curious whether you're rebuilding them on a schedule or only when dependencies change. Mine is plain markdown so there's nothing heavy to pre-warm, but I'd guess that's different for a real codebase.
