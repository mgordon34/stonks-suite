from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    service_name: str = "data-service"
    environment: str = "local"
    debug: bool = False
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8001
    
    # Logging
    log_level: str = "INFO"
    
    # External services
    rabbitmq_url: str = "amqp://localhost:5672"
    postgres_url: str = "postgresql://user:pass@localhost:5432/trading"
    redis_url: str = "redis://localhost:6379"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
