# Error handling direction

The API foundation uses FastAPI/Pydantic validation for malformed request bodies and parameters. Integration failures should be converted into stable JSON error responses in the service layer rather than leaking provider-specific credentials or internal stack traces.

Future production error responses should include a request ID for support and observability.
