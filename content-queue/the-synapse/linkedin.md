<!-- Source: src/content/writing/the-synapse.md · UNPOSTED · queued 2026-08-08 -->

Found a real gap in my AI operating system today and started wiring the fix.

The morning briefing and end-of-day recap work great inside their own folder. But I spend most of my day in other project folders (personal site, Tapo Canyon). And those are completely invisible to the brain that's supposed to keep track.

The morning briefing had no idea where yesterday went. The nightcap pulled nothing about what I actually built.

So I'm wiring what I'm calling a synapse. Three pieces:

1. A workspace registry that lists every project folder the OS should know about, each tagged with a stack priority. New unplaced folders surface in nightcap so they can be assigned or parked deliberately.

2. A pulse script that registers the folder on session start and writes a timestamp and folder name at session end and on each agent turn's close. Simple record. Morning coffee reads it.

3. A synthesis layer: `synapse-status.sh` reads the pulses, checks the registry, and hands the morning and evening routines a real picture of the day across all folders. That's wired now.

The guiding idea: connection is automatic, stack placement is intentional.

The brain doesn't need every detail of every project. It needs to know which ones were touched and how they map to priorities. Everything else it already knows.

The brain stays in one place. The work happens everywhere. The synapse connects them.
