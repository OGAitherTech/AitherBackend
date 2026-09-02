# Security design

- Secrets are loaded from environment/secret storage rather than source files.
- The backend is the trust boundary for provider credentials.
- CORS is explicitly configured.
- Authentication endpoints are placeholders until a real identity provider is connected.
- Placeholder endpoints do not pretend that users are authenticated or that AI provider calls succeeded.
- Production deployment should use HTTPS and a restricted CORS allowlist.
