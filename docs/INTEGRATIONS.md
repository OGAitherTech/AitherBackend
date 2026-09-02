# Integrations

AitherBackend is intentionally structured so external integrations can be added behind services without changing client-facing API contracts.

Planned integration boundaries:

- Identity provider -> `app/security` and `app/services`
- AI provider -> `app/services`
- Database -> `app/database.py`
- Cache/rate limiter -> `app/services`
- Update storage/CDN -> `app/services`
- Notifications -> `app/services`
