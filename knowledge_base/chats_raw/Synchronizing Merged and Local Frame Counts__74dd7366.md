# Synchronizing Merged and Local Frame Counts

**Session ID:** `74dd7366-d07b-4b57-817e-41e67a857293`  
**Created:** 2026-03-18 02:06:48 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\5b0d94244ce85c8130543581445ff9c1\chatSessions\74dd7366-d07b-4b57-817e-41e67a857293.jsonl`

---

## Turn 1 — 2026-03-18 02:13:17 UTC

**User:**

Ask mode for a sec while talk abou this....So id like to see if theres anything we can do to get merged frame count to match the local frame count, so the animation plays in lock step with each other in the app and they match? Arnt we blending frames on merged? I wish I could nail this thing so it looked right, merged frames seem to be less than locals, so hear me out , tnextrad loops every 3 to 7ish mins , can we just collect individual site images and make a merged for every loop? Im just trying to understand

**Copilot:**

Let me read the relevant scripts to understand the current pipeline before we discuss this.

---

## Turn 2 — 2026-03-18 02:24:07 UTC

**User:**

lets do it , because the way it is now isnt working onw the visuals side of things , its close in some areas and not others, nd they almost looks close now but they dont match and it looks like the merged is late and ends , then the locals pick up and the scans jump foward .  I just need the merge to show the movement and not add 2 scans from the same site in any single image , aI think you get what im going for, lets try it!

**Copilot:**

*(no response captured)*

---

## Turn 3 — 2026-03-18 03:47:56 UTC

**User:**

ok I have a strange one this time - so in my merged images I have a storm over the ocean jusdt south of FL , but its not found in my local  just south around keywest KBYX i think , I dont even understand how that can happen

**Copilot:**

Good mystery — this is actually expected behavior given how the merge works, and there are a few things happening simultaneously.

## Why the merged shows a storm that KBYX doesn't

**Multiple sites cover that area.** The ocean south of FL has overlapping footprints from at least:
- **KBYX** — Key West (southernmost, but its beam is scanning from ~24.6°N)
- **KAMX** — Miami (~24.6°N, but further east, different geometry)
- **KTBW** — Tampa (north, but wide coverage cone reaches south)

The merge composites all of them via max-alpha (highest dBZ wins per pixel). So a storm south of FL could be:

**1. In KAMX's sweet spot but outside KBYX's practical range**
NEXRAD range is ~460 km in principle, but the beam elevation rises as range increases — at 300+ km south of KBYX the beam is sampling well above the storm tops, so it literally misses the precip. KAMX sits at a different angle to the same storm and its beam geometry at that distance may still intersect the storm. The merged picks up KAMX's hit, the KBYX local shows nothing.

**2. Timing skew between site frames**
 grabs each site's single freshest settled frame. With  now, one merged image could be compositing KAMX data from :12 and KBYX data from :06. A fast-moving convective cell could be in the KAMX swath at :12 that didn't exist at :06 in KBYX's swath.

**3. Edge fade asymmetry**
 applies an edge fade starting at 60% radius (). A storm at the southern edge of KBYX's tile gets alpha-faded to near-zero, so the merge's max-alpha logic discards it. That same storm is in KAMX's inner coverage zone — full alpha — so the merge keeps KAMX's data. From the local KBYX tile it looks missing, but it's there in the merge via KAMX.

**4. The local view is only one site**
The local animation in the app shows `KBYX`'s own tile — an

---
