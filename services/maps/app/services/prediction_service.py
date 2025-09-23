import pandas as pd
import numpy as np
from shapely.geometry import Point
from datetime import datetime

# Importa lo que guardaste en predictor.py
from app.models.predictor import model, species_cols, feature_cols, zonas
from app.data.species_mapping import species_mapping 


def predict_species(lat: float, lon: float, timestamp: datetime):
    """
    Recibe lat/lon y un timestamp.
    Devuelve zona detectada y probabilidad de cada especie.
    """

    # 1. Determinar zona por polígono
    p = Point(lon, lat)
    zona = next(
        (row["name"] for _, row in zonas.iterrows() if row.geometry.contains(p)),
        "Fuera de zonas"
    )

    # 2. Extraer día y mes
    day, month = timestamp.day, timestamp.month

    # 3. Construir features raw
    raw = {
        "lat_bin": lat,
        "lon_bin": lon,
        "elevation": 10,   # 🔧 puedes cambiar por valor real si lo tienes
        "day_sin": np.sin(2*np.pi*day/31),
        "day_cos": np.cos(2*np.pi*day/31),
        "month_sin": np.sin(2*np.pi*month/12),
        "month_cos": np.cos(2*np.pi*month/12),
    }

    # 4. Asegurar que las columnas coinciden con el orden del entrenamiento
    features = pd.DataFrame(
        [[raw[col] for col in feature_cols]],
        columns=feature_cols
    )

    # 5. Predecir probabilidades multi-label
    y_pred_list = [est.predict_proba(features)[:, 1] for est in model.estimators_]
    y_pred_proba = np.vstack(y_pred_list).T  # shape (1, n_especies)

    # 6. Mapear especie → probabilidad
    results = [
        {
            "species": species_mapping.get(str(species), str(species)),  # Mapear a nombre científico si es posible
            "probability": float(prob)
        }
        for species, prob in zip(species_cols, y_pred_proba[0])
    ]

    # 7. Ordenar por probabilidad descendente
    results = sorted(results, key=lambda x: x["probability"], reverse=True)

    # 8. Retornar en formato esperado
    return {
        "zone": zona,
        "location": {"lat": lat, "lon": lon},
        "datetime": timestamp.isoformat(),
        "species_probabilities": results
    }