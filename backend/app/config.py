import os
import secrets
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Generate a secure default secret key if not provided
_default_secret = secrets.token_hex(32)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
SECRET_KEY = os.getenv("SECRET_KEY", _default_secret)
REGISTRY_URL = os.getenv("REGISTRY_URL", "https://example.com/registry")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../data/wedding.db")

# Security warnings for production
def check_security_config():
    """Check for insecure configuration and log warnings."""
    warnings = []

    if not ADMIN_PASSWORD:
        warnings.append("ADMIN_PASSWORD is not set! Admin login is disabled.")
    elif len(ADMIN_PASSWORD) < 12:
        warnings.append("ADMIN_PASSWORD is less than 12 characters. Use a stronger password!")
    elif ADMIN_PASSWORD in ["admin123", "password", "admin", "12345678"]:
        warnings.append("ADMIN_PASSWORD is a common/weak password. Change it immediately!")

    if SECRET_KEY == _default_secret:
        warnings.append("SECRET_KEY not set - using auto-generated key. Set SECRET_KEY in .env for production!")

    for warning in warnings:
        logger.warning(f"SECURITY WARNING: {warning}")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Email settings (SMTP)
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Isabella & Joshua")
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
