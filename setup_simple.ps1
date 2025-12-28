# setup_simple.ps1 - Setup sin complicaciones para Poker Coach Pro
Write-Host "=== POKER COACH PRO - SETUP SIMPLIFICADO ===" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Python
Write-Host "[1/3] Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "  Python: $pythonVersion" -ForegroundColor Green

# 2. Crear/limpiar entorno virtual
Write-Host "[2/3] Configurando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Encontrado 'venv' existente" -ForegroundColor Gray
    $choice = Read-Host "  ¿Recrear? (s/n) [n]"
    if ($choice -eq 's') {
        Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
        python -m venv venv
        Write-Host "  Entorno recreado" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "  Entorno creado" -ForegroundColor Green
}

# 3. Activar y instalar
Write-Host "[3/3] Instalando dependencias..." -ForegroundColor Yellow

# Activar entorno
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "  ERROR: No se pudo activar el entorno" -ForegroundColor Red
    exit 1
}

# Instalar pip actualizado
python -m pip install --upgrade pip --quiet

# Instalar dependencias
if (Test-Path "requirements.txt") {
    Write-Host "  Instalando paquetes..." -ForegroundColor Gray
    pip install -r requirements.txt
    
    # Verificar instalaciones clave
    Write-Host "  Verificando instalaciones..." -ForegroundColor Gray
    $key_packages = @("opencv-python", "numpy", "pillow", "pyautogui", "pytesseract")
    foreach ($pkg in $key_packages) {
        $check = pip show $pkg 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    ✅ $pkg" -ForegroundColor Green
        } else {
            Write-Host "    ⚠️  $pkg (no instalado)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "  ERROR: requirements.txt no encontrado" -ForegroundColor Red
    exit 1
}

# 4. Verificar estructura
Write-Host "`n[+] Verificando estructura..." -ForegroundColor Yellow
$required_dirs = @("src", "data", "config", "logs")
foreach ($dir in $required_dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Creado: $dir" -ForegroundColor Gray
    }
}

# Resultado final
Write-Host "`n" + ("=" * 50) -ForegroundColor Green
Write-Host "✅ SETUP COMPLETADO" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

Write-Host "`nPara iniciar el programa:" -ForegroundColor White
Write-Host "  python main.py" -ForegroundColor Cyan

Write-Host "`nPara desactivar el entorno:" -ForegroundColor Gray
Write-Host "  deactivate" -ForegroundColor White

Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan