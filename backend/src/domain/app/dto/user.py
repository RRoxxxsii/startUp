from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CreateUserDTO:
    password: str
    username: str
    email: str
    surname: str
    firstname: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass(frozen=True)
class AuthDTO:
    password: str
    email: str
