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
    """
    import time
    start_time = time.time()
    
    # Enforce minimum grid_size to avoid excessive computation
    if grid_size < 0.001:
        print(f"⚠️ grid_size {grid_size} too small, using minimum 0.001")
        grid_size = 0.001
    
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

    lats = np.arange(miny, maxy, grid_size)
    lons = np.arange(minx, maxx, grid_size)
    
    total_points = len(lats) * len(lons)
    print(f"📊 Zone: {zona_name}")
    print(f"📐 Grid: {len(lats)} x {len(lons)} = {total_points} potential points")
    print(f"🔍 Grid size: {grid_size} degrees (~{grid_size * 111:.0f}m)")

    # Limit maximum points to avoid timeout
    MAX_POINTS = 500
    if total_points > MAX_POINTS:
        # Adjust grid_size to stay under limit
        scale_factor = np.sqrt(total_points / MAX_POINTS)
        grid_size = grid_size * scale_factor
        lats = np.arange(miny, maxy, grid_size)
        lons = np.arange(minx, maxx, grid_size)
        print(f"⚠️ Too many points! Adjusting grid_size to {grid_size:.4f} ({len(lats)} x {len(lons)} = {len(lats) * len(lons)} points)")

    results = []
    points_processed = 0

    for la in lats:
        for lo in lons:
            pt = Point(lo, la)
            if zona_geom.contains(pt):  
                pred = predict_species(la, lo, timestamp)
                results.append(pred)
                points_processed += 1
    
    print(f"✅ Processed {points_processed} points inside zone in {time.time() - start_time:.2f}s")

    # Construir species_distributions
    species_distributions = []
    if results:
        species_list = [r["species"] for r in results[0]["species_probabilities"]]

        for species in species_list:
            areas = []
            max_prob = 0

            for r in results:
                sp = next(s for s in r["species_probabilities"] if s["species"] == species)
                prob = sp["probability"]

                if prob > 0.1:  # pintar solo si relevante
                    lat_c, lon_c = r["location"]["lat"], r["location"]["lon"]
                    cell = [
                        {"lat": lat_c - grid_size / 2, "lon": lon_c - grid_size / 2},
                        {"lat": lat_c - grid_size / 2, "lon": lon_c + grid_size / 2},
                        {"lat": lat_c + grid_size / 2, "lon": lon_c + grid_size / 2},
                        {"lat": lat_c + grid_size / 2, "lon": lon_c - grid_size / 2}
                    ]
                    areas.append({"polygon": cell, "probability": prob})

                    if prob > max_prob:
                        max_prob = prob

            if areas:
                species_distributions.append({
                    "species": species,
                    "max_probability": max_prob,
                    "areas": areas
                })

    return {
        "zone": zona_name,
        "location": {"lat": lat, "lon": lon},
        "datetime": timestamp.isoformat(),
        "species_distributions": species_distributions
    }