from abc import ABC, abstractmethod

from celery import chain
from src.domain.common.dto.mail import EmailDTO
from src.infrastructure.mailing.config import EmailSettings
from src.infrastructure.mailing.utils import get_mediator
from src.infrastructure.tasks.tasks import render_template, send


class AbstractEmailService(ABC):
    def __init__(self, settings: EmailSettings) -> None:
        self.settings = settings

    @abstractmethod
    def send_message(self, email_dto: EmailDTO) -> None:
        raise NotImplementedError


class SMTPLibEmailService(AbstractEmailService):
    def send_message(self, email_dto: EmailDTO) -> None:
        chain(
            render_template.s(email_dto.dict()), send.s(email_dto.dict())
        ).delay()


class DebugEmailService(AbstractEmailService):
    """
    Implements interface for sending email. But used in tests.
    Record states to an attribute of `Outbox` class.
    """

    def send_message(self, email_dto: EmailDTO) -> None:
        message = render_template(email_dto.dict())
        m = get_mediator()
        data = {"to_email": email_dto.to_email, "message": message}
        m.add_data_to_outbox(data)


class ConsoleEmailService(AbstractEmailService):
    def send_message(self, email_dto: EmailDTO) -> None:
        message = render_template(email_dto.dict())
        print(message)
