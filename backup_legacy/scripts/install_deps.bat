
---

## **📁 ARCHIVO: install_deps.bat**
**Ruta:** `poker-coach-pro/scripts/install_deps.bat`

```batch
@echo off
echo ========================================
echo    INSTALANDO POKER COACH PRO
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo Descarga Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Instalar dependencias
echo 📦 Instalando dependencias de Python...
pip install --upgrade pip
pip install opencv-python numpy pillow pytesseract pandas
pip install pyautogui mss websockets tinydb

echo.
echo 🎴 Creando directorios necesarios...

REM Crear directorios si no existen
if not exist "data\card_templates\ggpoker" mkdir "data\card_templates\ggpoker"
if not exist "data\card_templates\pokerstars" mkdir "data\card_templates\pokerstars"
if not exist "data\logs" mkdir "data\logs"

echo.
echo ✅ Instalacion completada!
echo.
echo Para iniciar el sistema:
echo   1. Abre GG Poker o PokerStars
echo   2. Ejecuta: python start_coach.py
echo   3. Selecciona tu plataforma
echo.
echo 🎯 Consejo: Empieza con stakes bajos para familiarizarte
pause