<!-- Source: src/content/writing/the-synapse.md · UNPOSTED · queued 2026-08-08 -->

found a real gap in my AI OS today.

morning coffee and nightcap work great inside their own folder. but i spend most of my day in other repos. and those are completely invisible to the brain.

the morning briefing had no idea where yesterday went.

so we're wiring a synapse. three pieces:

1. workspace registry: lists every project folder with a stack priority. unplaced folders surface in nightcap.

2. pulse script: registers the folder on session start. pulse writes at session end and each agent stop. timestamp + folder name.

3. synthesis layer: `synapse-status.sh` reads the pulses, checks the registry, hands morning/nightcap a real picture of the day. wired now.

the principle: connection is automatic. stack placement is intentional.

the brain stays in one place. the work happens everywhere.
