from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    host: str
    user: str
    password: SecretStr
    port: int
    name: str
    min_pool: int
    max_pool: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'