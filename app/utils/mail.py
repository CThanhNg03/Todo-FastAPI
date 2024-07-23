from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os

from app.config.auth import create_confirmation_token
from app.config.env import env


conf = ConnectionConfig(
    MAIL_USERNAME = env.mail["username"],
    MAIL_PASSWORD = env.mail["password"],
    MAIL_FROM = env.mail["from"],
    MAIL_PORT = 587,
    MAIL_SERVER = env.mail["server"],
    MAIL_SSL_TLS = False,
    MAIL_STARTTLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    MAIL_FROM_NAME = env.mail["from_name"]
)

mail = FastMail(conf)

async def send_confirm_email(email: str):
    confirmation_url=f"{os.getenv('BASE_URL')}/api/v1/users/confirm/{create_confirmation_token(email)}"
    message = MessageSchema(
        subject="CONFIRM YOUR EMAIL",
        recipients=[email],
        body=f"<p>Please go to the following link to confirm your email: {confirmation_url}<p>",
        subtype="html"
    )
    await mail.send_message(message)

    # return confirmation_url

