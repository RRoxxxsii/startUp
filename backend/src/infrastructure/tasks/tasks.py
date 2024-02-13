import ast
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.infrastructure.mailing.config import EmailSettings
from src.infrastructure.tasks.config import app


@app.task
def render_template(email_dto: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(EmailSettings.EMAIL_TEMPLATES),
        autoescape=select_autoescape(),
    )

    template = env.get_template(email_dto.get("template_name"))
    message = template.render(ast.literal_eval(email_dto.get("extra")))
    return message


@app.task
def send(rendered_message: str, email_dto: dict) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = email_dto.get("subject")
    message["To"] = email_dto.get("to_email")
    message["From"] = EmailSettings.MAIL_FROM

    part = MIMEText(rendered_message, "html")
    message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
        server.set_debuglevel(1)
        server.login(EmailSettings.MAIL_USERNAME, EmailSettings.MAIL_PASSWORD)
        server.sendmail(
            EmailSettings.MAIL_FROM,
            email_dto.get("to_email"),
            message.as_string(),
        )  # noqa
