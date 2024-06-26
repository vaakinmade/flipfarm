# from sqlite3 import Connection
from abc import ABC, abstractmethod
from typing import Any, Callable


class RepositoryInterface(ABC):

    @abstractmethod
    def __init__(self, db_conn: Callable[[], Any]) -> None:
        self.db = db_conn

    @abstractmethod
    def execute(self, query: str, data: tuple[Any, ...], commit: bool = False) -> Any:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass
