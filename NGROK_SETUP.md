# Guía Rápida: Usar Ngrok para Desarrollo con Teléfono Físico

## 🎯 ¿Por qué Ngrok?

Ngrok crea un túnel público a tu backend local, permitiendo:
- ✅ Probar en teléfono físico sin configurar red
- ✅ Funciona con cualquier WiFi/4G
- ✅ URLs HTTPS (necesario para algunas APIs)
- ✅ No necesitas configurar firewall

## 📦 Instalación

### Opción 1: Chocolatey (Recomendado en Windows)
```powershell
choco install ngrok
```

### Opción 2: Manual
1. Descarga desde https://ngrok.com/download
2. Extrae el .exe
3. Muévelo a una carpeta en tu PATH o úsalo directamente

## 🔑 Configuración Inicial (Solo una vez)

1. **Crea una cuenta gratis en https://ngrok.com**

2. **Obtén tu authtoken** desde el dashboard

3. **Configura el token**:
   ```powershell
   ngrok config add-authtoken TU_TOKEN_AQUI
   ```

## 🚀 Uso Diario

### 1. Inicia tu backend
```powershell
docker-compose up -d
```

### 2. Inicia ngrok
```powershell
ngrok http 8000
```

Verás algo como:
```
Forwarding  https://abc123-def-456.ngrok-free.app -> http://localhost:8000
```

### 3. Copia la URL de ngrok

Copia la URL que empieza con `https://` (ejemplo: `https://abc123-def-456.ngrok-free.app`)

### 4. Pégala en el código

Abre `mobile/config/environment.ts` y actualiza:

```typescript
const NGROK_URL = 'https://abc123-def-456.ngrok-free.app';
```

### 5. Reinicia Expo

```powershell
# En la terminal de Expo, presiona 'r' para reload
# O cierra y vuelve a ejecutar
cd mobile
npx expo start
```

### 6. Abre en tu teléfono

- Escanea el QR con la app **Expo Go**
- La app se conectará automáticamente a ngrok

## 📱 Ventajas vs IP Local

| Método | Configuración | WiFi | 4G/5G | HTTPS |
|--------|--------------|------|-------|-------|
| IP Local | Complicada | ✅ Misma red | ❌ | ❌ |
| Ngrok | Fácil | ✅ Cualquiera | ✅ | ✅ |

## ⚠️ Importante

1. **La URL de ngrok cambia cada vez que lo reinicias** (en la versión gratis)
   - Debes actualizar `NGROK_URL` cada vez
   - Versión paga tiene URLs fijas

2. **Ngrok tiene límites en la versión gratis**:
   - 40 conexiones/minuto
   - Suficiente para desarrollo

3. **Advertencia de seguridad de ngrok**:
   - Al abrir la URL en el navegador, verás una página de advertencia
   - Click en "Visit Site" para continuar
   - Esto NO afecta a tu app móvil

## 🔧 Debugging

### Ver tráfico HTTP
Ngrok tiene una interfaz web en:
```
http://127.0.0.1:4040
```

Ahí puedes ver todas las peticiones HTTP/WebSocket.

### Verificar que funciona
```powershell
# Probar desde tu PC
curl https://abc123.ngrok-free.app/health

# Probar desde el navegador de tu teléfono
# Abre: https://abc123.ngrok-free.app/health
```

## 🎨 Flujo Completo de Trabajo

```bash
# Terminal 1: Backend
docker-compose up -d

# Terminal 2: Ngrok
ngrok http 8000

# Terminal 3: Frontend
cd mobile
# Actualiza NGROK_URL en environment.ts
npx expo start
# Escanea QR con Expo Go en tu teléfono
```

## 💡 Tips

- **Guarda la terminal de ngrok abierta** mientras desarrollas
- **Crea un alias** para arrancar todo más rápido
- **Usa ngrok para compartir tu app** con testers remotos
- **El WebSocket funciona automáticamente** con ngrok (wss://)

## 🔄 Alternativa: IP Local (Más Complejo)

Si prefieres no usar ngrok:

1. Obtén tu IP local:
   ```powershell
   ipconfig
   ```

2. Busca IPv4 de tu adaptador WiFi (ej: `192.168.1.100`)

3. Actualiza `environment.ts`:
   ```typescript
   const NGROK_URL = 'http://192.168.1.100:8000';
   ```

4. Configura firewall:
   ```powershell
   New-NetFirewallRule -DisplayName "Winged Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

5. **Asegúrate que PC y teléfono estén en la misma WiFi**

## ❓ Problemas Comunes

### "ERR_NGROK_3200"
**Causa**: Authtoken no configurado
**Solución**: `ngrok config add-authtoken TU_TOKEN`

### "tunnel session failed: not found"
**Causa**: Puerto incorrecto o backend no corriendo
**Solución**: Verifica que `docker-compose ps` muestre servicios running

### "Network request failed" en la app
**Causa**: URL de ngrok incorrecta o expirada
**Solución**: Verifica que `NGROK_URL` coincida con la URL actual de ngrok
