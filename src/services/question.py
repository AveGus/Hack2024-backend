from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.question import question
from schemas.question import CreateQuestion
from services.database import get_async_session


async def create_question(new_question: CreateQuestion,session: AsyncSession = Depends(get_async_session)
                          ) -> question:
    n_question = question(**new_question.dict())
    session.add(n_question)
    await session.commit()
    await session.refresh(n_question)
    return n_question

async def get_all_questions_by_case_id(case_id: int,session: AsyncSession = Depends(get_async_session)
                                       ) -> list[question]:
    questions = await session.execute(select(question).where(question.case_id == case_id))
    return questions.scalars().all()