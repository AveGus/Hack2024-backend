# import asyncio
# from datetime import datetime, timedelta
#
# from fastapi import Depends, BackgroundTasks
# from pydantic import BaseModel
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette.websockets import WebSocket
#
# from models import Session
# from services.database import get_async_session
#
#
# class StartSessionRequest(BaseModel):
#     team_id: int
#     duration: int  # В секундах
#
#
# # Фоновая задача для отслеживания окончания времени
# async def session_timer(session_id: int, duration: int, session: AsyncSession = Depends(get_async_session)):
#     await asyncio.sleep(duration)
#     # Обновляем статус сессии
#     result = await session.execute(
#         Session.__table__.update()
#         .where(Session.id == session_id)
#         .values(status="time_up")
#     )
#     await session.commit()
#     print(f"Session {session_id} time is up.")
#
#
# @app.post("/sessions/start")
# async def start_session(request: StartSessionRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
#     # Создаем новую запись сессии
#     new_session = Session(
#         command_id=request.team_id,
#         start_time=datetime.utcnow(),
#         end_time=datetime.utcnow() + timedelta(seconds=request.duration),
#         status="performing",
#         duration=request.duration
#     )
#     db.add(new_session)
#     await db.commit()
#     await db.refresh(new_session)
#
#     # Запускаем фоновую задачу для отслеживания времени
#     background_tasks.add_task(session_timer, new_session.id, request.duration, db)
#
#     return {
#         "session_id": new_session.id,
#         "team_id": new_session.team_id,
#         "start_time": new_session.start_time,
#         "end_time": new_session.end_time,
#         "status": new_session.status
#     }
#
# @app.websocket("/ws/sessions/{session_id}")
# async def websocket_endpoint(websocket: WebSocket, session_id: int, db: AsyncSession = Depends(get_db)):
#     await websocket.accept()
#     try:
#         while True:
#             session = await db.get(Session, session_id)
#             if not session:
#                 await websocket.send_json({"error": "Session not found"})
#                 break
#
#             now = datetime.utcnow()
#             remaining_time = (session.end_time - now).total_seconds()
#             if remaining_time < 0:
#                 remaining_time = 0
#
#             await websocket.send_json({
#                 "session_id": session.id,
#                 "team_id": session.team_id,
#                 "remaining_time": remaining_time,
#                 "status": session.status
#             })
#
#             if session.status == "time_up":
#                 break
#
#             await asyncio.sleep(1)
#     except WebSocketDisconnect:
#         print(f"WebSocket disconnected for session {session_id}")