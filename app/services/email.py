from pathlib import Path

from fastapi import BackgroundTasks
from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType,
    NameEmail,
)
from pydantic import EmailStr

from app.core.config import settings


class EmailService:
    def __init__(self, background_tasks: BackgroundTasks):
        self._background_tasks = background_tasks

        self._conf = ConnectionConfig(
            MAIL_USERNAME=settings.email.username,
            MAIL_PASSWORD=settings.email.password,
            MAIL_FROM=settings.email.username,
            MAIL_PORT=settings.email.port,
            MAIL_SERVER=settings.email.server,
            MAIL_FROM_NAME=settings.email.from_name,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            TEMPLATE_FOLDER=Path(settings.email.templates_dir)
        )

        self._fast_mail = FastMail(self._conf)

    def send_email(
        self,
        email_to: EmailStr | str,
        subject: str,
        template_name: str,
        template_body: dict
    ) -> None:
        recipient = NameEmail(name="", email=str(email_to))

        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            template_body=template_body,
            subtype=MessageType.html
        )

        self._background_tasks.add_task(
            self._fast_mail.send_message,
            message,
            template_name=template_name
        )

    def send_verification_email(
        self, email_to: str, verification_code: str, verification_link: str
    ) -> None:
        self.send_email(
            email_to=email_to,
            subject=f'Подтверждение аккаунта. {settings.email.title}',
            template_name='verify_account.html',
            template_body={
                'title': settings.email.title,
                'verification_code': verification_code,
                'verification_link': verification_link,
            },
        )

    def send_change_password_email(
        self, email_to: str, reset_code: str, reset_link: str
    ) -> None:
        self.send_email(
            email_to=email_to,
            subject=f'Смена пароля. {settings.email.title}',
            template_name='change_password.html',
            template_body={
                'title': settings.email.title,
                'reset_code': reset_code,
                'reset_link': reset_link
            },
        )
