from typing import List

from fastapi import APIRouter, Response, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

from core.jinja2 import templates
from core.email import verify_confirmation_token
from services.tasks import send_email_with_verification_link_task
from services.email import send_email_with_verification_link
from .auth import authenticate_user
from .utils import get_password_hash, create_access_token
from .dao import UsersDAO
from .models import User
from .schemas import UserRegister as SUserRegister
from .schemas import UserAuth as SUserAuth
from .schemas import UserRead as SUserRead
from .exceptions import (
    UserAlreadyExistsException, 
    InvalidCredentialsException,
    PasswordMismatchException,
)


router = APIRouter(prefix='/auth', tags=['Auth'])

ACCESS_TOKEN_COOKIE = 'Access_Token'

@router.get('/', response_class=HTMLResponse, summary='Страница авторизации и регистрации')
async def root(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})

@router.post('/register/')
async def register(user_data: SUserRegister, request: Request) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException()
    
    if user_data.password != user_data.password_check:
        raise PasswordMismatchException()
    
    user_data.password = get_password_hash(user_data.password)
    await UsersDAO.add(**user_data.model_dump(exclude={'password_check'}))

    abs_url = str(request.url_for('confirm'))
    send_email_with_verification_link_task.delay(abs_url, user_data.email)

    return {'message': 'Пользователь успешно зарегестрирован!'}

@router.get('/users', response_model=List[SUserRead])
async def get_users():
    users: List[User] = await UsersDAO.find_all()
    return [{'id': user.id, 'username': user.username} for user in users]

@router.get('/confirm/')
async def confirm(token: str, request: Request):
    email = verify_confirmation_token(token)
    await UsersDAO.update(filter_by={'email': email}, update_data={'is_verified': True})
    abs_login_url = str(request.url_for('root'))
    return RedirectResponse(abs_login_url)

@router.post('/login/')
async def login(response: Response, user_data: SUserAuth) -> dict:
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if user is None:
        raise InvalidCredentialsException()
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь не подтвердил email')
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(ACCESS_TOKEN_COOKIE, access_token, httponly=True)
    return {ACCESS_TOKEN_COOKIE: access_token, 'Refresh_Token': None, 'Token_Type': 'Bearer'}

@router.post('/logout/')
async def logout(response: Response):
    response.delete_cookie(ACCESS_TOKEN_COOKIE)
    return {'message': 'Пользователь успешно вышел из системы'}
