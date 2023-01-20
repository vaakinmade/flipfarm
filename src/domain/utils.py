from enum import Enum
from typing import Any, Optional, Union


class FundStatus(Enum):
    PRE_FUNDING = "pre_funding"
    FUNDING = "funding"
    FUNDED = "funded"


class Money(object):
    value: int

    def __init__(self, amount: Any, convert_to_pence=True):
        if amount not in (0, None):
            if convert_to_pence:
                self.value = int(amount) * 100
            else:
                self.value = amount
        else:
            self.value = 0

    @staticmethod
    def validate_type(num):
        if type(num) is not Money:
            raise TypeError(f"{type(num)} cannot be added/subtracted/multiplied/divided by type Money()")

    def add(self, num):
        Money.validate_type(num)
        self.value = self.value + num.value
        return self

    # def multiplied_by(self, multiplier):
    #     Money.validate_type(multiplier)
    #     self.value = self.value * multiplier.value
    #     return self
    #
    # def divided_by(self, divisor):
    #     Money.validate_type(divisor)
    #     self.value = self.value / divisor.value
    #     return self
    #
    # def subtract(self, num):
    #     Money.validate_type(num)
    #     self.value = self.value - num.value
    #     return self

    @staticmethod
    def convert_from_pence(amount: int):
        """Return string equivalent of the provided value, formatted to 2 decimal places"""
        return "{:,.2f}".format(amount / 100)

    @staticmethod
    def extract_trailing_pence(amount: Union[int, float]):
        pence = Money.convert_from_pence(amount)
        trailing_pence = pence.split(".")[1]
        return trailing_pence

    @staticmethod
    def extract_leading_pence(amount: Union[int, float]):
        pence = Money.convert_from_pence(amount)
        leading_pence = pence.split(".")[0]
        return leading_pence


def validate_amount(amount: str, custom_amount: str) -> tuple[Any, Optional[str]]:
    error = None
    if not any([amount, custom_amount]):
        error = "An investment amount must be specified."
    elif all([amount, custom_amount]):
        error = "Please specify a single investment amount."

    if custom_amount:
        return custom_amount, error
    return amount, error
