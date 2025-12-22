@echo off
chcp 65001 > nul
title  POKER BOT EXTREMO - VERSI?N REPARADA
color 0A

echo ================================================
echo     BOT DE P?KER EXTREMO - VERSI?N REPARADA
echo ================================================
echo  Caracter?sticas:
echo     Tiempo de reacci?n m?nimo (50ms objetivo)
echo     Sin restricciones de seguridad
echo     Optimizaci?n de recursos m?xima
echo     Procesamiento paralelo completo
echo ================================================
echo.

REM Verificar Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ? Python no encontrado
    echo ?? Instala Python 3.11 desde python.org
    pause
    exit /b 1
)

echo  Python detectado

REM Instalar dependencias si es necesario
echo.
echo  Verificando dependencias...
python -c "import cv2" > nul 2>&1
if errorlevel 1 (
    echo   OpenCV no instalado. Instalando...
    pip install opencv-contrib-python numpy pyautogui psutil --quiet
    echo  Dependencias instaladas
) else (
    echo  Dependencias ya instaladas
)

REM Ejecutar bot
echo.
echo  Iniciando bot extremo...
echo   Presiona Ctrl+C para detener
echo ================================================
cd /d "%~dp0"
python "extreme_optimization\extreme_bot_simple.py"

pause
