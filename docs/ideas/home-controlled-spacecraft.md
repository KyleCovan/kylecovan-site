# Home-controlled spacecraft — first principles brief

**Status:** Idea intake. Not a published build. Not committed spend.
**Date:** 2026-08-10
**Constraint in force:** no new paid tools or subscriptions until a client is
paying. Every stage below has a zero-cash or nearly-zero-cash entry, and a
hard gate before money leaves the account.

This document is the heavy lifting: what the dream actually requires, which
parts of the dream physics will not allow, and a staged path that still delivers
the experience of piloting something beyond the atmosphere from home and
bringing pictures back.

---

## 0. The job to be done

Strip the romance and name the product:

> From a desk at home, send commands to a craft that has left the dense
> atmosphere, receive live or near-live visuals plus sensor data, and know
> that the craft is yours.

That sentence has five separable claims. Each one fails or succeeds on its own
physics:

| Claim | Hard constraint |
|---|---|
| **From home** | Residential power, zoning, antenna size, ISP uplink, FCC Part 97 / Part 5 |
| **Send commands** | Uplink power, licensed frequency, contact window, latency |
| **Craft beyond dense atmosphere** | Energy to get there; recovery or disposal when done |
| **Visuals + other data back** | Link budget (path loss × power × antenna gain × bandwidth) |
| **It is yours** | You own the bus, the license, the risk, the debris obligation |

If any one of those is non-negotiable and unmet, the idea is still a wish.

---

## 1. First principles — energy, orbit, and the word "space"

### 1.1 "Space" is not one place

| Regime | Altitude | What you get | What it costs an individual |
|---|---|---|---|
| **Near space (stratosphere)** | ~20–35 km | Black sky, curvature of Earth, 99% of air below you | Hundreds to low thousands USD; DIY recoverable |
| **Karman line / suborbital** | ≥100 km | Brief minutes of weightlessness; no orbit | Payload slot on a sounding rocket / New Shepard-class; five figures and up |
| **Low Earth orbit (LEO)** | ~300–600 km | Continuous free-fall; Earth passes every ~90 min | Rideshare; typically mid five figures for the smallest craft after aggregator markup |
| **Higher orbits** | GEO, lunar, etc | Out of scope for a first personal craft | |

The photograph that makes a human feel "I am in space" is available at 30 km.
The physics of *staying* there without falling back requires orbit. Those are
different products that share a camera and a radio.

**Decision this brief makes:** treat near-space as Stage A (prove the loop), and
LEO as Stage B (earn the word satellite). Do not skip A. A is where the control
and video problems get solved on a schedule you choose, not on a launch
manifest.

### 1.2 Why you cannot launch yourself into orbit

Orbital speed at LEO is ~7.8 km/s. Realistic launch Δv including gravity and
drag losses is ~9.4 km/s. Chemical rockets need mass ratios that make a
garage-built orbital launcher a national-lab problem, not a weekend one. FAA
commercial space rules close the rest of the door.

**Consequence:** for Stage B, you buy a ride. As of early 2026, SpaceX Transporter
SSO rideshare is publicly listed at **$350,000 for up to 50 kg** (plus $7,000/kg
above that). A 1U CubeSat does not need 50 kg, so individuals go through
**aggregators** who subdivide the slot. PocketQube (5 cm cube per "P") launch
slots have been marketed from roughly **€25k** for 1P via brokers such as Alba
Orbital — before bus, testing, licensing, insurance, and ground ops. Treat any
public number as a floor, not a budget.

### 1.3 Why you cannot "fly" an orbiter like a plane

Once on orbit:

- Continuous thrusting to "steer around" burns propellant you do not have on a
  picoclass craft, and creates conjunction risk with other objects.
- Debris mitigation and licensing assume a known orbit and a disposal plan, not
  freestyle piloting.
- Over a fixed home ground station you get **short contact windows** (often
  ~5–12 minutes, a few times per day), not a continuous cockpit link.

