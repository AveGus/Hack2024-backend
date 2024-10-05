from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

import fastapi_users

from authorization.base_config import auth_backend
from authorization.manager import get_user_manager
from models import Command, User
from schemas.command import CreateCommand, CommandType
from services.command import (create_command,
                              get_all_commands)
from services.command import get_command_by_id as get_command_by_id_router
from services.database import get_async_session

router = APIRouter(
    prefix="/commands",
    tags=["commands"],
)


@router.post('/', response_model=CommandType)
async def create_new_command(new_command: CreateCommand, session: AsyncSession = Depends(get_async_session)):
    command = await create_command(new_command, session)
    return command


@router.get('/', response_model=list[CommandType])
async def get_all_command(session: AsyncSession = Depends(get_async_session)):
    commands = await get_all_commands(session)
    return commands


@router.get('/{id}', response_model=CommandType)
async def get_command_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    command = await get_command_by_id_router(id, session)
    return command
