from src.infrastructure.mailing.config import EmailSettings
from src.infrastructure.mailing.services import (
    DebugEmailService,
    SMTPLibEmailService,
)


class MailingProvider:
    def __init__(self, settings: EmailSettings):
        self.settings = settings

    async def provide_mailing(self) -> SMTPLibEmailService:
        return SMTPLibEmailService(self.settings)

    async def provide_mailing_debug(self) -> DebugEmailService:
        return DebugEmailService(self.settings)


def mailing_provider():
    pass
