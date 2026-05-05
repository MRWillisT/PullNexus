# test-driven-development

A TDD workflow skill that teaches a model to design behavior-first code — writing the test, watching it fail, writing the minimum code to pass, then refactoring with confidence.

## What it teaches

- Write a failing test that captures the intended behavior before writing implementation
- Keep the red-green-refactor cycle tight (small steps, fast feedback)
- Use tests to drive interface design, not just verify existing code
- Distinguish unit, integration, and contract tests and when each belongs in the cycle
- Refactor safely: never change behavior and structure at the same time

## When to use

- Starting a new module, class, or function from scratch
- Adding a feature to existing code where the behavior isn't well-tested
- Refactoring a messy codebase incrementally
- Onboarding to a new codebase by writing characterization tests first

## Example invocations

```
I need to add a rate limiter — walk me through TDD for this.
Help me test-drive a user authentication flow in Python.
I want to refactor this class but it has no tests — where do I start?
```

## Format

ShareGPT JSONL — 7 conversation pairs covering TDD workflows across different languages and problem types.

## Tags

`testing`, `tdd`, `refactoring`, `development`, `behavior-driven`

## License

See `skill.json` for license details.
