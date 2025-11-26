import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from shapely.geometry import Point, Polygon
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
    
def predict_distribution(lat: float, lon: float, timestamp: datetime,
                         radius: float = 1000, grid_size: float = 0.002,
                         levels=(0.1, 0.3, 0.5, 0.7)):
    """
    Genera superficies suavizadas de distribución de especies usando interpolación.
    """

    # Paso 1: generar puntos alrededor
    delta = radius / 111000.0  # conversión m → grados (aprox)
    lats = np.arange(lat - delta, lat + delta, grid_size)
    lons = np.arange(lon - delta, lon + delta, grid_size)

    coords = []
    Zs = {}

    for la in lats:
        for lo in lons:
            punto = predict_species(la, lo, timestamp)
            for sp in punto["species_probabilities"]:
                species = sp["species"]
                prob = sp["probability"]
                if species not in Zs:
                    Zs[species] = []
                Zs[species].append((lo, la, prob))  # cuidado: shapely usa X=lon, Y=lat
            coords.append((lo, la))

    # Paso 2: grilla uniforme para interpolación
    grid_x, grid_y = np.meshgrid(
        np.linspace(min(lons), max(lons), 50),
        np.linspace(min(lats), max(lats), 50)
    )

    species_distributions = []

    for species, points in Zs.items():
        # Convertir a arrays
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]

        # Paso 3: interpolar con 'linear'
        grid_z = griddata((xs, ys), zs, (grid_x, grid_y), method="linear", fill_value=0)

        # Paso 4: extraer polígonos por niveles de probabilidad
        areas = []
        for level in levels:
            mask = grid_z >= level
            if not mask.any():
                continue

            # Extraer contorno aproximado
            indices = np.argwhere(mask)
            if len(indices) < 3:
                continue

            coords_poly = []
            for idx in indices:
                y_idx, x_idx = idx
                coords_poly.append({
                    "lat": float(grid_y[y_idx, x_idx]),
                    "lon": float(grid_x[y_idx, x_idx])
                })

            try:
                poly = Polygon([(c["lon"], c["lat"]) for c in coords_poly]).convex_hull
                areas.append({
                    "polygon": [{"lat": y, "lon": x} for x, y in poly.exterior.coords],
                    "probability": level
                })
            except Exception:
                pass

        if areas:
            max_prob = float(np.max(zs))
            species_distributions.append({
                "species": species,
                "max_probability": max_prob,
                "areas": areas
            })

    return {
        "zone": "Distribución local",
        "location": {"lat": lat, "lon": lon},
        "datetime": timestamp.isoformat(),
        "species_distributions": species_distributions
    }

def predict_distribution_in_zone(lat: float, lon: float, timestamp: datetime, grid_size: float = 0.001):
    """
    Predice distribución de especies dentro de la zona poligonal detectada.
    Optimizado para procesamiento por lotes (vectorizado).
    """
    p = Point(lon, lat)

    # Identificar la zona
    zona_row = next(
        ((row["name"], row.geometry) for _, row in zonas.iterrows() if row.geometry.contains(p)),
        None
    )

    if not zona_row:
        return {
            "zone": "Fuera de zonas",
            "location": {"lat": lat, "lon": lon},
            "datetime": timestamp.isoformat(),
            "species_distributions": []
        }

    zona_name, zona_geom = zona_row
    minx, miny, maxx, maxy = zona_geom.bounds  

    # Generar grilla de puntos
    lats = np.arange(miny, maxy, grid_size)
    lons = np.arange(minx, maxx, grid_size)
    
    # Crear lista de puntos válidos dentro del polígono
    valid_points = []
    for la in lats:
        for lo in lons:
            if zona_geom.contains(Point(lo, la)):
                valid_points.append((la, lo))
    
    if not valid_points:
        return {
            "zone": zona_name,
            "location": {"lat": lat, "lon": lon},
            "datetime": timestamp.isoformat(),
            "species_distributions": []
        }

    # Preparar features para predicción en lote
    day, month = timestamp.day, timestamp.month
    day_sin = np.sin(2*np.pi*day/31)
    day_cos = np.cos(2*np.pi*day/31)
    month_sin = np.sin(2*np.pi*month/12)
    month_cos = np.cos(2*np.pi*month/12)
    
    # Crear DataFrame con todos los puntos
    df_points = pd.DataFrame(valid_points, columns=['lat_bin', 'lon_bin'])
    df_points['elevation'] = 10
    df_points['day_sin'] = day_sin
    df_points['day_cos'] = day_cos
    df_points['month_sin'] = month_sin
    df_points['month_cos'] = month_cos
    
    # Asegurar orden de columnas
    features = df_points[feature_cols]
    
    # Predecir probabilidades (vectorizado)
    # model.predict_proba devuelve lista de arrays (n_samples, 2) por cada estimador
    # Queremos shape (n_samples, n_species)
    y_pred_list = [est.predict_proba(features)[:, 1] for est in model.estimators_]
    y_pred_proba = np.vstack(y_pred_list).T  # shape (n_samples, n_species)
    
    # Procesar resultados
    species_distributions = []
    
    # Iterar por especie (columna)
    for i, species_code in enumerate(species_cols):
        species_name = species_mapping.get(str(species_code), str(species_code))
        probs = y_pred_proba[:, i]
        
        # Filtrar puntos con probabilidad relevante (> 0.1)
        mask = probs > 0.1
        if not np.any(mask):
            continue
            
        max_prob = float(np.max(probs))
        areas = []
        
        # Obtener índices de puntos relevantes
        relevant_indices = np.where(mask)[0]
        
        for idx in relevant_indices:
            prob = float(probs[idx])
            lat_c, lon_c = valid_points[idx]
            
            # Crear celda cuadrada
            half_grid = grid_size / 2
            cell = [
                {"lat": lat_c - half_grid, "lon": lon_c - half_grid},
                {"lat": lat_c - half_grid, "lon": lon_c + half_grid},
                {"lat": lat_c + half_grid, "lon": lon_c + half_grid},
                {"lat": lat_c + half_grid, "lon": lon_c - half_grid}
            ]
            areas.append({"polygon": cell, "probability": prob})
            
        species_distributions.append({
            "species": species_name,
            "max_probability": max_prob,
            "areas": areas
        })
        
    # Ordenar especies por probabilidad máxima
    species_distributions.sort(key=lambda x: x["max_probability"], reverse=True)

    return {
        "zone": zona_name,
        "location": {"lat": lat, "lon": lon},
        "datetime": timestamp.isoformat(),
        "species_distributions": species_distributions
    }