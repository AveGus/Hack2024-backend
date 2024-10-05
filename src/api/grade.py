from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from authorization.base_config import auth_backend
from authorization.manager import get_user_manager
from models import User
from models.grade import grade
from schemas.grade import GradeSchema
from services.database import get_async_session

router = APIRouter(
    tags=["grade"],
    prefix="/grade",
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.post("/")
async def set_grade(gradeschema: list[GradeSchema], user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    global grades
    if user.is_jury:
        for i in gradeschema:
            grades = grade(command_id=i.command_id, user_id=user.id, question_id=i.question_id, score=i.score)
            session.add(grades)
            await session.commit()
        return grades
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


@router.get('/command/{command_id}')
async def get_grades(command_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(grade).where(grade.command_id == command_id)
    result = await session.execute(stmt)
    return result.scalars().all()

