"""Configuration management utilities"""
import os
from typing import Optional
from dotenv import load_dotenv

from ..models.email_models import EmailConfig

# Load environment variables
load_dotenv()


def get_email_config() -> EmailConfig:
    """Get email configuration from environment variables"""
    return EmailConfig(
        email_address=os.getenv("EMAIL_ADDRESS", ""),
        imap_server=os.getenv("IMAP_SERVER", "imap.gmail.com"),
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        imap_port=int(os.getenv("IMAP_PORT", "993")),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        use_ssl=os.getenv("USE_SSL", "true").lower() == "true"
    )


def get_email_password() -> str:
    """Get email password from environment variables"""
    return os.getenv("EMAIL_PASSWORD", "")


def get_api_key(service: str) -> Optional[str]:
    """Get API key for external services"""
    return os.getenv(f"{service.upper()}_API_KEY")
