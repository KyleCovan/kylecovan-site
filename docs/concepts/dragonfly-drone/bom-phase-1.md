# BOM — Phase 1 (soft platform)

**Purpose:** get a micro quad in the air controlled from a phone, with an optional camera path, **before** any dragonfly cosmetics.

**Spend posture:** prefer one kit over scatter-ordering parts. Confirm Apple Developer / tool spend against the standing no-new-subscriptions constraint before paying for distribution channels.

Prices move; treat dollar figures as 2026-order-of-magnitude.

## Kit path (preferred)

| Item | Qty | Approx | Notes |
|---|---|---|---|
| Seeed ESP-FLY DIY kit (XIAO ESP32-S3) | 1 | ~$60 | Frame, FC, motors, props — Co-Create with Max Imagination |
| Spare 1S LiPo 250 mAh (+ one spare) | 2 | ~$15–25 | Swappable packs beat waiting on charge |
| Prop set spares (CW/CCW) | 2–4 sets | ~$10 | You will break these |
| Micro USB-C cable | 1 | owned? | Flash + charge depending on board |
| **Optional:** 5.8 GHz AIO FPV cam compatible with frame | 1 | ~$20–40 | Path A video |
| **Optional:** cheap FPV monitor or used goggles | 1 | varies | Only if Path A |

**Tools you need if not already owned**

| Tool | Why |
|---|---|
| 0.01 g scale | Weight budget discipline |
| Soldering iron + fine solder | Repairs, camera leads |
| Lipo bag + 1S charger with storage charge | Don’t charge unattended on wood |
| Prop remover / tweezers | Fingers vs 70k RPM is a bad bet |

## DIY scatter path (only if kit unavailable)

Rough equivalent to ESP-FLY:

- Seeed XIAO ESP32-S3
- MPU-6050 breakout (or integrated FC PCB)
- 4× SI2300 (or kit MOSFET board)
- 4× 615 coreless motors + 30–31 mm props
- 50 mm-class printed frame (PETG or lightweight PLA)
- 1S 250 mAh JST-PH

Expect more debug time; the kit’s value is a known frame + wiring.

## Phase 2 add-ons (do not buy yet)

| Item | Why wait |
|---|---|
| Dragonfly shell materials (Mylar, carbon rod, transparent film) | Airframe must fly first |
| Resin printer time / service | CAD after crash geometry is known |
| Custom PCB | Premature until FC firmware is yours |
| XIAO ESP32-S3 Sense / camera | After stick latency is acceptable |

## Phase 4 / research (do not buy)

Piezo actuators, custom flexures, DelFly-style linkages — only after an explicit decision to open the flapping track.

## Software checklist (no cart)

- [ ] ESP-IDF or PlatformIO toolchain on the build machine
- [ ] Clone ESP-FLY / ESP-Drone firmware, flash, confirm motors (props off)
- [ ] Packet-capture the phone control protocol
- [ ] Scaffold SwiftUI stick app (personal device)
- [ ] Written failsafe behavior

## Acceptance for Phase 1 complete

1. Hover 30 seconds indoors over soft surface, phone-only sticks
2. Controlled landing (not a cut-throttle drop)
3. Documented AUW on the scale
4. Crash once, repair once, fly again (proves maintainability)
5. Decision recorded: Path A, Path B, or no camera for Phase 2
