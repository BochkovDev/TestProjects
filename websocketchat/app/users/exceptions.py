from typing import Any, Dict
from fastapi import HTTPException, status


class TokenExpiredException(HTTPException):
    ''' Raises when the provided token has expired '''
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        detail = detail or 'Token has expired.'
        headers = {'WWW-Authenticate': 'Bearer'} if headers is None else headers
        super().__init__(status_code, detail, headers)

class TokenNotFoundException(HTTPException):
    ''' Raises when the provided token is not found '''
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        detail = detail or 'Token not found.'
        headers = {'WWW-Authenticate': 'Bearer'} if headers is None else headers
        super().__init__(status_code, detail, headers)

class CredentialsException(HTTPException):
    ''' Raises when can't validate user's credentials '''
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        detail = 'Could not validate credentials'
        headers = {'WWW-Authenticate': 'Bearer'} if headers is None else headers
        super().__init__(status_code, detail, headers)

class UserAlreadyExistsException(HTTPException):
    ''' Raises when trying to register an already existing user '''
    def __init__(self, status_code: int = status.HTTP_409_CONFLICT, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        detail = 'User already exists'
        headers = {'WWW-Authenticate': 'Bearer'} if headers is None else headers
        super().__init__(status_code, detail, headers)

class InvalidCredentialsException(HTTPException):
    ''' Raises when email or password is invalid '''
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        detail = detail or 'Invalid email or password'
        headers = {'WWW-Authenticate': 'Bearer'} if headers is None else headers
        super().__init__(status_code, detail, headers)

class PasswordMismatchException(HTTPException):
    ''' Raises when the provided password does not match the expected one '''
    def __init__(self, status_code: int = status.HTTP_409_CONFLICT, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        detail = detail or 'Password does not match.'
        headers = {'WWW-Authenticate': 'Bearer'} if headers is None else headers
        super().__init__(status_code, detail, headers)