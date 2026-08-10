# Dragonfly drone — design brief

## What was asked

A drone that:

1. Is remote-controlled from an iPhone
2. Has a camera
3. Looks like a dragonfly **and** is the size of a dragonfly

Those three constraints do not pull in the same direction. The brief below separates what physics allows from what a home workshop can ship, then recommends a path that gets something flying from the phone before chasing insect authenticity.

## What “dragonfly size” actually means

| Reference | Wingspan | Mass | Camera | Phone control |
|---|---|---|---|---|
| Real dragonfly (typical large spp.) | ~5–10 cm | ~0.2–1 g | n/a | n/a |
| Harvard RoboBee | ~3 cm | ~0.08–0.26 g | no useful camera | tethered / lab power |
| DelFly Micro (TU Delft) | 10 cm | ~3 g | yes (tiny analog, ~0.4 g tx) | custom RC, ~50 m, ~3 min |
| DelFly Nimble | 33 cm | ~29 g | optional ~4 g payload | research platform |
| ESP-FLY DIY micro quad | ~5–7 cm frame | ~25–28 g w/ LiPo + FPV | optional analog FPV | Wi‑Fi phone app |
| X‑Fly / Bionic Bird class | bird-scale, not insect | tens of grams | usually none / weak | smartphone BLE/app |

**Takeaway:** the only free-flying camera ornithopter near true insect size is DelFly Micro — a university MAV with a gram-scale mass budget and minutes of flight. RoboBee is smaller still, but not a practical camera + iPhone product. Consumer “bionic bird” toys are closer to small birds than dragonflies.

So “looks like and is the size of a dragonfly” is either:

- **Literal:** research-grade flapping MAV (years, specialized tools, analog or ultra-micro video), or
- **Honest compromise:** insect *silhouette* and *scale class* (hand-sized or smaller), quadrotor propulsion under a dragonfly shell, digital or analog camera, iPhone UI.

This brief assumes the second unless Kyle explicitly chooses the research path.

## The three requirements, scored

### 1. Dragonfly size + appearance

Flapping four wings at insect Reynolds numbers needs:

- Extreme mass discipline (battery often eats 30%+ of takeoff weight)
- Carbon / Mylar / micro-linkage fabrication, not hobby PLA frames
- High flapping frequency (DelFly Micro ~30 Hz) and precise kinematics
- Almost no spare grams for Wi‑Fi SoCs, digital cameras, or App Store stacks

A quadrotor can wear a dragonfly shell. The props will still look like props up close, and the mass will be closer to 15–40 g than to 1 g unless custom everything.

### 2. Camera

| Class | Typical mass | What you get |
|---|---|---|
| Analog AIO FPV (5.8 GHz) | ~1.5–4 g | Live view on FPV goggles / ground receiver; phone needs a separate RX dongle or second radio path |
| ESP32-CAM / XIAO Sense JPEG over Wi‑Fi | ~5–15 g module class | Phone-native preview; higher latency; power hungry |
| DelFly-class analog micro camera + TX | ~0.4 g | Exists in labs; not a Digi-Key cart item with docs |

**Conflict:** digital Wi‑Fi video that an iPhone can show natively wants more mass and power than a true insect airframe has. Analog FPV is lighter but breaks the “just my iPhone” story unless the phone is paired with a receiver accessory.

### 3. iPhone remote control

iPhones speak BLE and Wi‑Fi well. They do **not** speak ExpressLRS / Crossfire / classic RC without hardware.

Practical phone stacks:

| Link | Latency | Range | Video on same link? | Notes |
|---|---|---|---|---|
| Wi‑Fi SoftAP (ESP-Drone style) | OK indoors | ~30–50 m typical | Yes (MJPEG / custom) | Simplest “phone only” path |
| BLE | Fine for sticks | Short | Poor for video | Good for telemetry / arming; weak for FPV |
| ESP-NOW | Low | Longer | No | Needs a companion TX; not native iPhone |
| Analog 5.8 GHz video + Wi‑Fi control | Split | Video depends on RX | Phone needs RX hardware | Best image per gram |

**iOS reality:** App Store distribution for a drone controller is extra work (TestFlight is enough for personal use). Background Wi‑Fi to an ESP SoftAP works; low-latency custom video on iOS is the hard software piece, not the joystick UI.

## Architecture options

### Option A — True flapping dragonfly (literal ask)

- **Pros:** Matches the dream.
- **Cons:** Fabrication, aero, and power are graduate-lab problems. iPhone + useful camera on a ~3 g vehicle is not a known hobby recipe.
- **AI leverage:** literature synthesis, control-theory helpers, CAD of linkages — **not** a substitute for a micro-robotics bench.
- **Verdict:** park unless this becomes a multi-year research build with partners/tools.

