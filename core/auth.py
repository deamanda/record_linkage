from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from models import User
from .config import settings
from .usermanager import get_user_manager


# Cookie settings
cookie_transport = CookieTransport(
    cookie_name="Prosept", cookie_max_age=3600 * 24 * 7
)


# JWT settings
def get_jwt_strategy() -> JWTStrategy:
    """JWT token settings"""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600 * 24 * 7)


# Base auth settings
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Current user settings
current_user = fastapi_users.current_user(active=True)
