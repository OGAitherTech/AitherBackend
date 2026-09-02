from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="AitherBackend",
    description="Central API backend for Aither Tech applications.",
    version="1.0.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "AitherBackend",
        "status": "online",
        "version": app.version,
        "docs": "/docs",
    }


@app.get("/api/health")
async def health() -> dict[str, object]:
    return {
        "status": "healthy",
        "service": "AitherBackend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/version")
async def version() -> dict[str, str]:
    return {"version": app.version}
