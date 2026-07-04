# Government Job Finder

A Flask-based Government Job Finder that collects recruitment notifications from official sources and filters jobs based on user qualifications.

## Current Status

The project now has a runnable Flask foundation with:

- Application factory
- Environment-based configuration
- SQLAlchemy, Flask-Migrate, Flask-Login, and CSRF extension wiring
- Health and home JSON endpoints
- Smoke tests
- Starter product and architecture documentation

## Planned Features

- Official job notification scraper
- Eligibility checker
- AI-assisted job matching
- Dashboard
- PDF parser
- Email notifications
- Daily scheduler

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app app.py run
```

Visit `http://127.0.0.1:5000/health` to verify the app is running.

## Tests

```bash
python -m pytest -q
```
