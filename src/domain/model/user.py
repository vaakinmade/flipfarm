from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime
from typing import Union

from ..ports.data_transfer_objects import UpdateUserInputDto, RegisterUserInputDto


@dataclass
class User:
    id_: str
    first_name: str
    last_name: str
    password: str
    email: str
    date_of_birth: datetime
    created_at: datetime
    is_active: bool


def user_factory(user: Union[RegisterUserInputDto, UpdateUserInputDto]) -> User:
    # TO-DO: data validation should happen here

    return User(id_=user.id_,
                first_name=user.first_name,
                last_name=user.last_name,
                password=user.password,
                email=user.email,
                created_at=user.created_at,
                date_of_birth=user.date_of_birth,
                is_active=user.is_active)
