from collections.abc import Callable

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.use_cases.cv_analyze_use_case import CVAnalyzeUseCase


class S3Settings(BaseSettings):
    """S3 connection settings."""

    access_key: str
    secret_access_key: str
    endpoint_url: str
    bucket_name: str
    region_name: str

    model_config = SettingsConfigDict(env_prefix="S3_", env_file=".env", extra="ignore")


class RabbitMQSettings(BaseSettings):
    """RabbitMQ connection settings."""

    port: int
    host: str
    user: str
    password: str

    queue_use_case_map: dict[str, Callable] = {
        "cv-analyze-stream": CVAnalyzeUseCase,
    }

    timeout: float = 30

    model_config = SettingsConfigDict(env_prefix="RABBITMQ_", env_file=".env", extra="ignore")


class MongoSettings(BaseSettings):
    """MongoDB connection settings."""

    port: int
    host: str
    user: str
    password: str

    db_name: str
    cv_analysis_collection_name: str

    @property
    def url(self) -> str:
        return f"mongodb://{self.user}:{self.password}@{self.host}/{self.db_name}"

    model_config = SettingsConfigDict(env_prefix="MONGODB_", env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Application settings container."""

    s3_settings: S3Settings = S3Settings()
    rabbitmq_settings: RabbitMQSettings = RabbitMQSettings()
    mongo_settings: MongoSettings = MongoSettings()


settings = Settings()
