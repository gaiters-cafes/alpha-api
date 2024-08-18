from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    api_key: str
    log_level: str = "INFO"

    model_config = ConfigDict(env_file=".config")

settings = Settings()