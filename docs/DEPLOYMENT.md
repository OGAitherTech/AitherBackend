# Deployment

## Container

Build and run the backend with the included Dockerfile:

```bash
docker build -t aither-backend .
docker run --rm -p 8000:8000 aither-backend
```

## Render

The repository includes `render.yaml`. Set any production environment variables in the hosting provider's secret/environment configuration.

## Production notes

- Use HTTPS at the edge.
- Configure a production CORS allowlist instead of broad origins.
- Store provider credentials in a secret manager.
- Add persistent database and cache services before enabling account storage.
- Use `fastapi run` for production rather than the development server. FastAPI documents `fastapi run` as its production-mode command. citeturn0search9
