from dao.base import BaseDAO
from .models import TelegramUser


class TelegramUsersDAO(BaseDAO):
    model = TelegramUser