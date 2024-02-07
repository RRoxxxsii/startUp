from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class CreateUserDTO:
    password: str
    username: str
    email: str
    surname: str
    firstname: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
