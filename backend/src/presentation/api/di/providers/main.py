from redis import Redis    # type: ignore
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.inmemory_db.service import RedisService
from src.infrastructure.mailing.config import SMTPMailConfig
from src.infrastructure.mailing.services import SMTPLibEmailService, DebugEmailService


class MailingProvider:
    def __init__(self, settings: SMTPMailConfig):
        self.settings = settings

    async def provide_mailing(self) -> SMTPLibEmailService:
        return SMTPLibEmailService(self.settings)

    async def provide_mailing_debug(self) -> DebugEmailService:
        return DebugEmailService(self.settings)


class RedisProvider:
    def __init__(self, pool: Redis):
        self.pool = pool

    async def provide_db(self):
        return RedisService(self.pool)


class DBProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def provide_db(self):
        async with self.pool() as session:
            yield UnitOfWork(session)
