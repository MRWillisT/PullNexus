# Improving sharpness of blended frames in app

**Session ID:** `b9b84d92-eba9-40e1-aab6-96c5347850d5`  
**Created:** 2026-03-18 18:19:33 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\5b0d94244ce85c8130543581445ff9c1\chatSessions\b9b84d92-eba9-40e1-aab6-96c5347850d5.jsonl`

---

## Turn 1 — 2026-03-18 18:20:35 UTC

**User:**

Is there another way to make the blended frames? right now when merged playes in the app its kinda blurry looking - just wondering if we can do it another way so the image stays sharp

**Copilot:**

You’re asking if there’s a better way to generate blended radar frames so playback looks sharper, and that makes sense. I’m going to quickly inspect how blending is currently implemented in the scripts, then I’ll suggest concrete alternatives that preserve edge detail better.I found the key blending path: the server currently creates in-between frames with , which will naturally soften echoes. Next I’ll inspect those exact functions and the app-side image rendering to identify the sharpest alternatives with minimal disruption.I confirmed server-side blending is a straight 50/50 pixel average, which explains the softness. I’m now locating the app renderer to rule out any extra blur from image scaling/filtering on the Android

---

## Turn 2 — 2026-03-18 18:26:08 UTC

**User:**

I just realized you maybe looking at older data in *.kt files - those files are old I think from before I moved the server to a seperate PC - The app is working fine its just the server images id like to fix , the local images look great in the app also so I dont want to mess with them at all

**Copilot:**

Perfect — that narrows it down cleanly to merged server frames only.

- The blur is coming from merged-frame interpolation on the server:  in , triggered by merged endpoint logic in .
- Local/site frames use a separate path in , so you can leave that untouched.

**Server-only fix (recommended)**
- In merged route , change:
  - 
  - to default `'false'` (or hard-set  for merged only).
- Keep local route default as-is (`'true'`) in .

That gives you sharp merged frames immediately, with zero changes to local image behavior.  
If you want, I can give you a tiny diff-style patch for just those merged-route lines so you can apply it on the server PC.

---

## Turn 3 — 2026-03-18 18:27:43 UTC

**User:**

Will I still have the current frame count becasue im syncing them with locals frame when I zoom in ?

**Copilot:**

Short answer: not with the exact same setting change.

- If you disable merged blending, merged endpoint count drops from about $2N-1$ to $N$ (because the inserted in-between frame is removed).  
- The inserted frame currently comes from , and merged blend toggle is read in .  
- Local frames still use their own blend path in , so local can remain unchanged.

If you want sharp merged frames and keep the same timeline length as today, use this server-only approach:
- Keep merged “interpolation slot,” but duplicate a real frame instead of Image.blend output (e.g., older, older, newer).  
- That preserves the current count behavior (roughly $2N-1$) without blur.

If you want, I can write the exact merged-only logic change (no local changes) as a tiny patch for the server

---

## Turn 4 — 2026-03-18 18:28:53 UTC

**User:**

sure that would be helpful

**Copilot:**

*(no response captured)*

---

## Turn 5 — 2026-03-18 18:29:46 UTC

**User:**

yes please

**Copilot:**

Use this merged-only variant (forward-biased cadence: older, newer, newer) in .

```diff
@@
 def _build_blended_frame_list(zoom_dir, frame_list):
-    """Return a frame list with one 50% blend inserted between each consecutive pair.
-
-    Sequence per gap: [older, 50% blend, newer]
-    This matches the local-site blend multiplier (2× raw count) so merged and
-    local animations loop at the same cadence in the app.
-    """
+    """Return a frame list with one inserted frame per gap, no blur.
+    Sequence per gap: [older, newer, newer] (forward-biased), total ~2N-1.
+    """
     out = []
     for i, f in enumerate(frame_list):
         out.append(f)
         if i + 1 < len(frame_list):
-            next_f = frame_list[i + 1]
-            blend50 = _ensure_blend_image(zoom_dir, f, next_f, alpha=0.50)
-            if blend50:
-                out.append(blend50)
+            out.append(frame_list[i + 1])
     return out
```

- Keeps merged frame count behavior for zoom-sync (~2N-1), but removes blur from .
- Leaves local/site logic untouched in .

If you want, I can also give a tiny cleanup snippet to stop/ignore old merged_blend files since they won’t be used anymore.

---
