from src.domain.app.exceptions.base import DomainException


class UserExists(DomainException):
    pass


class TokenDoesNotExist(DomainException):
    pass
