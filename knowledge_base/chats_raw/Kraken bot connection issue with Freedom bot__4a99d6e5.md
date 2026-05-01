# Kraken bot connection issue with Freedom bot

**Session ID:** `4a99d6e5-3186-465e-97b3-b8199e2d3268`  
**Created:** 2026-04-16 21:45:58 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\2832faeff98184b2f116b13fae9699e8\chatSessions\4a99d6e5-3186-465e-97b3-b8199e2d3268.jsonl`

---

## Turn 1 — 2026-04-16 21:47:28 UTC

**User:**

When im connected to Kracken the freedom bot wont work and connect to coins on kracken 📈 2026-04-16 17:45:25 · Freedom opportunity — 📊 Opportunity pipeline: universe=0 -> after-held-removal=0 (held=0).

**Copilot:**

Now I can see two problems. Let me check the Kraken client's tradeable symbols and the watchlist format:  Found the root cause. Kraken uses `USD` as quote currency, so  returns `BTCUSD`, `ETHUSD`, etc. But  always appends `USDT`, producing `BTCUSDT`, `ETHUSD`, etc. The  tradeable-symbols filter wipes out everything → `universe=0`.

The fix needs two parts:
1.  /  should use the exchange's actual quote currency when building the watchlist
2. The bootstrap scanner calls Binance-specific methods even on Kraken

Let me check how the exchange client is accessible in :  The  already has a  property. The fix is to use  in  instead of hardcoding `USDT`, and also fix the bootstrap scanner to skip Binance-specific calls on Kraken.

Let me read the relevant section of  and : Now I have the full picture. The issues are:

1. ****: builds symbols with hardcoded `USDT` suffix (from ), but Kraken symbols end in `USD` → tradeable filter removes everything.
2. ****: calls  /  which always fail on Kraken/silently return nothing.

The cleanest fix: use  /  when building the watchlist set, and use exchange-agnostic scanner methods for bootstrap.

Let me check what exchange-agnostic scanner methods exist: The scanner only has Binance-specific methods. The fix for bootstrapping is to guard against non-Binance clients. Let me also check the  `USDT` filter more precisely — the symbols come from  which hardcode `USDT`, and then the  filters only pass those

---
