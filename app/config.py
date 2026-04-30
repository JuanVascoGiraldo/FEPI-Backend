from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field
from pathlib import Path


ENV_FILE_PATH = Path(__file__).resolve().parent.parent / ".env"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore"
    )
    app_name: str = Field('FEPI API')
    port: int = Field(8000)
    workers: int = Field(1)
    reload: bool = Field(False)
    environment: str = Field('test')
    host: str = Field('127.0.0.1')
    mongodb_user: str = Field('')
    mongodb_password: str = Field('')
    mongodb_url: str = Field('mongodb://localhost:27017')
    mongodb_db: str = Field('fepi')
    JWT_ALGORITHM: str = Field('HS256')
    JWT_SECRET: str = Field('')

    def is_dev(self):
        return not (
            self.is_production() or
            self.is_stage() or
            self.is_qa() or
            self.is_test())

    def is_production(self) -> bool:
        return self.environment.lower() == 'prod'

    def is_stage(self) -> bool:
        return self.environment.lower() == 'stage'

    def is_qa(self) -> bool:
        return self.environment.lower() == 'qa'

    def is_test(self) -> bool:
        return self.environment.lower() == 'test'

    def get_open_api_path(self) -> str:
        if self.is_dev() or self.is_qa():
            return "/openapi.json"
        return ""

    def get_root_path(self) -> str:
        if self.is_dev() or self.is_qa() or self.is_test():
            return "/"
        return "/api"

    def get_reload(self) -> bool:
        return self.is_dev()


@lru_cache()
def get_settings():
    return Config()
