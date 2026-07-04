# High-Level Design

## Architecture
The application is a Flask web service with SQLAlchemy persistence, scheduled ingestion, and modular services for scraping, parsing, matching, and notifications.

## Main Components
- Web app: Flask application factory, blueprints, templates, and API endpoints.
- Database: SQLAlchemy models for users, jobs, sources, profiles, and scrape runs.
- Scraper services: fetch official pages, parse HTML/PDF notifications, and normalize data.
- Matching services: compare job requirements with user profiles.
- Scheduler: runs periodic ingestion tasks with APScheduler.
- Notifications: sends email or dashboard alerts for matching jobs.

## Data Flow
1. Scheduler requests active official sources.
2. Scraper fetches and parses notifications.
3. Repository layer upserts jobs and records scrape runs.
4. Matching service evaluates jobs against user profiles.
5. Web routes present jobs, matches, and saved searches.
