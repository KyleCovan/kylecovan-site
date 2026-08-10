# Phase A — first weekend: see a picture on your iPhone

Plain English. No flying yet. No puck yet. Just prove the weird camera idea works on a table.

## Why I said “living room” before (and why that was confusing)

That phrase was bad jargon. I only meant:

- indoors, in a normal house or workshop  
- not outdoors in wind  
- not a military / highway-range gadget  

Same with “product.” I meant “a thing you can actually use,” not “something for sale.”  

Sorry for the fog. From here down: normal words.

---

## What you’re building this weekend

A **desktop version of Pinna** — the new tiny camera idea.

You point it at something on your desk (a mug, a book cover).  
Your **iPhone shows a rough live picture** of that thing.

The camera on the desk is *not* a normal webcam. It uses one light sensor and a flickering pattern, and the phone does the math to turn that into an image. If that works on a table, the same idea can later shrink and ride on the dragonfly. If it doesn’t work on a table, we fix it here — cheap and safe — before any flying hardware.

**Success looks like:** you recognize the mug on your phone screen, updating a few times per second. Ugly is fine. Blank or pure noise is not done yet.

---

## The idea in one breath

Normal camera: millions of pixels all at once → heavy chip.  

This camera:

1. Light from the scene hits a **pattern** (like a tiny flickering checkerboard).  
2. One **light sensor** measures “how much light got through right now.”  
3. Change the pattern many times; record many numbers.  
4. Phone software says: “given these numbers and those patterns, what picture makes sense?”  

That’s it. The dragonfly later only needs to send those numbers. Your phone already knows how to be smart.

---

## What you need (bench parts)

You can substitute similar parts. Exact brands don’t matter.

| Thing | What it’s for | Rough cost |
|---|---|---|
| Photodiode or “light sensor” breakout | The single “eye cell” | a few $ |
| Small MCU board (XIAO / Arduino / Pico) | Reads the sensor, drives the pattern, sends numbers to a computer | ~$5–15 |
| Way to make patterns | Start simple: phone/tablet showing black-white patterns on screen *in front of* a tiny hole, **or** a small LCD / e‑ink / printed film on a little servo wheel | $0–40 |
| Cardboard + tape + a pinhole or cheap lenslet | Holds alignment so light from the scene reaches the sensor through the pattern | junk drawer |
| USB cable | Power + data to your Mac | owned |
| Your iPhone | Shows the reconstructed picture | owned |
| Computer (Mac is fine) | First weekend: run reconstruction, then AirPlay/stream or a tiny local server to the phone | owned |

Optional later: a real tiny shutter/LCD mask. **Not required day one.** Day one can be: MCU + photodiode staring at a second screen that flashes patterns.

### Simplest day-one setup (recommended)

```text
[ mug on desk ]
       |
       v
[ cardboard tube with a small hole ]
       |
       v
[ photodiode on MCU ]
       ^
       |
[ your computer or a second phone screen flashing patterns
  placed so the sensor "sees" scene light mixed with the pattern ]
```

Even simpler teaching setup used in labs: put the **pattern on a monitor**, put a **single pixel sensor** in front of the monitor while the “scene” is optically combined — but for a first gut-check, many people start with:

**Simulation first (evening 1):** no hardware. Feed a photo into software, pretend to take compressive measurements, reconstruct. Proves your phone/Mac math pipeline.  
**Hardware second (day 2):** real photodiode measurements.

Both count as Phase A. Hardware is the real confidence; sim is the confidence that you understand it.

---

## Weekend schedule

### Friday night — understand + simulate (1–2 hours)

1. Pick a photo of a mug.  
2. Run a small script that:  
   - makes random black/white patterns  
   - multiplies each pattern by the photo (dot product) → one number per pattern  
   - stacks ~500–1000 numbers  
   - reconstructs a blurry mug  
3. Put that reconstructed video/image on your iPhone (Messages to yourself, Local website, whatever is dumb and easy).

**Pass:** you see why “few numbers → picture” works at all.

### Saturday — real light sensor (2–4 hours)

1. Wire photodiode → MCU. Read values over serial. Wave your hand; numbers change.  
2. Build a crude tube so the sensor looks at one spot on your desk.  
3. Display patterns (second screen or printed wheel). Sync: MCU knows which pattern number it’s on when it samples.  
4. Save a burst of (pattern_id, value) to the Mac.  
5. Run the same reconstruction as Friday.  

**Pass:** reconstructed image is vaguely the real scene (edges of a book, shape of a mug).  

**If it’s garbage:** check sync (pattern id vs sample), stray light, sensor saturation. This is normal. Iterate Saturday evening.

### Sunday — get it on the iPhone live (2–3 hours)

1. Mac reconstructs each new burst.  
2. Show frames on iPhone:  
   - easiest: Mac runs a local webpage; iPhone on same Wi‑Fi opens it; or  
   - slightly more work: tiny iOS app that receives numbers and reconstructs (can wait a week).  
3. Aim for **≥3 updates per second**, 64×64-ish resolution.  

**Pass for Phase A:** you can point the desk rig at two different objects and tell them apart on the phone without looking at the desk.

---

## What “good enough” means (and what it doesn’t)

| Good enough now | Not required now |
|---|---|
| Recognize objects | Pretty HD video |
| A few frames per second | Cinema frame rate |
| Desk lighting | Outdoor sun |
| Cardboard mess | Dragonfly body |
| USB cable to Mac | Wireless optical link |

Phase A does **not** include flying, lasers, or the table puck. Those come after this picture works.

---

## How this connects to the dragonfly (so the weekend isn’t a random science fair)

```text
THIS WEEKEND (desk)          LATER (dragonfly)
-------------------------    --------------------------
Pattern + one sensor    →    same idea, shrunk as Pinna
Numbers to Mac/phone    →    numbers via light reflector
Phone shows picture     →    same phone app, in flight
Big battery / USB       →    tiny store + table beam puck
No wings                →    flapping body
```

You’re not building a toy camera for its own sake. You’re proving the only part of the plan that sounds magical: **“a dragonfly-weight camera can still give me a view on my iPhone.”**

---

## Safety / spend

- No lasers this weekend.  
- No spinning props.  
- Budget: often **under $50** if you already have a MCU; more if you buy a small LCD mask.  
- Don’t buy dragonfly frames, laser pucks, or exotic shutters until Phase A passes.

---

## When Phase A is done, what we do next (one line each)

- **B:** send those numbers across the room on a reflected light beam (no heavy radio on the bug).  
- **C:** table puck that can power a tiny flyer with a beam (indoors).  
- **D:** flapping body that hovers.  
- **E:** put A+B on D.

You only earned E by not skipping A.
