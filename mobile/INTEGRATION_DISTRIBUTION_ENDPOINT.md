# Integración del Endpoint de Distribución de Especies

## 📋 Resumen de Cambios

Se ha integrado el endpoint `/distribution` del servicio de mapas para reemplazar los datos simulados en la pantalla `nearbyScreen` con información real de distribución de especies.

## 🗂️ Archivos Modificados/Creados

### 1. **`mobile/services/mapsService.ts`** (NUEVO)
Servicio centralizado para comunicarse con el API de mapas:
- `getDistribution()`: Obtiene la distribución de especies en un radio determinado
- `getZones()`: Obtiene las zonas geográficas de Barranquilla
- Manejo automático de URLs según plataforma (Android/iOS/Web)
- Tipado completo con TypeScript

### 2. **`mobile/app/(app)/map/nearby/index.tsx`** (MODIFICADO)
Pantalla actualizada con datos reales:
- ✅ Carga automática de datos al obtener ubicación del usuario
- ✅ Botón de recarga para actualizar la distribución
- ✅ Indicador de carga mientras se obtienen los datos
- ✅ Mensajes de error descriptivos
- ✅ Alertas informativas con el número de especies encontradas

### 3. **`mobile/.env`** (MODIFICADO)
Agregada variable de entorno:
```env
EXPO_PUBLIC_MAPS_URL=http://10.0.2.2:8004
```

## 🚀 Cómo Usar

### 1. Iniciar el Servicio de Mapas

Asegúrate de que el servicio de mapas esté corriendo:

```powershell
# Opción 1: Solo el servicio de mapas
docker-compose up maps

# Opción 2: Todos los servicios
docker-compose up
```

Verifica que esté disponible en: `http://localhost:8004`

### 2. Configurar Variables de Entorno

Para **emulador Android**: Ya está configurado con `http://10.0.2.2:8004`

Para **dispositivo físico**: Necesitas exponer el puerto con ngrok:
```powershell
ngrok http 8004
```
Luego actualiza `.env`:
```env
EXPO_PUBLIC_MAPS_URL=https://tu-url-ngrok.ngrok-free.app
```

Para **iOS Simulator**: Usa `http://localhost:8004`

### 3. Ejecutar la App

```bash
cd mobile
npm install
npx expo start
```

## 📡 Endpoint Utilizado

### POST `/distribution`

**Request:**
```json
{
  "lat": 11.008083,
  "lon": -74.840134,
  "datetime": "2025-11-26T10:30:00.000Z",
  "radius": 500,
  "grid_size": 0.002
}
```

**Response:**
```json
{
  "zone": "Centro",
  "location": {
    "lat": 11.008083,
    "lon": -74.840134
  },
  "datetime": "2025-11-26T10:30:00",
  "species_distributions": [
    {
      "species": "Pitangus sulphuratus",
      "max_probability": 0.852,
      "areas": [
        {
          "polygon": [
            {"lat": 11.015, "lon": -74.854},
            {"lat": 11.024, "lon": -74.854},
            {"lat": 11.024, "lon": -74.845},
            {"lat": 11.015, "lon": -74.845}
          ],
          "probability": 0.7
        }
      ]
    }
  ]
}
```

## 🎯 Funcionalidades Implementadas

### ✅ Carga Automática
- Al abrir la pantalla, solicita permisos de ubicación
- Obtiene automáticamente la ubicación del usuario
- Llama al endpoint `/distribution` con la ubicación actual
- Muestra las especies encontradas en un radio de 500m

### ✅ Recarga Manual
- Botón "Recargar" en la esquina superior derecha
- Actualiza la distribución con la ubicación actual
- Indicador visual mientras carga

### ✅ Manejo de Errores
- Alertas descriptivas si no hay conexión con el servidor
- Mensaje si no se encuentran especies
- Fallback a datos de ejemplo si hay error

### ✅ Visualización en Mapa
- Polígonos de distribución por probabilidad
- Colores según probabilidad: Rojo (alta), Naranja (media), Amarillo (baja)
- Marcadores con porcentaje de probabilidad

## 🛠️ Parámetros Configurables

En el código puedes modificar:

```typescript
const radius = 500; // Radio en metros (default: 500)
const grid_size = 0.002; // Resolución de la grilla (~200m)
```

## 🐛 Troubleshooting

### Error: "No se pudo conectar con el servidor"
1. Verifica que el servicio de mapas esté corriendo: `docker-compose ps`
2. Verifica la URL en consola: debe mostrar "🗺️ Maps API URL: http://10.0.2.2:8004"
3. Prueba el endpoint manualmente: `curl http://localhost:8004/zones`

### Error: "Ubicación no disponible"
1. Verifica permisos de ubicación en el emulador/dispositivo
2. En emulador Android: Settings > Location > Turn on
3. Envía ubicación de prueba: En Android Studio > Extended Controls > Location

### No aparecen especies
1. Verifica que tu ubicación esté dentro de Barranquilla
2. El modelo solo tiene datos para ciertas zonas de Barranquilla
3. Prueba con coordenadas conocidas: lat: 11.008083, lon: -74.840134

## 📊 Ejemplo de Uso en Código

```typescript
import { getDistribution } from '../../../../services/mapsService';

// Obtener distribución
const data = await getDistribution(
  11.008083,  // latitud
  -74.840134, // longitud
  500,        // radio en metros
  0.002       // grid_size
);

// Usar los datos
setSpeciesData(data.species_distributions);
```

## 🔄 Próximas Mejoras

- [ ] Permitir al usuario ajustar el radio de búsqueda con un slider
- [ ] Cachear resultados para evitar llamadas repetidas
- [ ] Modo offline con datos precargados
- [ ] Filtrar especies por probabilidad mínima
- [ ] Exportar distribución como imagen o PDF

## 📝 Notas Técnicas

- El endpoint usa el modelo de ML `modelo_multilabel.pkl` (~377 MB)
- Se carga una sola vez al iniciar el servicio para mejor rendimiento
- La interpolación se hace con scipy.griddata usando método 'linear'
- Los polígonos se generan usando shapely.geometry.Polygon
