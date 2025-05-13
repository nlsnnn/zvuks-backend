import aiosmtplib

from jinja2 import Environment, FileSystemLoader
from email.message import EmailMessage
from app.users.models import User
from app.config import settings


env = Environment(loader=FileSystemLoader("app/email/templates"), enable_async=True)


class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str, is_html: bool = True):
        message = EmailMessage()
        message["From"] = settings.smtp.username
        message["To"] = to_email
        message["Subject"] = subject

        if is_html:
            message.add_alternative(body, subtype="html")
        else:
            message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=settings.smtp.host,
            port=settings.smtp.port,
            username=settings.smtp.username,
            password=settings.smtp.password,
            use_tls=True,
        )

    @staticmethod
    async def send_reset_password(user: User, link: str):
        template = env.get_template("reset_password.html")
        content = await template.render_async(username=user.username, reset_link=link)

        await EmailService.send_email(user.email, subject="Сброс пароля", body=content)

    @staticmethod
    async def send_release_notification(
        user: User,
        artist_username: str,
        release_type: str,
        release_link: str,
        release_image: str,
    ):
        template = env.get_template("release_notification.html")
        content = await template.render_async(
            username=user.username,
            artist_username=artist_username,
            release_type="новую песню" if release_type == "song" else "новый альбом",
            release_link=release_link,
            release_image=release_image,
        )

        await EmailService.send_email(
            user.email,
            subject=f"Новая песня от {artist_username}"
            if release_type == "song"
            else f"Новый альбом от {artist_username}",
            body=content,
        )
