from dataclasses import dataclass
from datetime import datetime
from typing import Union

from ..ports.data_transfer_objects import CreateCommodityInputDto, UpdateCommodityInputDto
from src.domain.utils import Money, FundStatus


@dataclass
class Commodity:
    id_: str
    name: str
    fund_status: FundStatus
    interest_yield: float
    location: str
    location_thumbnail: str
    category: str
    duration: int
    amount: Money
    amount_raised: Money
    created_at: datetime


def commodity_factory(commodity: Union[CreateCommodityInputDto, UpdateCommodityInputDto]) -> Commodity:
    # TO-DO: data validation should happen here

    return Commodity(id_=commodity.id_,
                     name=commodity.name,
                     fund_status=commodity.fund_status,
                     amount=commodity.amount,
                     amount_raised=commodity.amount_raised,
                     location=commodity.location,
                     location_thumbnail=commodity.location_thumbnail,
                     category=commodity.category,
                     duration=commodity.duration,
                     interest_yield=commodity.interest_yield,
                     created_at=commodity.created_at)
