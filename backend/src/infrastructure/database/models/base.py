from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class AbstractModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
