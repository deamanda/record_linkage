from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File

from api.v1.dealers.depends import dealerprice_by_id
from api.v1.dealers.repositories import (
    get_dealerprices,
    get_dealer,
)
from api.v1.dealers.schemas import (
    DealerPriceResponse,
    DealerResponse,
    DealerPrice,
)
from core.db_helper import db_helper
from fastapi import Query

from services.dealers import imports_dealerprice, imports_dealers

router = APIRouter(prefix="/dealers", tags=["Товары дилера"])


@router.post(
    "/import-csv/dealerprices", summary="Импорт данных дилеров из CSV"
)
async def imports_dealer_prices_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await imports_dealerprice(file, session)
    return {"message": "CSV data imported successfully"}


@router.post("/import-csv/dealers", summary="Импорт дилеров из CSV")
async def imports_dealers_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await imports_dealers(file, session)
    return {"message": "CSV data imported successfully"}


@router.get(
    "/price/{dealerprice_id}/",
    response_model=DealerPrice,
    summary="Получить товар дилера",
)
async def get_dealer_price(
    dealerprice: DealerPrice = Depends(dealerprice_by_id),
):
    return dealerprice


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
    return await get_dealerprices(session=session, page=page, size=size)


@router.get(
    "",
    response_model=DealerResponse,
    summary="Получить список дилеров",
)
async def get_all_dealers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=10),
):
    return await get_dealer(session=session, page=page, size=size)
