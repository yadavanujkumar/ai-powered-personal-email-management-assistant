"""AI service for email classification and analysis"""
import re
from typing import List
import logging
from datetime import datetime

from ..models.email_models import (
    EmailMessage, 
    EmailClassification, 
    EmailAnalysis
)

logger = logging.getLogger(__name__)


class AIEmailService:
    """Service for AI-powered email analysis"""
    
    # Categories for email classification
    CATEGORIES = {
        "work": ["meeting", "project", "deadline", "presentation", "report", "task"],
        "personal": ["family", "friend", "birthday", "invitation", "party"],
        "finance": ["invoice", "payment", "bank", "transaction", "billing", "receipt"],
        "promotions": ["sale", "discount", "offer", "deal", "promo", "advertise"],
        "newsletters": ["newsletter", "digest", "update", "subscription"],
        "social": ["facebook", "twitter", "linkedin", "instagram", "notification"],
        "spam": ["unsubscribe", "click here", "act now", "limited time", "winner"]
    }
    
    # Priority keywords
    URGENT_KEYWORDS = [
        "urgent", "asap", "immediately", "critical", "emergency",
        "important", "deadline", "today", "now", "priority"
    ]
    
    def __init__(self):
        """Initialize AI service"""
        logger.info("AI Email Service initialized")
    
    def classify_email(self, email: EmailMessage) -> EmailClassification:
        """Classify email into category and priority"""
        # Combine subject and body for analysis
        text = f"{email.subject} {email.body}".lower()
        
        # Determine category
        category_scores = {}
        for category, keywords in self.CATEGORIES.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        # Get category with highest score
        category = max(category_scores, key=category_scores.get)
        max_score = category_scores[category]
        
        # If no clear category, mark as general
        if max_score == 0:
            category = "general"
            confidence = 0.5
        else:
            # Calculate confidence based on score
            total_keywords = sum(len(keywords) for keywords in self.CATEGORIES.values())
            confidence = min(max_score / 10, 1.0)
        
        # Determine priority
        priority = self._determine_priority(email, text)
        
        # Extract tags
        tags = self._extract_tags(text)
        
        return EmailClassification(
            category=category,
            priority=priority,
            confidence=confidence,
            tags=tags
        )
    
    def _determine_priority(self, email: EmailMessage, text: str) -> str:
        """Determine email priority"""
        # Check for urgent keywords
        urgent_count = sum(1 for keyword in self.URGENT_KEYWORDS if keyword in text)
        
        # Check if sender is in subject (might be a reply)
        is_reply = text.startswith("re:") or text.startswith("fwd:")
        
        # Check recency
        time_diff = datetime.now() - email.date
        is_recent = time_diff.total_seconds() < 3600  # Less than 1 hour
        
        # Determine priority
        if urgent_count >= 2 or (urgent_count >= 1 and is_recent):
            return "high"
        elif is_reply or urgent_count == 1:
            return "medium"
        else:
            return "low"
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from email"""
        tags = []
        
        # Common action tags
        if any(word in text for word in ["meeting", "schedule", "calendar"]):
            tags.append("meeting")
        if any(word in text for word in ["deadline", "due", "submit"]):
            tags.append("action-required")
        if any(word in text for word in ["invoice", "payment", "pay"]):
            tags.append("payment")
        if any(word in text for word in ["question", "?", "help", "assist"]):
            tags.append("needs-response")
        
        return tags
    
    def analyze_email(self, email: EmailMessage) -> EmailAnalysis:
        """Perform complete email analysis"""
        # Classify email
        classification = self.classify_email(email)
        
        # Generate summary
        summary = self._generate_summary(email)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(email)
        
        # Generate suggested response
        suggested_response = self._suggest_response(email, classification)
        
        # Check if action is required
        action_required = "action-required" in classification.tags or classification.priority == "high"
        
        # Extract action items
        action_items = self._extract_action_items(email)
        
        return EmailAnalysis(
            email_id=email.id,
            classification=classification,
            summary=summary,
            sentiment=sentiment,
            suggested_response=suggested_response,
            action_required=action_required,
            action_items=action_items
        )
    
    def _generate_summary(self, email: EmailMessage) -> str:
        """Generate email summary"""
        # Simple extractive summary - first 2 sentences
        body = email.body.strip()
        sentences = re.split(r'[.!?]+', body)
        summary_sentences = [s.strip() for s in sentences[:2] if s.strip()]
        
        if not summary_sentences:
            return f"Email from {email.sender.email} regarding: {email.subject}"
        
        summary = ". ".join(summary_sentences) + "."
        if len(summary) > 200:
            summary = summary[:197] + "..."
        
        return summary
    
    def _analyze_sentiment(self, email: EmailMessage) -> str:
        """Analyze email sentiment"""
        text = f"{email.subject} {email.body}".lower()
        
        positive_words = [
            "thank", "appreciate", "great", "excellent", "good", 
            "happy", "pleased", "wonderful", "amazing", "love"
        ]
        negative_words = [
            "unfortunately", "sorry", "apologize", "issue", "problem",
            "concern", "disappointed", "frustrated", "urgent", "critical"
        ]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _suggest_response(
        self, 
        email: EmailMessage, 
        classification: EmailClassification
    ) -> str:
        """Suggest response based on email content"""
        templates = {
            "meeting": f"Thank you for your email. I'm available for a meeting. Could you please share some time slots that work for you?",
            "action-required": f"Thank you for bringing this to my attention. I'll review this and get back to you soon.",
            "payment": f"Thank you for the invoice. I'll process the payment and confirm once complete.",
            "needs-response": f"Thank you for your question. Let me look into this and I'll get back to you with more details."
        }
        
        # Check tags for appropriate template
        for tag in classification.tags:
            if tag in templates:
                return templates[tag]
        
        # Default response
        return f"Thank you for your email regarding '{email.subject}'. I'll review this and respond accordingly."
    
    def _extract_action_items(self, email: EmailMessage) -> List[str]:
        """Extract action items from email"""
        text = email.body.lower()
        action_items = []
        
        # Look for common action patterns
        action_patterns = [
            r"please\s+(.+?)(?:\.|$)",
            r"could you\s+(.+?)(?:\.|$)",
            r"can you\s+(.+?)(?:\.|$)",
            r"need to\s+(.+?)(?:\.|$)",
            r"should\s+(.+?)(?:\.|$)",
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text)
            for match in matches[:3]:  # Limit to 3 items
                if len(match.strip()) > 10 and len(match.strip()) < 100:
                    action_items.append(match.strip())
        
        return action_items[:5]  # Return max 5 action items
    
    def detect_spam(self, email: EmailMessage) -> bool:
        """Detect if email is likely spam"""
        text = f"{email.subject} {email.body}".lower()
        
        spam_indicators = 0
        
        # Check for spam keywords
        spam_keywords = [
            "congratulations you've won",
            "click here now",
            "act now",
            "limited time offer",
            "100% free",
            "no credit card",
            "dear friend",
            "nigerian prince"
        ]
        
        spam_indicators += sum(1 for keyword in spam_keywords if keyword in text)
        
        # Check for excessive punctuation
        if text.count("!") > 3 or text.count("?") > 3:
            spam_indicators += 1
        
        # Check for all caps subject
        if email.subject.isupper() and len(email.subject) > 10:
            spam_indicators += 1
        
        # Check for suspicious links
        if text.count("http") > 3:
            spam_indicators += 1
        
        return spam_indicators >= 3
