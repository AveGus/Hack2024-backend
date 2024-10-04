from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.question import create_question
from schemas.question import CreateQuestion, QuestionType
from services.database import get_async_session
from services.question import get_all_questions_by_case_id as get_all_questions_router

router = APIRouter(
    tags=["question"],
    prefix="/question",
)


@router.get("/", response_model=list[QuestionType])
async def get_question_by_case_id(case_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await get_all_questions_router(case_id, session)
    return result


@router.post('/', response_model=QuestionType)
async def create_question_by_case_id(new_question: CreateQuestion, session: AsyncSession = Depends(get_async_session)):
    result = await create_question(new_question, session)
    return result
