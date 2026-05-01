# pytest-and-testing

Practical pytest patterns for Python developers — from "I've never written tests" all the way to mocking exchange APIs, async testing, and measuring coverage. This skill teaches how to test real-world applications, not just trivial examples.

## What This Skill Covers

- **Getting started** — where to start when you've never written tests before
- **Mocking external APIs** — how to prevent tests from making real network calls or touching real money
- **Fixtures and conftest.py** — when to use them vs. inline setup, and why they matter
- **Parametrize** — testing multiple cases without duplicating test code
- **Async testing** — how to test `asyncio`-based code with `pytest-asyncio`
- **Coverage** — measuring and improving test coverage
- **Integration vs unit tests** — knowing when each is appropriate

## Who Should Use This Skill

Self-taught developers or "vibe coders" who build real applications but haven't yet established a testing practice. Especially useful for anyone building bots, scrapers, or tools that interact with external services (APIs, databases, exchanges).

## Example Prompts

- "I've never written tests before. Where do I start testing a trading bot?"
- "How do I mock the Binance API so tests don't make real calls?"
- "What are pytest fixtures and conftest.py? When should I use them?"
- "How do I test my async bot code?"
- "How do I measure and improve code coverage?"

## Usage

```bash
pullnexus pull pytest-and-testing
```

## License

CC0-1.0 — public domain.
