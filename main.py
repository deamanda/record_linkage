import uvicorn
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, File, UploadFile
from api.v1.routing.products import router as router_v1
from api.v1.services.products import imports_csv
from core.db_helper import db_helper
from models import Product

app = FastAPI()
app.include_router(router_v1, prefix="/api_v1")


@app.post("/import-csv/")
async def import_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await imports_csv(file, Product, session)
    return {"message": "CSV data imported successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
