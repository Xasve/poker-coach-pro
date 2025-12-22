@echo off
chcp 65001 > nul
title  POKER COACH PRO - Ejecutor Principal
color 0B

echo ================================================
echo    ?? POKER COACH PRO - EJECUTOR PRINCIPAL
echo ================================================
echo.
echo ?? OPCIONES DE EJECUCI?N:
echo.
echo 1. Sistema principal unificado (quick_start.py)
echo 2. Bot profesional
echo 3. Sistema de aprendizaje
echo 4. Verificar sistema
echo 5. Reparar problemas
echo 6. Salir
echo.

set /p choice="Seleccione opci?n (1-6): "

if "%choice%"=="1" (
    echo  Iniciando sistema principal...
    python quick_start.py
) else if "%choice%"=="2" (
    echo ?? Iniciando bot profesional...
    if exist "PROFESSIONAL_BOT_FIXED.bat" (
        call PROFESSIONAL_BOT_FIXED.bat
    ) else (
        echo ? Bot profesional no encontrado
        pause
    )
) else if "%choice%"=="3" (
    echo  Iniciando sistema de aprendizaje...
    if exist "complete_poker_learning_system.py" (
        python complete_poker_learning_system.py
    ) else (
        echo  Sistema de aprendizaje no encontrado
        pause
    )
) else if "%choice%"=="4" (
    echo ?? Verificando sistema...
    if exist "VERIFY_SYSTEM.py" (
        python VERIFY_SYSTEM.py
    ) else (
        echo ? Verificador no encontrado
        pause
    )
) else if "%choice%"=="5" (
    echo  Reparando problemas...
    if exist "FIX_ALL_PROBLEMS.ps1" (
        powershell -ExecutionPolicy Bypass -File FIX_ALL_PROBLEMS.ps1
    ) else (
        echo  Reparador no encontrado
        pause
    )
) else if "%choice%"=="6" (
    echo  Saliendo...
    timeout /t 1 /nobreak > nul
    exit /b 0
) else (
    echo ? Opci?n no v?lida
    pause
    call %0
)
