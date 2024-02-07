from abc import ABC, abstractmethod

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AbstractPasswordHandler(ABC):

    @abstractmethod
    def check_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError


class PasslibPasswordHandler(AbstractPasswordHandler):

    def check_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
