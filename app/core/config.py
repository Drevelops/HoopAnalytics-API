from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "HoopAnalytics API"
    VERSION: str = "0.1"

    DATABASE_URL: Optional[str] = None
    
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None

    SECRET_KEY: str = "secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    def get_database_url(self) -> str:
        # If Railway provides DATABASE_URL, use it directly
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # Otherwise, build from individual components (local development)
        if all([self.POSTGRES_SERVER, self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB, self.POSTGRES_PORT]):
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
        # Fallback for local development
        return "postgresql://username:password@localhost/hoopanalytics"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()