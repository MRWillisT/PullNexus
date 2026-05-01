# Python not recognized in command prompt

**Session ID:** `3a4b7022-bf43-4008-9d2d-9df76d3a4b8c`  
**Created:** 2026-03-23 17:53:59 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\globalStorage\emptyWindowChatSessions\3a4b7022-bf43-4008-9d2d-9df76d3a4b8c.jsonl`

---

## Turn 1 — 2026-03-23 17:57:11 UTC

**User:**

then how can i pip install -r requirements.txt
?

**Copilot:**

Same fix — use `py -m pip` instead of `pip`:

```
py -m pip install -r requirements.txt
```

This uses the `py` launcher to call pip through your installed Python, bypassing the PATH issue entirely. Run it from your project directory:

```
cd C:\Users\willa\Documents\GitHub\ESET-KeyGen
py -m pip install -r requirements.txt
```

---
