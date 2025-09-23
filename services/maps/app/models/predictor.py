import joblib
import geopandas as gpd



# Se carga 1 sola vez al iniciar el servidor (mejor performance)
model = joblib.load("app/data/modelo_multilabel.pkl")
species_cols = joblib.load("app/data/species_columns.pkl")
feature_cols = joblib.load("app/data/feature_columns.pkl") 



zonas = gpd.read_file("app/data/barriosbaq.geojson").to_crs(epsg=4326)