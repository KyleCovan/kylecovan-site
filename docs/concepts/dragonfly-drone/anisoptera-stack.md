# Anisoptera stack — invented subsystems

Named after the dragonfly infraorder. Four inventions, one vehicle. Each subsection states: principle, why historical designs skipped it, mass/power/info budget, and what must be fabricated.

---

## 0. System targets (closed together)

| Quantity | Target | Basis |
|---|---|---|
| AUW | **1.5–2.0 g** (stretch 1.0 g) | Large dragonfly class |
| Wingspan | **8–10 cm** | Visual + aero match |
| Continuous electrical at airframe | **0.30–0.55 W** | Actuators + sensing + modulator |
| Imaging | **64×64 → 128×128** reconstructed @ 3–10 Hz | Pilot awareness, not cinema |
| Control rate | **50–100 Hz** stick equivalents | Attitude |
| Room radius | **2–6 m** indoor v1 | Beam tracking + eye safety |
| Pilot device | **iPhone** | UI + NPU reconstruction + puck command |

---

## 1. Pinna — a new camera (not a tiny webcam)

### Principle

A camera is a **measurement engine**. Conventional modules spend mass on:

- glass / plastic lens groups  
- a million simultaneous integrators (the CMOS array)  
- an ISP that emits fat frames  
- a digital radio that emits fat packets  

**Pinna** inverts that. It takes **M ≪ N** linear measurements of an N-pixel scene using one (or few) photodetectors and a time-varying coded aperture, then reconstructs on the iPhone where mass is free.

Natural images are sparse in wavelet / learned dictionaries. Compressive sensing: for K-sparse signals in N dimensions, on the order of  

\[
M \sim \mathcal{O}(K \log N)
\]

measurements suffice. Example:

| N (pixels) | Assume K | M (order) | Bytes/frame @ 8-bit coeffs | @ 5 Hz |
|---|---|---|---|---|
| 64×64 = 4096 | 300–500 | ~400–800 | ~0.4–0.8 KB | ~16–32 kb/s |
| 128×128 = 16384 | 800–1200 | ~1–2k | ~1–2 KB | ~40–80 kb/s |

That bitrate fits **modulating-retroreflector** and even slow optical channels. It does **not** need Wi‑Fi SoC throughput.

Diffraction still sets the aperture’s angular resolution. Pinna does not claim super-resolution beyond the aperture; it claims **useful images without a gram-scale sensor die and lens barrel**.

### Mechanism (invented assembly)

```
scene light
   → metasurface / microlens film (≤ 20 mg)     # flat “cornea”
   → coded mask on DEA or MEMS (≤ 30 mg)       # time-varying patterns
   → single Si or organic photodiode (≤ 10 mg) # integrator
   → µW TIA + 8–10 bit SAR on a bare die (≤ 20 mg)
   → measurement stream to Return Gleam modulator
```

Optional foveation: bias pattern sequence toward optical flow / motion — insects already do this with few ommatidia and huge behavioral competence.

### Why this is a new camera

It is not “ESP32-CAM but smaller.” It has no frame buffer of N pixels onboard, no JPEG engine, and no Bayer ISP. The **canonical image exists first on the iPhone**, as a reconstructed field. That is a deliberate product definition: *the camera’s brain is the phone.*

### Mass / power

| | Budget |
|---|---|
| Mass | **80–150 mg** |
| Power | **1–5 mW** (photodiode + TIA + mask drive average) |

### Fabrication path

1. Bench Pinna on a stick (phone reconstructs)  
2. Soft-mount on a larger flapper / shaker to prove vibration tolerance  
3. Integrate abdomen “eye bump”  

Learned reconstruction (unrolled ISTA / diffusion priors) runs on the Neural Engine — the phone feature nobody used for insect MAVs yet.

---

## 2. Return Gleam — uplink without a radio transmitter

### Principle

RF transmitters need power amplifiers, crystals, antennas, protocol stacks — grams and milliwatts you do not have. A **modulating retroreflector (MRR)** lets the *ground* own the laser and the pointing. The aircraft only **loads** a shutter in front of a corner-cube or cat’s-eye, drawing little power, while returning a beam the interrogator already sent.

Naval Research Lab and follow-ons demonstrated **Mbps-class** MRR links to UAVs. We need **tens of kb/s** for Pinna — two orders of headroom.

### Mechanism (invented packaging for insect scale)

**Return Gleam** = 3–5 mm cat’s-eye or corner-cube + multiple-quantum-well or LCD/DEA shutter + drive from Pinna’s bit stream.

- Uplink: Pinna coefficients → OOK/PPM on shutter  
- Downlink (control): interrogator amplitude- or polarization-modulates the **same** beam; onboard photodiode taps a fraction for stick commands  
- Acquisition: retroreflection is directionally forgiving compared to aiming an onboard laser *at* the phone

### Why phones fit

The pilot holds the iPhone. A **Lumen Keel** puck (below) carries the laser + coarse tracker. The phone app commands the puck over BLE (arm, track enable, power level, control sticks forwarded). From the human’s point of view: *one phone in hand.* The puck is a tool, like AirPods are a tool — not a second pilot.

### Mass / power

| | Budget |
|---|---|
| Mass | **50–100 mg** |
| Modulator drive | **1–10 mW** average at our bitrate |

