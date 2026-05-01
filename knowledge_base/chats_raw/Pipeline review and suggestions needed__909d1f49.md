# Pipeline review and suggestions needed

**Session ID:** `909d1f49-73e1-4e33-9574-efd1450a4f55`  
**Created:** 2026-03-17 17:16:31 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\5b0d94244ce85c8130543581445ff9c1\chatSessions\909d1f49-73e1-4e33-9574-efd1450a4f55.jsonl`

---

## Turn 1 — 2026-03-17 17:19:42 UTC

**User:**

Can you look over my pipeline and see if anything stands out that should be diffrent? or changed? any suggestions?

**Copilot:**

I’m reviewing the production pipeline in Scripts with a code-review lens and will focus on operational risks, behavior mismatches, and places where the current design is likely to age badly.I’ve confirmed the core scripts are syntactically clean; now I’m checking lifecycle control, file handoff, and health semantics for the places where production pipelines usually fail quietly.I’ve found a few concrete issues already: at least one route can serve files outside the intended directory, and the watchdog coverage is inconsistent with the pipeline you described. I’m checking a couple more spots so I can separate real issues from style-only suggestions.

---

## Turn 2 — 2026-03-17 17:28:01 UTC

**User:**

Can you review these Findings and confirm they actually need fixed?  (note - velocity is activly being worked on so if docs need updated to avoid confusion please do that. ) 

The file-serving endpoints in delivery_guy.py:2211-2266, delivery_guy.py:2654-2697, and delivery_guy.py:2700-2719 build paths directly from user input and then pass them to send_file or open. On Windows, that is worth treating as a real security issue because backslashes can act as path separators. I would harden these by resolving the candidate path and rejecting anything that does not stay under the intended base directory.

The health and watchdog model has blind spots in delivery_guy.py:110, delivery_guy.py:1847-1889, and delivery_guy.py:2739-2806. Two problems stand out:

The documented pipeline in AGENTS.md lists get_nexrad_velocity.py as an active production script, but delivery_guy does not watch or restart it.
The health endpoint only marks a script missing if it exists in running_processes with the literal value not running. If a process never started and the key is absent entirely, it can slip through as not missing.
This means health can read healthier than reality.
The velocity pipeline ownership looks inconsistent. get_nexrad_velocity.py:34-35 downloads archives into data/VELOCITY, but cook_nexrad_velocity.py:35-36 analyzes data/NEXRAD instead. That makes the dedicated velocity downloader look unused by the analyzer. I would pick one source of truth:

Either velocity analysis should intentionally reuse the same Level II files as reflectivity, in which case get_nexrad_velocity.py is probably redundant and should be retired.
Or velocity should have its own archive flow, in which case cook_nexrad_velocity.py is pointed at the wrong input tree.
Several hot JSON files are rewritten in place instead of atomically, while readers already have JSON decode error handling that suggests you have seen read/write races before. The main spots are cook_nexrad_radar.py:924-926, delivery_guy.py:1482-1498, delivery_guy.py:2177-2178, and delivery_guy.py:2244-2245. The corresponding readers catching decode failures are in delivery_guy.py:2354-2357, delivery_guy.py:2486-2488, and delivery_guy.py:2692-2694. I would standardize on write temp file, flush, then os.replace for every shared JSON artifact.

There is an API contract mismatch around the source frames route. AGENTS.md describes GET /radar/<source>/frames as a frame-list endpoint, but delivery_guy.py:2190-2208 actually returns active sites, which overlaps with delivery_guy.py:2508-2525. That is not catastrophic, but it will create client confusion and future maintenance errors unless you either rename the route or fix the docs.

**Copilot:**

Let me read every flagged section before touching anything.

---

## Turn 3 — 2026-03-17 18:19:05 UTC

**User:**

they are getting Error fetching JSON from http://chaser.ddns.net:5000/radar/NEXRAD/KLVX/frames: SocketException - Connection reset - is that from out resent changes?

**Copilot:**

*(no response captured)*

---
