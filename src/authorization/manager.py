from typing import Optional
from authorization.utils import get_user_db
from fastapi_users import IntegerIDMixin, BaseUserManager
from fastapi import Request, Depends

from config import SECRET
from models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
