@echo off
chcp 65001 > nul
title  POKER BOT PROFESIONAL - 10+ A?OS EXPERIENCIA
color 0B

echo ================================================
echo     POKER BOT PROFESIONAL - SISTEMA EXPERTO
echo ================================================
echo  Caracter?sticas:
echo     Conocimiento de 10+ a?os de experiencia
echo     Validaci?n profesional en tiempo real
echo     Aprendizaje y mejora continuos
echo     Psicolog?a y metacognici?n integradas
echo ================================================
echo.

REM Verificar que estamos en el directorio correcto
cd /d "%~dp0"

REM Verificar dependencias
echo  Verificando dependencias...
python -c "import pandas" 2>nul
if errorlevel 1 (
    echo   Pandas no instalado. Instalando...
    python -m pip install pandas --quiet
)

python -c "import scipy" 2>nul
if errorlevel 1 (
    echo   Scipy no instalado. Instalando...
    python -m pip install scipy --quiet
)

echo  Dependencias verificadas

REM Ejecutar sistema profesional
echo.
echo  Iniciando sistema profesional...
echo   Por favor espera...

python "professional_system\integrate_professional.py"

echo.
echo  Sistema profesional finalizado
pause
