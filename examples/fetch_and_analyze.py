"""Example: Fetch and analyze emails using the Email Management Assistant API"""
import requests
import json
from datetime import datetime


def fetch_and_analyze_emails():
    """Fetch emails and analyze them with AI"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🔍 Fetching emails from inbox...")
    
    # Fetch emails
    fetch_response = requests.post(
        f"{base_url}/emails/fetch",
        json={
            "folder": "INBOX",
            "limit": 5,
            "unread_only": False
        }
    )
    
    if fetch_response.status_code != 200:
        print(f"❌ Error fetching emails: {fetch_response.text}")
        return
    
    emails = fetch_response.json()
    print(f"✅ Fetched {len(emails)} emails\n")
    
    # Analyze each email
    for i, email in enumerate(emails, 1):
        print(f"\n📧 Email {i}/{len(emails)}")
        print(f"   Subject: {email['subject']}")
        print(f"   From: {email['sender']['email']}")
        print(f"   Date: {email['date']}")
        
        # Analyze email
        analyze_response = requests.post(
            f"{base_url}/emails/analyze",
            json=email
        )
        
        if analyze_response.status_code == 200:
            analysis = analyze_response.json()
            
            print(f"\n   🤖 AI Analysis:")
            print(f"      Category: {analysis['classification']['category']}")
            print(f"      Priority: {analysis['classification']['priority']}")
            print(f"      Confidence: {analysis['classification']['confidence']:.2%}")
            print(f"      Sentiment: {analysis['sentiment']}")
            print(f"      Tags: {', '.join(analysis['classification']['tags'])}")
            
            if analysis['summary']:
                print(f"\n      Summary: {analysis['summary']}")
            
            if analysis['action_required']:
                print(f"\n      ⚠️  Action Required!")
                if analysis['action_items']:
                    print(f"      Action Items:")
                    for item in analysis['action_items']:
                        print(f"         - {item}")
            
            if analysis['suggested_response']:
                print(f"\n      💡 Suggested Response:")
                print(f"      {analysis['suggested_response']}")
        else:
            print(f"   ❌ Error analyzing email: {analyze_response.text}")
        
        print("\n" + "-" * 80)


if __name__ == "__main__":
    try:
        # Check if server is running
        health_response = requests.get("http://localhost:8000/api/v1/health")
        if health_response.status_code == 200:
            print("✅ Server is running\n")
            fetch_and_analyze_emails()
        else:
            print("❌ Server is not responding properly")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Make sure it's running on http://localhost:8000")
        print("   Start the server with: python main.py")
