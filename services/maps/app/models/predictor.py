import joblib
import geopandas as gpd
import pickle
import warnings

warnings.filterwarnings('ignore')

# Se carga 1 sola vez al iniciar el servidor (mejor performance)
try:
    print("🔄 Cargando modelo de ML...")
    # Intentar cargar con joblib primero
    model = joblib.load("app/data/modelo_multilabel.pkl")
    species_cols = joblib.load("app/data/species_columns.pkl")
    feature_cols = joblib.load("app/data/feature_columns.pkl")
    print("✅ Modelo cargado exitosamente")
except Exception as e:
    print(f"⚠️ Error con joblib: {e}")
    print("🔄 Intentando cargar con pickle...")
    try:
        # Intentar con pickle directo
        with open("app/data/modelo_multilabel.pkl", "rb") as f:
            model = pickle.load(f)
        with open("app/data/species_columns.pkl", "rb") as f:
            species_cols = pickle.load(f)
        with open("app/data/feature_columns.pkl", "rb") as f:
            feature_cols = pickle.load(f)
        print("✅ Modelo cargado con pickle")
    except Exception as e2:
        print(f"❌ Error crítico al cargar el modelo: {e2}")
        print("💡 El modelo necesita ser reentrenado con la versión actual de scikit-learn")
        raise

try:
    zonas = gpd.read_file("app/data/barriosbaq.geojson").to_crs(epsg=4326)
    print(f"✅ Zonas cargadas: {len(zonas)} polígonos")
except Exception as e:
    print(f"❌ Error al cargar zonas: {e}")
    raise