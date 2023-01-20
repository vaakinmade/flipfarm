from dataclasses import dataclass
from datetime import datetime
from typing import Union

from ..ports.data_transfer_objects import CreateInvestmentInputDto, UpdateInvestmentInputDto
from ..utils import Money


@dataclass
class Investment:
    id_: str
    commodity_id: int
    investor_id: int
    amount: Money
    status: str
    maturity_date: datetime
    created_at: datetime
    updated_at: datetime


def investment_factory(investment: Union[CreateInvestmentInputDto, UpdateInvestmentInputDto]) -> Investment:

    return Investment(id_=investment.id_,
                      commodity_id=investment.commodity_id,
                      investor_id=investment.investor_id,
                      amount=investment.amount,
                      status=investment.status,
                      maturity_date=investment.maturity_date,
                      created_at=investment.created_at,
                      updated_at=investment.updated_at)
