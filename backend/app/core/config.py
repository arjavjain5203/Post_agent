
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Post Office Agent SaaS"
    
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_SSL: bool = True

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Construct async MySQL URL
        # We handle SSL context via connect_args in database.py, but the URL is standard.
        # Removing ?ssl=true from URL string as we handle it in engine creation
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_TO_A_STRONG_RANDOM_STRING" # Fallback if JWT_SECRET not found, but we prefer JWT_SECRET
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    @computed_field
    @property
    def JWT_SECRET_KEY(self) -> str:
        # Allow env var JWT_SECRET to override SECRET_KEY if present (Pydantic might do this auto if aliased, but explicit is fine)
        # Actually, let's just use the Pydantic Settings way.
        return self.SECRET_KEY

    # Field Encryption (AES-256)
    ENCRYPTION_KEY: str
    
    # Admin
    ADMIN_SECRET: Optional[str] = None

    # WhatsApp (Meta Graph API)
    WHATSAPP_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_ID: Optional[str] = None

    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_FROM_NUMBER: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra="ignore",
        # Allow JWT_SECRET to populate SECRET_KEY
        fields={
            'SECRET_KEY': {'validation_alias': 'JWT_SECRET'},
        }
    )

settings = Settings()
