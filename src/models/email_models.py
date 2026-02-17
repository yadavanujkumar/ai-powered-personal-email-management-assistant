"""Email data models"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class EmailAddress(BaseModel):
    """Email address model"""
    name: Optional[str] = None
    email: EmailStr


class EmailMessage(BaseModel):
    """Email message model"""
    id: str
    subject: str
    sender: EmailAddress
    recipients: List[EmailAddress]
    cc: Optional[List[EmailAddress]] = []
    bcc: Optional[List[EmailAddress]] = []
    body: str
    html_body: Optional[str] = None
    date: datetime
    attachments: Optional[List[str]] = []
    is_read: bool = False
    is_starred: bool = False
    folder: str = "inbox"


class EmailClassification(BaseModel):
    """Email classification result"""
    category: str
    priority: str
    confidence: float
    tags: List[str] = []


class EmailAnalysis(BaseModel):
    """Complete email analysis"""
    email_id: str
    classification: EmailClassification
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    suggested_response: Optional[str] = None
    action_required: bool = False
    action_items: List[str] = []


class EmailConfig(BaseModel):
    """Email configuration"""
    email_address: EmailStr
    imap_server: str
    smtp_server: str
    imap_port: int = 993
    smtp_port: int = 587
    use_ssl: bool = True