So "remote control from home" in orbit honestly means:

1. **Telecommand during passes** — mode changes, camera point, transmit now,
   safe-hold.
2. **Stored command stacks** executed when out of view.
3. Optionally **attitude control** (point the camera), which *feels* like
   piloting without claiming continuous 6-DOF flight.

If the dream requires a continuous stick-and-throttle experience looking down at
Earth, that is Stage A (balloon / loitering near-space craft), not Stage B.

---

## 2. The data problem (this is the real boss fight)

### 2.1 Free-space path loss

Received power falls with the square of distance. A craft at 30 km (balloon) and
a craft at 500 km (LEO) differ by a factor of ~280 in slant-range power, before
antenna gains. HD video wants megabits. Amateur UHF CubeSat downlinks are often
measured in **kilobits**. Those two sentences explain most failed "live video
from my satellite" pitches.

### 2.2 What actually works for visuals

| Link class | Typical rate | Visual product |
|---|---|---|
| APRS / narrow telemetry | bits–hundreds of bits/s | GPS, temps, voltages — no pictures |
| SSDV / Wenet-style balloon imagery | ~tens of kb/s | Progressive JPEG frames assembling live |
| Narrow DATV (DVB-S2 amateur) | ~0.1–1 Mb/s | Soft 288p–480p video if power and antenna allow |
| Commercial S/X-band + dish | Mb/s+ | Real video; cost and license jump hard |

**Design rule:** for a personal craft, default the visual product to
**store-and-forward stills with occasional low-rate live**, not Netflix-from-orbit.
Stills of Earth from your own craft still satisfy the job-to-be-done. Chasing
live HD from a 1P PocketQube is how budgets and schedules die.

### 2.3 The home ground station is part of the craft

Without a ground segment, you do not have a remote-controlled ship. You have a
lost object. The minimum honest station:

- Directional antenna (Yagi for UHF; later a small dish for higher bands)
- Rotor or careful hand-tracking for passes / balloon chase
- Software-defined radio (RTL-SDR class for receive; transmit needs a real radio
  and a license)
- Modem + decoder software (SatDump, Wenet, custom)
- A mission UI: map, command queue, last image, health

SatNOGS exists as a networked receive layer. It is a gift for downlink. It does
not replace **your** uplink, and it does not make the craft yours in the control
sense.

---

## 3. Architecture that survives every stage

Build one stack. Swap the vehicle under it.

```
┌─────────────────────────────────────────────┐
│  Mission control (home)                     │
│  map · command queue · image gallery · logs │
└──────────────────┬──────────────────────────┘
                   │ IP to radio shed / window
┌──────────────────▼──────────────────────────┐
│  Ground RF                                  │
│  antenna · TNC/SDR · licensed transmitter   │
└──────────────────┬──────────────────────────┘
                   │ uplink commands / downlink TM+imagery
┌──────────────────▼──────────────────────────┐
│  Flight computer                            │
│  safe modes · command auth · store-forward  │
├─────────────┬───────────────┬───────────────┤
│ Power       │ ADCS/pointing │ Radios        │
│ battery+PV  │ or gondola    │ UHF ± higher  │
├─────────────┴───────────────┴───────────────┤
│ Payload: camera + IMU + pressure + GPS      │
└─────────────────────────────────────────────┘
         ▲
         │ vehicle: balloon gondola → PocketQube bus
```

**Non-negotiable software properties from day one:**

1. **Authenticated commands** — even on a balloon. Practice the habit.
2. **Safe mode that needs no ground** — watchdogs, power brownout behavior.
3. **Every packet logged** — you will debug from logs, not from vibes.
4. **One image pipeline** — capture → compress → prioritize → radio → reassemble.
   Do not invent a second pipeline when you change vehicles.

---

## 4. Staged path to reality

Each stage has an exit test. Do not buy the next stage's hardware until the
exit test is green. Cash gates respect the standing "no new paid tools until a
client is paying" rule: Stage 0 and most of Stage 1 are skill and scrap; Stage 2
is the first real spend and needs an explicit yes.

