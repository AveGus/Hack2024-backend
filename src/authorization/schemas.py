from typing import Optional

from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    is_jury: Optional[bool] = False
    project_id: Optional[int]


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    is_jury: bool = False
    project_id: Optional[int]


class Config:
    orm_mode = True
