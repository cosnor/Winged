# Configuración de Variables de Entorno

## Instalación Inicial

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita `.env` con tus valores reales:
```bash
# .env
API_BASE_URL=http://192.168.1.22:8007
GOOGLE_MAPS_API_KEY=tu_clave_real_de_google_maps
```

## Variables Disponibles

- **API_BASE_URL**: URL base de tu backend (puede ser IP local, localhost, o ngrok)
- **GOOGLE_MAPS_API_KEY**: Clave de API de Google Maps para Android

## Uso en el Código

Las variables están disponibles a través de `expo-constants`:

```javascript
import Constants from 'expo-constants';

const API_BASE_URL = Constants.expoConfig?.extra?.API_BASE_URL;
```

## Notas Importantes

- ⚠️ **NUNCA** subas el archivo `.env` a git (ya está en `.gitignore`)
- ✅ **SÍ** sube el archivo `.env.example` como plantilla para otros desarrolladores
- 🔄 Después de cambiar `.env`, reinicia Expo: `npx expo start -c`

## Ejemplos de URLs

```bash
# Desarrollo local (Docker en tu PC)
API_BASE_URL=http://192.168.1.22:8007

# Usando ngrok
API_BASE_URL=https://tu-url.ngrok-free.dev

# Localhost (solo emulador)
API_BASE_URL=http://localhost:8007
```
