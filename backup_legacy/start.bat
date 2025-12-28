@echo off
title Poker Coach Pro
echo  POKER COACH PRO - SISTEMA DE AN?LISIS GTO
echo ============================================

REM Verificar entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo  Entorno virtual no encontrado
    echo Ejecuta: python -m venv venv
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar dependencias
python -c "import cv2, mss" 2>nul
if errorlevel 1 (
    echo   Dependencias faltantes
    echo Instalando dependencias...
    pip install -r requirements.txt -q
)

REM Men? principal
:menu
cls
echo  POKER COACH PRO - MENU PRINCIPAL
echo ============================================
echo 1. Modo SIMULADO (pruebas)
echo 2. Detectar PokerStars (modo REAL)
echo 3. Capturar templates de cartas
echo 4. Verificar instalaci?n
echo 5. Salir
echo ============================================
set /p choice="Selecciona una opci?n (1-5): "

if "%choice%"=="1" goto simulated
if "%choice%"=="2" goto detect
if "%choice%"=="3" goto capture
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto exit

echo  Opci?n inv?lida
timeout /t 2 >nul
goto menu

:simulated
echo.
echo  Iniciando modo SIMULADO...
python main.py
pause
goto menu

:detect
echo.
echo ?? Detectando PokerStars...
echo Aseg?rate de tener PokerStars abierto en una mesa...
python detect_coords.py
pause
goto menu

:capture
echo.
echo ?? Captura de templates...
python capture_templates.py
pause
goto menu

:verify
echo.
echo  Verificando instalaci?n...
python -c "import sys; print(f'Python {sys.version}')"
python -c "import cv2; print(f'OpenCV {cv2.__version__}')"
python -c "import mss; print(f'MSS instalado')"
echo.
echo  Verificaci?n completada
pause
goto menu

:exit
echo.
echo  Hasta pronto!
timeout /t 2 >nul
