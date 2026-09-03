# Aither Notes API

This document reserves the backend contract used by Aither Notes.

The Aither Notes client expects a backend base URL and sync endpoints. Configure authentication and persistence in the backend before enabling production sync.

Required behavior:

- `GET /api/notes` returns a JSON object containing a `notes` array.
- `PUT /api/notes` accepts a JSON object containing a `notes` array and returns the saved notes.
- CORS must allow the Aither Notes GitHub Pages origin.
- Authentication should be handled with standard secure session/token mechanisms; never put a private server secret in the frontend.
