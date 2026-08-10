# Remote control — first principles

## The job

Move your intent (throttle, attitude, arm, kill) to the aircraft **fast, far, and reliably**, and get enough feedback (attitude feel, telemetry, camera) to keep flying outside.

## Break the job into channels

| Channel | Bits needed | Failure cost | Best medium outdoors |
|---|---|---|---|
| Control (sticks) | Very low | Craft falls / flyaway | Dedicated RC radio (e.g. ExpressLRS) |
| Telemetry | Low | You fly blind on battery/RSSI | Same RC link (return telemetry) |
| Camera | High | You lose FPV; may still LOS-fly | Separate video RF (or compressive data RF) |
| Compute / UI | — | Annoyance | Phone or goggles display |

Phones try to mash these together on Wi‑Fi. That is convenient at a desk and weak in a field.

## Why “iPhone as the remote” fails outdoors (physics + humans)

1. **Link budget:** phone Wi‑Fi / BLE are short-range, indoor-biased, busy-band protocols.  
2. **Antenna:** phone antenna in your hand/pocket is a bad TX for a sky target.  
3. **Failsafe culture:** RC protocols assume “no packets → known safe behavior.” Phone apps flake differently.  
4. **Sticks:** glass has no spring-return proprioception; sun washes the screen.  
5. **Single-point failure:** fumble the phone, control path dies.

None of that is “Apple vs Android.” It is the wrong tool as **primary** outdoor RC.

## Why a real handset wins

- Mechanical gimbals → consistent inputs without looking  
- RF module designed for range (power, antenna, LoRa-style PHY in ELRS, etc.)  
- Switches for arm/mode/kill you can find by touch  
- Hours of battery as a *transmitter*  
- Mature failsafe behavior  

iPhone then mounts as **viewer** (clamp) or stays in the pocket while you use goggles.

## Recommended setup for this project

**Primary:** ExpressLRS-class handset (Radiomaster Pocket or similar).  
**Secondary:** iPhone app for camera view (via ground receiver), map, logs, Pinna reconstruction.  
**Alternate:** handset + FPV goggles; phone only for setup.

## Aircraft side

- ELRS receiver (light)  
- Flight controller with proper failsafe  
- Video or Pinna data transmitter sized for the range goal  
- Do not carry a phone-grade Wi‑Fi AP to “save” buying a $60–100 radio  

## Indoor exception

Phone-only SoftAP is still fine for **desk tests** and learning UI. It is not the field architecture.
