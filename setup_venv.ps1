# setup_venv.ps1 - Creador de entorno para Poker Coach Pro
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  POKER COACH PRO - SETUP COMPLETO" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. VERIFICAR PYTHON 3.11
Write-Host "`n[1/4] Verificando Python 3.11..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -like "*3.11*") {
    Write-Host "  ✅ Python 3.11 detectado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Versión de Python diferente: $pythonVersion" -ForegroundColor Yellow
    Write-Host "  ℹ️  Se recomienda Python 3.11 para compatibilidad" -ForegroundColor Yellow
}

# 2. CREAR ENTORNO VIRTUAL
Write-Host "`n[2/4] Creando entorno virtual 'venv'..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ⚠️  El directorio 'venv' ya existe." -ForegroundColor Yellow
    $choice = Read-Host "  ¿Eliminar y recrear? (s/n)"
    if ($choice -eq 's') {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "  ✅ Entorno virtual recreado" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️  Usando entorno existente" -ForegroundColor Yellow
    }
} else {
    python -m venv venv
    Write-Host "  ✅ Entorno virtual creado" -ForegroundColor Green
}

# 3. ACTIVAR Y INSTALAR DEPENDENCIAS
Write-Host "`n[3/4] Activando entorno e instalando dependencias..." -ForegroundColor Yellow

# Activar entorno en PowerShell
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "  ✅ Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "  ❌ No se pudo activar el entorno" -ForegroundColor Red
    exit 1
}

# Actualizar pip
Write-Host "  ↳ Actualizando pip..." -ForegroundColor Gray
python -m pip install --upgrade pip

# Instalar dependencias
Write-Host "  ↳ Instalando paquetes desde requirements.txt..." -ForegroundColor Gray
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "  ✅ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "  ❌ requirements.txt no encontrado" -ForegroundColor Red
    exit 1
}

# 4. CREAR ESTRUCTURA DE CARPETAS
Write-Host "`n[4/4] Creando estructura de proyecto..." -ForegroundColor Yellow

$folders = @(
    "src\core",
    "src\ui", 
    "src\integration",
    "src\utils",
    "data\gto_ranges",
    "tests",
    "scripts"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Force -Path $folder | Out-Null
        Write-Host "  📁 Creado: $folder" -ForegroundColor Gray
    }
}

# Crear archivos __init__.py en src/
@("src\__init__.py", "src\core\__init__.py", "src\utils\__init__.py") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType File -Path $_ | Out-Null
    }
}

Write-Host "`n✅ SETUP COMPLETADO" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "`nPasos siguientes:" -ForegroundColor White
Write-Host "1. El entorno virtual está ACTIVADO (venv)" -ForegroundColor Gray
Write-Host "2. Ejecuta el punto de entrada:" -ForegroundColor Gray
Write-Host "   python main.py" -ForegroundColor White
Write-Host "3. Para desactivar el entorno:" -ForegroundColor Gray  
Write-Host "   deactivate" -ForegroundColor White
Write-Host "`n==========================================" -ForegroundColor Cyan