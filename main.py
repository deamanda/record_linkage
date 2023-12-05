import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.v1.users.schemas import UserRead, UserCreate, UserUpdate
from core.auth import auth_backend, fastapi_users, current_user
from core.config import settings
from api.v1 import router as router_v1


app = FastAPI(
    title="Prosept - разметка товаров",
    description="Cервис для полуавтоматической разметки товаров",
    openapi_url="/v1/openapi.json",
    docs_url="/docs/v1",
    version="v1",
)
app.include_router(
    router=router_v1,
    prefix=settings.api_prefix,
    dependencies=[Depends(current_user)],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["Аутентификация"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["Аутентификация"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/users",
    tags=["Пользователь"],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
