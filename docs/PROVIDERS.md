# Provider integration

Provider-specific SDKs and credentials should be isolated from the API routers. Routers validate requests and call services; services communicate with providers; provider credentials are read from environment/secret storage.

This keeps Aither clients independent from the underlying provider and makes provider changes safer.
