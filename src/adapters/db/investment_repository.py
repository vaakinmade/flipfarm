from typing import Callable, Any
from src.domain.ports.repository import RepositoryInterface
from src.domain.ports.investment_service import InvestmentDBOperationError


class InvestmentRepository(RepositoryInterface):

    def __init__(self, db_conn: Callable[[], Any]) -> None:
        self.db_conn = db_conn()

    def execute(self, query: str, data: tuple[Any, ...], commit: bool = False) -> Any:
        cursor = self.db_conn().cursor()
        try:
            cursor.execute(query, data)
            if commit:
                self.commit()
        except Exception as err:
            self.db_conn().rollback()
            raise InvestmentDBOperationError(err) from err

        return cursor

    def commit(self) -> None:
        self.db_conn().commit()
