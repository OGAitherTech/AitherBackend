# Aither clients

AitherBackend is designed to serve browser, iPhone/mobile, desktop, and other Aither Tech clients through the same HTTPS API.

Clients should call the public API endpoints and never receive private provider credentials.

Recommended client flow:

```text
Aither app
   -> HTTPS
AitherBackend
   -> authenticated service
Database / AI provider / update storage
```
