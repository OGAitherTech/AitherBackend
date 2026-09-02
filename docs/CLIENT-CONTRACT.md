# Client contract

Aither clients can safely start against the foundation endpoints while the backend integrations are being implemented.

Important: a response such as `authenticated: false` or `success: false` is intentional when a provider is not configured. Clients should display a useful setup/error state instead of treating it as a successful login or AI response.
