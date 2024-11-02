from sqlalchemy import ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base, str_uniq


class TelegramUser(Base):
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    user: Mapped['User'] = relationship(back_populates='telegram_user', single_parent=True)