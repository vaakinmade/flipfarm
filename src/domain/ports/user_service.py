from typing import Optional, Any
from time import time

import jwt
from jwt import DecodeError, ExpiredSignatureError

from . import RegisterUserInputDto, UpdateUserInputDto
from src.domain.model import user_factory, User
from .repository import RepositoryInterface
from src.main import config


class UserDBOperationError(Exception):
    pass


class UserEmailNotUniqueError(Exception):
    pass


class UserService:

    def __init__(self, user_repo: RepositoryInterface) -> None:
        self.user_repo = user_repo

    def create(self, user: RegisterUserInputDto) -> User:
        user = user_factory(user)
        data = (user.id_, user.first_name, user.last_name, user.password, user.email, user.date_of_birth,
                user.is_active, user.created_at)
        query = "INSERT INTO investor(id_, first_name, last_name, password, email, date_of_birth, is_active, " \
                "created_at) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            self.user_repo.execute(query, data, commit=True)
        except Exception as err:
            raise UserDBOperationError(err) from err
        return user

    def get_user_by_email(self, email: str) -> Optional[tuple[Any, ...]]:
        data = (email,)
        query = "SELECT * FROM investor WHERE email = %s;"
        try:
            cursor = self.user_repo.execute(query, data)
            return cursor.fetchone()
        except Exception as err:
            raise UserDBOperationError() from err

    def get_user_by_id(self, id_: str) -> Optional[tuple[Any, ...]]:
        data = (id_,)
        query = "SELECT * FROM investor WHERE id_ = %s;"
        try:
            cursor = self.user_repo.execute(query, data)
            return cursor.fetchone()
        except Exception as err:
            raise UserDBOperationError() from err

    def set_password(self, user: UpdateUserInputDto):
        user = user_factory(user)

        data = (user.password, user.id_)
        query = "UPDATE investor SET password = %s WHERE id_ = %s;"

        try:
            self.user_repo.execute(query, data, commit=True)
        except UserDBOperationError as err:
            raise UserDBOperationError(err) from err
        return user

    def activate_user(self, user: UpdateUserInputDto):
        user = user_factory(user)

        data = (user.is_active, user.id_)
        query = "UPDATE investor SET is_active = %s WHERE id_ = %s;"

        try:
            self.user_repo.execute(query, data, commit=True)
        except UserDBOperationError as err:
            raise UserDBOperationError(err) from err
        return user


def get_user_token(user_id: str, token_use: str, expires_in: int = 600) -> str:
    return jwt.encode(
        {token_use: user_id, 'exp': time() + expires_in},
        config.SECRET_KEY, algorithm='HS256')


def verify_token(token, token_use):
    try:
        id_ = jwt.decode(token, config.SECRET_KEY,
                         algorithms=['HS256'])[token_use]
    except (DecodeError, ExpiredSignatureError) as err:
        return
    return id_
