# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Prerequisites
- Python 3.8 or higher
- Email account with IMAP/SMTP access (Gmail, Outlook, etc.)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/yadavanujkumar/ai-powered-personal-email-management-assistant.git
cd ai-powered-personal-email-management-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your email credentials:
```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

**For Gmail users:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Generate an App Password at https://myaccount.google.com/apppasswords
4. Use the generated app password in your `.env` file

### 4. Run the Application
```bash
python main.py
```

The API will be available at http://localhost:8000

### 5. Access the API Documentation
Open your browser and go to:
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Testing the API

### Using curl

**Check health:**
```bash
curl http://localhost:8000/api/v1/health
```

**Fetch emails:**
```bash
curl -X POST http://localhost:8000/api/v1/emails/fetch \
  -H "Content-Type: application/json" \
  -d '{"folder": "INBOX", "limit": 10, "unread_only": false}'
```

### Using Python

```python
import requests

# Check health
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Fetch emails
response = requests.post(
    "http://localhost:8000/api/v1/emails/fetch",
    json={"folder": "INBOX", "limit": 10, "unread_only": False}
)
emails = response.json()
print(f"Fetched {len(emails)} emails")
```

## Docker Deployment

### Using Docker:
```bash
docker build -t email-assistant .
docker run -p 8000:8000 \
  -e EMAIL_ADDRESS=your-email@gmail.com \
  -e EMAIL_PASSWORD=your-app-password \
  email-assistant
```

### Using Docker Compose:
```bash
# Create .env file first with your credentials
docker-compose up
```

## Common Issues

### "Failed to connect to IMAP"
- Check your email address and password
- For Gmail, make sure you're using an App Password, not your regular password
- Check that IMAP is enabled in your email settings

### "Connection refused"
- Make sure no other application is using port 8000
- Try changing the port in `main.py`

### "Module not found"
- Make sure you've installed all dependencies: `pip install -r requirements.txt`
- Make sure you're in the virtual environment

## Next Steps

1. Explore the API documentation at `/docs`
2. Try different AI features like classification and analysis
3. Customize the AI classification categories in `src/services/ai_service.py`
4. Add your own email processing rules

## Support

For issues or questions:
- Open an issue on GitHub
- Check the full README.md for detailed documentation