### Option B — Micro quadrotor + dragonfly shell (recommended product path)

- **Pros:** Phone control and camera already exist on kits (~25 g). Shell + paint + slender body can read “dragonfly” at a glance. Iterate airframe after the link works.
- **Cons:** Not true insect flight. Props visible. Still small-battery (~5 min) and indoor-first.
- **AI leverage:** high — CAD shell, firmware forks, SwiftUI app, CV experiments later.
- **Verdict:** best “heavy lifting → something that flies from the phone.”

### Option C — Buy a bionic bird (X‑Fly class) and learn

- **Pros:** Fastest way to feel flapping + phone control.
- **Cons:** Bird, not dragonfly. Camera usually absent or weak. Less transferable to insect scale.
- **Verdict:** optional learning detour, not the target vehicle.

### Option D — Hybrid research (DelFly-inspired)

- Build or acquire a larger flapping trainer (20–30 cm class), then shrink.
- Only after Option B proves the phone/camera UX you actually want.

## Recommended path

**Phase 0 — Lock the product definition (no spend)**

Answer in writing (see `decision-gates.md`):

- Indoor only, or outdoor in wind?
- “Looks like” from 2 m away, or entomology-accurate?
- Live video on the same iPhone, or control on phone + FPV goggles?
- Target flight time (2 min vs 8 min changes everything)?
- Budget ceiling (standing constraint: no new paid subscriptions; hardware kit spend is a separate call)?

**Phase 1 — Soft platform: phone-controlled micro quad**

- Hardware: ESP-FLY (XIAO ESP32-S3) or equivalent open micro quad (~$60 kit class).
- Goal: arm, fly, land from iPhone; optional analog FPV first.
- Deliverable: notes on latency, range, crash rate, battery life.
- **Kill / continue gate:** if phone control is miserable, fix the link before any biomimicry.

**Phase 2 — Dragonfly identity layer**

- CAD a slender abdomen + four wing *shapes* (decorative or semi-functional covers) around a 40–65 mm quad.
- Prefer clear / veined wing films that don’t block prop inflow; or push props into a “body” layout with careful ducting (harder).
- Recolor: warm earth / iridescent blues-greens — avoid toy-plastic look.
- Goal: photographs and short clips that read “dragonfly drone” without lying about propulsion.

**Phase 3 — Shrink + integrate camera for phone preview**

- Custom PCB / lighter motors / smaller LiPo if Phase 2 works.
- Prefer one SoC for FC + Wi‑Fi video if mass allows; else keep analog FPV and document the phone accessory honestly.
- Only here consider custom molded body.

**Phase 4 — Flapping research (optional, expensive)**

- Open only if Phases 1–3 still leave the flapping requirement non-negotiable.
- Study DelFly papers, linkage designs, and whether a *hover-capable* four-wing is required vs forward-flight ornithopter.

## What AI can carry vs what needs hands

| Workstream | AI / remote agent | Needs Kyle / shop |
|---|---|---|
| Feasibility, BOM, firmware research | High | Review + buy |
| iOS controller app (TestFlight) | High | Apple Developer account, device test |
| Flight-controller firmware fork | Medium–high | Bench flash, IMU tune, crashes |
| Dragonfly shell CAD → print | High | Printer / resin / finishing |
| True flapping mechanism | Low–medium | Micro fabrication, iteration |
| Outdoor reliability / wind | Low | Flight testing |

**Default Shift answer:** AI can own the software stack, CAD, and documentation end-to-end. AI cannot own first flight, crash repair, or insect-scale flapping without a physical lab. Start where AI leverage is highest (Phase 1 software + Phase 2 shell).

## Risks worth naming early

1. **Mass creep.** Every “nice” feature (GPS, digital HD, obstacle avoid) destroys insect scale.
2. **Regulatory.** Even tiny drones are aircraft. Recreational rules, airspace, and privacy still apply; don’t film people without thinking.
3. **Expectation drift.** “Dragonfly” in a pitch deck often means *cute micro drone*. Literal size is a different project.
4. **Cost vs priorities.** This is a new limb. It should be placed in the priority stack before kit money moves — Onesimus was not mounted in the environment that wrote this brief.
5. **Site scope.** If this becomes public on kylecovan.com, it is a **build** (show the work), never a service offering.

## Suggested decision

1. Treat **Option B + Phases 0–2** as the real project.
2. Keep literal flapping as a labeled stretch goal, not the definition of success.
3. Do not open a live `/builds/` page until there is hardware in hand and Kyle writes the one-liner.
4. Next concrete action if greenlit: buy Phase 1 kit (see `bom-phase-1.md`) and scaffold an iOS TestFlight controller against the kit’s Wi‑Fi protocol.
