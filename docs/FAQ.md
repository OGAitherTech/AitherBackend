# FAQ

## Does the backend have real AI yet?

Not in the foundation release. The `/api/ai/chat` contract is present, but it intentionally reports that the provider is not configured.

## Does login work yet?

Not yet. The authentication endpoints are a safe foundation until a real identity provider and persistent user store are connected.

## Can Aither apps use this now?

Yes. They can use the health, version, status, config, and documented foundation endpoints while the real services are added.
