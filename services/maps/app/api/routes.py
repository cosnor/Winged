from fastapi import APIRouter
from datetime import datetime
from app.models.schemas import PredictionRequest, PredictionResponse, DistributionRequest, DistributionZoneRequest
from app.services.prediction_service import predict_species, predict_distribution, predict_distribution_in_zone

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    """
    Endpoint principal: recibe lat/lon + timestamp y devuelve
    probabilidades de todas las especies en esa zona.
    """
    return predict_species(req.latitude, req.longitude, req.timestamp)


@router.get("/zones")
def get_zones():
    """
    (Opcional) Devuelve todas las zonas como GeoJSON,
    para que el frontend pueda dibujarlas en el mapa.
    """
    import geopandas as gpd
    zonas = gpd.read_file("app/data/barriosbaq.geojson").to_crs(epsg=4326)
    return zonas.__geo_interface__

@router.post("/distribution")
def distribution(request: DistributionRequest):
    dt = datetime.fromisoformat(request.datetime.replace("Z", "+00:00"))
    return predict_distribution(
        lat=request.lat,
        lon=request.lon,
        timestamp=dt,
        radius=request.radius,
        grid_size=request.grid_size
    )
    
@router.post("/distribution-zone")
def distribution_zone(request: DistributionZoneRequest):
    dt = datetime.fromisoformat(request.datetime.replace("Z", "+00:00"))
    return predict_distribution_in_zone(
        lat=request.lat,
        lon=request.lon,
        timestamp=dt,
        grid_size=request.grid_size
    )
