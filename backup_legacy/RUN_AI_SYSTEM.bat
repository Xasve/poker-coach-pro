@echo off
chcp 65001 > nul
title  POKER AI - Sistema Completo de Detecci?n
color 0E

echo ================================================
echo     POKER AI - DETECCI?N DE CARTAS EN TIEMPO REAL
echo ================================================
echo.
echo  Este sistema ejecuta el integrador completo de IA
echo  Incluye: OCR de cartas + An?lisis GTO + Overlay
echo.
echo  OPCIONES:
echo.
echo 1.  Ejecutar sistema completo (recomendado)
echo 2.  Instalar dependencias completas
echo 3.  Ejecutar solo calibrador
echo 4.  Ejecutar modo prueba
echo 5.  Salir
echo.

set /p choice="Seleccione opci?n (1-5): "

if "%choice%"=="1" (
    echo.
    echo  INICIANDO SISTEMA COMPLETO...
    echo.
    
    REM Verificar que exista el integrador
    if exist "POKER_AI_INTEGRATOR.py" (
        echo  Integrador de IA encontrado
        echo  Iniciando an?lisis en tiempo real...
        echo.
        timeout /t 2 /nobreak > nul
        python POKER_AI_INTEGRATOR.py
    ) else (
        echo  Integrador no encontrado
        echo  Instalando primero...
        call :install_dependencies
        goto :menu_retry
    )
    
) else if "%choice%"=="2" (
    echo.
    echo ?? INSTALANDO DEPENDENCIAS COMPLETAS...
    echo.
    if exist "INSTALLER_COMPLETE.py" (
        python INSTALLER_COMPLETE.py
    ) else (
        echo ? Instalador no encontrado
        echo ?? Descargue el repositorio completo
        pause
    )
    
) else if "%choice%"=="3" (
    echo.
    echo  EJECUTANDO CALIBRADOR...
    echo.
    if exist "POKERSTARS_CALIBRATOR.py" (
        python POKERSTARS_CALIBRATOR.py
    ) else (
        echo  Calibrador no encontrado
        pause
    )
    
) else if "%choice%"=="4" (
    echo.
    echo  EJECUTANDO MODO PRUEBA...
    echo.
    if exist "POKER_AI_INTEGRATOR.py" (
        echo Ejecutando en modo prueba...
        python POKER_AI_INTEGRATOR.py
    ) else (
        echo  Integrador no encontrado
        pause
    )
    
) else if "%choice%"=="5" (
    echo.
    echo ?? Saliendo...
    timeout /t 1 /nobreak > nul
    exit /b 0
    
) else (
    echo ? Opci?n no v?lida
    pause
    goto :menu_retry
)

exit /b 0

:install_dependencies
echo  Instalando dependencias m?nimas...
python -m pip install opencv-python numpy mss pyautogui
exit /b 0

:menu_retry
call %0
