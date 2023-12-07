from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    models,
    schemas,
)

from core.db_helper import db_helper
from models.users import User
from .config import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User Experience Settings"""

    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        """Action after registration"""
        print(f"User {user.id} has registered.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """Action when creating a user"""
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(db_helper.get_user_db)):
    yield UserManager(user_db)
