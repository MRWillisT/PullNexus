# Voice Profile (About-Me Generator)

A two-prompt workflow that extracts your unique writing voice through a structured 100-question interview, then compresses the result into a compact `about-me.md` file any LLM can use as standing context.

Pull this skill to get the two prompts and drop them into any chat model — Claude, ChatGPT, Gemini, or a local model via Ollama/LM Studio.

## What This Skill Covers

- **Prompt 1 — The Interview:** A "Taste Interviewer" system prompt that runs a 100-question deep-dive across your beliefs, writing mechanics, aesthetic preferences, voice, structural habits, hard nos, and red flags. One question at a time, with push-back on vague answers.
- **Prompt 2 — The Compiler:** A "Voice Compiler" system prompt that takes the raw interview transcript and distills it into a compact, token-efficient `about-me.md` (target: 2,000–4,000 tokens) that any AI can ingest at session start.
- The final file uses an XML-structured `<about_me>` format covering: usage rules, voice fingerprint, writing laws, communication laws, hard refusals, taste loves/disgusts, phrase bank, signature tells, decision rules, productive contradictions, and golden examples.

## Who Should Use This Skill

Writers, founders, content creators, or anyone who wants an AI to produce first drafts that actually sound like them. Also useful for teams where one person's voice needs to be distributed across ghostwriters or AI assistants.

## How to Use

```bash
pullnexus pull voice-profile
```

This gives you two prompt files. Run them in order in a single chat session:

1. Open a **fresh chat** with your preferred model.
2. Paste `prompt1_interviewer.md` as your first message.
3. Answer all 100 questions (voice dictation like Wispr Flow makes this faster).
4. In the **same conversation**, paste `prompt2_compiler.md`.
5. Save the output as `about-me.md` in your model's context/memory folder.

### Tips

- Use an extended-thinking or long-context model for Prompt 1 (the transcript will be large).
- Test the compressed file in a blank session before committing to it.
- Revisit and update the file as your voice evolves — use Obsidian or any Markdown editor.
- If your LLM agent asks before loading context files ("Load about-me.md? [y/n]"), that's agent-level behavior — configure it in your agent's system prompt, not here.

## File Structure

```
voice-profile/
├── skill.json               # Skill metadata
├── README.md                # This file
├── prompt1_interviewer.md   # The 100-question Taste Interviewer prompt
├── prompt2_compiler.md      # The Voice Compiler / compression prompt
└── examples.jsonl           # Fine-tuning examples for local models
```

## License

CC0-1.0 — public domain, free to use for any purpose.

Original workflow by [@rubenhassid](https://x.com/rubenhassid).
