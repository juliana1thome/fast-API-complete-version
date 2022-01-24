from pydantic import BaseSettings

# Also, it performs validation
class Settings(BaseSettings):
    db_passw: str
    db_username: str
    db_hostname: str
    db_name: str

    class Config:
        env_file = ".env"

# Creating an instance of settings class
settings = Settings()

