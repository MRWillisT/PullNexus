# Local image projection methods explained

**Session ID:** `f0b511ba-3ed2-4592-88c4-50bd29af3e0e`  
**Created:** 2026-03-14 02:22:54 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\99eab3bb4320f5b1b1040bb529541341\chatSessions\f0b511ba-3ed2-4592-88c4-50bd29af3e0e.jsonl`

---

## Turn 1 — 2026-03-14 02:25:08 UTC

**User:**

well my issue is somehow when moving thie server to another box the projection is all screwed up now , I need to let the instance on the server box know what it was before the move

**Copilot:**

I understand—you want the server instance to explicitly use the same CRS as before the migration so rendering matches. I’m going to locate where your pipeline writes/reads georeferencing and then set the CRS/projection in code or config so it’s deterministic on every box.I found the likely culprit: projection metadata is written in , and it has a fallback path if  isn’t installed. I’ll inspect that logic to confirm whether the moved server is skipping `.prj` creation or writing the wrong CRS.

---

## Turn 2 — 2026-03-14 02:27:34 UTC

**User:**

jest tell me what to have the other instance running on that machine to do and ill send it over to him

**Copilot:**

Send this to the other machine operator:

1) Open PowerShell in the project root ().

2) Set the CRS env var to old behavior (WGS84 lat/lon):
- Current session: `$env:MERGED_CRS_EPSG='4326'`
- Persist for future shells: `setx MERGED_CRS_EPSG 4326`

3) Restart the radar server process () so it picks up the env var.

4) Force fresh merged output sidecars (recommended):
- Delete old merged files in  (`.png`, `.pgw`, `.prj`) or wait for next merge cycle.

5) Verify projection on a newly created merged frame:
- `Get-Content E:\MapServer\tiles\NEXRAD\merged\zoom4\*.prj | Select-String 'EPSG",4326'`

If they run it as a Windows service, make sure  is set in that service account/environment (not just an interactive shell), then restart the service.

---
