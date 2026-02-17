"""Email service for IMAP/SMTP operations"""
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime
from typing import List, Optional
import logging

from ..models.email_models import EmailMessage, EmailAddress, EmailConfig

logger = logging.getLogger(__name__)


class EmailService:
    """Service for managing email operations"""
    
    def __init__(self, config: EmailConfig, password: str):
        """Initialize email service with configuration"""
        self.config = config
        self.password = password
        self.imap_connection = None
        self.smtp_connection = None
    
    def connect_imap(self) -> None:
        """Connect to IMAP server"""
        try:
            if self.config.use_ssl:
                self.imap_connection = imaplib.IMAP4_SSL(
                    self.config.imap_server, 
                    self.config.imap_port
                )
            else:
                self.imap_connection = imaplib.IMAP4(
                    self.config.imap_server, 
                    self.config.imap_port
                )
            
            self.imap_connection.login(
                self.config.email_address, 
                self.password
            )
            logger.info("Successfully connected to IMAP server")
        except Exception as e:
            logger.error(f"Failed to connect to IMAP: {e}")
            raise
    
    def connect_smtp(self) -> None:
        """Connect to SMTP server"""
        try:
            self.smtp_connection = smtplib.SMTP(
                self.config.smtp_server, 
                self.config.smtp_port
            )
            self.smtp_connection.starttls()
            self.smtp_connection.login(
                self.config.email_address, 
                self.password
            )
            logger.info("Successfully connected to SMTP server")
        except Exception as e:
            logger.error(f"Failed to connect to SMTP: {e}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from email servers"""
        if self.imap_connection:
            try:
                self.imap_connection.logout()
            except Exception:
                pass
        if self.smtp_connection:
            try:
                self.smtp_connection.quit()
            except Exception:
                pass
    
    def fetch_emails(
        self, 
        folder: str = "INBOX", 
        limit: int = 50,
        unread_only: bool = False
    ) -> List[EmailMessage]:
        """Fetch emails from specified folder"""
        if not self.imap_connection:
            self.connect_imap()
        
        try:
            self.imap_connection.select(folder)
            
            # Search criteria
            search_criteria = "UNSEEN" if unread_only else "ALL"
            _, message_numbers = self.imap_connection.search(None, search_criteria)
            
            emails = []
            for num in message_numbers[0].split()[-limit:]:
                _, msg_data = self.imap_connection.fetch(num, "(RFC822)")
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Parse email
                parsed_email = self._parse_email(email_message, num.decode(), folder)
                emails.append(parsed_email)
            
            return emails
        except Exception as e:
            logger.error(f"Failed to fetch emails: {e}")
            raise
    
    def _parse_email(self, email_message, email_id: str, folder: str = "inbox") -> EmailMessage:
        """Parse email message to EmailMessage model"""
        # Decode subject
        subject, encoding = decode_header(email_message["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        
        # Parse sender
        sender_str = email_message.get("From", "")
        sender = self._parse_email_address(sender_str)
        
        # Parse recipients
        to_str = email_message.get("To", "")
        recipients = [self._parse_email_address(addr) for addr in to_str.split(",")]
        
        # Parse date
        date_str = email_message.get("Date", "")
        try:
            email_date = email.utils.parsedate_to_datetime(date_str)
        except Exception:
            email_date = datetime.now()
        
        # Get body
        body = ""
        html_body = None
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True).decode()
        else:
            body = email_message.get_payload(decode=True).decode()
        
        return EmailMessage(
            id=email_id,
            subject=subject,
            sender=sender,
            recipients=recipients,
            body=body,
            html_body=html_body,
            date=email_date,
            folder=folder
        )
    
    def _parse_email_address(self, address_str: str) -> EmailAddress:
        """Parse email address string"""
        try:
            name, email_addr = email.utils.parseaddr(address_str)
            return EmailAddress(name=name if name else None, email=email_addr)
        except Exception:
            return EmailAddress(email=address_str)
    
    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        html: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """Send email"""
        if not self.smtp_connection:
            self.connect_smtp()
        
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.config.email_address
            msg["To"] = ", ".join(to)
            
            if cc:
                msg["Cc"] = ", ".join(cc)
            if bcc:
                msg["Bcc"] = ", ".join(bcc)
            
            # Add body
            msg.attach(MIMEText(body, "plain"))
            if html:
                msg.attach(MIMEText(html, "html"))
            
            # Send
            recipients = to + (cc or []) + (bcc or [])
            self.smtp_connection.send_message(msg, to_addrs=recipients)
            logger.info(f"Successfully sent email to {to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
