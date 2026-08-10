# iPhone role — pilot, director, camera brain

The iPhone is not an afterthought controller for a Wi‑Fi quad. In Anisoptera it is **three instruments in one.**

## 1. Pilot

SwiftUI (or equivalent) app:

- Mode 2 virtual sticks → forwarded to **Lumen Keel** over BLE at 50–100 Hz  
- Keel encodes stick packets onto the **interrogator beam** (amplitude/Polarization/PPM)  
- Emergency stop kills laser power *and* commands disarm (failsafe: beam loss → controlled fold / glide / soft drop — choose and test)

Arming: two-step on phone + keel interlock (tilt switch / lid / presence).

## 2. Director of the optical companion

**Lumen Keel** (palm puck) owns Class-appropriate IR laser, TX optics, coarse/fine tracking, and MRR receiver photodiode.

Phone responsibilities:

- Pairing, status, battery of puck  
- Enable track / set max power / geo of “flight cone”  
- Display link quality (return strength, bit error proxy)  
- User-visible eye-safety state  

Human workflow: place puck on table facing the room, open app, fly. **Still “from my iPhone.”** The puck is infrastructure, not a second brain you pilot.

### Why a puck is not cheating

First principles energy section: phone torch irradiance cannot close hover power at room scale. Denying the puck to preserve a slogan would strand the vehicle. Accepting the puck preserves the *control* requirement and the *physics*.

## 3. Camera brain (Pinna reconstruction)

Pinna does not send images. It sends **measurement vectors**.

Phone pipeline:

1. Demodulate Return Gleam bitstream (via keel USB/BLE/Wi‑Fi local link — keel has the photoreceiver)  
2. Reconstruct frames with a learned algorithm on the **Neural Engine** (unrolled iterative shrinkage, tiny transformer, or diffusion prior — pick by latency)  
3. Show video pane; never block control loop on a late frame  

Target: 3–10 Hz reconstructed view @ 64–128 px class for piloting; burst higher-res stills when hovering in beam.

### Optional assist

Phone rear cameras watch the craft’s IR return / beacon to help the keel’s tracker (sensor fusion). That uses a capability every iPhone already has.

## What we do *not* build on iOS in v1

- App Store public distribution (TestFlight / personal device first)  
- On-phone laser (unsafe / insufficient)  
- Pretending SoftAP ESP-Drone protocol is the end architecture  

## Latency budget

| Path | Target |
|---|---|
| Stick → keel → beam → actuator | < 40 ms |
| Pinna measurement → reconstruct → display | < 150 ms typical; pilot may LOS-fly if late |
| Beam loss → safe response | < 100 ms |

## Security / safety

- Beam hard-limited; covers; tilt kill  
- Encrypted BLE to puck; open optical encoding is line-of-sight limited by design  
- No cloud requirement for flight
