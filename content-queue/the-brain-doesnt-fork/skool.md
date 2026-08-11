<!-- Source: src/content/writing/the-brain-doesnt-fork.md · UNPOSTED · queued 2026-08-08 -->

Consolidated my AI tools today. Canceled Claude, everything through Cursor now.

Quick thing I learned in the process that might save someone else the same mistake:

When I moved to one surface, the tempting move was to copy my AI OS into every project so it'd "follow me." Don't do this. Two copies drift and within a couple weeks you're maintaining two systems that are supposed to be one.

The better move is a thin pointer. My OS is plain markdown files. They're readable from any path. So I wrote a User Rule for Cursor that points at the OS files on demand rather than copying them.

Same pattern as a lot of good system design: make the core surface-agnostic, teach each surface to find it.

Curious if anyone else has run into this when switching between Claude Code, Cursor, or other tools. How'd you handle carrying your context across surfaces?
