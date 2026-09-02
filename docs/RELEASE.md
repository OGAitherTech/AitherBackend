# Release checklist

- Run `pytest -q`.
- Confirm no secrets are committed.
- Review CORS origins.
- Set production environment variables.
- Configure database and authentication before enabling account features.
- Deploy with `fastapi run` or the included container configuration.
- Verify `/api/health` after deployment.
