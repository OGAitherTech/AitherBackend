# AitherBackend

The central backend API for Aither Tech applications.

## 🌐 AitherTech site

**GitHub Pages:** https://ogaithertech.github.io/AitherTech/

The Pages site is the public AitherTech frontend. AitherBackend provides the API foundation behind future connected account and application features.

> **Important:** The backend is not claimed to be publicly deployed just because the frontend is on GitHub Pages. Live API connectivity depends on an actual backend deployment and matching CORS configuration.

## v2.0 account foundation

AitherBackend includes a persistent account/session foundation in addition to the existing FastAPI APIs.

### Included

- FastAPI API
- Persistent SQLite database by default
- Account registration
- Secure password hashing using Python's built-in `scrypt`
- Server-side opaque sessions
- HttpOnly session cookie
- Login and logout
- Session inspection with `GET /api/auth/session`
- Existing health, status, AI, apps, updates, notifications, config, and OpenAPI APIs
- Configurable CORS
- Environment-based settings
- Docker support
- Render deployment configuration
- Automated API tests
- GitHub Actions CI

## Authentication API

| Endpoint | Purpose |
| --- | --- |
| `POST /api/auth/register` | Create an account and start a session |
| `POST /api/auth/login` | Authenticate an account |
| `POST /api/auth/logout` | End the current session |
| `GET /api/auth/session` | Check the current session |
| `GET /api/users/me` | Existing user endpoint; authentication integration is being migrated to the session foundation |

Registration requires a name, email, and password of at least 8 characters.

## Database

The default database is a local SQLite file at `./aither.db`. Set `DATABASE_URL` to another supported SQLite URL when deploying or developing.

No users or fake production data are seeded into the repository.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000` and the interactive docs at `http://127.0.0.1:8000/docs`.

## Connecting the Pages frontend

For local development, configure the frontend to call the local API and send cookies with requests. For a deployed GitHub Pages frontend, the backend must be deployed at a real HTTPS URL and that URL must be added to the frontend configuration.

The backend CORS configuration must include the actual frontend origin. Do not put private API/provider keys in the Pages frontend.

## Docker

```bash
docker build -t aither-backend .
docker run --rm -p 8000:8000 aither-backend
```

## Security

Provider/API secrets stay server-side and must be supplied through environment variables or a secrets manager. Never put private provider keys into Aither frontend applications.

Session tokens are stored only as SHA-256 hashes in the database. Passwords are stored as salted `scrypt` hashes, never plaintext.

For production, enable secure cookies with `SECURE_COOKIES=true` and use HTTPS. Restrict `CORS_ORIGINS` to the actual Aither frontend origins.

## Roadmap

- Connect AitherTech account pages to the deployed backend
- PostgreSQL production adapter and migrations
- Email verification delivery
- Password reset delivery
- CSRF strategy for browser-based state-changing requests
- Stronger auth rate limiting
- Request logging and observability
- Production security headers
- Real update/version distribution
- Notifications delivery
- Expanded integration tests
- Production deployment and monitoring

Features on the roadmap are not represented as live services until they are implemented and deployed.
