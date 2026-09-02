# Operations

Check these endpoints after deployment:

```text
GET /healthz
GET /api/health
GET /api/status
GET /api/version
```

If `/healthz` fails, treat the service as unavailable. If `/api/health` or `/api/status` reports a problem, inspect application logs and dependencies.
