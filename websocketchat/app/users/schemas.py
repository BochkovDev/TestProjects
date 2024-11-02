from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    username: str = Field(..., description='Никнейм')
    email: EmailStr = Field(..., description='Email')
    password: str = Field(..., min_length=8, max_length=50, description='Пароль')
    password_check: str = Field(..., min_length=8, max_length=50, description='Пароль')

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description='Email')
    password: str = Field(..., min_length=8, max_length=50, description='Пароль')

class UserRead(BaseModel):
    id: int = Field(..., description="ID")
    username: str = Field(..., description="Никнейм")
