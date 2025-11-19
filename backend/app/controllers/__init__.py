"""Controllers package for the backend app.

Each controller module exposes an `APIRouter` named `router`. We re-export
the routers here so other modules (like `main`) can import them from a
single place: `from .controllers import users_router`.
"""

from .users import router as users_router
from .sightings import router as sightings_router
from .achievements import router as achievements_router
from .maps import router as maps_router
from .health import router as health_router
from .ml_worker import router as ml_worker_router
__all__ = [
	"users_router",
	"sightings_router",
	"achievements_router",
	"maps_router",
	"ml_worker_router",
	"health_router",
]
