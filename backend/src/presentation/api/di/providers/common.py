from src.infrastructure.secure.services import PasslibPasswordService


def get_password_service():
    return PasslibPasswordService()


def mailing_provider() -> None:
    pass


def uow_provider() -> None:
    pass


def in_memory_provider() -> None:
    pass
