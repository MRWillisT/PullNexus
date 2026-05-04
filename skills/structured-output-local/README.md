# Structured Output (Local)

**Get reliable JSON and typed data from local LLMs — without an API wrapper.**

Cloud APIs like OpenAI have a `response_format: json_object` option. Local models don't always have that guarantee. This skill teaches the full stack: schema injection in the system prompt, retry-validate loops, and Python code patterns that work reliably with Ollama, llama.cpp, and LM Studio.

---

## Why Local Models Fail at JSON

- No guaranteed `json_mode` enforcement at the API level
- Temperature too high → invalid tokens in JSON
- No schema → model invents its own structure
- No example → model wraps output in prose
- Long context → model forgets format rules

All of these are fixable with prompt engineering and a retry loop.

---

## Step 1: System Prompt with Schema Injection

Always inject the exact schema into the system prompt. Never describe it in prose.

```
You are a data extraction assistant.

You MUST respond with ONLY valid JSON. No prose. No explanation. No markdown code fences.
Do not include any text before or after the JSON.

The JSON must match this exact schema:
{
  "name": "<string>",
  "confidence": <number between 0 and 1>,
  "tags": ["<string>", ...],
  "summary": "<string, max 100 words>"
}

If you cannot extract a field, use null for that field. Never omit fields.
```

Key rules:
- Use `<type>` placeholders inline in the schema to signal expected types
- Say "No prose. No explanation. No markdown." explicitly — models often wrap JSON in ```json fences
- Always say what to do when data is missing (`null`) rather than leaving it undefined

---

## Step 2: Low Temperature for JSON

JSON is a precision task. Set temperature low:

```python
payload = {
    "model": "llama3.1:8b-instruct-q4_K_M",
    "messages": [...],
    "temperature": 0.1,   # <-- critical
    "stream": False
}
```

---

## Step 3: Parse and Validate

Parse the response and validate against your schema before trusting it.

```python
import json
import re

def extract_json(text: str) -> dict | None:
    """Strip prose/fences and parse JSON from model output."""
    # Remove markdown fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
```

---

## Step 4: Retry-Validate Loop

Wrap the entire call in a retry loop. For most models, Q4+ at temperature 0.1, this succeeds on the first try 95%+ of the time. The loop is insurance.

```python
import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
SCHEMA = {
    "name": "<string>",
    "confidence": "<number 0-1>",
    "tags": ["<string>"],
    "summary": "<string>"
}

SYSTEM_PROMPT = f"""You are a data extraction assistant.
Respond ONLY with valid JSON. No prose. No markdown fences.
Schema:
{json.dumps(SCHEMA, indent=2)}
If a field cannot be filled, use null. Never omit fields."""

def extract_structured(text: str, max_retries: int = 3) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Extract information from this text:\n\n{text}"}
    ]

    for attempt in range(max_retries):
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3.1:8b-instruct-q4_K_M",
            "messages": messages,
            "temperature": 0.1,
            "stream": False
        })
        response.raise_for_status()
        content = response.json()["message"]["content"]

        # Strip fences
        content = re.sub(r"^```(?:json)?\s*", "", content.strip())
        content = re.sub(r"\s*```$", "", content.strip())

        try:
            data = json.loads(content)
            # Validate required fields
            required = {"name", "confidence", "tags", "summary"}
            if required.issubset(data.keys()):
                return data
        except json.JSONDecodeError:
            pass

        # Add correction message for retry
        messages.append({"role": "assistant", "content": content})
        messages.append({
            "role": "user",
            "content": "That was not valid JSON. Try again. Output ONLY the JSON object, nothing else."
        })

    raise ValueError(f"Failed to get valid JSON after {max_retries} attempts")
```

---

## Using Ollama's Native JSON Mode

Ollama supports a `format: "json"` parameter that constrains tokens to valid JSON. Use it when available:

```python
response = requests.post(OLLAMA_URL, json={
    "model": "llama3.1:8b-instruct-q4_K_M",
    "messages": messages,
    "format": "json",   # <-- Ollama native JSON mode
    "temperature": 0.1,
    "stream": False
})
```

This doesn't enforce your specific schema, but it guarantees valid JSON syntax. Combine it with schema injection in the system prompt for best results.

---

## Schema Patterns

### Flat object
```json
{"field": "value", "count": 0, "flag": true}
```

### Nested object
```json
{"person": {"name": "string", "age": 0}, "active": true}
```

### Array of objects
```json
[{"id": 0, "label": "string"}]
```
For arrays, also say: "Respond with a JSON array. First character must be `[`."

### Enum fields
```json
{"status": "one of: pending|active|closed"}
```

---

## Pydantic Validation (Optional)

If you're already using Pydantic:

```python
from pydantic import BaseModel, ValidationError
from typing import Optional

class Extraction(BaseModel):
    name: Optional[str]
    confidence: float
    tags: list[str]
    summary: Optional[str]

try:
    result = Extraction(**raw_dict)
except ValidationError as e:
    # Log and retry
    print(e.errors())
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| JSON is wrapped in ```json fences | Strip with regex before parsing |
| Extra text before/after JSON | Use regex to find `{...}` or `[...]` block |
| Fields missing | Add "Never omit fields. Use null if unknown." to system prompt |
| Wrong types (number as string) | Specify types explicitly: `"score": <integer>` |
| Inconsistent array length | Add "Always include all items, even if empty list `[]`" |
| Nested JSON fails | Show a concrete filled example in the system prompt |

---

## Pairs Well With

- `prompt-engineering` — master format control first
- `small-model-reasoning-boost` — improve reasoning before extraction
- `spec-first-development` — design your schema before coding the pipeline

---

## License

CC0-1.0 — public domain, free to use for any purpose.
