from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File

from api.v1.dealers.schemas import DealerPriceResponse
from api.v1.products.repositories import get_products
from core.db_helper import db_helper
from fastapi import Query

from services.dealers import imports_dealerprice

router = APIRouter(prefix="/dealers", tags=["Товары дилера"])


@router.post("/import-csv/", summary="Импорт данных дилеров из CSV")
async def imports_product_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await imports_dealerprice(file, session)
    return {"message": "CSV data imported successfully"}


@router.get(
    "/price/",
    response_model=DealerPriceResponse,
    summary="Получить товары дилеров",
)
async def get_all_dealer_price(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=10),
):
    return await get_products(session=session, page=page, size=size)


# @router.get(
#     "",
#     response_model=List[Dealer],
#     summary="Получить список дилеров",
# )
# async def get_all_dealer_price(
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
#     page: int = Query(ge=1, default=1),
#     size: int = Query(ge=1, le=100, default=10),
# ):
#     return await get_products(session=session, page=page, size=size)
