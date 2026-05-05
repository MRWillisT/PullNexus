# webapp-testing

An end-to-end web application testing skill covering UI behavior, API contracts, and regression coverage — focused on tests that catch real failures without being brittle.

## What it teaches

- Structure E2E tests around user flows, not implementation details
- Write API tests that validate contracts (status, shape, error handling)
- Design tests that are resilient to minor UI changes (prefer semantic selectors)
- Triage flaky tests and fix root causes rather than adding retries
- Decide what belongs in unit vs. integration vs. E2E layers

## When to use

- Building a test suite for a web app from scratch
- Diagnosing flaky or brittle tests
- Adding regression coverage after a bug
- Choosing between Playwright, Cypress, or API-level tests

## Example invocations

```
Help me write E2E tests for a login + dashboard flow.
My Playwright tests are flaky in CI but pass locally — what's wrong?
How should I structure tests for a REST API with auth?
```

## Format

ShareGPT JSONL — 7 conversation pairs covering UI testing, API testing, flakiness, and test strategy decisions.

## Tags

`testing`, `web`, `qa`, `regression`, `playwright`, `e2e`

## License

See `skill.json` for license details.
