import datetime
from typing import Annotated

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class AbstractModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


time_created = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
