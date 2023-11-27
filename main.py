import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.v1 import router as router_v1

app = FastAPI(
    title="Prosept - разметка товаров",
    description="Cервис для полуавтоматической разметки товаров",
    openapi_url="/v1/openapi.json",
    docs_url="/docs/v1",
    version="v1",
)
app.include_router(router=router_v1, prefix=settings.api_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
