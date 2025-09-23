from fastapi import APIRouter
from app.models.schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import predict_species

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
    zonas = gpd.read_file("services/maps/app/data/barriosbaq.geojson").to_crs(epsg=4326)
    return zonas.__geo_interface__