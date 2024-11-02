import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.settings import ROOT_DIR
from users.dao import UsersDAO
from users.models import User
from users.utils import verify_password
from bot.dao import TelegramUsersDAO

class BotSettings(BaseSettings):
    API_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(ROOT_DIR, '.env', '.env.bot'),
        extra='ignore',
    )
_bot_settings = BotSettings()

API_TOKEN = _bot_settings.API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    email = State()
    password = State()

@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.reply('Привет! Я ваш бот уведомлений.')

@dp.message(Command('bind'))
async def bind_email(message: Message, state: FSMContext):
    """Начинаем процесс привязки аккаунта"""
    await message.reply('Введите ваш email:')
    await state.set_state(Form.email)

@dp.message(F.text, Form.email)
async def process_email(message: Message, state: FSMContext):
    """Обрабатываем введенный email"""
    email = message.text

    await state.update_data(email=email)

    await message.reply('Введите пароль от аккаунта:')
    await state.set_state(Form.password)

@dp.message(F.text, Form.password)
async def process_password(message: Message, state: FSMContext):
    """Обрабатываем введенный пароль и проверяем пользователя в базе данных"""
    password = message.text

    await state.update_data(password=password)

    user_data = await state.get_data()
    email = user_data['email']
    password = user_data['password']

    user: User = await UsersDAO.find_one_or_none(email=email)
    if not user:
        await message.reply('Пользователь с таким email не найден.')
        await state.clear()
        return

    if not verify_password(password, user.password):
        await message.reply('Неверный пароль.')
        await state.clear() 
        return

    telegram_id = message.from_user.id
    await TelegramUsersDAO.add(telegram_id=telegram_id, user_id=user.id)

    await message.reply(f'Аккаунт {email} успешно привязан к вашему Telegram.')

    await state.clear()

@dp.message(F.text)
async def echo_message(message: Message):
    await message.reply(f'Вы написали: {message.text}')

async def notify_user(telegram_user_id: int, username: str):
    """Отправка уведомления пользователю"""
    notification_text = f'Пользователь `{username}`: Отправил вам сообщение!'
    await bot.send_message(telegram_user_id, notification_text)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