### What we refuse to assume

We do not assume a 2 g craft can run ESP32 Wi‑Fi SoftAP. That assumption is historical, not physical. Information can leave the craft as **modulated light it did not have to generate**.

---

## 3. Lumen Keel — energy as a beam, not only a cell

### Principle

Hover at ~0.4 W for minutes needs hundreds of joules. Packaged lithium at **milligram** scales loses energy density to electrodes, pouch, protection. Robofly-class work already showed **laser-to-PV liftoff at 190 mg**. DARPA power-beaming work shows the ground segment is the hard engineered part — not a physics prohibition.

**Lumen Keel** is a palm-sized companion: eye-interlocked IR laser + PV-matching optics + tracker. Onboard: thin PV patch on the wings/abdomen + **100–300 mg** peak-power capacitor / micro-Li cell for brownout and brief beam-out.

### Irradiance honesty (why not “iPhone torch only”)

A phone torch dumps ~0.1–0.3 W optical into a wide cone. At 2 m the spot is large; PV area on a dragonfly is ~1–2 cm². Delivered electrical power after PV efficiency (~20–30% at matched λ) is **milliwatts**, not the **hundreds of milliwatts** actuators need.

So: **phone-alone optical power does not close the hover equation.** A collimated, tracked keel beam does. We invent the keel as part of the product, not a failure of the idea.

Hybrid mission modes:

| Mode | Energy | Flight |
|---|---|---|
| Docked beam | Lumen Keel | Continuous room flight |
| Free glide / dash | onboard micro-store | seconds to ~1–2 min depending on store |
| Perch + sip | beam when in view | dragonfly-like behavior |

### Mass / power onboard

| | Budget |
|---|---|
| PV + wiring | **50–150 mg** |
| Micro-store | **100–300 mg** |
| HV boost for piezo/DEA (if needed) | **50–100 mg** (UW showed ~104 mg electronics class) |

Electrical available under beam: **0.25–0.6 W** depending on laser class and tracking (engineered, eye-safe interlocks mandatory).

---

## 4. Vein Drive — flapping that is the body

### Principle

At dragonfly Reynolds numbers, flapping is not nostalgia — it matches the aero regime and the *look*. Quad props are a different machine wearing a costume.

**Vein Drive:** four wings (or two pairs) with **conductive structural veins** (power + sense), membrane from Mylar / elastomer, actuation by **piezo or dielectric elastomer (DEA)**. The wing is actuator, antenna-adjacent structure, and PV substrate where possible — multifunctional mass, not stacked subsystems.

Control: amplitude / phase offsets between wings for roll/yaw/pitch (DelFly Nimble–class control insight) running on a bare-die MCU or analog+tiny state machine (tens of milligrams), not a flight-controller board designed for 100 g quads.

### Mass

| | Budget |
|---|---|
| Wings + veins + actuators | **400–800 mg** |
| Carbon abdomen / thorax shell | **150–300 mg** |
| Control die + IMU (bare) | **30–80 mg** |

---

## 5. Combined mass closeout (v1 target)

| Subsystem | Mass (mg) |
|---|---|
| Vein Drive (wings + actuators) | 600 |
| Structure | 220 |
| Pinna | 120 |
| Return Gleam | 80 |
| PV + micro-store + boost | 350 |
| Control die + IMU + wiring | 80 |
| Margin | 150 |
| **Total** | **~1600 mg (1.6 g)** |

This closes **on paper** with margin. It fails if any subsystem reverts to hobby packaging (JST connectors, FR4 boards, lens barrels, ceramic Wi‑Fi modules). Packaging discipline *is* the project.

---

## 6. Information closeout

| Channel | Rate needed | Carrier |
|---|---|---|
| Control downlink | ~5–10 kb/s | Modulated interrogator beam (primary) or BLE beacon assist |
| Image uplink | ~20–80 kb/s | Return Gleam MRR |
| Telemetry | ~1 kb/s | Multiplexed on uplink |

All are far below published MRR Mbps demonstrations. The scarce resource is **tracking while flapping**, not raw bandwidth.

---

## 7. iPhone’s real job (vast, underused)

1. Pilot UI (sticks, arm, modes)  
2. Command Lumen Keel over BLE  
3. Show reconstructed Pinna frames (NPU)  
4. Optional: use phone cameras to help track the Gleam return optically (OCC assist)  
5. Log flights, run calibration of Pinna patterns  

The phone is not underpowered for this. Historical designs never **asked** it to be the camera brain and the interrogator director.

---

## 8. What would falsify Anisoptera

Be honest — first principles cuts both ways:

- If Pinna cannot produce pilot-usable images under flapping vibration after serious optics/control work → redesign oculus (multi-diode, shorter exposure), do not jump to a 25 g CMOS quad and call it the same idea  
- If MRR link drops every wingbeat and coding cannot ride through → stabilize abdomen attitude or sync sampling to phase  
- If living-room eye-safe beam power cannot deliver ≥0.25 W electrical onboard → enlarge PV, shorten free-flight expectations, or accept a ceiling-mounted keel  

Those are engineering falsifiers. They are **not** “Wi‑Fi SoCs weigh 2 g therefore dragonflies cannot have cameras.”
