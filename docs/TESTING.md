# Testing

Run the test suite with:

```bash
pytest -q
```

The GitHub Actions workflow runs the same suite on pushes and pull requests. The tests cover root metadata, health, dependencies, CORS, auth validation/foundation behavior, AI endpoints, apps, updates, notifications, users, configuration, and OpenAPI availability.
