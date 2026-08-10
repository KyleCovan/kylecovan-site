# Remote control — pigeon ornithopter

## The job

Move your intent (throttle, attitude, arm, kill) to the pigeon **fast, far, and reliably**, and get enough feedback (telemetry, camera) to keep flying outside.

## Break the job into channels

| Channel | Bits needed | Failure cost | Best medium outdoors |
|---|---|---|---|
| Control (sticks) | Very low | Craft falls / flyaway | Dedicated RC radio (e.g. ExpressLRS) |
| Telemetry | Low | You fly blind on battery/RSSI | Same RC link (return telemetry) |
| Camera | High | You lose FPV; may still LOS-fly | Separate video RF |
| Compute / UI | — | Annoyance | Phone or goggles display |

Phones try to mash these together on Wi‑Fi. That is convenient at a desk and weak in a field.

## Why “iPhone as the remote” fails outdoors

1. **Link budget:** phone Wi‑Fi / BLE are short-range, indoor-biased.  
2. **Antenna:** phone in hand/pocket is a bad TX for a sky target.  
3. **Failsafe:** RC protocols assume “no packets → known safe behavior.”  
4. **Sticks:** glass has no spring-return; sun washes the screen.  
5. **Drop risk:** fumble the phone, control path dies.

## Recommended setup

**Primary:** ExpressLRS-class handset (Radiomaster Pocket or similar).  
**Secondary:** iPhone for camera view (via ground receiver), map, logs.  
**Alternate:** handset + FPV goggles; phone only for setup.

## On the pigeon

- ELRS receiver  
- Flight controller with proper failsafe  
- Video transmitter sized for the range goal  

## Indoor / bench exception

Phone SoftAP sticks are fine for desk bring-up only — not the field architecture.
