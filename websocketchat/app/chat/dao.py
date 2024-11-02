from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.sessions import connection
from dao.base import BaseDAO
from .models import Message


class MessagesDAO(BaseDAO):
    model: Message = Message

    @classmethod
    @connection(commit=True)
    async def get_messages_between_users(cls, user_id_1: int, user_id_2: int,  *, session: AsyncSession):
        query = select(cls.model).filter(
            or_(
                and_(cls.model.sender_id == user_id_1, cls.model.recipient_id == user_id_2),
                and_(cls.model.sender_id == user_id_2, cls.model.recipient_id == user_id_1)
            )
        ).order_by(cls.model.id)
        result = await session.execute(query)
        return result.scalars().all()