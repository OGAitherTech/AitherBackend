# API examples

## Health

```bash
curl http://localhost:8000/api/health
```

## Version

```bash
curl http://localhost:8000/api/version
```

## AI foundation

```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Hello"}'
```