### Stage 0 — Desk satellite (week-scale, ~$0–$150 if starting from nothing)

**Build:** a "craft" on the workbench: Raspberry Pi (or MCU) + camera +
temperature sensor + fake radio over USB/serial to a laptop "ground station."

**Prove:**

- Command uplink changes mode (idle / capture / transmit).
- Downlink returns telemetry + a still.
- Mission UI shows map pin (fake GPS), last image, battery proxy.

**Exit test:** you can sit in another room and operate it over the local network
as if it were far away. If the UI feels dead here, orbit will not save it.

**Cash:** prefer hardware already owned. If buying, one used Pi + camera module
is the ceiling.

### Stage 1 — Line-of-sight drone / kite / car roof (week-to-month)

**Build:** same stack, real RF at short range (licensed amateur or ISM as
appropriate). Pointing optional.

**Prove:**

- Command latency and packet loss under real RF.
- Image downlink under motion.
- Failures: brownout, watchdog reboot, lost link → safe mode.

**Exit test:** five successful sessions with logged command/ack and at least one
recognizable image per session.

**License note:** transmitting on amateur bands requires an amateur radio
license. Receiving-only can start earlier. Get the license in parallel with
Stage 0; it is on the critical path for everything that leaves the desk.

### Stage 2 — Near-space balloon (the first true "space" experience)

**Build:** foam/3D-printed gondola, latex or chloroprene balloon, parachute,
cutdown, GPS tracker (APRS or equivalent), camera, UHF imagery downlink
(Wenet/SSDV-class or a narrow video experiment), cold-rated batteries, FAA
notice where required.

**Prove the actual dream loop:**

- Launch, climb through the jet stream, black sky, curvature.
- Live progressive images (or constrained live video) to a ground station you
  operate.
- Uplink commands in flight (reboot payload, switch camera, force transmit).
- Recover the craft.

**Exit test:** one recovered flight with (a) at least one image clearly showing
the curvature / dark sky, (b) a logged telecommand that changed behavior in
flight, (c) a post-flight report you would publish.

**Why this stage is mandatory:** it is the only place an individual can iterate
weekly, keep the craft, and rehearse licensing + RF + thermal + recovery before
a one-way orbital shot.

**Cash:** historically DIY recoverable HABs land in the low hundreds to low
thousands depending on how fancy the RF gets. Do not start until Stage 1 is
green and there is budget earmarked without touching runway needed for paid
client work.

### Stage 3 — Orbital picoclass (PocketQube / 1U)

**Build or buy bus:** structure, EPS, radio, optional ADCS, camera. Prefer a
flight-proven bus over a custom structure for a first mission.

**Mission design that fits the physics:**

- Primary: Earth imaging stills + health telemetry.
- Secondary: telecommand of camera/mode during passes.
- Explicit non-goals: continuous piloting, HD livestream, propulsion theater.

**Ops:**

- FCC (or equivalent) satellite authorization and ITU coordination path —
  start paperwork early; it can dominate the calendar.
- Tracking (TLE from Space-Track once catalogued).
- Home station for your passes + SatNOGS as receive backup.
- Debris / disposal plan matching the license.

**Exit test:** first pass that returns an authenticated telemetry frame; first
pass that returns an image; first pass that accepts a command and confirms it.

**Cash:** launch slot alone can be mid five figures for the smallest forms;
full mission (bus + test + license + ops) is usually higher. This is a
**capital decision**, not a hobby purchase. Gate: client revenue covers it, or
it is deliberately funded as a named personal project with a written ceiling.

---

## 5. What "remote controlled from home" should mean in the UI

Design the cockpit around contact reality, not sci-fi.

**Always visible**

- Craft state: power, temperature, mode, last contact
- Next contact window (orbital) or live track (balloon)
- Last image, with capture time and compression stats
- Command queue with ack / timeout / reject

