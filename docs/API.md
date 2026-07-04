# API Notes

The current application exposes a minimal smoke-test API while the main product routes are being built.

## `GET /`
Returns a JSON service payload with application status.

## `GET /health`
Returns `{ "status": "ok" }` for uptime checks.

## Planned APIs
- `GET /jobs` for listing jobs.
- `GET /jobs/<id>` for job detail.
- `POST /profile` for profile updates.
- `GET /matches` for personalized job matches.
- `POST /admin/sources` for source management.
