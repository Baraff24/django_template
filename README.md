# Django template

Docker-first template with Django REST Framework, token authentication, verified email registration, Google/Apple OAuth, PostgreSQL, Redis, Celery and Caddy.

## Versions

Verified against the stable releases available on 2026-10-06:

| Component | Version |
| --- | --- |
| Python | 3.14.8 |
| Django | 6.1.2 |
| Django REST Framework | 3.18.1 |
| dj-rest-auth | 7.2.0 |
| django-allauth | 65.19.7 |
| Celery | 5.6.3 |
| PostgreSQL | 18.6 |
| Redis server | 8.10.2 |
| Redis Python client | 6.4.0 |
| Psycopg | 3.3.6 |
| Gunicorn / Uvicorn / Uvicorn worker | 26.2.0 / 0.54.0 / 0.4.0 |
| Caddy | 2.11.7 |

`requirements.in` contains direct dependencies. `requirements.txt` locks the entire dependency tree with hashes. The Redis client deliberately stays below 6.5 because Celery's Kombu dependency requires it; the Redis server has its own independent version. Allauth's `socialaccount` extra installs the OAuth and cryptography dependencies required by Google and Apple. Django uses Psycopg 3 and standard-library time zones; `psycopg2` and `pytz` are no longer needed.

Release references: [Django](https://www.djangoproject.com/download/), [DRF](https://www.django-rest-framework.org/community/release-notes/), [allauth](https://docs.allauth.org/en/latest/release-notes/recent.html), [official Docker image tags](https://github.com/docker-library/official-images/tree/master/library).

## Development

1. Copy `.env.example` to `.env` and replace the secret key and database password.
2. Run `docker compose up --build -d`.
3. Open <http://localhost:8000/admin/> or <http://localhost:8000/api/v1/schema/swagger-ui/>.
4. Create an admin account with `docker compose exec app python manage.py createsuperuser`.

Compose selects `config.settings.development` automatically. Application code and email templates are mounted from the workspace. The server uses Gunicorn with the maintained `uvicorn_worker.UvicornWorker`; restart the app after code changes (`docker compose restart app`). Dependencies are installed at image build time; rebuild after changing them.

Database and Redis health checks delay application/worker startup until both services are ready. Startup applies committed migrations and collects static files. Tests and migration generation are explicit development commands:

```sh
docker compose exec app python manage.py makemigrations
docker compose exec app python manage.py makemigrations --check --dry-run
docker compose exec app python manage.py test accounts
docker compose exec app python manage.py spectacular --validate --file /tmp/schema.yml
docker compose exec app ruff check .
```

Celery worker and Beat run in separate containers; run only one Beat instance per deployment. Beat's schedule is persisted in its own volume. PostgreSQL is exposed only on `127.0.0.1:5432` in development. Redis stays inside the Docker network.

## Production

Use a separate production `.env`. Set a unique `SECRET_KEY`, database credentials, `DJANGO_ALLOWED_HOSTS` to the public hostname, `DJANGO_CSRF_TRUSTED_ORIGINS` / `DJANGO_CORS_ALLOWED_ORIGINS` to the required HTTPS origins, and `DOMAIN` / `CADDY_EMAIL` for Caddy. Switch `EMAIL_BACKEND` to `django.core.mail.backends.smtp.EmailBackend` and configure working SMTP credentials.

```sh
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml exec app python manage.py check --deploy
```

Production always selects `config.settings.production` and disables debug, regardless of the `.env` debug value. HTTPS redirects, secure cookies and HSTS are enabled; use a domain whose subdomains also support HTTPS or configure `SECURE_HSTS_INCLUDE_SUBDOMAINS=False` and `SECURE_HSTS_PRELOAD=False` as appropriate. Caddy serves static/media files from the same paths used by Django, proxies other requests, and persists its certificates. PostgreSQL and Redis are not exposed on host ports. Redis enables AOF persistence for queued tasks/results.

## Environment configuration

See `.env.example` for the complete starting configuration. Database credentials and `SECRET_KEY` are required. Host lists, CORS and CSRF origins are comma-separated. `SITE_ID` defaults to `1`, matching Django's initial Site record; keep the existing site ID when upgrading an existing application and configure its domain/name in admin.

Development uses the console email backend by default. Email verification is mandatory: newly registered users must verify their email before logging in. Profile completion requires a verified, active account and all four fields (`first_name`, `last_name`, `telephone`, `gender`). User details/list additionally require a completed profile; only superusers can list users. User API responses exclude password hashes and privilege fields; email/status cannot be changed through the general profile endpoint.

OAuth credentials are optional for starting the template. Configure each provider either through `.env` or a SocialApp in Django admin, without duplicating it in both places. Apple also needs `APPLE_CERTIFICATE_KEY` containing the PEM private key, with literal `\n` between lines. Actual OAuth callbacks require valid credentials and provider-side redirect URL configuration.

Browser account pages live under `/api/v1/auth/account/`, separate from the REST endpoints, so email-confirmation redirects reach a working login page. The password-reset HTML email links to allauth's browser form; the REST reset endpoints remain available for API clients. Adapt the email link explicitly if a separate frontend handles password resets. `LOGIN_URL` and `LOGIN_REDIRECT_URL` are configurable environment variables. Old allauth callback paths under `/api/v1/auth/` remain accessible; configure new OAuth applications using callbacks under `/api/v1/auth/account/`.

## Updating dependencies

With [uv](https://docs.astral.sh/uv/) installed, update the direct pins in `requirements.in`, then regenerate the lock file:

```sh
uv pip compile requirements.in --python-version 3.14 --universal --generate-hashes --upgrade --output-file requirements.txt
docker compose build
docker compose up -d
docker compose exec app python -m pip check
docker compose exec app python manage.py check
docker compose exec app python manage.py makemigrations --check --dry-run
docker compose exec app python manage.py test accounts
```

Python 3.12 or later is required by Django 6.1; the supplied image and `.python-version` use Python 3.14.8. The Python container does not need compilers or PostgreSQL development headers because Psycopg uses its binary distribution.

## Upgrading an existing deployment

The old template used PostgreSQL 16 and `./data/postgresql`. The new configuration uses PostgreSQL 18 and a named volume mounted at `/var/lib/postgresql`, as required by the official PostgreSQL 18 image. The old data directory is left untouched and is **not** automatically imported. Before switching an existing deployment, take a logical database dump with the old PostgreSQL version, test restoring it into a fresh PostgreSQL 18 volume, then migrate the application and verify the data. Do not mount a PostgreSQL 16 data directory into PostgreSQL 18. Back up existing media and copy it into the new media volume as well.

The custom user model now has a committed initial migration. For a fresh database, ordinary `migrate` is enough. Existing deployments that generated migrations at startup must retain/reconcile their original migration files and history before upgrading; do not blindly replace them or fake migrations. `--fake-initial` is appropriate only after verifying that existing tables exactly match the initial migration.

Stopping services with `docker compose down` preserves named volumes. `docker compose down -v` deletes their contents.

## Verification

The update was tested on Linux ARM64 in the supplied Python 3.14.8 container with PostgreSQL 18.6 and Redis 8.10.2. Both Compose configurations started successfully. All 23 account/authentication tests passed, including registration, token login/logout, email verification, browser confirmation/reset links, profile completion and authorization checks. Dependency validation, migration drift checks, Ruff and OpenAPI validation passed. Production deployment checks reported no issues; Caddy served admin/account pages and static assets over HTTPS, and a real Celery task completed through Redis with its result retrieved from the backend.

SMTP delivery and Google/Apple provider callbacks still require real credentials and external configuration to validate. dj-rest-auth 7.2.0 currently emits an upstream allauth deprecation warning during password reset with username/email login; the password reset tests pass with the pinned versions.
