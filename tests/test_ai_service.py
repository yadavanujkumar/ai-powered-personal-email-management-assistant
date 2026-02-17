"""Tests for AI Email Service"""
import pytest
from datetime import datetime

from src.services.ai_service import AIEmailService
from src.models.email_models import EmailMessage, EmailAddress


@pytest.fixture
def ai_service():
    """Create AI service instance"""
    return AIEmailService()


@pytest.fixture
def sample_email():
    """Create a sample email for testing"""
    return EmailMessage(
        id="test-1",
        subject="Urgent: Project Deadline Tomorrow",
        sender=EmailAddress(name="John Doe", email="john@example.com"),
        recipients=[EmailAddress(email="test@example.com")],
        body="Please complete the project report by tomorrow. This is urgent and needs immediate attention.",
        date=datetime.now(),
        folder="inbox"
    )


def test_classify_email_work_category(ai_service, sample_email):
    """Test email classification for work category"""
    classification = ai_service.classify_email(sample_email)
    
    assert classification.category == "work"
    assert classification.priority in ["high", "medium", "low"]
    assert 0 <= classification.confidence <= 1


def test_classify_email_high_priority(ai_service, sample_email):
    """Test priority detection for urgent emails"""
    classification = ai_service.classify_email(sample_email)
    
    assert classification.priority == "high"


def test_sentiment_analysis_neutral(ai_service, sample_email):
    """Test sentiment analysis"""
    analysis = ai_service.analyze_email(sample_email)
    
    assert analysis.sentiment in ["positive", "negative", "neutral"]


def test_spam_detection_legitimate(ai_service, sample_email):
    """Test spam detection for legitimate email"""
    is_spam = ai_service.detect_spam(sample_email)
    
    assert not is_spam


def test_spam_detection_spam_email(ai_service):
    """Test spam detection for spam email"""
    spam_email = EmailMessage(
        id="spam-1",
        subject="CONGRATULATIONS YOU'VE WON!!!",
        sender=EmailAddress(email="spam@spammer.com"),
        recipients=[EmailAddress(email="test@example.com")],
        body="Click here now! Act now! Limited time offer! 100% free! You've won a million dollars!",
        date=datetime.now(),
        folder="inbox"
    )
    
    is_spam = ai_service.detect_spam(spam_email)
    
    assert is_spam


def test_action_items_extraction(ai_service):
    """Test action items extraction"""
    email = EmailMessage(
        id="action-1",
        subject="Tasks for this week",
        sender=EmailAddress(email="manager@example.com"),
        recipients=[EmailAddress(email="test@example.com")],
        body="Please review the document. Could you send the report by Friday? Need to schedule a meeting.",
        date=datetime.now(),
        folder="inbox"
    )
    
    analysis = ai_service.analyze_email(email)
    
    assert len(analysis.action_items) > 0


def test_email_summary_generation(ai_service, sample_email):
    """Test email summary generation"""
    analysis = ai_service.analyze_email(sample_email)
    
    assert analysis.summary is not None
    assert len(analysis.summary) > 0
    assert len(analysis.summary) <= 300


def test_suggested_response_generation(ai_service, sample_email):
    """Test suggested response generation"""
    analysis = ai_service.analyze_email(sample_email)
    
    assert analysis.suggested_response is not None
    assert len(analysis.suggested_response) > 0


def test_promotional_email_classification(ai_service):
    """Test classification of promotional emails"""
    promo_email = EmailMessage(
        id="promo-1",
        subject="50% Sale! Limited Time Offer",
        sender=EmailAddress(email="sales@store.com"),
        recipients=[EmailAddress(email="test@example.com")],
        body="Don't miss our amazing sale! Get 50% discount on all items. Offer ends soon!",
        date=datetime.now(),
        folder="inbox"
    )
    
    classification = ai_service.classify_email(promo_email)
    
    assert classification.category == "promotions"


def test_meeting_email_tagging(ai_service):
    """Test meeting email tagging"""
    meeting_email = EmailMessage(
        id="meeting-1",
        subject="Schedule Meeting for Next Week",
        sender=EmailAddress(email="colleague@example.com"),
        recipients=[EmailAddress(email="test@example.com")],
        body="Can we schedule a meeting next week to discuss the project? Please share your availability.",
        date=datetime.now(),
        folder="inbox"
    )
    
    classification = ai_service.classify_email(meeting_email)
    
    assert "meeting" in classification.tags
