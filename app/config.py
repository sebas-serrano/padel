# BIEN en Pydantic 2
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_MYSQL_PATH: str
    ADMIN_TOKEN: str = "Bearer <default_token>"

    # Así activas la carga de variables desde .env
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
