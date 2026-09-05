from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AitherBackend"
    app_version: str = "2.6.1"
    environment: str = "development"
    cors_origins: str = "http://localhost:3000,http://localhost:5173,https://ogaithertech.github.io"
    database_url: str = "sqlite:///./aither.db"
    session_ttl_hours: int = 168
    secure_cookies: bool = True
    cookie_samesite: str = "none"
    app_url: str = "https://github.com/OGAitherTech/AitherTech"
    verification_base_url: str = "https://aitherbackend.onrender.com"
    # Resend SMTP defaults. Keep the API key/password in the hosting environment, never in Git.
    smtp_host: str = "smtp.resend.com"
    smtp_port: int = 587
    smtp_username: str = "resend"
    smtp_password: str = ""
    smtp_from_email: str = "onboarding@resend.dev"
    smtp_from_name: str = "Aither"
    verification_token_hours: int = 24
    openrouter_api_key: str = ""
    openrouter_url: str = "https://openrouter.ai/api/v1/chat/completions"
    ai_model: str = "openai/gpt-oss-120b"
    ai_temperature: float = 0.7
    ai_timeout_seconds: float = 90.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        required_origins = {
            "https://ogaithertech.github.io",
            "http://localhost:3000",
            "http://localhost:5173",
        }
        for origin in required_origins:
            if origin not in origins:
                origins.append(origin)
        return origins

    @property
    def session_cookie_samesite(self) -> str:
        value = self.cookie_samesite.strip().lower()
        if value not in {"lax", "strict", "none"}:
            return "lax"
        if value == "none" and not self.secure_cookies:
            return "lax"
        return value


settings = Settings()
