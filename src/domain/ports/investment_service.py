from enum import Enum
from typing import Optional, Any

from . import CreateInvestmentInputDto, UpdateInvestmentInputDto
from src.domain.ports.repository import RepositoryInterface
from src.domain.model import Investment, investment_factory
from src.domain.utils import Money


class InvestmentDBOperationError(Exception):
    ...


class InvestmentService:

    def __init__(self, investment_repo: RepositoryInterface) -> None:
        self.investment_repo = investment_repo

    def create(self, investment: CreateInvestmentInputDto) -> Optional[Investment]:
        _investment = investment_factory(investment)
        data = (_investment.id_, _investment.commodity_id, _investment.investor_id,
                _investment.amount.value, _investment.status, _investment.maturity_date, _investment.created_at,
                _investment.updated_at)
        query = "INSERT INTO investment (id_, commodity_id, investor_id, amount, status," \
                "maturity_date, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            self.investment_repo.execute(query, data, commit=True)
        except Exception as err:
            raise InvestmentDBOperationError(err) from err
        return _investment

    def update_investment_amount(self, investment: UpdateInvestmentInputDto):
        data = (investment.amount.value, investment.id_)
        query = "UPDATE investment SET amount = %s WHERE id_ = %s"
        try:
            self.investment_repo.execute(query, data, commit=True)
        except Exception as err:
            raise InvestmentDBOperationError(err) from err

    def get_investment_by_id(self, _id: int) -> Investment:
        data = (_id,)
        query = "SELECT i.id, amount, status, maturity_date FROM investment i JOIN commodity c ON " \
                "i.commodity_id = c.id WHERE i.id = %s"

        investment = self.investment_repo.execute(query, data).fetchone()
        return investment

    def get_investment_by_investor_and_commodity_id(self, investor_id: int, commodity_id: int) -> Investment:
        data = (investor_id, commodity_id)
        query = "SELECT i.id, i.id_, i.amount, status, maturity_date FROM investment i JOIN " \
                "commodity c ON i.commodity_id = c.id WHERE i.investor_id = %s AND i.commodity_id = %s"
        try:
            cursor = self.investment_repo.execute(query, data, commit=True)
            return cursor.fetchone()
        except Exception as err:
            raise InvestmentDBOperationError(err) from err

    def get_investments_by_investor_id(self, investor_id: int) -> dict[Any, Any]:
        data = (investor_id,)
        query = "SELECT i.id, i.id_, i.amount, status, maturity_date, c.id as c_id, c.id_ as c_id_," \
                "name, interest_yield, c.amount as c_amount, c.amount_raised, location, location_thumbnail, " \
                "category, duration, fund_status "\
                "FROM investment i LEFT JOIN commodity c ON i.commodity_id = c.id WHERE i.investor_id = %s"
        try:
            cursor = self.investment_repo.execute(query, data, commit=True)
            return cursor.fetchall()
        except Exception as err:
            raise InvestmentDBOperationError(err) from err


def calculate_percentage(amount: Money, percent: float) -> float:
    return (percent/100) * float(amount.value)


class Status(Enum):
    ACTIVE = "active"
    LIVE = "live"
    COMPLETED = "completed"
