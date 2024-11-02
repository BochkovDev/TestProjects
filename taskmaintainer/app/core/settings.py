import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ('Settings', 'settings', 'APP_DIR', 'ROOT_DIR')

APP_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = APP_DIR.parent


class _DataBase(BaseSettings):
    HOST: str 
    PORT: int
    NAME: str
    USER: str
    PASSWORD: str

    @property
    def URL(self) -> str:
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}'
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(ROOT_DIR, '.env', '.db'),
    )


class _Redis(BaseSettings):
    HOST: str
    PORT: str
    DATABASE: int = 0
    PASSWORD: str

    @property
    def URL(self) -> str:
        return f'redis://{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(ROOT_DIR, '.env', '.redis'),
    )


class _Template(BaseSettings):
    TEMPLATE_DIR: Path = APP_DIR / 'templates'
    AUTO_RELOAD_TEMPLATES: bool

    model_config = SettingsConfigDict(
        env_file=os.path.join(ROOT_DIR, '.env', '.template'),
    )


class Settings(BaseSettings):
    SECRET_KEY: str
    STATIC_DIR: Path = APP_DIR / 'static'
    MEDIA_URL: Path = APP_DIR / 'media'
    TEMPLATE: _Template
    DATABASE: _DataBase
    REDIS: _Redis

    model_config = SettingsConfigDict(
        env_file=os.path.join(ROOT_DIR, '.env', '.env'),
    )
settings = Settings(
    TEMPLATE=_Template(),
    DATABASE=_DataBase(),
    REDIS=_Redis(),
)