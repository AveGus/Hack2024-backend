from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select, update
from starlette.middleware.cors import CORSMiddleware

from models import User, Command
from api.case import router as case_router
from api.command import router as command_router
from api.question import router as question_router
from authorization.manager import get_user_manager
from authorization.base_config import auth_backend
from authorization.schemas import UserRead, UserCreate
from api.grade import router as grade_router
from services.database import get_async_session

#from api.session import router as session_router
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

#app.include_router(session_router, prefix="/api")


@app.get('/user')
async def read_user(user: User = Depends(current_user)):
    return {
        "email": user.email,
        "username": user.username,
        "is_jury": user.is_jury,
    }



from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from models import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import asyncio


class StartSessionRequest(BaseModel):
    command_id: int
    duration: int  # В секундах


# Фоновая задача для отслеживания окончания времени
async def session_timer(session_id: int, duration: int, session: AsyncSession = Depends(get_async_session)):
    await asyncio.sleep(duration)
    # Обновляем статус сессии
    result = await session.execute(
        select(Session)
        .where(Session.id == session_id)
    )
    await session.commit()
    print(f"Session {session_id} time is up.")


@app.post("/sessions/start")
async def start_session(request: StartSessionRequest, background_tasks: BackgroundTasks,
                        db: AsyncSession = Depends(get_async_session)):
    # Создаем новую запись сессии
    new_session = Session(
        command_id=request.command_id,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(seconds=request.duration),
        status="performing",
        duration=request.duration
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    stmt = update(Command).where(Command.id == request.command_id).values(status="Выступают")
    await db.execute(stmt)
    await db.commit()


    # Запускаем фоновую задачу для отслеживания времени
    background_tasks.add_task(session_timer, new_session.id, request.duration, db)

    return {
        "session_id": new_session.id,
        "command_id": new_session.command_id,
        "start_time": new_session.start_time,
        "end_time": new_session.end_time,
        "status": new_session.status
    }


@app.get("/sessions/{session_id}")
async def get_session_status(session_id: int, db: AsyncSession = Depends(get_async_session)):
    session = await db.get(Session, session_id)
    if not session:
        return {"error": "Session not found"}

    now = datetime.utcnow()
    remaining_time = (session.end_time - now).total_seconds()
    if remaining_time < 0:
        remaining_time = 0
        stmt = update(Command).where(Command.id == session.command_id).values(status="Не оценено")
        await db.execute(stmt)
        await db.commit()

    return {
        "session_id": session.id,
        "team_id": session.command_id,
        "remaining_time": remaining_time,
        "status": session.status
    }


@app.websocket("/ws/sessions/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, db: AsyncSession = Depends(get_async_session)):
    await websocket.accept()
    try:
        while True:
            session = await db.get(Session, session_id)
            if not session:
                await websocket.send_json({"error": "Session not found"})
                break

            now = datetime.utcnow()
            remaining_time = (session.end_time - now).total_seconds()
            if remaining_time < 0:
                remaining_time = 0

            await websocket.send_json({
                "session_id": session.id,
                "team_id": session.command_id,
                "remaining_time": remaining_time,
                "status": session.status
            })

            if session.status == "time_up":
                break

            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
