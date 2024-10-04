from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Command
from schemas.command import CreateCommand, CommandType
from services.database import get_async_session


async def create_command(new_command: CreateCommand, session: AsyncSession = Depends(get_async_session)
                         ) -> Command:
    command = Command(**new_command.dict())
    session.add(command)
    await session.flush()
    await session.commit()
    await session.refresh(command)
    return command


async def get_all_commands(session: AsyncSession = Depends(get_async_session)
                           ) -> list[Command]:
    stmt = select(Command)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_command_by_id(id: int, session: AsyncSession = Depends(get_async_session)) -> Command:
    stmt = select(Command).where(Command.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
