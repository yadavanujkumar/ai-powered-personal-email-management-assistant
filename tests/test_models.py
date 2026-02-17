"""Tests for email models"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from src.models.email_models import (
    EmailAddress,
    EmailMessage,
    EmailClassification,
    EmailConfig
)


def test_email_address_creation():
    """Test EmailAddress model creation"""
    email = EmailAddress(name="John Doe", email="john@example.com")
    
    assert email.name == "John Doe"
    assert email.email == "john@example.com"


def test_email_address_without_name():
    """Test EmailAddress without name"""
    email = EmailAddress(email="test@example.com")
    
    assert email.name is None
    assert email.email == "test@example.com"


def test_email_address_invalid_email():
    """Test EmailAddress with invalid email"""
    with pytest.raises(ValidationError):
        EmailAddress(email="invalid-email")


def test_email_message_creation():
    """Test EmailMessage creation"""
    email = EmailMessage(
        id="1",
        subject="Test Subject",
        sender=EmailAddress(email="sender@example.com"),
        recipients=[EmailAddress(email="recipient@example.com")],
        body="Test body",
        date=datetime.now(),
        folder="inbox"
    )
    
    assert email.id == "1"
    assert email.subject == "Test Subject"
    assert not email.is_read
    assert email.folder == "inbox"


def test_email_classification_creation():
    """Test EmailClassification creation"""
    classification = EmailClassification(
        category="work",
        priority="high",
        confidence=0.95,
        tags=["urgent", "meeting"]
    )
    
    assert classification.category == "work"
    assert classification.priority == "high"
    assert classification.confidence == 0.95
    assert len(classification.tags) == 2


def test_email_config_creation():
    """Test EmailConfig creation"""
    config = EmailConfig(
        email_address="test@gmail.com",
        imap_server="imap.gmail.com",
        smtp_server="smtp.gmail.com"
    )
    
    assert config.email_address == "test@gmail.com"
    assert config.imap_port == 993
    assert config.smtp_port == 587
    assert config.use_ssl
