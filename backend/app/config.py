import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
REGISTRY_URL = os.getenv("REGISTRY_URL", "https://example.com/registry")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../data/wedding.db")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
