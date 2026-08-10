# Field revision — outdoor, distance, and the real remote

**Ask (updated):** dragonfly-sized flyer with a camera, usable **outside at a real distance**, remote-controlled in a way that is actually practical — iPhone only if it earns that job.

**Method:** first principles. Old indoor optical stack stays as an optional *bench* path. It is not the field architecture.

---

## Plain English first

**Yes, still doable — but the outdoor version is a different machine than the indoor desk demo.**

Outside, at distance:

- You cannot count on a table laser to feed the bug power. The flyer needs its **own battery**.
- A phone’s Wi‑Fi / Bluetooth is a weak, short, finicky control link for something in the sky. **Sticks on a real radio** are the practical primary control.
- Your iPhone can still be useful — as a **viewer / map / brain** — but it should not be the only thing keeping the craft from falling.

Also honest: a **true 1–2 gram** dragonfly in normal outdoor wind is fighting physics. Gusts shove harder than the vehicle weighs. For outdoor distance, we size for a **dragonfly look at a mass that can fight a breeze** (think large-dragonfly to small-hand-bird class), not a costume on a toy that only works in still air.

---

## First principles that bind outdoors

### 1. Energy has to ride along

Hover/cruise still costs power \(P\). Flight time \(t\) needs energy \(E \approx P \cdot t\) **on the aircraft** once you leave a beamed room.

Beamed light fails outdoors at distance because:

- sunlight swamps / heats the receiver  
- eye-safe lasers don’t deliver enough watts at long range into a tiny PV  
- keeping a beam on a moving insect at hundreds of meters is a tracking weapon problem, not a hobby problem  

So: **battery (or fuel cell) onboard.** That raises mass. That is not a historical superstition; it is joules.

### 2. Wind is a force, not a vibe

Dynamic pressure \(\tfrac{1}{2}\rho v^{2}\). A modest breeze on a few square centimeters of wing/body is comparable to the weight of a 1–2 g craft. Real dragonflies manage with superb sensing and continuous correction; a first robot will not.

**Field target mass class:** about **15–40 g** AUW for a dragonfly-*shaped* outdoor flyer you can actually take outside on a normal day.  
**True 1–2 g** remains a calm-air / research / indoor stretch — not the definition of “works outside at distance.”

We are not abandoning the look. We are refusing to lie about wind.

### 3. Control bits are cheap; a good radio link is not optional

Stick data is tiny (kilobits per second). What you need at distance is **link budget**:

- transmit power  
- antenna gain / orientation  
- frequency and modulation that punch through noise  
- a protocol with failsafe when packets stop  

A phone SoftAP was built for web pages ten feet away. ExpressLRS-class radio was built for “craft still answers a kilometer away.” That difference is RF engineering, not brand loyalty.

### 4. Video is a second channel

Camera data wants far more bits than sticks. Outdoors, **optical retro-reflector links** (the indoor “Return Gleam” idea) lose to alignment, sun, and range.

So field video/data rides **RF** (lightweight digital, analog FPV, or Pinna’s compressive numbers over a small radio). Phone or goggles **display**; they do not have to **originate** the control RF.

### 5. Human factors are physics too

Touch-screen sticks in sun glare, no tactile center spring, phone drop = loss of control, eyes on glass instead of sky — these fail in the field even when the radio somehow works. A proper controller has **mechanical gimbals** because pilots need proprioception.

---

## What the iPhone is good at (and what it isn’t)

| Job | iPhone? | Why |
|---|---|---|
| Primary flight controls outdoors | **No** | Weak long-range RF role, bad sticks, glare, drop risk |
| Live map / telemetry / battery / RSSI | **Yes** | Great screen, GPS in your hand for *you*, apps |
| Watching the camera feed | **Yes, if fed** | Needs a receiver path into the phone (Wi‑Fi from a ground box, or USB/Lightning RX, or controller with phone clamp) |
| Reconstructing Pinna compressive video | **Yes** | NPU / CPU belong on the ground |
| Mission setup, logging, share clip | **Yes** | |

**Rule:** iPhone = **mission computer + viewer**.  
**Not:** the only radio holding the aircraft up.

---

## The remote control (practical answer)

### Recommended field kit: split control and view

```text
┌──────────────────────────┐
│  RADIO HANDSET             │  physical sticks, switches, failsafe
│  (e.g. ExpressLRS class)   │  kilometers-class link budget
└────────────┬─────────────┘
             │  control RF (low rate, high reliability)
             v
        DRAGONFLY CRAFT
             │  video / compressive data RF (separate or shared carefully)
             v
┌──────────────────────────┐
│  GROUND VIDEO PATH         │  diversity RX / decoder box / goggles
└────────────┬─────────────┘
             │  Wi‑Fi or cable
             v
┌──────────────────────────┐
│  iPHONE (optional clamp)   │  watch feed, map, telemetry, reconstruct Pinna
└──────────────────────────┘
```

**Why this wins on first principles**

1. Control channel optimized for range and failsafe.  
2. Video channel optimized for bandwidth.  
3. Human gets real sticks.  
4. Phone still in the loop where it’s strong.

### Controller options ranked for *this* project

| Option | Outdoor distance | Stick feel | Practicality | Verdict |
|---|---|---|---|---|
| iPhone-only Wi‑Fi/BLE | Poor | Poor | Easy indoors, fragile outside | Reject as primary |
| Gamepad ble’d to phone | Poor–fair | Mediocre | Gimmick | Reject |
| **ELRS handset (Pocket-class) + phone as viewer** | Strong | Strong | Buyable now, light learning curve | **Default** |
| Integrated smart controller (sticks + big screen, DJI-style) | Strong | Strong | Costlier; nicest single object | Later polish |
| FPV goggles + handset; phone in pocket | Strong | Strong | Best for immersion; phone secondary | Excellent alternate |

Day-one field remote: **Radiomaster Pocket–class ExpressLRS transmitter** (or equivalent). Put the iPhone on a clamp mount for video/telemetry when you want it — or use goggles and leave the phone for planning.

### On the aircraft (control radio)

A modern ELRS receiver can be **under a gram to a few grams**. That mass is worth it. Do not invent a worse radio to keep an “iPhone-only” slogan.

---

## Field airframe (Anisoptera Field)

Still dragonfly-shaped. Still camera. Still first principles — different mass closeout.

| Piece | Role outdoors |
|---|---|
| **Vein Drive** (flapping) *or* hybrid flap + tiny props hidden in silhouette | Lift in breeze; flapping preferred for look, hybrid allowed if thrust margin demands it |
| **Onboard battery** | Mission energy (minutes, not laser sip) |
| **ELRS RX + bare FC** | Control |
| **Pinna or light FPV cam** | See; Pinna still helps if we need lower bitrate over longer RF |
| **Small video/data TX** | Get pixels or Pinna numbers home |
| **iPhone on ground** | View / reconstruct / map — not the uplink radio |

### Example outdoor mass sketch (order of magnitude)

| Subsystem | Mass |
|---|---|
| Structure + dragonfly shell/wings | 8–15 g |
| Actuation (flap and/or micro props) | 5–12 g |
| Battery | 6–12 g |
| FC + ELRS RX + wiring | 2–4 g |
| Camera + VTX / data TX | 3–8 g |
| **AUW** | **~25–45 g** |

Looks like a dragonfly (or a large one). Flies outside. Not a fruit-fly robot. That is the honest outdoor ask.

True **≤2 g** outdoor distance remains a research moonshot (wind + joules). We keep it labeled stretch, not the success definition.

---

## What happens to the indoor inventions?

| Indoor idea | Field fate |
|---|---|
| Pinna compressive camera | **Keep** — lower bitrate helps long RF links |
| Return Gleam (optical MRR) | Bench / short-range only; **not** field primary |
| Lumen Keel power beam | Lab endurance / indoor demo only |
| iPhone as sole stick radio | **Demoted** — viewer + computer |
| Vein Drive look | **Keep** as identity |

Phase A (desk Pinna → picture on phone) **still worth doing**. It proves the camera brain split. It does not prove outdoor range.

---

## Distance — say numbers

Without promising brochure fiction:

| Link | Realistic design goal (line of sight, open area) |
|---|---|
| Control (ELRS-class) | **1–5+ km** possible in good setups; design for **solid 500 m–2 km** first |
| Analog/digital video | Often shorter than control; plan video usable to **hundreds of meters**, improve later |
| “Across the yard / park” | Should feel boringly reliable before chasing kilometers |

Legal note (not optional): outdoors you are flying an aircraft. Follow local rules (LOS, altitude, registration, where you may fly). First principles include not getting grounded by law.

---

## Success definition (updated)

You win when:

1. Craft **looks like a dragonfly** in photos/video.  
2. You fly it **outside** on a normal mild day (not only dead-calm indoors).  
3. Control is from a **real handset**, failsafe works when the link dies.  
4. You get a **camera view** on goggles or iPhone at a useful distance (start: across a park).  
5. Mass is whatever the wind/energy math required — optimized downward over time, not fantasized first.

---

## Next concrete steps

1. Lock this field definition (this file).  
2. Keep Phase A as camera proof.  
3. Buy/borrow an **ELRS handset** early and learn sticks on any trainer sim / tiny whoop — skill transfer matters more than iPhone UI.  
4. Design Field airframe around battery + ELRS + camera TX, dragonfly silhouette.  
5. Only then chase gram-shaving and Pinna bitrate tricks for longer video range.
