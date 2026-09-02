"""Database integration placeholder.

The v1 foundation intentionally has no persistent database yet. This module
provides a stable location for the database session/configuration layer when
storage is added.
"""


async def healthcheck() -> bool:
    return True
