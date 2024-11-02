from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import TelegramUser
from db.database import Base, str_uniq


class User(Base):
    username: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    telegram_user: Mapped['TelegramUser'] = relationship('TelegramUser', uselist=False, back_populates='user')