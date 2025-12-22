@echo off
chcp 65001 > nul
title  POKER BOT PROFESIONAL - EJECUCI?N SEGURA
color 0A

echo ================================================
echo    ?? POKER COACH PRO - SISTEMA REPARADO
echo ================================================
echo Este archivo soluciona todos los errores previos
echo y ejecuta el sistema correctamente.
echo ================================================
echo.

REM Verificar Python
python --version 2>nul
if errorlevel 1 (
    echo  Python no encontrado
    echo  Instala Python 3.11 desde python.org
    pause
    exit /b 1
)

echo  Python detectado

REM Verificar OpenCV (error m?s com?n)
echo  Verificando OpenCV (cv2)...
python -c "import cv2" 2>nul
if errorlevel 1 (
    echo   OpenCV no encontrado. Instalando...
    echo  Esto puede tomar unos minutos...
    python -m pip install opencv-contrib-python --quiet
    if errorlevel 1 (
        echo ? Error instalando OpenCV
        echo ?? Intenta: python -m pip install opencv-python
        pause
        exit /b 1
    )
    echo ? OpenCV instalado
) else (
    echo ? OpenCV ya est? instalado
)

REM Verificar otras dependencias importantes
echo ?? Verificando otras dependencias...
python -c "import numpy" 2>nul
if errorlevel 1 (
    echo  Instalando NumPy...
    python -m pip install numpy --quiet
)

python -c "import pyautogui" 2>nul
if errorlevel 1 (
    echo  Instalando PyAutoGUI...
    python -m pip install pyautogui --quiet
)

REM Ejecutar sistema
echo.
echo  Iniciando Poker Bot Professional...
echo   Por favor espera...

REM Intentar diferentes scripts en orden de prioridad
if exist "professional_system\integrate_professional.py" (
    echo  Usando sistema profesional completo...
    python "professional_system\integrate_professional.py"
) else if exist "extreme_optimization\extreme_bot_simple.py" (
    echo  Usando bot extremo optimizado...
    python "extreme_optimization\extreme_bot_simple.py"
) else if exist "quick_start.py" (
    echo  Usando sistema original...
    python quick_start.py
) else (
    echo  ERROR: No se encontr? ning?n script ejecutable
    echo  Archivos en el directorio:
    dir /b *.py
    echo  Aseg?rate de estar en la carpeta poker-coach-pro
)

echo.
echo  Programa finalizado
pause
