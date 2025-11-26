# Script para configurar Android SDK para Expo
# Ejecutar: powershell -ExecutionPolicy Bypass -File setup-android.ps1

Write-Host "[+] Configurando Android SDK para desarrollo con Expo..." -ForegroundColor Cyan
Write-Host ""

# Detectar la ruta del Android SDK
$possiblePaths = @(
    "$env:LOCALAPPDATA\Android\Sdk",
    "C:\Android\Sdk",
    "$env:USERPROFILE\Android\Sdk"
)

$androidSdkPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $androidSdkPath = $path
        Write-Host "[OK] Android SDK encontrado en: $androidSdkPath" -ForegroundColor Green
        break
    }
}

if (-not $androidSdkPath) {
    Write-Host "[!] Android SDK no encontrado en las rutas comunes." -ForegroundColor Yellow
    Write-Host "    Por favor, completa la instalacion de Android SDK desde Android Studio:" -ForegroundColor Yellow
    Write-Host "    Tools -> SDK Manager -> Install Android SDK" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    Ruta esperada: $env:LOCALAPPDATA\Android\Sdk" -ForegroundColor Yellow
    exit 1
}

# Configurar variables de entorno de usuario
Write-Host ""
Write-Host "[+] Configurando variables de entorno..." -ForegroundColor Cyan

[System.Environment]::SetEnvironmentVariable('ANDROID_HOME', $androidSdkPath, 'User')
[System.Environment]::SetEnvironmentVariable('ANDROID_SDK_ROOT', $androidSdkPath, 'User')

Write-Host "    ANDROID_HOME = $androidSdkPath" -ForegroundColor Gray
Write-Host "    ANDROID_SDK_ROOT = $androidSdkPath" -ForegroundColor Gray

# Agregar herramientas de Android al PATH
Write-Host ""
Write-Host "[+] Actualizando PATH..." -ForegroundColor Cyan

$currentPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')
$pathsToAdd = @(
    "$androidSdkPath\platform-tools",
    "$androidSdkPath\emulator",
    "$androidSdkPath\tools",
    "$androidSdkPath\tools\bin"
)

$pathArray = $currentPath -split ';'
$updated = $false

foreach ($pathToAdd in $pathsToAdd) {
    if ($pathArray -notcontains $pathToAdd) {
        $currentPath += ";$pathToAdd"
        $updated = $true
        Write-Host "    + $pathToAdd" -ForegroundColor Gray
    }
}

if ($updated) {
    [System.Environment]::SetEnvironmentVariable('Path', $currentPath, 'User')
    Write-Host "    [OK] PATH actualizado" -ForegroundColor Green
} else {
    Write-Host "    [i] PATH ya estaba configurado correctamente" -ForegroundColor Blue
}

# Actualizar variables en la sesion actual
$env:ANDROID_HOME = $androidSdkPath
$env:ANDROID_SDK_ROOT = $androidSdkPath
$env:Path = $currentPath

Write-Host ""
Write-Host "[OK] Configuracion completada!" -ForegroundColor Green
Write-Host ""
Write-Host "[+] Verificacion:" -ForegroundColor Cyan
Write-Host "    ANDROID_HOME: $env:ANDROID_HOME" -ForegroundColor Gray

# Verificar herramientas disponibles
Write-Host ""
Write-Host "[+] Verificando herramientas instaladas..." -ForegroundColor Cyan

$adbPath = "$androidSdkPath\platform-tools\adb.exe"
$emulatorPath = "$androidSdkPath\emulator\emulator.exe"

if (Test-Path $adbPath) {
    Write-Host "    [OK] ADB encontrado" -ForegroundColor Green
    try {
        $adbVersion = & $adbPath version 2>$null | Select-Object -First 1
        Write-Host "         $adbVersion" -ForegroundColor Gray
    } catch {}
} else {
    Write-Host "    [!] ADB no encontrado. Instala 'Android SDK Platform-Tools' desde SDK Manager" -ForegroundColor Yellow
}

if (Test-Path $emulatorPath) {
    Write-Host "    [OK] Emulator encontrado" -ForegroundColor Green
    try {
        $emulatorVersion = & $emulatorPath -version 2>$null | Select-Object -First 1
        Write-Host "         $emulatorVersion" -ForegroundColor Gray
    } catch {}
} else {
    Write-Host "    [!] Emulator no encontrado. Instala 'Android Emulator' desde SDK Manager" -ForegroundColor Yellow
}

# Listar emuladores disponibles
Write-Host ""
Write-Host "[+] Emuladores disponibles:" -ForegroundColor Cyan

if (Test-Path $emulatorPath) {
    try {
        $avds = & $emulatorPath -list-avds 2>$null
        if ($avds) {
            foreach ($avd in $avds) {
                Write-Host "    [AVD] $avd" -ForegroundColor Green
            }
        } else {
            Write-Host "    [!] No hay emuladores creados aun." -ForegroundColor Yellow
            Write-Host "        Crea uno desde Android Studio: Tools -> Device Manager -> Create Device" -ForegroundColor Gray
        }
    } catch {
        Write-Host "    [!] Error al listar emuladores" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "[+] Proximos pasos:" -ForegroundColor Cyan
Write-Host "    1. Cierra y vuelve a abrir PowerShell/Terminal" -ForegroundColor White
Write-Host "    2. Si no tienes emuladores, crealos en Android Studio (Device Manager)" -ForegroundColor White
Write-Host "    3. Ejecuta: cd mobile; npx expo start" -ForegroundColor White
Write-Host "    4. Presiona 'a' para abrir en Android" -ForegroundColor White
Write-Host ""
Write-Host "[+] Para iniciar emulador manualmente:" -ForegroundColor Cyan
Write-Host "    emulator -avd <nombre_del_emulador>" -ForegroundColor Gray
Write-Host ""
