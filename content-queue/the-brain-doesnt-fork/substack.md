<!-- Source: src/content/writing/the-brain-doesnt-fork.md · UNPOSTED · queued 2026-08-08 -->

For a while I was running two AI tools in parallel. Cursor for the code and repo work, and the Claude app for thinking, planning, and drafting. The logic made sense: different tools for different jobs.

Today I canceled the Claude app subscription.

Cursor handles everything now. The planning, the creative work, the post drafts, the repo sessions. One surface.

That decision created a temptation worth naming, because the obvious solution to it was the wrong one.

When Cursor became the only surface, the natural thing to do was to copy my AI operating system into every Cursor project. Paste the brain into each repo so it follows me. That would have been a mistake.

Two copies of a brain drift. You update one and forget the other. You make a decision in one session and it doesn't reach the other. Within a few weeks you're managing two systems that are supposed to be one, and neither of them fully is.

The right move was simpler.

My AI OS (Onesimus) is just plain markdown files. Every file in it is readable from anywhere, as long as you have the path. So instead of copying it, I wrote a thin User Rule for Cursor, pointing at the Onesimus files on demand. When an agent needs my priorities, it reads them. When it needs my voice, it reads that. When it needs a decision, it checks the log.

One brain. A thin pointer as the delivery layer. The brain doesn't move and it doesn't fork.

The distinction that made this obvious: Onesimus is surface-agnostic. The files don't care whether they're read by a Claude app or a Cursor agent. Only the delivery layer differs. So the right thing to change was the delivery layer, not the files.

If you're building something like this, that's the pattern worth holding. The temptation when you change surfaces is to replicate the brain. The better move is to make the brain surface-agnostic and teach each delivery layer to find it.

---

*This is part of a running log of building an AI operating system for a one-person business. Previous entries are on my [Personal AI OS build page](https://kylecovan.com/builds/personal-ai-os).*
