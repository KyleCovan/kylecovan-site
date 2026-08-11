<!-- Source: src/content/writing/the-synapse.md · UNPOSTED · queued 2026-08-08 -->

Found a gap in my AI OS setup and curious if others have run into this.

My morning briefing and end-of-day recap work inside their own folder. But most of my actual work happens in other project folders. And those are invisible to the brain. The morning briefing had no idea where yesterday went.

Starting to wire a fix I'm calling a synapse:

- A workspace registry that lists every project folder with a stack priority
- A pulse script that registers the folder on session start and writes a timestamp + folder name at session end and on each agent stop
- `synapse-status.sh` reads those logs so morning coffee and nightcap can describe the full day across all projects

The guiding idea: connection is automatic, stack placement is intentional.

Has anyone solved this in their own second brain or AI OS? The "brain in one folder, work in many folders" problem seems like it'd come up for anyone building this kind of setup.
