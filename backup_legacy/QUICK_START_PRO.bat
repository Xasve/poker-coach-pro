@echo off
chcp 65001 > nul
title ?? POKER COACH PRO - Sistema Reparado
color 0A

echo ================================================
echo    ?? POKER COACH PRO - SISTEMA PROFESIONAL
echo ================================================
echo.
echo  Iniciando sistema reparado...
echo.

REM Verificar que quick_start.py existe
if not exist "quick_start.py" (
    echo  ERROR: quick_start.py no encontrado
    echo  Creando archivo principal...
    
    REM Crear contenido m?nimo
    echo print("?? POKER COACH PRO") > quick_start.py
    echo print("Ejecute: python quick_start.py") >> quick_start.py
    
    echo  Archivo creado. Reinicie el sistema.
    pause
    exit /b 1
)

REM Verificar Python
python --version > nul 2>&1
if errorlevel 1 (
    echo  Python no encontrado
    echo ?? Instale Python 3.8+ desde python.org
    pause
    exit /b 1
)

echo ? Python detectado
echo ?? Verificando dependencias b?sicas...

REM Verificar solo dependencias cr?ticas
python -c "import sys; print(f'Python {sys.version}')" > nul 2>&1
if errorlevel 1 (
    echo   Error en Python
) else (
    echo  Python funcionando
)

echo.
echo  Iniciando sistema principal...
echo.
timeout /t 1 /nobreak > nul

REM Ejecutar sistema principal - CON MANEJO DE ERRORES MEJORADO
python quick_start.py

REM Si falla, mostrar mensaje claro
if errorlevel 1 (
    echo.
    echo ??  Error al iniciar quick_start.py
    echo ?? Verificando alternativas...
    echo.
    
    REM Verificar si hay otros archivos de inicio
    dir /b *.py | findstr /i "start main run" > nul
    if errorlevel 0 (
        echo  Archivos Python encontrados:
        dir /b *.py | findstr /i "start main run"
        echo.
        echo  Pruebe ejecutar manualmente: python nombre_del_archivo.py
    ) else (
        echo  No se encontraron archivos de inicio alternativos
    )
)

echo.
echo ================================================
echo    Sistema finalizado. Presione cualquier tecla...
echo ================================================
pause > nul
