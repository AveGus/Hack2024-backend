from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware

from models import User
from api.case import router as case_router
from api.command import router as command_router
from api.question import router as question_router
from authorization.manager import get_user_manager
from authorization.base_config import auth_backend
from authorization.schemas import UserRead, UserCreate
from api.grade import router as grade_router
app = FastAPI()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(case_router, prefix="/api")
app.include_router(command_router, prefix="/api")
app.include_router(question_router, prefix="/api")
app.include_router(grade_router, prefix="/api")