from fastapi import APIRouter
from app.api.v1 import coursito
# These modules will be imported as they are implemented:
# from app.api.v1 import cogito, habitforge, timetunes, insightbridge, zetta, coachpilot

router = APIRouter()

# Include all app-specific routers
router.include_router(coursito.router)

# These routers will be included as they are implemented:
# router.include_router(cogito.router)
# router.include_router(habitforge.router)
# router.include_router(timetunes.router)
# router.include_router(insightbridge.router)
# router.include_router(zetta.router)
# router.include_router(coachpilot.router)

@router.get("/hello")
def read_hello():
    return {"message": "Hello, World!"}