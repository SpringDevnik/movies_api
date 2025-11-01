import os.path
from typing import Mapping

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

_DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class _SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_DOTENV,
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )


class _ApiSettings(_SettingsBase):
    AUTH_API_BASE_URL: str = "https://auth.dev-cinescope.coconutqa.ru/"
    MOVIES_API_BASE_URL: str = "https://api.dev-cinescope.coconutqa.ru/"
    SUPER_ADMIN_LOGIN: SecretStr
    SUPER_ADMIN_PASSWORD: SecretStr
    BASE_HEADERS: Mapping[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


class _DbSettings(_SettingsBase):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USERNAME: SecretStr
    DB_PASSWORD: SecretStr


class _Settings(_SettingsBase):
    api: _ApiSettings = _ApiSettings()
    db: _DbSettings = _DbSettings()


settings = _Settings()
