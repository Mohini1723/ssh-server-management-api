import asyncio
import sys
from app.email import EmailService
from dotenv import load_dotenv

# Load env vars to ensure we have the credentials
load_dotenv()

async def test_email():
    target_email = sys.argv[1] if len(sys.argv) > 1 else "mohini@example.com"
    print(f"Attempting to send test email to: {target_email}")
    print("Check your inbox (and spam folder) after this runs.")
    
    try:
        await EmailService.send_welcome_email(target_email)
        print("Email send function completed (check console for success/fail logs from app/email.py).")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_email.py <your_email@gmail.com>")
    else:
        asyncio.run(test_email())
