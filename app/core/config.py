from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "English Word Trainer"
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
