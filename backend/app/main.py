from fastapi import FastAPI

# Minimal main: wire routers from the controllers package. Implementations
# (endpoints, models) live inside `backend/app/controllers/*`.

app = FastAPI(title="Winged BFF", version="0.1.0")

from .controllers import (
    users_router,
    sightings_router,
    achievements_router,
    maps_router,
    health_router,
)


app.include_router(users_router)
app.include_router(sightings_router)
app.include_router(achievements_router)
app.include_router(maps_router)
app.include_router(health_router)

