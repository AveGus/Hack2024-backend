from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Case
from schemas.Case import CaseCreateSchema, CaseType
from services.database import get_async_session


async def create_case(new_case: CaseCreateSchema, session: AsyncSession = Depends(get_async_session)
) -> Case:
    case = Case(**new_case.dict())
    session.add(case)
    await session.flush()
    await session.commit()
    await session.refresh(case)
    return case


async def get_all_case(session: AsyncSession = Depends(get_async_session)
                       ):
    stmt = select(Case)
    result = await session.execute(stmt)
    return result.scalars().all()
