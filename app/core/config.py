from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Word English Trainer Backend"
    API_PREFIX: str = "/api"
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"


settings = Settings()
