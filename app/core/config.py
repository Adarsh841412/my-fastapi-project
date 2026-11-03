from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These variables will automatically look for matching names in your .env file
    DATABASE_URL: str
    secret_key:str 
    refresh_secret_key:str 
    algorithm:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES :int 
    REFRESH_TOKEN_EXPIRE_MINUTES :int 
    timeout:int 

    # Tells Pydantic to look for a file named .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single global instance of settings that you can import anywhere
settings = Settings()