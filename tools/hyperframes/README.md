# HyperFrames

Write HTML. Render video. Built for agents.

**GitHub:** [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) · 14.8k ★ · **License:** Apache-2.0 · by HeyGen

---

## What it does

HyperFrames is an open-source video rendering framework where compositions are plain HTML files with data attributes. No React, no proprietary DSL — if you can write HTML, you can make a video.

- **HTML-native** — compositions are HTML + CSS + GSAP/Lottie/Three.js. No build step. The `index.html` plays as-is in the browser.
- **AI-first** — ships skills for Claude Code, Cursor, Codex, and Gemini CLI. Agents already speak HTML.
- **Deterministic rendering** — same input = identical output. Designed for automated pipelines.
- **Frame Adapter pattern** — bring your own animation runtime (GSAP, Anime.js, Lottie, CSS, Three.js, WAAPI).

---

## Quick start

```bash
# Option 1: inject skills into your AI agent (recommended)
npx skills add heygen-com/hyperframes
# then prompt: "/hyperframes create a 10-second product intro with a fade-in title"

# Option 2: manual project
npx hyperframes init my-video
cd my-video
npx hyperframes preview   # live reload in browser
npx hyperframes render    # render to MP4
```

**Requirements:** Node.js >= 22, FFmpeg

---

## Agent skills (slash commands in Claude Code)

| Skill | What it teaches |
|---|---|
| `/hyperframes` | HTML composition authoring, captions, TTS, audio-reactive animation, transitions |
| `/hyperframes-cli` | Init, lint, preview, render, doctor |
| `/hyperframes-media` | TTS (Kokoro), transcription (Whisper), background removal (u2net) |
| `/gsap` | GSAP timelines — paused registration, deterministic seeking |
| `/animejs` | Anime.js timelines for HyperFrames seeking |
| `/lottie` | lottie-web / dotLottie with paused playback |
| `/three` | Three.js scenes driven by `hf-seek` events |

---

## Example agent prompts

```
/hyperframes Create a 10-second product intro with a fade-in title, background video, and music.
/hyperframes Turn this CSV into an animated bar chart race.
/hyperframes Make a 9:16 TikTok-style hook video about [topic] with captions synced to TTS.
/hyperframes Summarize the attached PDF into a 45-second pitch video.
```

---

## Packages

| Package | Purpose |
|---|---|
| `hyperframes` | CLI — create, preview, lint, render |
| `@hyperframes/core` | Types, parsers, linter, runtime, frame adapters |
| `@hyperframes/engine` | Seekable page-to-video capture (Puppeteer + FFmpeg) |
| `@hyperframes/producer` | Full render pipeline (capture + encode + audio mix) |
| `@hyperframes/studio` | Browser-based composition editor |
| `@hyperframes/player` | Embeddable `<hyperframes-player>` web component |
| `@hyperframes/shader-transitions` | WebGL shader transitions |

---

## 50+ catalog blocks

```bash
npx hyperframes add flash-through-white   # shader transition
npx hyperframes add instagram-follow      # social overlay
npx hyperframes add data-chart            # animated chart
```

Full catalog: [hyperframes.heygen.com/catalog](https://hyperframes.heygen.com/catalog/blocks/data-chart)

---

## vs Remotion

HyperFrames is inspired by Remotion but differs on one core bet: HTML authoring vs React components. Key differences:

- **No build step** — compositions play as-is in the browser
- **Library-clock animations** (GSAP, Anime.js) are frame-accurate vs wall-clock during render
- **Fully open source** (Apache 2.0) vs Remotion's source-available license with per-company thresholds

---

## Docs

[hyperframes.heygen.com](https://hyperframes.heygen.com/introduction) · [Quickstart](https://hyperframes.heygen.com/quickstart) · [Guides](https://hyperframes.heygen.com/guides/gsap-animation) · [API Reference](https://hyperframes.heygen.com/packages/core)
