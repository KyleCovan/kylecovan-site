# Weight budgets

All numbers are approximate and meant for trade studies, not certification. Weigh every part on a 0.01 g scale before trusting a design.

## Target classes

| Class | Takeoff mass | Wingspan / diagonal | Realistic camera | Phone link |
|---|---|---|---|---|
| **Insect-literal** | 1–4 g | 5–10 cm | Analog micro only | Custom RF, not App Store Wi‑Fi SoC |
| **Hand-micro quad** | 18–30 g | 40–70 mm prop-to-prop | Analog FPV or tiny Wi‑Fi JPEG | Wi‑Fi SoftAP viable |
| **Shell-clad dragonfly look** | 25–45 g | body ~8–12 cm | Same as above | Same |
| **Comfortable DIY + digital preview** | 40–80 g | 65–100 mm | Better sensors | Easier Wi‑Fi video |

**Product recommendation:** design for **hand-micro** first (~25 g AUW), accept that a real dragonfly is ~10–50× lighter, and treat every gram added for looks as a flight-time tax.

## Reference tear-downs

### DelFly Micro (~3.07 g) — proof that camera + insect scale exists in labs

| Part | Mass |
|---|---|
| Battery (30 mAh LiPo) | ~1.0 g |
| Camera + transmitter | ~0.4 g |
| Motor | ~0.45 g |
| Receiver | ~0.2 g |
| Actuators | ~0.5 g |
| Structure / rest | ~0.52 g |

Flight ~2–3 minutes, range ~50 m. No ESP32-class Wi‑Fi, no Swift app stack on board.

### ESP-FLY class (~25 g with battery) — proof phone control is hobby-reachable

| Part | Mass (order of magnitude) |
|---|---|
| 3D-printed 50 mm frame | ~4 g |
| XIAO ESP32-S3 | ~ few g |
| 4× 615 coreless + props | dominant with battery |
| MPU-6050 + MOSFET board | included in stack |
| 1S 250 mAh LiPo | often ~6–8 g class |
| Optional AIO FPV cam | +~3 g → ~28 g AUW |

Flight ~5 minutes. Wi‑Fi phone control demonstrated. Video over the same ESP link is still immature on stock firmware — plan analog FPV or a firmware project.

## Example budget: “dragonfly look” micro quad (Phase 2 target)

Aim: **≤ 32 g** AUW, indoor, phone sticks + live preview.

| Subsystem | Target | Notes |
|---|---|---|
| Airframe + dragonfly shell | 5–8 g | Thin PET/Mylar wings; hollow abdomen; no solid resin body |
| FC + MCU + IMU | 3–5 g | Prefer single board (XIAO-class) |
| 4× motors + props | 6–8 g | 615 or lighter if thrust allows ≥2:1 T/W |
| ESCs / MOSFETs | 1–2 g | Often on FC board |
| Battery 1S 150–250 mAh | 5–8 g | Biggest lever on flight time |
| Camera path A: analog AIO | 2–4 g | Needs ground RX for phone or goggles |
| Camera path B: Wi‑Fi JPEG | 4–8 g | Heavier / hotter; true phone-only preview |
| Wiring, tape, connectors | 1–2 g | Always underestimated |
| **Reserve** | 2 g | Cosmetics, repairs, antenna |

If Path B blows the budget, ship Path A and say so — honesty beats a grounded HD dream.

## Mass rules of thumb

1. **Battery ≈ 25–35%** of AUW on micro quads. Cutting capacity to hit “insect weight” cuts flight to toy-hop territory.
2. **Thrust-to-weight ≥ 2:1** for controllable indoor flight; ≥ 3:1 if you add a shell that catches air.
3. **Shell drag** can cost more than shell mass. Open wing films beat closed “ornament” wings over props.
4. Every connector you can solder permanently is a win. JST housings are heavy at this scale.

## What to give up to get smaller

| If you need… | Drop… |
|---|---|
| Closer to 15 g | Digital video, thick 3D print, 250 mAh → 100–150 mAh |
| Closer to 10 g | Phone Wi‑Fi SoC → discrete RX; custom PCB; no shell |
| Closer to 3 g | Flapping research program; analog only; accept 2–3 min |

## Measurement checklist (do this in Phase 1)

- [ ] Weigh bare frame
- [ ] Weigh FC stack
- [ ] Weigh one motor + prop × 4
- [ ] Weigh battery full
- [ ] Weigh camera option A and B separately
- [ ] Sum vs scale (catch double-counted screws)
- [ ] Hover current draw → estimated minutes = (mAh × 0.8 × V) / (W_hover) rough energy check
