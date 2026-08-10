# Pigeon pivot — anatomically accurate outdoor flyer

**Question:** What if it’s a pigeon instead of a dragonfly — can it be anatomically correct and accurate, with camera, outdoor distance, practical remote?

**Short answer:** **Yes — pigeon scale is a much better match for outdoor distance than dragonfly scale.** Anatomical accuracy is doable in layers. “Looks and flaps like a rock pigeon” is a serious but known class of problem. “Indistinguishable from a live pigeon at arm’s length including every joint and feather” is a longer craft project, not a physics veto.

---

## First principles: why pigeon helps

| Constraint | Dragonfly ask | Pigeon ask |
|---|---|---|
| Real animal mass | ~0.2–1 g | **~300–500 g** (rock pigeon / *Columba livia*) |
| Wingspan | ~5–10 cm | **~60–70 cm** |
| Flap rate | tens of Hz | **~5–8 Hz** (much easier mechanisms) |
| Outdoor wind | Brutal at gram scale | Manageable; birds live in it |
| Battery + camera + radio | Fights every gram | **Comfortable fit** |
| Anatomical detail (feathers, beak, eyes) | Almost no mass budget for cosmetics | Room for real/synthetic feathers, sculpted body |

Energy, wind, and payload all scale in your favor. The hard part shifts from “can anything fly?” to **“can the wing skeleton and skin move like a pigeon’s?”**

Existence proofs nearby (not copies): Festo SmartBird / BionicSwift (gull/swift-inspired flappers with torsion and feather-like covers), Stanford **PigeonBot** (real pigeon feathers on a jointed wing for morphing — glider-focused research), hobby/consumer ornithopters. Pigeon-specific joint kinematics are published (shoulder/elbow/wrist coupling in free flight). You stand on science; you still have to build.

---

## What “anatomically correct” can mean (pick a level)

Be precise or the project never ends.

### Level A — Field silhouette (good outdoor robot)

- Body length, wingspan, mass within rock-pigeon range  
- Head–body–tail proportions right  
- Wings flap with active twist (not a toy “bat on a stick”)  
- Covered so it reads as a pigeon at **park distance** (10–30 m)  
- Camera in/near head or breast, not a dangling GoPro brick  

**Doable as the main build target.**

### Level B — Anatomical flight machine (serious biomimetics) — **LOCKED 2026-08-10**

**This is the project success bar.** See [`LOCKED.md`](LOCKED.md) and [`level-b-build.md`](level-b-build.md).

Level A, plus:

- Wing planform matches pigeon (primary/secondary layout)  
- Shoulder–elbow–wrist degrees of freedom inspired by real joint data (even if under-actuated: one motor + linkages that *approximate* coupled bird motion)  
- Feathered or feather-analogue wing surface that opens/closes area in flight (Festo-style / PigeonBot-style insight)  
- Tail used for pitch/yaw like a bird  
- Legs that fold in flight and can stand/perch (even if clumsy)  

**Doable with a multi-phase build; this is the “anatomically accurate” sweet spot.**

### Level C — Taxidermy / forensic accuracy

Level B, plus:

- Correct feather count/types, iridescence, eye ring, cere, feet scales  
- Head bob / neck DOF  
- Breathing-looking abdomen, micro-motions at rest  
- Silent enough and styled enough that a birder is unsure at 5 m  

**Possible as craft + covering art on top of a working Level B airframe.** Heavier time cost; not required for camera + distance + RC.

### What we do *not* promise

- Living tissue, real metabolism, or “full biological skeleton with hollow bones and air sacs” as the structure — carbon/foam/feathers on a mechanism is the honest engineering substrate  
- Perfect hover like a quad — pigeons are mostly forward-flight / burst / glide animals; design for that  
- Passing as wildlife for covert anything — say the ethics out loud if that’s ever the motive; this doc assumes open hobby/research use  

---

## System that fits a pigeon body (field stack)

Same outdoor first principles as before; mass is no longer the enemy.

```text
RADIO HANDSET (ELRS-class)
        │ control
        v
┌─────────────────────────────────────┐
│  PIGEON AIRFRAME ~350–500 g         │
│  - flapping drive + wing torsion    │
│  - battery in breast/keel volume    │
│  - FC + ELRS RX                     │
│  - camera in head (or chest port)   │
│  - video TX                         │
│  - optional: real/synthetic feathers│
└─────────────────────────────────────┘
        │ camera RF
        v
  goggles and/or iPhone viewer
```

**Remote:** still a **real handset** outdoors. iPhone = viewer/map. Pigeon size doesn’t make phone Wi‑Fi a good primary RC; it just makes everything else easier.

**Camera:** a normal lightweight digital or FPV camera fits in a pigeon head sculpt. Pinna compressive camera is optional here — nice for radio thrift, not required for mass.

**Flight time:** with tens of watts (SmartBird-class numbers were ~23 W for a 450 g gull-scale bird), a few hundred grams of LiPo can mean **minutes to low tens of minutes** depending on throttle and flap duty — design for that, measure, don’t brochure.

---

## Anatomy → mechanism map (Level B)

| Real pigeon part | Engineering stand-in |
|---|---|
| Keel / breast muscle mass | Main drive motor(s) + battery pack (put mass where the bird has mass — helps CG) |
| Humerus / radius-ulna / manus | Carbon spars + joints; under-actuated linkages from published joint couplings |
| Primaries / secondaries | Real feathers (ethical sourced / molted) or molded feather vanes on spars |
| Alula | Small servo or passive aero surface later |
| Tail fan | Servo-driven pitch/yaw stabilizer |
| Head / neck | Fairing + camera; limited pan if mass allows |
| Legs / feet | Fold under belly; perch legs v2 |
| Eyes | Glass/resin lenses; camera behind one or between |

**CG rule from nature:** birds are nose/breast-heavy relative to wings. Put battery and motor where the pectorals would be so it *balances* like a pigeon, not like a quad with a bird sock on it.

---

## Build order (pigeon)

1. **Study pack** — rock pigeon morphometrics (mass, span, wing area) + one paper on joint kinematics; decide Level A vs B.  
2. **Bench flapper** — one wing pair, measure thrust/power, no skin.  
3. **Torsion / twist** — add active or carefully tuned passive twist (this is what makes bird flight efficient).  
4. **Body + CG** — pigeon torso, battery in keel, radio + FC.  
5. **Handset flights** — lawn / park, no fancy covering.  
6. **Camera** — head mount, video to goggles/phone.  
7. **Skinning** — feathers / covers for anatomical look (Level B→C).  
8. **Legs / perch** — after it flies cleanly.

Do not start with a taxidermy shell and hope it flies. **Fly first, dress second.**

---

## Comparison verdict

| | Dragonfly path | **Pigeon path** |
|---|---|---|
| Outdoor distance | Hard / needs mass growth anyway | **Natural fit** |
| Anatomical accuracy | Limited by grams | **Actually achievable** |
| Camera | Exotic or compromised | Standard micro cam fine |
| RC | Handset | Same handset — easier integration |
| Effort | Micro-robotics lab flavor | Biomimetic mechanism + craft covering |

If the goal is **outdoor + distance + anatomically convincing + camera**, **pigeon is the better primary vehicle.** Keep dragonfly as a later micro challenge if you still want it.

---

## Success definition (pigeon) — Level B LOCKED

You win when the Level B checklist in [`LOCKED.md`](LOCKED.md) is complete: avian wing path + twist, feathered/analogue surfaces, bird-like tail and folding legs, outdoor handset flight, integrated camera at park distance. Level C museum finish is optional later — not required to call this done.
