from main_bot import notify_user
from bot.models import TelegramUser
from bot.dao import TelegramUsersDAO


async def send_telegram_notification(user_id: int, username: str):
    telegram_user: TelegramUser = await TelegramUsersDAO.find_one_or_none(user_id=user_id)
    if not telegram_user:
        return
    await notify_user(telegram_user.telegram_id, username)