# Foundation status

The v1 foundation intentionally returns safe placeholder responses for integrations that require persistent infrastructure or provider credentials. This keeps the API contract usable by Aither clients while avoiding fake authentication, AI responses, or stored app data.

The next implementation step is connecting real persistence, authentication, and the selected AI provider behind these stable API contracts.
