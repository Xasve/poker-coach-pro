# setup_fixed.ps1 - Creador de entorno PARA POKER COACH PRO
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  POKER COACH PRO - SETUP COMPLETO" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. VERIFICAR PYTHON 3.11
Write-Host "`n[1/4] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ Python detectado: $pythonVersion" -ForegroundColor Green
    
    if ($pythonVersion -like "*3.11*") {
        Write-Host "  ✅ Versión 3.11 (recomendada)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Versión diferente a 3.11" -ForegroundColor Yellow
        Write-Host "  ℹ️  El proyecto fue probado con Python 3.11" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Python no encontrado en PATH" -ForegroundColor Red
    Write-Host "  ℹ️  Instala Python 3.11 desde python.org" -ForegroundColor Yellow
    exit 1
}

# 2. CREAR ENTORNO VIRTUAL
Write-Host "`n[2/4] Configurando entorno virtual..." -ForegroundColor Yellow

$venvPath = "venv"
if (Test-Path $venvPath) {
    Write-Host "  ⚠️  El directorio 'venv' ya existe" -ForegroundColor Yellow
    $choice = Read-Host "  ¿Recrear desde cero? (s/n)"
    
    if ($choice -eq 's') {
        Write-Host "  🗑️  Eliminando entorno virtual anterior..." -ForegroundColor Gray
        Remove-Item -Recurse -Force $venvPath -ErrorAction SilentlyContinue
        python -m venv $venvPath
        Write-Host "  ✅ Entorno virtual recreado" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️  Usando entorno existente" -ForegroundColor Yellow
    }
} else {
    Write-Host "  📁 Creando nuevo entorno virtual..." -ForegroundColor Gray
    python -m venv $venvPath
    if (Test-Path $venvPath) {
        Write-Host "  ✅ Entorno virtual creado" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Error creando entorno virtual" -ForegroundColor Red
        exit 1
    }
}

# 3. ACTIVAR Y INSTALAR DEPENDENCIAS
Write-Host "`n[3/4] Instalando dependencias..." -ForegroundColor Yellow

# Verificar si estamos en entorno virtual
if (-not $env:VIRTUAL_ENV) {
    Write-Host "  ⚡ Activando entorno virtual..." -ForegroundColor Gray
    
    if (Test-Path "$venvPath\Scripts\Activate.ps1") {
        & "$venvPath\Scripts\Activate.ps1"
        Write-Host "  ✅ Entorno activado" -ForegroundColor Green
    } else {
        Write-Host "  ❌ No se pudo activar el entorno" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  ✅ Entorno ya activado: $env:VIRTUAL_ENV" -ForegroundColor Green
}

# Actualizar pip
Write-Host "  🔄 Actualizando pip..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet
Write-Host "  ✅ pip actualizado" -ForegroundColor Green

# Verificar requirements.txt
if (-not (Test-Path "requirements.txt")) {
    Write-Host "  ❌ requirements.txt no encontrado" -ForegroundColor Red
    Write-Host "  ℹ️  Ejecuta primero clean_requirements.py" -ForegroundColor Yellow
    exit 1
}

# Instalar dependencias
Write-Host "  📦 Instalando paquetes (esto puede tomar unos minutos)..." -ForegroundColor Gray
$requirementsContent = Get-Content "requirements.txt" | Where-Object { $_ -notmatch '^#' -and $_.Trim() -ne '' }
$packageCount = ($requirementsContent | Measure-Object).Count

Write-Host "  📊 $packageCount paquetes por instalar..." -ForegroundColor Gray

# Instalar en grupos para mejor manejo de errores
$installed = 0
$failed = @()

foreach ($package in $requirementsContent) {
    $pkgName = $package.Split('>=')[0].Split('<=')[0].Trim()
    Write-Host "    ↳ Instalando $pkgName..." -ForegroundColor DarkGray
    
    $result = pip install $package --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        $installed++
    } else {
        $failed += $pkgName
        Write-Host "      ⚠️  Error con $pkgName" -ForegroundColor DarkYellow
    }
}

Write-Host "  ✅ $installed/$packageCount paquetes instalados" -ForegroundColor Green

if ($failed.Count -gt 0) {
    Write-Host "  ⚠️  Fallos: $($failed.Count) paquetes" -ForegroundColor Yellow
    $failed | ForEach-Object { Write-Host "    • $_" -ForegroundColor DarkYellow }
}

# 4. CREAR ESTRUCTURA DE CARPETAS
Write-Host "`n[4/4] Creando estructura del proyecto..." -ForegroundColor Yellow

# Lista de carpetas necesarias
$folders = @(
    "src\core",
    "src\ui", 
    "src\integration",
    "src\utils",
    "data\gto_ranges",
    "tests",
    "scripts",
    "logs",
    "config"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Force -Path $folder | Out-Null
        Write-Host "  📁 Creado: $folder" -ForegroundColor Gray
    }
}

# Crear archivos __init__.py necesarios
$initFiles = @("src\__init__.py", "src\core\__init__.py", "src\utils\__init__.py", "src\integration\__init__.py")
foreach ($file in $initFiles) {
    if (-not (Test-Path $file)) {
        New-Item -ItemType File -Path $file -Force | Out-Null
        Write-Host "  📄 Creado: $file" -ForegroundColor Gray
    }
}

# RESULTADO FINAL
Write-Host "`n" + ("=" * 50) -ForegroundColor Green
Write-Host "✅ SETUP COMPLETADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

Write-Host "`n📊 RESUMEN:" -ForegroundColor White
Write-Host "  • Entorno virtual: $venvPath" -ForegroundColor Gray
Write-Host "  • Python: $pythonVersion" -ForegroundColor Gray
Write-Host "  • Paquetes instalados: $installed/$packageCount" -ForegroundColor Gray

if ($failed.Count -gt 0) {
    Write-Host "  • Paquetes con error: $($failed.Count)" -ForegroundColor Yellow
}

Write-Host "`n🚀 PASOS SIGUIENTES:" -ForegroundColor White
Write-Host "  1. El entorno virtual está ACTIVADO" -ForegroundColor Gray
Write-Host "  2. Ejecuta el punto de entrada:" -ForegroundColor Cyan
Write-Host "     python main.py" -ForegroundColor White
Write-Host "  3. Para desactivar el entorno:" -ForegroundColor Gray  
Write-Host "     deactivate" -ForegroundColor White
Write-Host "  4. Para reactivar en futuras sesiones:" -ForegroundColor Gray
Write-Host "     .\venv\Scripts\Activate" -ForegroundColor White

Write-Host "`n🔧 PROBLEMAS COMUNES:" -ForegroundColor Yellow
Write-Host "  • Si hay errores de OpenCV: pip install opencv-python-headless" -ForegroundColor Gray
Write-Host "  • Tesseract OCR requiere instalación separada" -ForegroundColor Gray
Write-Host "  • Ejecuta como Administrador si hay permisos" -ForegroundColor Gray

Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "🎯 ¡Poker Coach Pro está listo para desarrollo!" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan