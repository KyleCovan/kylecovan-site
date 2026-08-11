<!-- Source: src/content/writing/the-brain-doesnt-fork.md · UNPOSTED · queued 2026-08-08 -->

# The brain doesn't fork

For a while I was running two AI tools in parallel. Cursor for the code and repo work, and the Claude app for thinking, planning, and drafting. The logic made sense: different tools for different jobs.

Today I canceled the Claude app subscription.

Cursor handles everything now. The planning, the creative work, the post drafts, the repo sessions. One surface.

That decision created a temptation worth naming, because the obvious solution to it was the wrong one.

When Cursor became the only surface, the natural thing to do was to copy my AI operating system into every Cursor project. Paste the brain into each repo so it follows me. That would have been a mistake.

Two copies of a brain drift. You update one and forget the other. Within a few weeks you're managing two systems that are supposed to be one, and neither of them fully is.

The right move was simpler.

My AI OS (Onesimus) is just plain markdown files. Every file in it is readable from anywhere, as long as you have the path. So instead of copying it, I wrote a thin User Rule for Cursor that points at those files on demand. When an agent needs my priorities, it reads them. When it needs my voice, it reads that. When it needs a past decision, it checks the log.

One brain. A thin pointer as the delivery layer. The brain doesn't move and it doesn't fork.

The distinction that made this obvious: the files are surface-agnostic. They don't care whether they're read by a Claude app or a Cursor agent. Only the delivery layer differs. So the right thing to change was the delivery layer, not the files.

If you're building an AI OS or a second brain you want to carry across tools, that's the pattern worth holding. The temptation when you change surfaces is to replicate. The better move is to build surface-agnostic files and teach each delivery layer to find them.

---

*Part of a running log of building an AI operating system for a one-person business.*
