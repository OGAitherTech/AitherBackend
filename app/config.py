from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AitherBackend"
    app_version: str = "2.4.0"
    environment: str = "development"
    # All GitHub Pages Aither project sites share the same web origin.
    cors_origins: str = "http://localhost:3000,http://localhost:5173,https://ogaithertech.github.io"
    database_url: str = "sqlite:///./aither.db"
    session_ttl_hours: int = 168
    secure_cookies: bool = True
    cookie_samesite: str = "none"
    app_url: str = "https://github.com/OGAitherTech/AitherTech"
    openrouter_api_key: str = ""
    openrouter_url: str = "https://openrouter.ai/api/v1/chat/completions"
    ai_model: str = "openai/gpt-oss-120b"
    ai_temperature: float = 0.7
    ai_timeout_seconds: float = 90.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def session_cookie_samesite(self) -> str:
        value = self.cookie_samesite.strip().lower()
        if value not in {"lax", "strict", "none"}:
            return "lax"
        if value == "none" and not self.secure_cookies:
            return "lax"
        return value


settings = Settings()
