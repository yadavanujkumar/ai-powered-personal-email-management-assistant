"""Example: Send an email using the Email Management Assistant API"""
import requests


def send_email_example():
    """Send a test email"""
    base_url = "http://localhost:8000/api/v1"
    
    print("📧 Sending email...\n")
    
    email_data = {
        "to": ["recipient@example.com"],
        "subject": "Test Email from Email Management Assistant",
        "body": "This is a test email sent using the AI-Powered Email Management Assistant API.",
        "html": "<html><body><h1>Test Email</h1><p>This is a test email sent using the <b>AI-Powered Email Management Assistant</b> API.</p></body></html>"
    }
    
    response = requests.post(
        f"{base_url}/emails/send",
        json=email_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
        print(f"   To: {', '.join(email_data['to'])}")
        print(f"   Subject: {email_data['subject']}")
    else:
        print(f"❌ Error sending email: {response.text}")


if __name__ == "__main__":
    try:
        # Check if server is running
        health_response = requests.get("http://localhost:8000/api/v1/health")
        if health_response.status_code == 200:
            print("✅ Server is running\n")
            
            # Get confirmation before sending
            recipient = input("Enter recipient email address: ")
            confirm = input(f"Send test email to {recipient}? (yes/no): ")
            
            if confirm.lower() == 'yes':
                send_email_example()
            else:
                print("❌ Email sending cancelled")
        else:
            print("❌ Server is not responding properly")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Make sure it's running on http://localhost:8000")
        print("   Start the server with: python main.py")
