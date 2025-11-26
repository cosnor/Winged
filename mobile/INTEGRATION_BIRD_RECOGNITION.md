# Integración de Reconocimiento de Aves - Frontend Mobile

## 📋 Descripción

Integración completa del servicio de reconocimiento de aves (ML Worker) con el frontend móvil de Winged usando WebSocket para comunicación en tiempo real.

## 🏗️ Arquitectura

### Componentes Principales

1. **Hook: `useBirdAnalysis`** (`mobile/hooks/useBirdAnalysis.ts`)
   - Maneja la conexión WebSocket con el servicio ML Worker
   - Envía archivos de audio (base64) para análisis
   - Recibe detecciones de aves en tiempo real
   - Auto-reconexión en caso de desconexión

2. **Contexto: `BirdDetectionContext`** (`mobile/context/bird-detection-context.tsx`)
   - Almacena el registro global de aves identificadas
   - Comparte detecciones entre pantallas
   - Persiste los resultados durante la sesión

3. **Componentes UI:**
   - `AudioRecorder`: Graba audio y lo envía automáticamente para análisis
   - `AudioSelector`: Permite seleccionar archivos de audio existentes y analizarlos

4. **Pantallas:**
   - `identify/record.tsx`: Pantalla de grabación de audio
   - `identify/audioupload.tsx`: Pantalla de selección de archivos

## 🔌 Conexión WebSocket

### URL de Conexión

El hook `useBirdAnalysis` construye automáticamente la URL del WebSocket:

```typescript
// Desarrollo con emulador Android
ws://10.0.2.2:8007/ml-worker/ws

// Desarrollo con simulador iOS
ws://localhost:8007/ml-worker/ws

// Producción
wss://tu-api-produccion.com/ml-worker/ws
```

La URL se genera automáticamente desde `API_BASE_URL` en `mobile/config/environment.ts`.

### Protocolo de Mensajes

#### Cliente → Servidor

```json
{
  "type": "analyze_audio",
  "audio": "<base64_encoded_audio>",
  "filename": "recording_1234567890.wav"
}
```

#### Servidor → Cliente

**Conexión establecida:**
```json
{
  "type": "connected",
  "available_commands": ["analyze_audio", "get_status"]
}
```

**Análisis aceptado:**
```json
{
  "type": "analysis_accepted",
  "analysis_id": "abc123"
}
```

**Progreso del análisis:**
```json
{
  "type": "analysis_progress",
  "message": "Procesando audio..."
}
```

**Análisis completado:**
```json
{
  "type": "analysis_completed",
  "analysis": {
    "detections": [
      {
        "species_name": "Turdus grayi",
        "common_name": "Mirla Parda",
        "scientific_name": "Turdus grayi",
        "confidence": 0.87,
        "start_time": 2.5,
        "end_time": 5.3
      }
    ]
  }
}
```

**Error:**
```json
{
  "type": "error",
  "message": "Descripción del error"
}
```

## 🎯 Flujo de Uso

### Grabación de Audio

1. Usuario abre pantalla `identify/record.tsx`
2. Presiona botón de micrófono para iniciar grabación
3. Presiona nuevamente para detener
4. El componente `AudioRecorder`:
   - Convierte el audio grabado a base64
   - Envía automáticamente al servicio vía WebSocket
   - Muestra estado "Analizando..."
5. Al recibir detecciones:
   - Se agregan al contexto global `BirdDetectionContext`
   - Aparecen automáticamente en `BirdRegistry`

### Selección de Archivo

1. Usuario abre pantalla `identify/audioupload.tsx`
2. Presiona "Seleccionar archivo"
3. Elige un archivo de audio del dispositivo
4. Opcionalmente reproduce el audio para verificar
5. Presiona botón "Analizar Audio"
6. El componente `AudioSelector`:
   - Lee el archivo y lo convierte a base64
   - Envía al servicio vía WebSocket
   - Muestra estado "Analizando..."
7. Las detecciones se agregan automáticamente al registro

## 🛠️ Configuración

### Variables de Entorno

El archivo `mobile/config/environment.ts` maneja automáticamente la configuración según la plataforma:

```typescript
// Para emulador Android
Platform.OS === 'android' ? 'http://10.0.2.2:8007' : 'http://localhost:8007'
```

### Requisitos del Backend

1. **Docker Compose** debe estar corriendo:
   ```bash
   docker-compose up -d
   ```

2. **ML Worker** debe estar disponible en el puerto configurado (8003 interno, 8007 gateway)

3. **WebSocket endpoint** debe estar expuesto en `/ml-worker/ws`

## 📦 Dependencias

Todas las dependencias ya están incluidas en `package.json`:

- `expo-audio`: Grabación de audio
- `expo-file-system`: Lectura de archivos y conversión a base64
- `expo-document-picker`: Selección de archivos
- WebSocket: Nativo de React Native

## 🔍 Debugging

### Ver logs de conexión

```typescript
console.log('🔌 Conectando a WebSocket:', wsUrl);
console.log('✅ WebSocket conectado');
console.log('📨 Mensaje recibido:', message.type);
```

### Estados de la conexión

El hook proporciona:
- `connected`: Boolean - Estado de conexión
- `analyzing`: Boolean - Audio en análisis
- `error`: String | null - Último error
- `detections`: Array - Detecciones recibidas

### Verificar que el backend esté corriendo

```bash
# Verificar servicios
docker-compose ps

# Ver logs del ML Worker
docker-compose logs -f ml_worker

# Probar conexión HTTP
curl http://localhost:8007/health
```

## 🐛 Problemas Comunes

### "Sin conexión al servidor"

**Causa**: El backend no está corriendo o no es accesible
**Solución**:
1. Verifica que docker-compose esté corriendo
2. Verifica la IP en `environment.ts`
3. Para emulador Android usa `10.0.2.2:8007`
4. Para iOS simulator usa `localhost:8007`

### "Error al enviar el audio"

**Causa**: Audio muy grande o formato no soportado
**Solución**:
1. Limita la duración de la grabación
2. Verifica que el formato sea WAV o MP3
3. Revisa los logs del ML Worker

### WebSocket se desconecta constantemente

**Causa**: Firewall o timeout del servidor
**Solución**:
1. Aumenta el timeout del servidor
2. Implementa heartbeat/ping-pong
3. Verifica que no haya proxy bloqueando WebSocket

## 📝 Ejemplo de Uso

```typescript
import { useBirdAnalysis } from '../hooks/useBirdAnalysis';

function MyComponent() {
  const { connected, analyzing, detections, analyzeAudio, error } = useBirdAnalysis();

  const handleAnalyze = async (base64Audio: string) => {
    try {
      await analyzeAudio(base64Audio, 'my-audio.wav');
    } catch (err) {
      console.error('Error:', err);
    }
  };

  return (
    <View>
      <Text>Estado: {connected ? 'Conectado' : 'Desconectado'}</Text>
      {analyzing && <Text>Analizando...</Text>}
      {error && <Text>Error: {error}</Text>}
      {detections.map(d => (
        <Text key={d.species_name}>{d.common_name} ({d.confidence})</Text>
      ))}
    </View>
  );
}
```

## 🚀 Próximos Pasos

- [ ] Agregar persistencia local de detecciones (AsyncStorage)
- [ ] Implementar caché de imágenes de especies
- [ ] Agregar opción de guardar avistamientos
- [ ] Integrar con servicio de mapas para geolocalización
- [ ] Implementar sincronización con backend cuando haya conexión
