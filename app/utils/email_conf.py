import random, string
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import status
from app.utils.error_handler import server_error
from .get_env import settings

def generate_verification_code(length: int = 6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

conf = ConnectionConfig(
    MAIL_USERNAME=str(settings.MAIL_USERNAME),
    MAIL_PASSWORD=str(settings.MAIL_PASSWORD),
    MAIL_FROM=str(settings.MAIL_FROM),
    MAIL_PORT=int(settings.MAIL_PORT),
    MAIL_SERVER=str(settings.MAIL_SERVER),
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_SSL_TLS=True,
    MAIL_STARTTLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

def verify_email_html(login_email:str = None, password:str = None, username:str = None, code:str = None):

    html = f"""
    <br>
    <h1>Welcome</h1>
    <h3>Here are your login details</h3>
    <p>Here are your details <br> Login_email:  {login_email} <br> Password: {password} <br> Username:{username}</P>
    <h4> Verification code <h1>{code}</h1> </h4>
    """

    return html

def forgot_password_email_html(code:str):

    html = f"""
    <br>
    <h1>Welcome</h1>
    <h3>Forgot password code</h3>
    <h4> Verification code <h1>{code}</h1> </h4>
    """

    return html

async def send_email(subject, recipients, body):
    fast_mail = FastMail(conf)
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        subtype="html",
        body=body,
    )
    try:
        await fast_mail.send_message(message)
    except Exception as e:
        raise server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to send email: {str(e)}")

