from typing import Optional
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError

from core.settings import settings
from .exceptions import TokenExpiredException, CredentialsException


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.AUTH.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES

def get_password_hash(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.

    :param password: Пароль, который нужно захешировать.
    :return: Захешированный пароль.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли открытый пароль захешированному.

    :param plain_password: Открытый пароль.
    :param hashed_password: Захешированный пароль.
    :return: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Создает JWT с заданными данными и временем истечения.

    :param data: Данные, которые нужно закодировать в токен (например, ID пользователя).
    :return: Закодированный JWT.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({'exp': expire})  
    encode_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)  
    return encode_jwt

def verify_access_token(token: str) -> str:
    """
    Проверяет и декодирует JWT, возвращает ID пользователя.

    :param token: JWT, который нужно проверить.
    :return: ID пользователя из токена.
    :raises TokenExpiredException: Если токен истек.
    :raises CredentialsException: Если токен недействителен или не содержит ID пользователя.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('sub')  
        if not user_id:
            raise CredentialsException()  
        return user_id  
    except ExpiredSignatureError:
        raise TokenExpiredException()  
    except JWTError as e:
        print(e) 
        raise CredentialsException()