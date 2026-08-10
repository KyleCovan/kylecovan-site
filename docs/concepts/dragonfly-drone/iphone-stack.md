# iPhone control + video stack

Goal: fly from an iPhone without a separate RC transmitter. Video on the same phone is a stretch goal with real mass cost.

## Recommended architecture (Phase 1–2)

```
┌─────────────────────┐         Wi‑Fi SoftAP          ┌──────────────────────┐
│  iPhone             │◄─────────────────────────────►│  Drone (ESP32-S3)     │
│  SwiftUI app        │   UDP/TCP: sticks, arm,       │  flight controller    │
│  - virtual sticks   │   telemetry                   │  IMU + motor drivers  │
│  - arm / mode       │                               │                      │
│  - battery / RSSI   │   optional MJPEG / custom     │  camera module (opt.) │
│  - video pane       │◄──────────────────────────────│                      │
└─────────────────────┘                               └──────────────────────┘
```

**Why Wi‑Fi SoftAP first:** matches existing ESP-Drone / ESP-FLY patterns, needs no extra radio, and the phone already knows how to join an SSID. BLE is a fine secondary channel; it is a poor sole carrier for video.

## Control plane

### Messages (minimum viable)

| Direction | Payload | Rate |
|---|---|---|
| Phone → drone | throttle, yaw, pitch, roll (normalized −1…1) | 50–100 Hz |
| Phone → drone | arm, disarm, flight mode, emergency stop | event |
| Drone → phone | armed, batt V, RSSI, orientation (optional) | 10–20 Hz |

Keep the protocol boring: length-prefixed binary or CBOR over UDP. JSON-over-TCP is fine for bring-up and too heavy for sticks long-term.

### Safety

- **Failsafe:** if no stick packet for >200–300 ms → disarm or controlled descend (pick one and test over carpet).
- **Arm gesture:** two-step arm (switch + confirm) so a pocket tap cannot spin props.
- **Geo / altitude:** skip GPS at this mass; indoor only until Phase 3+.
- **Prop guards:** for any demo near people or dogs.

### Existing software to fork / study

- ESP-Drone / Crazyflie-inspired ESP-IDF firmwares used by ESP-FLY and LiteWing
- Seeed Co-Create ESP-FLY repo (kit firmware + docs)
- ESP-NOW path as a *future* low-latency option with a companion stick — not Phase 1

Stock phone apps in this ecosystem lean Android. **Plan on a custom iOS client** rather than waiting for parity.

## Video plane — three honest paths

### Path A — Analog FPV (lightest air side)

- On aircraft: 5.8 GHz AIO cam/VTX (~2–4 g)
- On ground: FPV goggles **or** USB-C / Lightning RX dongle into the phone
- Pros: best grams, mature hobby parts
- Cons: “iPhone only” is false unless you add hardware; legality of VTX power / band matters by country

### Path B — Wi‑Fi MJPEG / JPEG push (true phone preview)

- ESP32-S3 + camera (XIAO Sense or similar) streams frames to the app
- Pros: one device in your hand
- Cons: heat, mass, latency (often 100–300+ ms), bandwidth fights control packets — QoS carefully or use two sockets with control prioritized

### Path C — Split brains

- Tiny FC for flight (or same chip dual-core with care)
- Separate video module
- Only if debugging proves one chip cannot do both

**Phase 1 recommendation:** fly with **no camera** or **Path A**, prove sticks. Add Path B only after hover is boring.

## iOS app sketch

### Stack

- SwiftUI + Network.framework (UDP) or NWConnection
- Multipeer is the wrong tool; join the drone SoftAP (user toggles Wi‑Fi, or use NEHotspotConfiguration with caveats)
- Local-only; no cloud telemetry required

### Screens (v1)

1. **Connect** — SSID hint, connection state, battery once linked
2. **Fly** — left stick throttle/yaw, right stick pitch/roll (or mode 2 layout toggle), arm, panic
3. **Video** — placeholder until Path B/A lands; never block control UI on frame decode

### Distribution

| Path | When |
|---|---|
| Xcode → personal device | Day one |
| TestFlight internal | When builds need to leave the Mac |
| App Store | Only if others will fly it; expect review questions for drone control apps |

Apple Developer Program is a paid account — check the standing “no new paid tools until a client is paying” constraint before assuming App Store. Personal-device deploy may already be covered if a membership exists.

## Latency budget (feel)

| Loop | Target |
|---|---|
| Stick → motor response | < 40 ms preferred, < 80 ms usable indoor |
| OSD / telemetry | < 100 ms |
| Video (if any) | < 150 ms “pilotable”; > 300 ms is sightseeing |

If video lags, **keep piloting on telemetry + line of sight**, not on the stream.

## Security (even for a toy)

- Change default SoftAP password
- Do not bridge the drone AP to your home LAN
- Assume anyone nearby could join an open ESP AP and send sticks — open AP is fine only in empty fields with prop guards and short flights

## Phase 1 bring-up order

1. Stock firmware + whatever Android reference app exists (borrow a device if needed) — prove airframe
2. Document the Wi‑Fi protocol (packet captures)
3. Minimal iOS stick app → same packets
4. Failsafe test (walk out of range on purpose, props removed first)
5. Then camera
