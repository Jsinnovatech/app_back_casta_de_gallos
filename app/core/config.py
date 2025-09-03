from decouple import config
from typing import List

class Settings:
    # 🔐 JWT Configuration
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 🗄️ Database
    DATABASE_URL: str = config(
        "DATABASE_URL", 
        default="postgresql://user:password@host:port/database"
    )
    
    # 📸 Cloudinary
    CLOUDINARY_CLOUD_NAME: str = config("CLOUDINARY_CLOUD_NAME", default="your_cloud_name")
    CLOUDINARY_API_KEY: str = config("CLOUDINARY_API_KEY", default="your_api_key")
    CLOUDINARY_API_SECRET: str = config("CLOUDINARY_API_SECRET", default="your_api_secret")
    
    # 📧 SendGrid Email Service
    SENDGRID_API_KEY: str = config("SENDGRID_API_KEY", default="your_sendgrid_api_key")
    SENDGRID_FROM_EMAIL: str = config("SENDGRID_FROM_EMAIL", default="your@email.com")
    SENDGRID_FROM_NAME: str = config("SENDGRID_FROM_NAME", default="Your App Name")
    
    # 🌐 CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 🔄 Environment
    ENVIRONMENT: str = config("ENVIRONMENT", default="local")

settings = Settings()