import uvicorn
from fastapi import FastAPI

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

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
