from pydantic import BaseSettings

# Also, it performs validation
class Settings(BaseSettings):
    ALGORITHM: str
    JWT_ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

    class Config:
        env_file = ".env"

# Creating an instance of settings class
settings = Settings()

