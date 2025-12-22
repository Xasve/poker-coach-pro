@echo off
chcp 65001 > nul
title  POKER BOT PRO - INICIO R?PIDO
color 0A

echo ================================================
echo     POKER COACH PRO - SISTEMA PROFESIONAL
echo ================================================
echo Este script soluciona todos los problemas y
echo ejecuta el sistema profesional correctamente.
echo ================================================
echo.

cd /d "%~dp0"

echo  Paso 1: Instalando dependencias necesarias...
echo    (Esto puede tomar unos minutos)

REM Instalar OpenCV primero (el m?s importante)
python -c "import cv2" 2>nul
if errorlevel 1 (
    echo  Instalando OpenCV...
    python -m pip install opencv-contrib-python --quiet
    if errorlevel 1 (
        echo   Error con opencv-contrib, probando opencv-python...
        python -m pip install opencv-python --quiet
    )
    echo  OpenCV instalado
) else (
    echo  OpenCV ya est? instalado
)

REM Instalar otras dependencias esenciales
echo  Instalando otras dependencias...
python -m pip install numpy --quiet
python -m pip install pyautogui --quiet
python -m pip install pandas --quiet
echo  Dependencias b?sicas instaladas

REM Instalar dependencias profesionales (opcionales)
echo  Instalando dependencias profesionales...
python -c "import scipy" 2>nul
if errorlevel 1 (
    python -m pip install scipy --quiet
    echo  Scipy instalado
) else (
    echo  Scipy ya est? instalado
)

echo.
echo  Paso 2: Verificando instalaci?n...
python -c "
try:
    import cv2, numpy, pandas, pyautogui
    print(' TODAS LAS DEPENDENCIAS INSTALADAS:')
    print(f'   OpenCV: {cv2.__version__}')
    print(f'   NumPy: {numpy.__version__}')
    print(f'   Pandas: {pandas.__version__}')
    print(' Sistema profesional listo!')
except ImportError as e:
    print(f' Error: {e}')
    print(' Intenta: python -m pip install [paquete_faltante]')
"

echo.
echo  Paso 3: Iniciando sistema profesional...
echo   Cargando conocimiento de 10+ a?os...

REM Verificar que el script profesional existe
if exist "professional_system\integrate_professional.py" (
    python "professional_system\integrate_professional.py"
) else if exist "extreme_optimization\extreme_bot_simple.py" (
    echo   Sistema profesional no encontrado, usando bot extremo
    python "extreme_optimization\extreme_bot_simple.py"
) else (
    echo  ERROR: No se encontr? ning?n script de bot
    echo  Ejecuta primero: python quick_start.py
)

pause
