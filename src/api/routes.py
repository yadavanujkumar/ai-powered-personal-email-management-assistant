"""FastAPI routes for email management"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from ..services.email_service import EmailService
from ..services.ai_service import AIEmailService
from ..models.email_models import EmailMessage, EmailAnalysis, EmailConfig
from ..utils.config import get_email_config, get_email_password

router = APIRouter()


# Request/Response models
class EmailFetchRequest(BaseModel):
    folder: str = "INBOX"
    limit: int = 50
    unread_only: bool = False


class EmailSendRequest(BaseModel):
    to: List[str]
    subject: str
    body: str
    html: Optional[str] = None
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None


class AnalysisRequest(BaseModel):
    email_id: str


# Dependency to get email service
def get_email_service() -> EmailService:
    """Get configured email service"""
    config = get_email_config()
    password = get_email_password()
    
    if not config.email_address or not password:
        raise HTTPException(
            status_code=400,
            detail="Email configuration not set. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables."
        )
    
    return EmailService(config, password)


# Dependency to get AI service
def get_ai_service() -> AIEmailService:
    """Get AI service"""
    return AIEmailService()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Email Management Assistant"}


@router.post("/emails/fetch", response_model=List[EmailMessage])
async def fetch_emails(
    request: EmailFetchRequest,
    email_service: EmailService = Depends(get_email_service)
):
    """Fetch emails from specified folder"""
    try:
        emails = email_service.fetch_emails(
            folder=request.folder,
            limit=request.limit,
            unread_only=request.unread_only
        )
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        email_service.disconnect()


@router.post("/emails/send")
async def send_email(
    request: EmailSendRequest,
    email_service: EmailService = Depends(get_email_service)
):
    """Send an email"""
    try:
        success = email_service.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            html=request.html,
            cc=request.cc,
            bcc=request.bcc
        )
        if success:
            return {"status": "success", "message": "Email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        email_service.disconnect()


@router.post("/emails/analyze", response_model=EmailAnalysis)
async def analyze_email(
    email: EmailMessage,
    ai_service: AIEmailService = Depends(get_ai_service)
):
    """Analyze email using AI"""
    try:
        analysis = ai_service.analyze_email(email)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/emails/classify")
async def classify_email(
    email: EmailMessage,
    ai_service: AIEmailService = Depends(get_ai_service)
):
    """Classify email into category and priority"""
    try:
        classification = ai_service.classify_email(email)
        return classification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/emails/spam-check")
async def check_spam(
    email: EmailMessage,
    ai_service: AIEmailService = Depends(get_ai_service)
):
    """Check if email is spam"""
    try:
        is_spam = ai_service.detect_spam(email)
        return {"is_spam": is_spam, "email_id": email.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_config():
    """Get current email configuration (without password)"""
    try:
        config = get_email_config()
        return {
            "email_address": config.email_address,
            "imap_server": config.imap_server,
            "smtp_server": config.smtp_server,
            "imap_port": config.imap_port,
            "smtp_port": config.smtp_port,
            "use_ssl": config.use_ssl
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
