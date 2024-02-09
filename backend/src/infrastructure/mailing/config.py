import os
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class EmailSettings:
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")

    EMAIL_TEMPLATES = os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '../../..'
            )
        ),
        "templates/emails/"
    )

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
