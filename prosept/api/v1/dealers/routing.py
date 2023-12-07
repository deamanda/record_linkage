from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File, Query

from api.v1.dealers.depends import dealerprice_by_id
from api.v1.dealers.repositories import (
    get_dealerprices,
    get_dealers,
)
from api.v1.dealers.schemas import (
    DealerPrice,
    Dealer,
    DealerPriceView,
)
from core.db_helper import db_helper
from fastapi_pagination import LimitOffsetPage, paginate

from services.import_csv.dealers import imports_dealerprice, imports_dealers
from services.choices import DealerPriceStatus, SortedField

router = APIRouter(prefix="/dealers", tags=["Товары дилера"])


@router.post(
    "/import-csv/dealerprices",
    summary="Импорт данных дилеров из CSV",
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
    response_model=DealerPriceView,
    summary="Получить товар дилера",
)
async def get_dealer_price(
    dealerprice: DealerPrice = Depends(dealerprice_by_id),
):
    return dealerprice


@router.get(
    "/price",
    response_model=LimitOffsetPage[DealerPriceView],
    summary="Получить товары дилеров",
)
async def get_all_dealer_price(
    dealer_name: str = Query(default=None, description="Dealer"),
    search_query: str = Query(default=None, description="Search"),
    status: DealerPriceStatus = Query(
        default=None, description="Matching status"
    ),
    sort_by: SortedField = Query(default=None, description="Sort by"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_dealerprices(
        session=session,
        sort_by=sort_by,
        status=status,
        search_query=search_query,
        dealer_name=dealer_name,
    )
    return paginate(value)


@router.get(
    "",
    response_model=LimitOffsetPage[Dealer],
    summary="Получить список дилеров",
)
async def get_all_dealers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_dealers(session=session)
    return paginate(value)
