# AIS Ship Count Fallback Data Issue

**Session ID:** `0b41f769-b02e-40d3-945c-edaa8d53253a`  
**Created:** 2026-04-10 02:40:49 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\e6cf8961ae1a9541be622fe1bddfc429\chatSessions\0b41f769-b02e-40d3-945c-edaa8d53253a.jsonl`

---

## Turn 1 — 2026-04-10 02:41:26 UTC

**User:**

for some reason my ais ship count is using fallback data

**Copilot:**

I'll trace why the AIS count is falling back and fix the source of it.

---

## Turn 2 — 2026-04-10 02:51:31 UTC

**User:**

Try Again

**Copilot:**

## ✅ AIS ship count issue finished

I traced it to .

### What was happening
- The **live AIS websocket is currently silent** in this environment.
- The app was dropping into **synthetic estimated fallback** instead of reusing the last real AIS snapshot.

### Fix applied
-  now **prefers the last real cached AIS data** before using generated fallback data.
-  now labels those rows as `cache` instead of `est`.

### Verified result
I ran a fresh check and got:

```json
{
  "configured": true,
  "running": false,
  "vessel_count": 0,
  "cached_vessel_count": 670,
  "using_cached": true,
  "using_fallback": false
}
```

Chokepoint counts are now coming from **cached real AIS data**, e.g.:
- `Strait of Hormuz`: `42`
- `Strait of Malacca`: `499`
- `Bosphorus`: `4`
- `Cape of Good Hope`: `125`

---

## Note
> The upstream `AISStream` feed/key still appears not to be returning live messages right now, so this fix prevents fake fallback counts from showing while that feed is quiet.

If you want, I can next make the UI explicitly show **“Live / Cached / Estimated”** status text.

---

## Turn 3 — 2026-04-10 02:54:26 UTC

**User:**

can you remove the work cashe frome these and move the km reading to the left so its all inside the box? if you have to you can add a indacator light in the top right corner of the box geen for coneected to ais - yellow for cashed - red for fallback - no words the light alone will be fine

**Copilot:**

I'll clean up the AIS snapshot card and keep the status indicator inside the box.

---

## Turn 4 — 2026-04-10 02:57:43 UTC

**User:**

can we also implaments a rul to keep retrying for live data and not settle on cashed or fallback

**Copilot:**

I'll update the AIS worker to keep retrying for live data instead of settling on cached or fallback.

---

## Turn 5 — 2026-04-10 03:01:19 UTC

**User:**

sure that sounds good

**Copilot:**

I'll add the retry blink to the AIS indicator and verify the card rendering.

---
