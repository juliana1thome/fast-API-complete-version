from pydantic import BaseModel, BaseSettings

# Also, it performs an validation
class Settings(BaseSettings):
    MY_DB_PASSW: int

    class Config:
        env_file = ".env"

# Creating an instance of settings class
settings = Settings()

