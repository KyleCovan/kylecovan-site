<!-- Source: src/content/writing/the-synapse.md · UNPOSTED · queued 2026-08-08 -->

# The brain that couldn't see the rest of the work

The morning briefing worked fine inside my AI operating system. It pulled priorities, checked the decisions log, looked at what I'd planned the day before.

Then I'd spend six hours in a different project folder. When nightcap ran that evening, it couldn't see any of it. The brain that was supposed to keep track of things had no idea where the work happened.

That's an honest gap. The brain knows what's in its own folder. It doesn't automatically know what's happening anywhere else.

**How the gap shows up**

My personal site lives in one folder. My Tapo Canyon work lives in another. Spend a day in either and the AI OS sees none of it. The morning briefing the next day has no sense of where yesterday went.

The information exists. It's just somewhere the brain can't reach.

**The synapse**

The solution is three pieces.

A workspace registry: a file in the OS listing every project folder the brain should know about, each tagged with a path, a stack priority, and a status. New unplaced projects surface in nightcap so they can be assigned or parked deliberately.

A pulse script: session start registers the folder if it's new. The pulse line itself writes at session end and at the close of each agent turn. Timestamp and which folder was active. Simple. Morning coffee reads those lines and knows where the work happened.

A synthesis layer: `synapse-status.sh` reads the pulses, checks the registry, and hands morning coffee and nightcap an actual picture of the whole day. That's wired now.

**The idea behind it**

Connection is automatic. Stack placement is intentional.

The brain doesn't need to know every detail of every project. It needs to know which ones were touched, in which order, and how they map to priorities. Everything else it knows already.

Once this is running, the morning briefing can describe yesterday's work without being told. Nightcap can flag a new project and ask where it belongs.

The brain stays in one place. The work happens everywhere. The synapse is what connects them.
