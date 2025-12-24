from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "test@example.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

class EmailService:
    @staticmethod
    async def send_welcome_email(email: EmailStr):
        html = """
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Welcome to Technorizen!</h2>
                <p>Hello,</p>
                <p>Thanks for coming with us. We are excited to have you on board.</p>
                <br>
                <p>Best Regards,</p>
                <p>The Team</p>
            </body>
        </html>
        """

        message = MessageSchema(
            subject="Welcome to Technorizen!",
            recipients=[email],
            body=html,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        try:
            await fm.send_message(message)
            print(f"Email sent to {email}")
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")
