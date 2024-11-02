from fastapi import Request, HTTPException, status, Depends

from core.settings import settings
from .exceptions import TokenNotFoundException, CredentialsException
from .dao import UsersDAO
from .utils import verify_access_token


ACCESS_TOKEN_COOKIE = 'Access_Token'

def get_token(request: Request):
    """
    Извлекает токен доступа из куки.

    :param request: HTTP запрос.
    :raises TokenNotFoundException: Если токен не найден в куках.
    :return: Токен доступа.
    """
    token = request.cookies.get(ACCESS_TOKEN_COOKIE)
    if not token:
        raise TokenNotFoundException()
    return token

async def get_current_user(token: str = Depends(get_token)):
    """
    Получает текущего пользователя, проверяя токен доступа.

    :param token: Токен доступа, полученный из куки.
    :raises CredentialsException: Если токен недействителен.
    :raises HTTPException: Если пользователь не найден.
    :return: Объект пользователя.
    """
    user_id = verify_access_token(token)
    if not user_id:
        raise CredentialsException()

    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user