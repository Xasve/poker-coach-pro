# install_auto_capture.ps1
Write-Host " INSTALANDO SISTEMA DE CAPTURA AUTOMÁTICA" -ForegroundColor Cyan
Write-Host "=" * 70

# Verificar Python
Write-Host "`n1 VERIFICANDO PYTHON..." -ForegroundColor Green
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host " Python no encontrado" -ForegroundColor Red
    exit 1
}
Write-Host "    $pythonVersion" -ForegroundColor Green

# Verificar/crear entorno virtual
Write-Host "`n2 CONFIGURANDO ENTORNO VIRTUAL..." -ForegroundColor Green
if (-not (Test-Path "venv")) {
    Write-Host "   Creando entorno virtual..." -ForegroundColor Gray
    python -m venv venv --prompt="PokerCoach"
}
.\venv\Scripts\Activate.ps1
Write-Host "    Entorno activado" -ForegroundColor Green

# Instalar dependencias básicas
Write-Host "`n3 INSTALANDO DEPENDENCIAS BÁSICAS..." -ForegroundColor Green
$basicPackages = @(
    "numpy==1.24.4",
    "opencv-python==4.9.0.80",
    "pillow==10.3.0",
    "mss==9.0.1",
    "pyyaml==6.0.1"
)

foreach ($pkg in $basicPackages) {
    Write-Host "   📦 $pkg" -NoNewline -ForegroundColor Gray
    pip install $pkg -q
    Write-Host " ✅" -ForegroundColor Green
}

# Instalar scikit-learn (puede requerir build tools)
Write-Host "`n4 INSTALANDO MACHINE LEARNING..." -ForegroundColor Green
Write-Host "     Esta instalación puede tomar unos minutos" -ForegroundColor Yellow

try {
    pip install scikit-learn==1.3.2 -q
    Write-Host "    scikit-learn instalado" -ForegroundColor Green
} catch {
    Write-Host "     Error instalando scikit-learn" -ForegroundColor Yellow
    Write-Host "    Instala manualmente si hay problemas:" -ForegroundColor Gray
    Write-Host "      pip install scikit-learn==1.3.2 --no-deps" -ForegroundColor Gray
}

# Instalar dependencias adicionales
Write-Host "`n5 INSTALANDO DEPENDENCIAS ADICIONALES..." -ForegroundColor Green
$extraPackages = @(
    "pandas==2.1.4",
    "matplotlib==3.8.2",
    "colorama==0.4.6",
    "tqdm==4.66.1"
)

foreach ($pkg in $extraPackages) {
    Write-Host "    $pkg" -NoNewline -ForegroundColor Gray
    pip install $pkg -q
    Write-Host " " -ForegroundColor Green
}

# Verificar instalación
Write-Host "`n6 VERIFICANDO INSTALACIÓN..." -ForegroundColor Green
python -c "
try:
    import cv2, numpy, mss, sklearn
    print('✅ Todas las dependencias instaladas correctamente')
    print(f'   OpenCV: {cv2.__version__}')
    print(f'   NumPy: {numpy.__version__}')
    print(f'   scikit-learn: {sklearn.__version__}')
except ImportError as e:
    print(f' Error: {e}')
"

# Crear estructura de directorios
Write-Host "`n7 CREANDO ESTRUCTURA..." -ForegroundColor Green
$folders = @(
    "data/card_templates/auto_captured",
    "models",
    "reports",
    "training_data"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
    Write-Host "    $folder" -ForegroundColor Gray
}

Write-Host "`n" + "=" * 70 -ForegroundColor Yellow
Write-Host "🎉 ¡INSTALACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Yellow

Write-Host "`n🚀 PARA INICIAR EL SISTEMA:" -ForegroundColor Cyan
Write-Host "   1. Activa entorno: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   2. Configura PokerStars: python detect_coords.py" -ForegroundColor White
Write-Host "   3. Ejecuta captura: python start_auto_capture.py" -ForegroundColor White

Write-Host "`n COMANDOS DISPONIBLES:" -ForegroundColor Cyan
Write-Host "   python src/auto_capture_system.py    - Sistema completo" -ForegroundColor Gray
Write-Host "   python src/card_detector.py          - Solo detector" -ForegroundColor Gray
Write-Host "   python src/auto_template_capturer.py - Solo capturador" -ForegroundColor Gray
Write-Host "   python src/card_classifier.py        - Solo clasificador" -ForegroundColor Gray

Write-Host "`n  NOTAS IMPORTANTES:" -ForegroundColor Yellow
Write-Host "    Asegúrate de tener PokerStars abierto y visible" -ForegroundColor White
Write-Host "    La primera ejecución puede ser lenta" -ForegroundColor White
Write-Host "    Usa Ctrl+C para detener cualquier proceso" -ForegroundColor White

pause
