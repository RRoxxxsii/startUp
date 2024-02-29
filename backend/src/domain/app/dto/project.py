from dataclasses import asdict, dataclass

from src.infrastructure.database.models import UserORM


@dataclass
class CreateProjectDTO:
    title: str
    category_id: int
    user_id: int
    description: str | None = None

    def dict(self):
        return {k: v for k, v in asdict(self).items()}
