# AI-Powered Personal Email Management Assistant

An intelligent email management system that leverages AI to automatically classify, prioritize, and manage your emails. Built with FastAPI, Python, and Docker for easy deployment and scalability.

## 🚀 Features

### Email Operations
- **IMAP/SMTP Integration**: Connect to any email provider supporting IMAP/SMTP protocols
- **Fetch Emails**: Retrieve emails from specific folders with filtering options
- **Send Emails**: Send emails with support for CC, BCC, and HTML content
- **Multiple Folder Support**: Work with different email folders (inbox, sent, drafts, etc.)

### AI-Powered Intelligence
- **Smart Classification**: Automatically categorize emails (work, personal, finance, promotions, newsletters, social, spam)
- **Priority Detection**: Identify urgent and high-priority emails based on content analysis
- **Sentiment Analysis**: Determine the emotional tone of emails (positive, negative, neutral)
- **Action Items Extraction**: Automatically extract action items and tasks from email content
- **Spam Detection**: Intelligent spam filtering using pattern recognition
- **Auto-Response Suggestions**: Generate contextual response suggestions based on email content

### Email Analytics
- **Email Summarization**: Get quick summaries of long emails
- **Tag Extraction**: Automatically tag emails (meeting, action-required, payment, needs-response)
- **Confidence Scoring**: Get confidence levels for classifications

## 📋 Requirements

- Python 3.8+
- Email account with IMAP/SMTP access
- Docker (optional, for containerized deployment)

## 🔧 Installation

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yadavanujkumar/ai-powered-personal-email-management-assistant.git
cd ai-powered-personal-email-management-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:
```env
# Email Configuration
EMAIL_ADDRESS=your-email@example.com
EMAIL_PASSWORD=your-app-specific-password

# IMAP Settings (Gmail defaults shown)
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993

# SMTP Settings (Gmail defaults shown)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# SSL/TLS
USE_SSL=true
```

**Note for Gmail Users**: 
- Enable 2-factor authentication
- Generate an [App Password](https://support.google.com/accounts/answer/185833)
- Use the app password instead of your regular password

5. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build the Docker image**
```bash
docker build -t email-assistant .
```

2. **Run the container**
```bash
docker run -d \
  -p 8000:8000 \
  -e EMAIL_ADDRESS=your-email@example.com \
  -e EMAIL_PASSWORD=your-app-password \
  --name email-assistant \
  email-assistant
```

## 📖 API Documentation

Once the application is running, access:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Key Endpoints

#### Health Check
```http
GET /api/v1/health
```

#### Fetch Emails
```http
POST /api/v1/emails/fetch
Content-Type: application/json

{
  "folder": "INBOX",
  "limit": 50,
  "unread_only": false
}
```

#### Send Email
```http
POST /api/v1/emails/send
Content-Type: application/json

{
  "to": ["recipient@example.com"],
  "subject": "Hello from Email Assistant",
  "body": "This is the email body",
  "html": "<p>This is the <b>HTML</b> body</p>"
}
```

#### Analyze Email
```http
POST /api/v1/emails/analyze
Content-Type: application/json

{
  "id": "1",
  "subject": "Meeting Tomorrow",
  "sender": {"email": "sender@example.com"},
  "recipients": [{"email": "you@example.com"}],
  "body": "Let's schedule a meeting for tomorrow...",
  "date": "2024-01-01T10:00:00Z",
  "folder": "inbox"
}
```

#### Classify Email
```http
POST /api/v1/emails/classify
```

#### Check for Spam
```http
POST /api/v1/emails/spam-check
```

#### Get Configuration
```http
GET /api/v1/config
```

## 🏗️ Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # FastAPI routes and endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── email_models.py    # Pydantic models for email data
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_service.py   # IMAP/SMTP email operations
│   │   └── ai_service.py      # AI classification and analysis
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Configuration management
│       └── logger.py           # Logging setup
├── tests/                      # Test suite
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .env.example               # Example environment variables
└── README.md                   # This file
```

## 🔐 Security Best Practices

1. **Never commit credentials**: Always use environment variables or secret management systems
2. **Use app-specific passwords**: For Gmail and other providers, use app-specific passwords
3. **Enable 2FA**: Always enable two-factor authentication on your email account
4. **Secure API**: In production, implement authentication and rate limiting
5. **HTTPS Only**: Always use HTTPS in production environments

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use secure secret management (AWS Secrets Manager, Azure Key Vault, etc.)
2. **API Authentication**: Implement OAuth2 or JWT authentication
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Monitoring**: Set up logging and monitoring (Prometheus, Grafana, etc.)
5. **Load Balancing**: Use a reverse proxy (Nginx, Apache) for load balancing

### Docker Compose Example

```yaml
version: '3.8'

services:
  email-assistant:
    build: .
    ports:
      - "8000:8000"
    environment:
      - EMAIL_ADDRESS=${EMAIL_ADDRESS}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
      - IMAP_SERVER=${IMAP_SERVER}
      - SMTP_SERVER=${SMTP_SERVER}
    restart: unless-stopped
```

## 📊 AI Classification Categories

The system automatically classifies emails into these categories:

- **Work**: Meeting invitations, project updates, deadlines, reports
- **Personal**: Family, friends, social invitations
- **Finance**: Invoices, payments, banking, receipts
- **Promotions**: Sales, discounts, offers, deals
- **Newsletters**: Subscriptions, digests, updates
- **Social**: Social media notifications
- **Spam**: Unwanted or suspicious emails
- **General**: Emails that don't fit other categories

## 🎯 Priority Levels

- **High**: Urgent emails requiring immediate attention
- **Medium**: Important emails that need attention soon
- **Low**: Regular emails that can be handled later

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI and Python
- Powered by intelligent classification algorithms
- Designed for personal productivity enhancement

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🔮 Future Enhancements

- Integration with OpenAI GPT for advanced email understanding
- Machine learning model training for personalized classification
- Email scheduling and delayed sending
- Template management for common responses
- Multi-account support
- Mobile app integration
- Browser extension
- Calendar integration for meeting scheduling
- Attachment management and search
- Email thread analysis
- Contact management integration

---

**Note**: This is an AI-powered email management assistant. Always review AI-generated classifications and suggestions before taking action on important emails.