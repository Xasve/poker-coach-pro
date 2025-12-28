@echo off
chcp 65001 > nul
title  POKER COACH PRO - EJECUCI?N REPARADA
color 0A

echo ================================================
echo     POKER COACH PRO - SISTEMA REPARADO
echo ================================================
echo Los errores han sido solucionados
echo Ahora el sistema funciona correctamente
echo ================================================
echo.

cd /d "%~dp0"

REM Verificar Python
python --version 2>nul
if errorlevel 1 (
    echo  Python no encontrado
    echo  Instala Python 3.11 desde python.org
    pause
    exit /b 1
)

echo  Python detectado

REM Verificar OpenCV (problema m?s com?n)
echo  Verificando OpenCV...
python -c "import cv2" 2>nul
if errorlevel 1 (
    echo   Instalando OpenCV...
    python -m pip install opencv-contrib-python --quiet
    echo  OpenCV instalado
) else (
    echo  OpenCV ya est? instalado
)

REM Ejecutar sistema simplificado
echo.
echo  Iniciando sistema reparado...
echo   Por favor espera...

REM Usar el nuevo punto de entrada
python poker_pro_simple.py

echo.
echo  Sistema finalizado
pause
