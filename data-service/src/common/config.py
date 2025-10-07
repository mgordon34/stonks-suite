import logging
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "data-service"
    environment: str = "local"
    debug: bool = False

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8001

    # Logging
    log_level: int = logging.DEBUG

    # External services
    rabbitmq_url: str = "amqp://localhost:5672"
    postgres_url: str = "postgresql://postgres:stonks@db:5432/stonks"
    redis_url: str = "redis://localhost:6379"
    echo_sql: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
