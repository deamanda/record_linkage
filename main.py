import uvicorn
from fastapi import FastAPI
from routing.v1.products import router as router_v1


app = FastAPI()
app.include_router(router_v1, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
