from typing import Union, Sequence, Type

from sqlalchemy import update as sqlalchemy_update 
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import Base
from db.sessions import connection


class BaseDAO:
    model: Type[Base]

    @classmethod
    @connection
    async def find_one_or_none(cls, *, session: AsyncSession, **filter_by) -> Union[Type[Base], None]:
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod
    @connection
    async def find_all(cls, *, session: AsyncSession, **filter_by) -> Sequence[Type[Base]]:
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    @connection(commit=True)
    async def add(cls, *, session: AsyncSession, **data) -> None:
        new_instance = cls.model(**data)
        session.add(new_instance)
    
    @classmethod
    @connection(commit=True)
    async def delete(cls, *, session: AsyncSession, **delete_by) -> None:
        conditions = [getattr(cls.model, k) == v for k, v in delete_by.items()]

        if conditions:
            query = sqlalchemy_delete(cls.model).where(*conditions)
            await session.execute(query)
    
    @classmethod
    @connection(commit=True)
    async def update(cls, *, session: AsyncSession, filter_by: dict, update_data: dict) -> None:
        conditions = [getattr(cls.model, k) == v for k, v in filter_by.items()]
        if conditions:
            query = (
                sqlalchemy_update(cls.model)
                .where(*conditions)
                .values(**update_data)
            )
            await session.execute(query)
