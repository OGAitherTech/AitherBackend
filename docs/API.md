# AitherBackend API

## Health

`GET /api/health`

Returns basic service health and a UTC timestamp.

`GET /api/health/dependencies`

Returns the state of configured backend dependencies.

## Service

`GET /api/status`

Returns the service operational state.

`GET /api/version`

Returns the running API version.

## AI

`GET /api/ai/models`

Lists models exposed by the configured AI provider.

`POST /api/ai/chat`

Accepts a chat message and optional model. The provider integration is intentionally not enabled in the foundation release.

## Apps

`GET /api/apps`

Lists registered Aither applications.

`POST /api/apps`

Accepts an app name, version, and platform for future registration storage.

## Authentication and users

`POST /api/auth/login`

Authentication foundation endpoint.

`POST /api/auth/logout`

Logout foundation endpoint.

`GET /api/users/me`

Returns the current authenticated user when an authentication provider is configured.

## Updates and notifications

`GET /api/updates`

Lists available application updates.

`GET /api/notifications`

Lists notifications for the authenticated user when notification storage is configured.

## Public configuration

`GET /api/config`

Returns non-secret application configuration intended for clients.
