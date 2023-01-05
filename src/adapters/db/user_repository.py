from typing import Callable, Any

from psycopg2 import InterfaceError, ProgrammingError, OperationalError

from src.domain.ports.repository import RepositoryInterface
from src.domain.ports.user_service import UserDBOperationError
from src.main.config import get_db


class UserRepository(RepositoryInterface):

    def __init__(self, db_conn: Callable[[], Any]) -> None:
        self.db_conn = db_conn()

    def execute(self, query: str, data: tuple[Any, ...], commit: bool = False) -> Any:
        cursor = self.db_conn().cursor()
        try:
            cursor.execute(query, data)
            if commit:
                self.commit()
        except (InterfaceError, OperationalError) as err:
            print("Possible db connection error:", err)
            self.retry_query(query, data)
        except ProgrammingError as err:
            self.db_conn().rollback()
            raise UserDBOperationError(err) from err

        return cursor

    def commit(self) -> None:
        self.db_conn().commit()

    def retry_query(self, query, data) -> None:
        self.db_conn = get_db()
        self.execute(query, data)
