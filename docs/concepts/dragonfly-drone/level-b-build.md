# Level B build sequence — rock pigeon

Locked target: [`LOCKED.md`](LOCKED.md). Fly the mechanism before dressing it.

---

## Targets (numbers to design against)

| Spec | Target | Notes |
|---|---|---|
| Species reference | Rock pigeon (*Columba livia*) | Photos + morphometrics, not memory |
| AUW | 350–500 g | Stay in bird ballpark |
| Wingspan | 60–70 cm | Match planform, not gull-scale 2 m |
| Flap rate | ~5–8 Hz cruise | Measure on bench |
| Flight mode | Forward flight, climb, glide, landing | Not quad hover |
| Control | ELRS-class handset | Failsafe mandatory |
| Video | Head cam → goggles and/or phone via ground RX | |
| Endurance goal v1 | ≥ 3–5 min useful flight | Improve after it flies |

---

## Phase 0 — Study pack (before buying carbon)

1. Collect reference: top/side/front photos of rock pigeon, wing outstretched.  
2. Note: body length, span, wing area rough outline on graph paper or CAD.  
3. Skim one pigeon wing-kinematics paper (shoulder/elbow/wrist coupling).  
4. Watch Festo SmartBird / BionicSwift flight video once for torsion intuition — then design **pigeon-sized**, don’t copy gull span.  
5. Buy/borrow **ELRS handset**; start simulator stick time in parallel with Phase 1.

**Exit:** one-page sketch with dimensions + CG guess (battery in breast).

---

## Phase 1 — Bench flapper (naked wing pair)

**Goal:** one drive producing lift/thrust you can measure.

| Parts (typical) | Role |
|---|---|
| Brushless motor + ESC sized for ~20–40 W class | Flap power (tune after bench) |
| Crank / linkage / gears | Convert rotation → flap |
| Carbon tube spars (humerus / forearm stand-ins) | Structure |
| Rig stand + scale / load cell | Measure mean lift |
| Bench PSU or test LiPo | Power |

**Exit:** sustained flapping at target Hz; record power draw and lift. If lift << weight target, change wing area / twist / gearing **before** building a pretty body.

---

## Phase 2 — Avian path + twist (Level B heart)

**Goal:** flapping path looks like a bird, not a door hinge.

1. Add elbow/wrist (or linked under-actuated joints) so the wingtip traces a pigeon-like stroke.  
2. Add **active torsion** (servo/gear in wing) or carefully tuned aero-elastic twist.  
3. Film slow-mo next to a reference pigeon flight clip; iterate until “bird” not “bat”.  

**Exit:** side-by-side video you’re willing to show as “mechanism looks avian.”

---

## Phase 3 — Feathered / analogue surface

**Goal:** wing area that opens/closes and sheds air on the upstroke better than a solid plate.

Options:

- Synthetic feather vanes on spars (repairable, repeatable)  
- Real molted feathers on a jointed frame (PigeonBot-style insight; ethics: use shed/sourced feathers, not harm birds)  

**Exit:** same bench test as Phase 1 with covering on — net lift/efficiency up or flight behavior improved.

---

## Phase 4 — Body, CG, radio, tail, legs

| Item | Placement |
|---|---|
| LiPo battery | Breast / keel volume (where muscle mass is) |
| FC + ELRS RX | Center body, antennas clear of carbon where possible |
| Tail fan + servos | Pitch/yaw |
| Legs | Fold under; stand on ground |
| Foam/carbon torso | Pigeon proportions; access hatch for battery |

**Exit:** powered taxi / short hops on handset indoors or calm yard, props/wings guarded as needed; failsafe verified **props/wings restrained first**.

---

## Phase 5 — Outdoor flight (undressed OK)

**Goal:** controlled outdoor flight on a mild day.

- Line-of-sight, legal airspace, soft field for landings  
- Log AUW, pack voltage, flight minutes  
- Trim tail and flap amplitude until track is controllable  

**Exit:** Gate “airframe flies outdoors” checked. Ugly foam is fine.

---

## Phase 6 — Camera

- Lightweight cam in head sculpt (or breast port if head CG hurts)  
- Video TX; ground RX → goggles and/or iPhone  
- Park-scale distance test  

**Exit:** you can steer using the view (or LOS + view assist).

---

## Phase 7 — Anatomical dress (finish Level B)

- Head/beak/eye fairings to pigeon proportion  
- Body covering (fabric/foam/feather) that survives flapping  
- Legs look like pigeon legs when perched (function already proven)  
- No dangling gear visible at park distance  

**Exit:** Level B acceptance checklist in `LOCKED.md` all checked.

---

## Shopping posture (don’t binge Phase 7 first)

**Buy early:** handset, bench motor/ESC, carbon tube, basic tools, test LiPos, charger, safety gear.  
**Buy later:** feathers/covering art, final head sculpt, pretty legs.  
**Never skip:** failsafe test, weight log, outdoor flight before cosmetics.

Rough early spend order of magnitude: handset + bench drive + materials often land in the **low hundreds of USD** before camera/VTX finish — verify live prices; don’t treat this as a quote.

---

## Parallel skill track (doesn’t wait on airframe)

- EdgeTX / ELRS bind + failsafe on any tiny trainer or sim  
- Basic composite / foam shaping  
- One CAD assembly of wing linkage (even crude)  

---

## If something breaks the lock

| Problem | Response |
|---|---|
| Flapping never makes outdoor margin | Declare hybrid assist **openly**, keep Level B look — or reopen lock |
| Want museum 5 m realism | That’s Level C — new decision, after B ships |
| Want dragonfly again | Separate project; don’t derail B |
