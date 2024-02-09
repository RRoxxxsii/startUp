from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class EmailDTO:
    to_email: str
    subject: str
    extra: dict[str, str | int]
    template_name: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
