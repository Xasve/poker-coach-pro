@echo off
echo ========================================
echo    INSTALADOR SISTEMA DE CALIDAD
echo    Poker Coach Pro - Validación Avanzada
echo ========================================
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo Ejecuta primero: python setup_folders.py
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

echo 📦 Creando estructura de directorios...
if not exist "src\quality" mkdir src\quality
if not exist "data\quality_reports" mkdir data\quality_reports

echo.
echo 📄 Creando archivos del sistema de calidad...

REM Crear archivos del sistema de calidad
(
echo # Archivos del sistema de validación de calidad
echo decision_validator.py
echo decision_analyzer.py
echo quality_dashboard.py
) > src\quality\__init__.py

echo.
echo 🚀 Para probar el sistema de calidad:
echo   1. Ejecuta: python test_quality.py
echo   2. O usa: python poker_coach_with_quality.py
echo.
echo 📊 El sistema evaluará:
echo   - Calidad de decisiones (0-100)
echo   - Comparación con estrategia GTO
echo   - Áreas de mejora específicas
echo   - Estadísticas detalladas
echo.
pause