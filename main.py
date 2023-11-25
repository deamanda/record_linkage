import uvicorn
from fastapi import FastAPI
from api.v1.routing.products import router as router_v1


app = FastAPI()
app.include_router(router_v1, prefix="/api_v1")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
