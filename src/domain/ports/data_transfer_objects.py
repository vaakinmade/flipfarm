from dataclasses import dataclass, asdict
from datetime import datetime
from uuid import uuid4

from werkzeug.security import generate_password_hash
from src.domain.utils import Money


@dataclass
class InputDto:

    def __init__(self):
        pass

    def to_dict(self):
        return asdict(self)

    # @classmethod
    # def from_dict(cls, dict_):
    #     return cls(**dict_)

    @staticmethod
    def is_money(amount):
        if type(amount) is not Money:
            raise TypeError(f"{type(amount)} not an instance of Money")


@dataclass
class RegisterUserInputDto(InputDto):
    id_: str
    first_name: str
    last_name: str
    password: str
    email: str
    date_of_birth: datetime
    is_active: bool
    created_at: datetime


def register_user_factory(password: str, email: str, first_name: str = None, last_name: str = None,
                          is_active: bool = False, date_of_birth: datetime = None) -> RegisterUserInputDto:
    return RegisterUserInputDto(id_=str(uuid4()), first_name=first_name, last_name=last_name,
                                date_of_birth=date_of_birth,
                                password=generate_password_hash(password), email=email, is_active=is_active,
                                created_at=datetime.now())


@dataclass
class UpdateUserInputDto(RegisterUserInputDto):
    pass


def update_user_factory(id_: str, first_name: str = None, last_name: str = None, password: str = None,
                        email: str = None, date_of_birth: datetime = None, is_active: bool = None,
                        created_at: datetime = None) -> UpdateUserInputDto:
    if password:
        password = generate_password_hash(password)
    return UpdateUserInputDto(id_=id_, first_name=first_name, last_name=last_name, password=password, email=email,
                              date_of_birth=date_of_birth, is_active=is_active, created_at=created_at)


@dataclass
class CreateCommodityInputDto(InputDto):
    id: int
    id_: str
    name: str
    cycle: int
    interest_yield: float
    location: str
    category: str
    duration: int
    amount: Money
    location_thumbnail: str
    amount_raised: Money
    funded: bool
    created_at: datetime

    # def __init__(self, **kwargs):
    #     super().__init__()
    #     for k, v in kwargs.items():
    #         setattr(self, k, v)
    #         if k in ("amount", "amount_raised"):
    #             setattr(self, k, Money(v, convert_to_pence=False))


def create_commodity_factory(name: str, interest_yield: float, location: str, category: str, duration: int,
                             amount: Money, cycle: int = None, funded: bool = False,
                             location_thumbnail: str = None, amount_raised: Money = Money(0)
                             ) -> CreateCommodityInputDto:
    return CreateCommodityInputDto(id_=str(uuid4()),
                                   name=name,
                                   cycle=cycle,
                                   interest_yield=interest_yield,
                                   location=location,
                                   location_thumbnail=location_thumbnail,
                                   category=category,
                                   duration=duration,
                                   amount=amount,
                                   amount_raised=amount_raised,
                                   funded=funded,
                                   created_at=datetime.now())


@dataclass
class UpdateCommodityInputDto(InputDto):
    id: int
    id_: str
    name: str
    cycle: int
    interest_yield: float
    location: str
    category: str
    duration: int
    amount: Money
    location_thumbnail: str
    amount_raised: Money
    funded: bool
    created_at: datetime


def update_commodity_factory(id_: str, id: int = None, name: str = None, interest_yield: float = None, location: str = None,
                             category: str = None, duration: int = None, amount: Money = None, cycle: int = None,
                             funded: bool = None, location_thumbnail: str = None, amount_raised: Money = None,
                             created_at: datetime = None
                             ) -> UpdateCommodityInputDto:

    UpdateCommodityInputDto.is_money(amount_raised)

    return UpdateCommodityInputDto(id_=id_,
                                   id=id,
                                   name=name,
                                   cycle=cycle,
                                   interest_yield=interest_yield,
                                   location=location,
                                   location_thumbnail=location_thumbnail,
                                   category=category,
                                   duration=duration,
                                   amount=amount,
                                   amount_raised=amount_raised,
                                   funded=funded,
                                   created_at=created_at)


@dataclass
class CreateInvestmentInputDto(InputDto):
    id_: str
    commodity_id: int
    investor_id: int
    investment_yield: float
    amount: Money
    status: str
    maturity_date: datetime
    created_at: datetime
    updated_at: datetime


def create_investment_factory(commodity_id: int, investor_id: int, amount: Money, status: str,
                              investment_yield: float = None, maturity_date: datetime = None
                              ) -> CreateInvestmentInputDto:

    CreateInvestmentInputDto.is_money(amount)

    return CreateInvestmentInputDto(id_=str(uuid4()), commodity_id=commodity_id, investor_id=investor_id,
                                    investment_yield=investment_yield, amount=amount, status=status,
                                    maturity_date=maturity_date, created_at=datetime.now(), updated_at=datetime.now())


@dataclass
class UpdateInvestmentInputDto(CreateInvestmentInputDto):
    pass


def update_investment_factory(id_: str, commodity_id: int = None, investor_id: int = None,
                              investment_yield: float = None, amount: Money = None, status: str = None,
                              maturity_date: datetime = None, created_at: datetime = None, updated_at: datetime = None
                              ) -> UpdateInvestmentInputDto:

    UpdateInvestmentInputDto.is_money(amount)

    return UpdateInvestmentInputDto(id_=id_,
                                    commodity_id=commodity_id,
                                    investor_id=investor_id,
                                    investment_yield=investment_yield,
                                    amount=amount,
                                    status=status,
                                    maturity_date=maturity_date,
                                    created_at=created_at,
                                    updated_at=updated_at)
