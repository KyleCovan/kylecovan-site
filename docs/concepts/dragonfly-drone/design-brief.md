# Design brief — first principles revision

## The ask (unchanged)

1. Remote-controlled from an iPhone  
2. Has a camera  
3. Looks like a dragonfly **and** is the size of a dragonfly  

## What the first draft got wrong

It treated three **historical assemblies** as if they were **physical necessities**:

| Assumed onboard | What physics actually requires onboard |
|---|---|
| CMOS camera module + lens + ISP | A way to collect scene photons and turn them into *information* |
| Wi‑Fi / BLE SoC transmitter | A way to move that information to the phone |
| Flight battery sized for the whole mission | Energy *available during flight* (stored **or** delivered) |
| Quad frame + 4 ESCs as the only practical airframe | Lift + control authority at insect Reynolds numbers |

DelFly, RoboBee, and ESP-FLY are existence proofs of **pieces**. They are not upper bounds on what a recombined system can do. Copying their bill of materials into a dragonfly silhouette is what makes the problem look closed.

## First principles (non‑negotiable)

These are not “industry best practices.” They are constraints. Everything else is negotiable packaging.

1. **Mass:** large dragonflies are order **10⁻¹–10⁰ g**. Target AUW: **≤ 2.0 g** (stretch **≤ 1.0 g**).
2. **Lift power:** insect-scale hover/forward flight needs order **10⁻¹ W** electrical at the actuators once conversion losses are included (UW laser-powered fly class: electronics drew **>250 mW** just to drive piezo wings at 190 mg vehicle scale). Budget **0.25–0.60 W** continuous at the airframe for a 1–2 g flapper.
3. **Information, not pixels:** a “camera” is an information channel from scene → pilot. Resolution is whatever the channel + prior + compute can reconstruct — not whatever a VGA sensor datasheet prints.
4. **Diffraction is real:** aperture diameter *D* still limits angular resolution (~1.22 λ/D). Computational imaging does not create photons or violate diffraction; it **uses priors** so fewer measurements still yield a useful image.
5. **Energy conservation is real:** 0.4 W for 10 minutes is 240 J. At 1 g AUW you will not carry that in a packaged LiPo without eating the mass budget. Therefore mission energy is either **short** or **beamed** or **hybrid**.
6. **The iPhone is already a supercomputer with radios, an IR illuminator ecosystem, cameras, and an NPU.** Putting equivalent silicon on a 2 g vehicle is the historical mistake.

## The inversion

**Old stack (fails at dragonfly mass):**

```
scene → heavy lens+CMOS → onboard ISP → Wi‑Fi TX → phone display
         battery powers motors + TX + camera
```

**Anisoptera stack (designed to close):**

```
scene → Pinna (ultralight compressive oculus)
          → bits modulate Return Gleam (modulating retroreflector)
          → phone/puck laser interrogates; phone NPU reconstructs frames

phone app → control bits on interrogator beam (or BLE beacon)
          → Vein Drive flapping actuators

Lumen Keel puck → eye-interlocked IR power beam → onboard PV + thin store
```

The aircraft keeps **transduction and actuation**. The ground keeps **joules, joules-per-bit transmit power, and reconstruction.**

## Existence proofs we recombine (not copy)

| Piece | What it already showed | What we do not copy |
|---|---|---|
| DelFly Micro (~3 g, camera) | Free flight + *some* camera near insect size | Their analog TX mass budget as destiny |
| RoboBee / Robofly | Milligram flapping mechanisms | Tether as permanent destiny |
| UW laser-powered fly (190 mg) | **Wireless optical power** can lift insect-scale robots | Enclosure-only forever — we productize the interrogator as a puck |
| NRL / Oxford MRRs | **Mbps optical uplink with almost no onboard TX power** via modulating retroreflector | Large UAV packaging |
| Single-pixel / compressive cameras | Images from one detector + known patterns + sparse priors | Lab optical-table bulk |
| iPhone Neural Engine | On-device learned reconstruction at video-class rates | Using it only for Portrait mode |

The invention is the **joint system**, especially the camera (**Pinna**) and the phone-centric optical duplex (**Return Gleam** + **Lumen Keel**). Details and budgets: [`anisoptera-stack.md`](anisoptera-stack.md).

## Why this meets all three requirements

| Requirement | How Anisoptera satisfies it |
|---|---|
| Dragonfly size & look | Four-wing flapping airframe at 5–10 cm span, ≤2 g, vein aesthetics are structural (conductors + spars), not decals on a quad |
| Camera | Pinna is a real imaging instrument (scene photons → measurements → reconstructed view). It is a **new camera architecture**, not a missing camera |
| iPhone control | Pilot UI, reconstruction, and link supervision run on iPhone; optical companion puck is slaved to the phone (BLE). The phone remains the control surface you hold |

## What we are still inventing (honest R&D, not magic)

Physics allows the budgets below. Engineering must still integrate them:

1. **Pinna** as a ≤150 mg compressive oculus with stable calibration in flight vibration  
2. **Return Gleam** MRR at ~50–100 mg that holds link while the body pitches at flapping frequency  
3. **Lumen Keel** auto-track power beam safe enough to use indoors at home  

4. **Vein Drive** efficiency good enough that 0.3–0.5 W electrical yields controlled flight at 1–2 g  

None of those require new particles or violated thermodynamics. They require **focused invention** on packaging, tracking, and control — which is exactly what “make this doable” means.

## Non-goals (so the design stays sharp)

- Not a highway-range surveillance platform  
- Not App Store consumer toy on day one  
- Not “iPhone flashlight alone powers hover at 5 m” (irradiance math fails; see power section in the stack doc)  
- Not claiming DelFly’s analog camera was “wrong” — only that **digital phone-native imaging at gram scale needs a different camera**

## Recommended stance

Treat Anisoptera as the **definition of done** for this idea. Use phased proofs that each remove one historical assumption (see `bom-phase-1.md`), not a detour into a 25 g quad that quietly abandons the ask.
