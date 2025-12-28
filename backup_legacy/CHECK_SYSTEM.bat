@echo off
chcp 65001 > nul
title  VERIFICADOR DEL SISTEMA
color 0B

echo ================================================
echo     VERIFICACI?N DEL SISTEMA POKER BOT
echo ================================================
echo Este script verifica que todo est? instalado
echo correctamente y muestra el estado del sistema.
echo ================================================
echo.

echo  INFORMACI?N DEL SISTEMA:
echo.

echo  Python:
python --version
if errorlevel 1 (
    echo  Python no encontrado en PATH
) else (
    echo  Python detectado
)

echo.
echo  DEPENDENCIAS INSTALADAS:
echo.

python -c "import cv2" 2>nul && echo  OpenCV (cv2) || echo  FALTA: OpenCV (cv2)
python -c "import numpy" 2>nul && echo  NumPy || echo  FALTA: NumPy
python -c "import pyautogui" 2>nul && echo  PyAutoGUI || echo  FALTA: PyAutoGUI
python -c "import pandas" 2>nul && echo  Pandas || echo  FALTA: Pandas
python -c "import scipy" 2>nul && echo  SciPy || echo  FALTA: SciPy

echo.
echo  ARCHIVOS DISPONIBLES:
echo.

if exist "professional_system\integrate_professional.py" (
    echo  Sistema profesional disponible
) else (
    echo   Sistema profesional no encontrado
)

if exist "extreme_optimization\extreme_bot_simple.py" (
    echo  Bot extremo disponible
) else (
    echo   Bot extremo no encontrado
)

if exist "quick_start.py" (
    echo  Sistema original disponible
) else (
    echo  Sistema original no encontrado
)

echo.
echo  RECOMENDACIONES:
echo.
python -c "import cv2" 2>nul || echo 1. Instalar OpenCV: python -m pip install opencv-python
python -c "import numpy" 2>nul || echo 2. Instalar NumPy: python -m pip install numpy

echo.
echo  COMANDOS DISPONIBLES:
echo     .\RUN_POKER_PRO.bat      - Ejecutar sistema principal
echo     .\INSTALL_ONLY.bat       - Instalar dependencias
echo     python quick_start.py    - Sistema original

echo.
pause
