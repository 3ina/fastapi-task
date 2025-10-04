from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_flight_selector
from app.external_apis.flightAdaptor import NormalizedFlight
from app.selectors.flightSelector import FlightSelector

router = APIRouter(prefix="/flights", tags=["Flights"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[NormalizedFlight],
)
async def get_flights(flight_selector: FlightSelector = Depends(get_flight_selector)):
    # TODO : add filters and search
    return await flight_selector.get_all_normalized_flights()
