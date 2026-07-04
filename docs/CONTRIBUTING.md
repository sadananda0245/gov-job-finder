# Contributing

## Setup
1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and adjust local values.
4. Run tests with `python -m pytest -q`.

## Guidelines
- Add tests for every behavior change.
- Keep dependencies pinned in `requirements.txt`.
- Use Flask blueprints for routes.
- Keep scraping logic in services, not route handlers.
- Store secrets in `.env`, never in tracked source files.
