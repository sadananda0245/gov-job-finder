# Database Design

## Initial Tables

### users
Stores authentication and profile ownership data.

### user_profiles
Stores eligibility attributes such as education, category, date of birth, location preferences, and experience.

### job_sources
Stores trusted official source metadata, including name, base URL, source type, and active status.

### jobs
Stores normalized job notifications, including title, department, location, application dates, source URL, and raw source metadata.

### job_eligibility_rules
Stores structured eligibility criteria extracted from notifications.

### saved_jobs
Stores jobs saved by users.

### scrape_runs
Stores scheduler execution metadata, status, counts, and errors.

## Migration Strategy
Use Flask-Migrate/Alembic for schema changes. Every model change should include a migration and a test covering the expected schema behavior.
