# Mensajes de Validación de Contraseña

## Errores del Servicio de Usuarios → Traducciones del Gateway

El gateway detecta los siguientes errores del servicio de usuarios y los traduce a mensajes en español:

### Validaciones de Contraseña (Status 400)

| Error Original (EN) | Mensaje Traducido (ES) | Cuándo aparece |
|-------------------|---------------------|----------------|
| "Password must be at least 8 characters long" | "La contraseña debe tener al menos 8 caracteres" | Contraseña < 8 caracteres |
| "Password must contain at least one uppercase letter" | "La contraseña debe contener al menos una letra mayúscula" | No tiene mayúsculas |
| "Password must contain at least one number" | "La contraseña debe contener al menos un número" | No tiene dígitos |
| Cualquier otro error con "password" | "Contraseña inválida. Debe tener al menos 8 caracteres, una mayúscula y un número" | Fallback genérico |

### Otras Validaciones (Status 400)

| Error Original | Mensaje Traducido | Cuándo aparece |
|---------------|------------------|----------------|
| "Invalid name" | "Nombre inválido. Verifica el formato del nombre." | Nombre vacío/inválido |

### Errores de Email (Status 422)

| Error Original | Mensaje Traducido | Cuándo aparece |
|---------------|------------------|----------------|
| "value is not a valid email address" | "El texto no es un email válido" | Email malformado |

### Errores de Registro (Status 409)

| Error Original | Mensaje Traducido | Cuándo aparece |
|---------------|------------------|----------------|
| Email already exists | "El correo ya está registrado." | Email duplicado |

## Ejemplos de Uso

### Prueba desde el móvil o curl:

```bash
# Test 1: Contraseña muy corta
curl -X POST http://localhost:8007/users/signup \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","email":"test@example.com","password":"abc123"}'

# Respuesta esperada: {"detail":"La contraseña debe tener al menos 8 caracteres"}
```

```bash
# Test 2: Sin mayúscula
curl -X POST http://localhost:8007/users/signup \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","email":"test@example.com","password":"abcdefgh1"}'

# Respuesta esperada: {"detail":"La contraseña debe contener al menos una letra mayúscula"}
```

```bash
# Test 3: Sin número
curl -X POST http://localhost:8007/users/signup \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","email":"test@example.com","password":"Abcdefgh"}'

# Respuesta esperada: {"detail":"La contraseña debe contener al menos un número"}
```

```bash
# Test 4: Contraseña válida
curl -X POST http://localhost:8007/users/signup \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","email":"test@example.com","password":"Abcdefgh1"}'

# Respuesta esperada: 201 Created con tokens
```

## Implementación

Los mensajes se mapean en `backend/app/controllers/users.py` en la función `signup_user()` líneas ~149-158.

El gateway detecta el texto del error retornado por el servicio de usuarios y lo traduce antes de enviarlo al frontend móvil.
