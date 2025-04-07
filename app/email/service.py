import aiosmtplib
from email.message import EmailMessage
from config import settings


class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str):
        message = EmailMessage()
        message["From"] = settings.smtp.username
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=settings.smtp.host,
            port=settings.smtp.port,
            username=settings.smtp.username,
            password=settings.smtp.password,
            use_tls=True,
        )
