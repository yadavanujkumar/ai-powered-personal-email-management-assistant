"""Example: Check emails for spam using the Email Management Assistant API"""
import requests
from datetime import datetime


def check_spam():
    """Check emails for spam"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🔍 Fetching emails and checking for spam...\n")
    
    # Fetch emails
    fetch_response = requests.post(
        f"{base_url}/emails/fetch",
        json={
            "folder": "INBOX",
            "limit": 10,
            "unread_only": False
        }
    )
    
    if fetch_response.status_code != 200:
        print(f"❌ Error fetching emails: {fetch_response.text}")
        return
    
    emails = fetch_response.json()
    print(f"✅ Checking {len(emails)} emails for spam\n")
    
    spam_count = 0
    
    # Check each email for spam
    for i, email in enumerate(emails, 1):
        # Check spam
        spam_response = requests.post(
            f"{base_url}/emails/spam-check",
            json=email
        )
        
        if spam_response.status_code == 200:
            result = spam_response.json()
            is_spam = result['is_spam']
            
            status = "🚫 SPAM" if is_spam else "✅ Legitimate"
            print(f"{status} - {email['subject'][:60]}")
            print(f"         From: {email['sender']['email']}")
            
            if is_spam:
                spam_count += 1
            
        else:
            print(f"❌ Error checking email: {spam_response.text}")
    
    print(f"\n📊 Summary:")
    print(f"   Total emails checked: {len(emails)}")
    print(f"   Spam detected: {spam_count}")
    print(f"   Legitimate emails: {len(emails) - spam_count}")


if __name__ == "__main__":
    try:
        # Check if server is running
        health_response = requests.get("http://localhost:8000/api/v1/health")
        if health_response.status_code == 200:
            print("✅ Server is running\n")
            check_spam()
        else:
            print("❌ Server is not responding properly")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Make sure it's running on http://localhost:8000")
        print("   Start the server with: python main.py")
