from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    firebase_credentials_path: str = "./firebase-service-account.json"
    firebase_credentials_json: str = ""
    firebase_database_url: str = ""
    cors_origins: str = "http://localhost:4200"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
