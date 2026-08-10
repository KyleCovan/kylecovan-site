# Weight budget — Anisoptera (gram-scale closeout)

Budgets are design ceilings. Weigh on a **0.001–0.01 g** scale. If a part only exists in hobby packaging, the task is to **repackage**, not to accept the packaging as physics.

## Target

| | |
|---|---|
| AUW | **≤ 2.0 g** |
| Stretch | **≤ 1.0 g** (drop free-flight store, rely on beam) |
| Span | **8–10 cm** |

## Line items (v1)

| Subsystem | Ceiling | Notes |
|---|---|---|
| Vein Drive wings + actuators | 0.60 g | Piezo/DEA; veins are structure |
| Thorax / abdomen structure | 0.22 g | Carbon + film; no solid resin brick |
| Pinna (compressive oculus) | 0.12 g | Metasurface + mask + 1 diode + bare TIA |
| Return Gleam MRR | 0.08 g | Cat’s-eye / cube + shutter |
| PV + wiring | 0.10 g | Wing/abdomen patch |
| Micro-store + HV boost | 0.25 g | Peak + brownout; beam carries mission joules |
| Control die + IMU + harness | 0.08 g | Bare die / flex, not FR4 FC |
| Margin | 0.15 g | Cosmetics, adhesive, repair |
| **Total** | **1.60 g** | |

## What is *forbidden* in the flying mass (put it on the ground)

| Ground / phone | Why it must not fly |
|---|---|
| JPEG/ISP pipeline | Pinna reconstructs on iPhone NPU |
| Wi‑Fi PA + antenna module | Return Gleam replaces TX power |
| Mission-energy LiPo for 10 min hover | Lumen Keel beams joules |
| Plastic lens stack for VGA CMOS | Diffraction-limited flat film + compute |
| Quad motors, props, 4 ESC board | Wrong aero machine for the ask |

## Scaling math (energy)

Continuous draw estimate \(P = 0.40\,\mathrm{W}\).

| Store mass | Optimistic usable energy density | Energy | Hover time if store-only |
|---|---|---|---|
| 0.25 g | 100 Wh/kg effective | 90 J | ~3.8 min |
| 0.25 g | 50 Wh/kg effective (more honest at this scale) | 45 J | ~1.9 min |
| 0 g store | beamed only | — | continuous under track |

**Conclusion:** free-flight minutes are a **store-density** problem; continuous room flight is a **beam** problem. Anisoptera chooses beam-primary, store-secondary — not because batteries are “bad,” but because packaged Wh/kg at 250 mg is a materials limit we will not wish away.

## Lift check (order of magnitude)

Need thrust ≈ weight for hover: \(2\,\mathrm{g} \Rightarrow \sim0.020\,\mathrm{N}\).

At flapping efficiencies reported for piezo MAVs, electrical power of a few ×10⁻¹ W class has already produced liftoff at **≪ 1 g** (UW 190 mg laser fly). Scaling to 1.6 g is an actuator/area problem, not a category error. If measured T/W < 1.2 after Vein Drive v1, enlarge wing area or raise beam power — do not add propellers unless Gate 4 explicitly abandons biomimetic lift.

## Camera mass comparison (why Pinna exists)

| Approach | Typical mass | Fits ≤2 g AUW? |
|---|---|---|
| Digital CMOS module + lens | 1–5+ g | No |
| Analog FPV AIO | 1.5–4 g | No |
| DelFly-class analog cam+TX | ~0.4 g | Marginal (eats budget; not phone-native) |
| **Pinna** | **0.08–0.15 g** | **Yes** |

## Weighing protocol

1. Weigh each flex/die before potting  
2. Weigh wings alone, then with actuator  
3. Weigh MRR assembly dry  
4. Sum vs whole vehicle on the same scale  
5. Any connector >20 mg needs a redesign justification
