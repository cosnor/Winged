from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Minimal main: wire routers from the controllers package. Implementations
# (endpoints, models) live inside `backend/app/controllers/*`.

app = FastAPI(title="Winged BFF", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .controllers import (
    users_router,
    sightings_router,
    achievements_router,
    maps_router,
    ml_worker_router,
    health_router,
)


app.include_router(users_router)
app.include_router(sightings_router)
app.include_router(achievements_router)
app.include_router(maps_router)
app.include_router(ml_worker_router)
app.include_router(health_router)

