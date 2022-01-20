from pydantic import BaseSettings

# Also, it performs validation
class Settings(BaseSettings):
    db_passw: str

    class Config:
        env_file = ".env"

# Creating an instance of settings class
settings = Settings()

