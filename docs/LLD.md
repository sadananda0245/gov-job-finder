# Low-Level Design

## Flask App Factory
`app.create_app` creates the Flask application, loads environment-specific configuration, initializes extensions, and registers blueprints.

## Extensions
`extensions.py` owns unbound extension instances:
- `db`
- `migrate`
- `login_manager`
- `csrf`

## Routes
Routes are grouped under `app/routes`. The initial home blueprint exposes `/` and `/health` until the dashboard and API routes are implemented.

## Testing
Tests use the `testing` configuration with an in-memory SQLite database and disabled CSRF.
