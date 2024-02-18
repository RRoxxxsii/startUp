from abc import ABC, abstractmethod


class AbstractInMemoryService(ABC):
    def __init__(self, pool):
        self._pool = pool

    @abstractmethod
    def set_value(self, key, value) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key) -> str | list | dict | int:
        raise NotImplementedError

    @abstractmethod
    def delete_value(self, key) -> None:
        raise NotImplementedError


class RedisService(AbstractInMemoryService):
    def set_value(self, key, value) -> None:
        self._pool.set(key, value)

    def get_value(self, key) -> str | list | dict | int:
        return self._pool.get(key)

    def delete_value(self, key) -> None:
        self._pool.delete(key)


class StubInMemoryService(AbstractInMemoryService):
    _storage: dict = {}

    def __init__(self, pool):  # noqa
        self.pool = self._storage

    def set_value(self, key, value) -> None:
        self.pool[key] = value

    def get_value(self, key) -> str | list | dict | int:
        return self.pool.get(key)

    def delete_value(self, key) -> None:
        del self.pool[key]
