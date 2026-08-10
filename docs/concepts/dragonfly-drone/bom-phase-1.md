# Build order — prove Anisoptera without abandoning the ask

Each phase proves one inversion. **Do not “temporarily” solve Phase N with a 25 g Wi‑Fi quad** unless a gate explicitly kills Anisoptera.

## Phase A — Pinna on the bench (camera invention)

**Goal:** phone shows a reconstructed live view from a single-detector coded imager.

| Need | Notes |
|---|---|
| Photodiode + TIA | Breakout OK on bench |
| Coded mask | LCD shutter, printed film wheel, or DEA |
| Metasurface or simple lenslet | Start with lenslet; replace later |
| Host MCU | Streams measurements over USB/serial to Mac/phone |
| Reconstruction code | Python → Core ML / NPU |

**Pass:** recognizable 64×64 scene @ ≥3 Hz under desk lighting.  
**Fail:** if only dense raster scanning of N pixels works, compressive path needs better priors — iterate algorithms before adding flight.

Spend: optics + electronics dozens to low hundreds of USD. No airframe yet.

## Phase B — Return Gleam on a stick

**Goal:** measurement stream survives an MRR optical link across a room.

| Need | Notes |
|---|---|
| Corner-cube or cat’s-eye | Small optic |
| Modulator | MQW if obtainable; else LCD/liquid crystal shutter for low rate proof |
| Interrogator | Lab laser + PD on the receiver side (keel prototype) |
| Pointing | Manual first, then simple galvo/tracker |

**Pass:** ≥20 kb/s usable throughput at 3–6 m with bit error low enough for Pinna.  
**Fail:** improve modulator / optics; do not add Wi‑Fi TX to the *aircraft* mockup as the “fix.”

## Phase C — Lumen Keel power

**Goal:** deliver ≥0.25 W electrical into a PV + boost load the size of the abdomen budget.

| Need | Notes |
|---|---|
| IR laser + driver | Interlocked enclosure or certified product path |
| PV matched to λ | Small cells |
| Tracker | Keep spot on PV while target moves on a rail |

**Pass:** continuous power under motion profile that mimics slow flight.  
**Eye safety:** non-negotiable; enclosed range until interlocks are real.

Reference existence: UW laser-powered 190 mg liftoff — we are productizing, not proposing new physics.

## Phase D — Vein Drive lifter

**Goal:** 1–2 g class flapping vehicle hovers / orbits under beamed power **without** Pinna first.

| Need | Notes |
|---|---|
| Piezo or DEA wings | Follow RoboBee/Robofly fabrication literature |
| HV drive electronics | Milligram-class packaging |
| Beam tracking on moving target | Hardest integration |

**Pass:** 30 s controlled flight under keel.  
**Only here** does AUW get sacred.

## Phase E — Integrate Pinna + Gleam on the flyer

**Goal:** phone shows reconstructed video from the living aircraft while you pilot from the app.

**Pass:** the original ask, indoors.

## Explicitly retired path

ESP-FLY / 25 g phone quad was the **old** brief’s on-ramp. It teaches sticks, not Anisoptera. Use it only as a **human training tool** for iOS UI, never as the vehicle architecture.

## Rough cost posture (orders of magnitude)

| Phase | Order |
|---|---|
| A–B | $100–800 materials + time |
| C | Dominated by safe laser + tracking (can be $1k+ if bought wrong — design before shopping) |
| D–E | Fabrication tooling is the real cost; partner with a micro-robotics lab if needed |

Standing rule still applies: no new **subscriptions** lightly; capital parts are a conscious Gate 0 choice.
