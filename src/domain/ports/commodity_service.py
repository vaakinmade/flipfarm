from typing import Optional, Any

from . import CreateCommodityInputDto, UpdateCommodityInputDto
from src.domain.ports.repository import RepositoryInterface
from src.domain.model import Commodity, commodity_factory
from src.domain.utils import Money


class CommodityDBOperationError(Exception):
    pass


class CommodityService:

    def __init__(self, commodity_repo: RepositoryInterface) -> None:
        self.commodity_repo = commodity_repo

    def create(self, commodity: CreateCommodityInputDto) -> Optional[Commodity]:
        commodity = commodity_factory(commodity)
        data = (commodity.id_, commodity.name, commodity.interest_yield, commodity.location,
                commodity.location_thumbnail, commodity.category, commodity.duration, commodity.amount.value,
                commodity.fund_status.value, commodity.created_at)
        query = "INSERT INTO commodity (id_, name, interest_yield, location, location_thumbnail, category, duration, " \
                "amount, fund_status, created_at)" " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            self.commodity_repo.execute(query, data, commit=True)
        except CommodityDBOperationError as err:
            raise CommodityDBOperationError(err) from err
        return commodity

    def update_amount_raised(self, commodity: UpdateCommodityInputDto):
        data = (commodity.amount_raised.value, commodity.fund_status.value, commodity.id_)
        query = "UPDATE commodity SET amount_raised = %s, fund_status = %s WHERE id_ = %s"
        try:
            self.commodity_repo.execute(query, data, commit=True)
        except Exception as err:
            raise CommodityDBOperationError(err) from err

    def get_all_commodities(self) -> Optional[list[Any]]:
        data = ()
        query = "SELECT * FROM commodity WHERE fund_status = 'funding' OR category = 'exclusive' ORDER BY category \
        DESC"
        try:
            cursor = self.commodity_repo.execute(query, data, commit=True)
            return cursor.fetchall()
        except Exception as err:
            raise CommodityDBOperationError() from err

    def get_commodity_by_id(self, id_: str) -> dict:
        data = (id_,)
        query = "SELECT * FROM commodity WHERE id_ = %s;"
        try:
            cursor = self.commodity_repo.execute(query, data, commit=True)
            return cursor.fetchall()
        except Exception as err:
            raise CommodityDBOperationError() from err

    def get_commodity_investment_for_investor(self, id_: int, investor_id: int) -> dict:
        data = (id_, investor_id)
        query = "SELECT c.id, c.id_, name, interest_yield, c.amount, location, location_thumbnail, " \
                "category, duration, amount_raised, fund_status, i.id as i_id, i.id_ as i_id_ FROM commodity " \
                "c LEFT JOIN investment i ON c.id = i.commodity_id WHERE c.id_ = %s AND i.investor_id = %s"
        try:
            cursor = self.commodity_repo.execute(query, data, commit=True)
            return cursor.fetchone()
        except Exception as err:
            raise CommodityDBOperationError(err) from err


def get_new_raised_amount(amount: str, max_amount: Money, amount_raised: Money) -> tuple[Money, bool, bool]:
    amount = Money(amount)
    new_amount_raised = amount.add(amount_raised)
    fully_funded, exceeded_max_amount = False, False
    if new_amount_raised.value > max_amount.value:
        exceeded_max_amount = True
    elif new_amount_raised.value == amount:
        fully_funded = True
    return new_amount_raised, fully_funded, exceeded_max_amount


def calculate_percentage_raised(amount: Money, amount_raised: Money) -> int:
    percentage = (amount_raised.value / amount.value) * 100
    return round(percentage)


