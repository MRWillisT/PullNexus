# Discord Bot Builder (with Local AI)

**Build a Discord bot powered by a local LLM running on Ollama — with per-user context, slash commands, and a configurable persona.**

This skill covers the complete stack: discord.py event handling, Ollama API integration, per-user conversation history, rate limiting, and slash command setup. Everything runs locally — no OpenAI required.

---

## Prerequisites

```bash
pip install discord.py requests python-dotenv
```

You'll also need:
- Ollama running locally: `ollama serve` + a model pulled (e.g. `ollama pull llama3.1:8b-instruct-q4_K_M`)
- A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)
- Bot invited to your server with `bot` + `applications.commands` scopes and `Send Messages`, `Read Message History`, `Use Slash Commands` permissions

---

## Project Structure

```
discord-bot/
├── .env                  # DISCORD_TOKEN, OLLAMA_MODEL
├── bot.py                # Main bot file
└── conversation.py       # Per-user context manager
```

---

## Environment Variables

```bash
# .env
DISCORD_TOKEN=your_discord_bot_token_here
OLLAMA_MODEL=llama3.1:8b-instruct-q4_K_M
OLLAMA_URL=http://localhost:11434/api/chat
MAX_HISTORY=10           # messages per user to keep in context
```

---

## conversation.py — Per-User Context Manager

```python
from collections import defaultdict, deque
from threading import Lock

class ConversationManager:
    """Thread-safe per-user conversation history with a rolling window."""

    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self._histories: dict[int, deque] = defaultdict(
            lambda: deque(maxlen=max_history)
        )
        self._lock = Lock()

    def add_message(self, user_id: int, role: str, content: str) -> None:
        with self._lock:
            self._histories[user_id].append({"role": role, "content": content})

    def get_history(self, user_id: int) -> list[dict]:
        with self._lock:
            return list(self._histories[user_id])

    def clear(self, user_id: int) -> None:
        with self._lock:
            self._histories[user_id].clear()
```

---

## bot.py — Complete Bot

```python
import os
import time
import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from conversation import ConversationManager

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_K_M")
MAX_HISTORY = int(os.environ.get("MAX_HISTORY", "10"))

# Rate limiting: max 1 message per user every N seconds
RATE_LIMIT_SECONDS = 3
_last_request: dict[int, float] = {}

SYSTEM_PROMPT = """You are Nexus, a helpful and friendly AI assistant living in Discord.
You are concise — responses are 1-3 paragraphs unless the user asks for more detail.
You are honest about being an AI. You don't pretend to be human.
You keep conversation history and remember context from earlier in the chat."""

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
conversations = ConversationManager(max_history=MAX_HISTORY)


def query_ollama(user_id: int, user_message: str) -> str:
    """Send a message to Ollama and return the response text."""
    conversations.add_message(user_id, "user", user_message)
    history = conversations.get_history(user_id)

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
        ],
        "stream": False,
        "temperature": 0.7,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        reply = response.json()["message"]["content"]
    except requests.Timeout:
        conversations.get_history(user_id).pop() if history else None
        return "Sorry, the model took too long to respond. Try again."
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

    conversations.add_message(user_id, "assistant", reply)
    return reply


def is_rate_limited(user_id: int) -> bool:
    now = time.monotonic()
    if user_id in _last_request:
        if now - _last_request[user_id] < RATE_LIMIT_SECONDS:
            return True
    _last_request[user_id] = now
    return False


@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user} | Synced slash commands")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Respond to direct mentions
    if bot.user in message.mentions:
        user_id = message.author.id

        if is_rate_limited(user_id):
            await message.reply("Please wait a moment before sending another message.")
            return

        # Strip the mention from the message content
        content = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not content:
            await message.reply("Yes? How can I help you?")
            return

        async with message.channel.typing():
            reply = query_ollama(user_id, content)

        # Discord messages have a 2000 character limit
        if len(reply) > 1990:
            # Split into chunks
            chunks = [reply[i:i+1990] for i in range(0, len(reply), 1990)]
            await message.reply(chunks[0])
            for chunk in chunks[1:]:
                await message.channel.send(chunk)
        else:
            await message.reply(reply)

    await bot.process_commands(message)


# Slash command: /ask
@tree.command(name="ask", description="Ask the AI a question")
@app_commands.describe(question="Your question for the AI")
async def ask_command(interaction: discord.Interaction, question: str):
    user_id = interaction.user.id

    if is_rate_limited(user_id):
        await interaction.response.send_message(
            "Please wait a moment before sending another message.", ephemeral=True
        )
        return

    await interaction.response.defer(thinking=True)
    reply = query_ollama(user_id, question)

    if len(reply) > 1990:
        chunks = [reply[i:i+1990] for i in range(0, len(reply), 1990)]
        await interaction.followup.send(chunks[0])
        for chunk in chunks[1:]:
            await interaction.followup.send(chunk)
    else:
        await interaction.followup.send(reply)


# Slash command: /clear — reset conversation history
@tree.command(name="clear", description="Clear your conversation history with the AI")
async def clear_command(interaction: discord.Interaction):
    conversations.clear(interaction.user.id)
    await interaction.response.send_message(
        "Your conversation history has been cleared.", ephemeral=True
    )


# Slash command: /model — show which model is running
@tree.command(name="model", description="Show which AI model is currently running")
async def model_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Running model: `{OLLAMA_MODEL}` via Ollama at `{OLLAMA_URL}`",
        ephemeral=True
    )


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
```

---

## Running the Bot

```bash
# Make sure Ollama is running
ollama serve &

# Start the bot
python bot.py
```

---

## Customizing the Persona

Edit `SYSTEM_PROMPT` in `bot.py`:

```python
SYSTEM_PROMPT = """You are Axel, a sarcastic but helpful developer assistant.
You give brutally honest feedback on code. You never sugarcoat.
You speak in short, punchy sentences. You use dark humor occasionally.
You are an expert in Python, JavaScript, and system design."""
```

---

## Switching Models

Edit `.env` or change `OLLAMA_MODEL` directly. All Ollama models work:

```bash
# Code-focused
OLLAMA_MODEL=qwen2.5-coder:7b-instruct-q4_K_M

# Reasoning-focused  
OLLAMA_MODEL=deepseek-r1:8b

# Smallest (for Raspberry Pi hosting)
OLLAMA_MODEL=phi3:mini
```

---

## Common Issues

| Problem | Fix |
|---|---|
| Bot doesn't respond | Check bot has `message_content` intent AND it's enabled in Discord Developer Portal |
| Slash commands not showing | Call `await tree.sync()` on startup; wait up to 1 hour for global sync, or sync to a specific guild for instant testing |
| Ollama timeout | Model too large for hardware — switch to a smaller/faster model or increase timeout |
| "ConnectionRefusedError" | Ollama isn't running — `ollama serve` |
| Bot responds to itself | `if message.author.bot: return` — already handled in the template |
| Rate limit too aggressive | Reduce `RATE_LIMIT_SECONDS` or use per-guild limits |

---

## Extending: Per-Channel System Prompts

```python
CHANNEL_PROMPTS: dict[int, str] = {
    123456789: "You are a Python tutor. Only answer Python questions.",
    987654321: "You are a creative writing partner. Be imaginative and elaborate.",
}

def get_system_prompt(channel_id: int) -> str:
    return CHANNEL_PROMPTS.get(channel_id, SYSTEM_PROMPT)
```

---

## Pairs Well With

- `ollama` — model management and API reference
- `model-selection-guide` — pick the right model for a Discord use case
- `prompt-engineering` — tune the persona system prompt

---

## License

CC0-1.0 — public domain, free to use for any purpose.
