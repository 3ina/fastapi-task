from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from app.selectors.airportSelector import AirportSelector
from app.core.dependencies import get_airport_selector

router = APIRouter(prefix="/airports", tags=["Airports"])


class AirportResponse(BaseModel):
    id: int
    name: str
    code: str


class GetResponse(BaseModel):
    airports: list[AirportResponse]
    total: int
    page: int
    size: int


@router.get("/", status_code=status.HTTP_200_OK, response_model=GetResponse)
async def get(
    page: int = Query(1, ge=1, description="Page Number"),
    size: int = Query(10, ge=1, le=100, description="Item per page"),
    airports_selector: AirportSelector = Depends(get_airport_selector),
):
    return await airports_selector.get_airports(page=page, size=size)
