from typing import Union

from pydantic import EmailStr

from .models import User
from .dao import UsersDAO
from .utils import verify_password


async def authenticate_user(email: EmailStr, password: str) -> Union[User, None]:
    """
    Аутентифицирует пользователя по адресу электронной почты и паролю.

    :param email: Адрес электронной почты пользователя.
    :param password: Пароль пользователя.
    :return: Объект пользователя, если аутентификация успешна; иначе None.
    """
    user: Union[User, None] = await UsersDAO.find_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user