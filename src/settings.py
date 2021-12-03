from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "rpi"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
