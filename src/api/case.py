from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.database import get_async_session
from schemas import Case
from schemas.Case import CaseCreateSchema, CaseType
from services.case import create_case as create_case_service, get_all_case

router = APIRouter(
    prefix="/case",
    tags=["case"],
)


@router.post("/", response_model=CaseType)
async def create_case(new_case: CaseCreateSchema, session: AsyncSession = Depends(get_async_session)):
    case = await create_case_service(new_case, session)
    return case


@router.get("/", response_model=list[CaseType])
async def get_cases(session: AsyncSession = Depends(get_async_session)):
    all_cases = await get_all_case(session)
    return all_cases
