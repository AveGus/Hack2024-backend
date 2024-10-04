from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
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


@router.post("/{command_id}")
async def set_grade(gradeschema: GradeSchema, user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    grades = grade(command_id=gradeschema.command_id,
                   user_id=user.id, question_id=gradeschema.question_id, score=gradeschema.score)
    session.add(grades)
    session.commit()
    return grades
