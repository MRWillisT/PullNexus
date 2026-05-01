# Improving Local AI in Continue Dev Plugin

**Session ID:** `1783c55d-5940-49c8-a751-6471e456aaa8`  
**Created:** 2026-04-22 16:36:50 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\globalStorage\emptyWindowChatSessions\1783c55d-5940-49c8-a751-6471e456aaa8.jsonl`

---

## Turn 1 — 2026-04-22 16:55:15 UTC

**User:**

are theere any tweaks you can do to my local ai to make it beter? - im using it in the continue dev plugin

**Copilot:**

Looking at your config, here are several concrete improvements:

1. **Add an embeddings model** — enables the `codebase` context provider, which lets the AI search your whole project semantically
2. **Add more context providers** — `problems` (LSP errors), `folder`, and `codebase`
3. **Tune autocomplete options** — reduce debounce delay, cap tokens for speed
4. **Set context length** — tells the model how much code it can hold in mind
5. **Add a system prompt** — steers responses toward being concise and code-focused First, pull the embeddings model (needed for codebase search):

---

## Turn 2 — 2026-04-22 16:56:12 UTC

**User:**

[Terminal ef72fd09-845c-4d5a-a676-f1a0489dec4d notification: command completed with exit code 0. Use send_to_terminal to send another command or kill_terminal to stop it.]
Terminal output:
PS C:\Users\willa> ollama pull nomic-embed-text 2>&1 | Select-String -Pattern "pulling|success|error" | Select-Object -Last 5

pulling 970aa74c0a90: 100% 
ΓûòΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûÅ 274 MB            
             
pulling c71d239df917: 100% 
ΓûòΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûÅ  11 KB            
             
pulling ce4a164fc046: 100% 
ΓûòΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûÅ   17 B            
             
pulling 31df23ea7daa: 100% 
ΓûòΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûêΓûÅ  420 B            
             
success

**Copilot:**

`nomic-embed-text` is installed. Now updating your config: 
```

```
Done. Here's a summary of what changed:

| Tweak | Effect |
|---|---|
| `contextLength: 16384 / 8192` | Tells Continue how much code the model can read at once — prevents silent truncation |
| `systemMessage` | Steers the 14B model to give concise, surgical answers instead of over-explaining |
| `embeddingsProvider: nomic-embed-text` | Powers `@codebase` — lets you semantically search your whole project |
| `debounceDelay: 300` | Autocomplete triggers 200ms faster |
| `maxPromptTokens: 1024` | Keeps autocomplete snappy by limiting prompt size |
| `prefixPercentage: 0.85` | Biases autocomplete toward what's before the cursor (more relevant) |
| `provider: problems` | Feeds LSP errors/warnings into chat context automatically |
| `provider: folder` | Lets you type `@folder` to include an entire directory |
| `provider: codebase` | Lets you type `@codebase` to search your whole project |

**To use `@codebase`:** open your project in VS Code, then run **Continue: Index Codebase** from the command palette the first time.

---

## Turn 3 — 2026-04-22 17:02:28 UTC

**User:**

yeah hes kinda stupid

**Copilot:**

The model is pretending to call a `read_file` tool — local Ollama models can't actually execute tools, so it just stalls. The fix is a better system prompt that tells it to look at what's already in its context (Continue injects open files automatically via the `open` provider), plus the user should tag files explicitly. 
```

```
Also, to make sure your open files are always visible to the model, start your messages with `@currentFile` or `@open` — this explicitly injects the file content into the prompt rather than relying on the model to figure it out.

So instead of

---
