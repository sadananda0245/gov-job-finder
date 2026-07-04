# Software Requirements Specification

## Purpose
Government Job Finder helps users discover official government job notifications and evaluate whether they match a user's qualifications.

## Users
- Job seeker: searches jobs, saves roles, and reviews eligibility.
- Administrator: manages trusted sources and monitors ingestion jobs.

## Functional Requirements
1. Collect job notifications only from configured official sources.
2. Store normalized job records with title, organization, location, dates, source URL, and eligibility criteria.
3. Allow users to define education, age, category, location, and experience preferences.
4. Match jobs to user profiles and explain eligibility results.
5. Provide a dashboard, saved jobs, and notification preferences.
6. Schedule daily source checks and record ingestion outcomes.

## Non-Functional Requirements
- Prefer source transparency over opaque ranking.
- Avoid scraping private or unofficial mirrors by default.
- Keep source URLs and timestamps for auditability.
- Make ingestion idempotent to avoid duplicate jobs.
