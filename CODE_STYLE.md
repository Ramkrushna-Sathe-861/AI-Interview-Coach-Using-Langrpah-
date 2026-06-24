Code Style Guidelines (Intermediate-friendly)

Goal
----
Keep code readable, testable, and approachable for intermediate engineers.

Rules
-----
- Prefer small functions with clear names over large classes when possible.
- Write concise docstrings for modules, functions, and classes.
- Use type hints for public functions and return values.
- Avoid heavy import-time side effects; use lazy initializers or factory functions.
- Keep functions short (single responsibility) and compose them.
- Use simple error handling with informative messages (raise HTTPException in endpoints).
- Keep configuration in `app.config` or environment variables; avoid hard-coded secrets.
- Add unit tests for core logic and mock external services (HTTP/OpenAI).

Examples
--------
- Use `ask_chat(profile, target_role, history)` instead of a large manager class for a single feature.
- Provide a thin `LLMService` wrapper but implement the logic in plain functions for readability.

Testing
-------
- Mock network calls (`requests.post`, `openai.ChatCompletion.create`) in tests.
- Prefer dependency injection for easier testing (pass in a custom client to the factory).

Formatting
----------
- Keep consistent spacing and naming.
- Run `black`/`ruff` locally if desired.


If you'd like, I can add a minimal test that follows these guidelines next.