**Commands worth implementing**

- `safe` — immediate safe mode
- `capture` — take N frames
- `downlink` — prioritize image buffer
- `point` — if ADCS exists (nadir / limb / target lat-lon)
- `beacon_rate` — trade power for contact probability

**Commands to refuse**

- Anything that implies continuous thrust without a propulsion subsystem and a
  conjunction process
- Anything unauthenticated
- Anything that can brick the radio without a watchdog recovery path

---

## 6. Regulatory and safety red lines

These are not paperwork trivia. They are part of the vehicle.

1. **Amateur radio license** before any Stage 1 transmit on ham bands.
2. **FAA balloon rules / NOTAMs** for Stage 2 — uncontrolled free balloons have
   mass and packing-density limits; know which side of the line you are on.
3. **No encryption on amateur satellite/ham downlinks** when operating under
   Part 97 — design auth for commands without pretending the downlink is a
   private VPN.
4. **Orbital debris** — if it cannot demise or be disposed per the license,
   it does not fly.
5. **Export / ITAR awareness** if buying certain radios, IMUs, or working with
   non-US partners — check before assuming a shopping cart is fine.
6. **Insurance and liability** for recovery (balloon lands on property) and for
   orbital ops as required by the launch integrator / regulator.

---

## 7. Recommended default configuration (opinionated)

If the goal is to make the dream real rather than to win a novelty contest:

| Layer | Choice | Why |
|---|---|---|
| Stage A vehicle | Recoverable HAB gondola | Iterate, keep the craft, real "space" visuals |
| Compute | Raspberry Pi Zero 2 W or MCU+Pi hybrid | Power vs OpenCV/encode reality |
| Camera | Pi Camera or small global-shutter module | Enough for Earth disk / limb |
| Downlink | UHF SSDV/Wenet-class stills first | Proven amateur path; video later if margin exists |
| Uplink | Narrow telecommand on licensed UHF | Simple, auditable |
| Ground | RTL-SDR receive + licensed handheld/mobile for TX + Yagi | Home-operable |
| Stage B vehicle | 1P–3P PocketQube or 1U via aggregator | Smallest honest orbit |
| Stage B imaging | Still store-and-forward | Matches link budget |
| Non-goal | Live 1080p from orbit on day one | Physics and cash both say no |

---

## 8. The first three concrete actions (no romance)

Do these before naming the craft or designing a logo.

1. **Get (or schedule) the amateur radio license.** Critical path for every
   transmit stage.
2. **Build Stage 0 this month** on hardware already owned. Ship the mission UI
   and the command/ack loop. Put the repo somewhere Onesimus can see it once
   the SSD is mounted, and park stack placement as `unplaced` until
   `/synapse place`.
3. **Write the one-sentence mission** you would put on a license form and on a
   build page: what the craft does, for whom, and what success looks like in
   one flight or one month on orbit.

If step 2 is boring, the later stages will be misery with better scenery.

---

## 9. What this is not

- Not a published `/builds/` page yet. A build page waits for work that exists
  in the world, not a brief.
- Not a commitment to orbital spend.
- Not a Tapo Canyon commercial offering. If this ever appears on kylecovan.com,
  it is personal portfolio under the August 4 scope rule: show the work, never
  sell a service from this site.
- Not advice to buy tools or subscriptions while the standing cash constraint
  holds. Stages that need money wait on an explicit gate.

---

## 10. Open questions only Kyle can close

1. Is the emotional product **live piloting** (favors balloon / loiter) or
   **owning an object on orbit** (favors PocketQube stills + telecommand)?
2. What is the hard cash ceiling for Stage 2 and for Stage 3, separately?
3. Solo build, church/school partnership, or AMSAT-style collaboration?
4. Should the public story live on kylecovan.com as a future build, or stay
   private until first recovered flight?

Until (1) and (2) are answered, Stage 0–1 still proceed. Stage 2+ do not.
