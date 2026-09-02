# AitherBackend architecture

```text
Aither apps / website
        |
        v
   AitherBackend
        |
  +-----+----------------+
  |     |        |       |
 Auth  AI      Apps   Updates
  |     |        |       |
 Users  Provider Registry Distribution
        |
        v
   Database / cache / external services
```

The API layer is split into small FastAPI routers. Business logic belongs in `app/services`, data models belong in `app/models`, security helpers belong in `app/security`, and persistence integration belongs in `app/database.py`.

Provider secrets must remain on the backend and never be exposed to browser, mobile, or desktop clients.
