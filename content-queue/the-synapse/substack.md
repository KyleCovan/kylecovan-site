<!-- Source: src/content/writing/the-synapse.md · UNPOSTED · queued 2026-08-08 -->

The morning briefing worked fine inside my AI operating system. It pulled my priorities, checked the decisions log, looked at what I'd planned the day before. That part worked.

Then I'd spend the next six hours in a different project folder, and when nightcap ran at the end of the day it couldn't see any of it. The morning didn't know what I'd been building. The night didn't know either. Each session in another project was invisible to the brain that was supposed to keep track of things.

That's an honest gap and worth naming. The brain knows what's in its own folder. It doesn't automatically know what's happening anywhere else.

**How the gap shows up**

My personal site lives in one folder. My Tapo Canyon work lives in another. If I spend a day in the personal site repo, Onesimus sees none of it. Nightcap pulls nothing about what I actually did. The morning briefing the next day has no sense of where yesterday went.

The information exists. It's just somewhere the brain can't reach.

**The synapse**

The solution is three pieces, and the idea behind them is simple: connection is automatic, stack placement is intentional.

The first is a workspace registry. A file in Onesimus that lists every project folder the brain should know about, each one tagged with a path, a stack priority, and a status. New projects that haven't been placed yet show up as "unplaced" so nightcap can ask about them.

The second is a pulse script. Session start registers the folder if it's new. The pulse line itself writes at session end and at the close of each agent turn: a timestamp and which folder was active. Morning coffee reads those lines and knows where the work happened. No elaborate summarizing, just a clear record.

The third is the synthesis layer. `synapse-status.sh` reads the pulse files, checks the registry, and gives morning coffee and nightcap an actual picture of the whole day across all folders. That's wired now.

**What it's solving**

The goal isn't to make the brain aware of every detail across every project. It's to know which ones I touched, in which order, and how they map to my priority stack. Everything else it already knows from context.

Once this is running, the morning briefing can say "you were in the personal site most of yesterday" without me telling it. Nightcap can ask about a new project and decide whether it belongs in a workstream or gets parked.

The brain stays in one place. The work happens everywhere. The synapse connects them.

---

*This is part of a running log of building an AI operating system for a one-person business. Previous entries are on my [Personal AI OS build page](https://kylecovan.com/builds/personal-ai-os).*
