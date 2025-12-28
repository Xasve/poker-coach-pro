@echo off
chcp 65001 > nul
title ?? POKER BOT EXTREMO - VERSI?N REPARADA
color 0A

echo ================================================
echo    ?? BOT DE P?KER EXTREMO - VERSI?N REPARADA
echo ================================================
echo ? Caracter?sticas:
echo    ? Tiempo de reacci?n m?nimo (50ms objetivo)
echo     Sin restricciones de seguridad
echo     Optimizaci?n de recursos m?xima
echo     Procesamiento paralelo completo
echo ================================================
echo.

REM Verificar Python y encontrar pip correctamente
echo  Verificando Python...
where python > nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python no encontrado en PATH
    echo  Soluci?n: 
    echo 1. Abre PowerShell como Administrador
    echo 2. Ejecuta: [System.Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python311;C:\Python311\Scripts", "User")
    echo 3. Reinicia la terminal
    pause
    exit /b 1
)

REM Usar python -m pip para evitar errores de PATH
echo ? Python detectado
echo ?? Verificando y instalando dependencias...
echo.

REM M?todo 1: Intentar con python -m pip
echo ?? M?todo 1: Usando python -m pip...
python -c "import sys; print(f'Python: {sys.version.split()[0]}')" 2>nul
python -m pip install --upgrade pip --quiet 2>nul

REM M?todo 2: Verificar si pip est? disponible directamente
echo  Verificando OpenCV...
python -c "import cv2" 2>nul
if errorlevel 1 (
    echo  OpenCV no encontrado. Instalando...
    
    REM Intentar m?ltiples m?todos de instalaci?n
    echo  Intentando instalaci?n con diferentes m?todos...
    
    REM M?todo A: pip normal
    python -m pip install opencv-contrib-python numpy pyautogui psutil --quiet 2>nul
    if errorlevel 1 (
        echo  M?todo A fall?, intentando M?todo B...
        
        REM M?todo B: pip con timeout
        python -m pip install opencv-python --quiet --timeout 30 2>nul
        if errorlevel 1 (
            echo  M?todo B fall?, intentando M?todo C...
            
            REM M?todo C: Usar ruta completa de pip si existe
            where pip > pip_location.txt 2>nul
            for /f "tokens=*" %%i in (pip_location.txt) do (
                echo  Usando pip encontrado en: %%i
                "%%i" install opencv-python --quiet 2>nul
            )
            del pip_location.txt 2>nul
            
            REM Verificar de nuevo
            python -c "import cv2" 2>nul
            if errorlevel 1 (
                echo ? No se pudo instalar OpenCV autom?ticamente
                echo ?? Instalaci?n manual requerida:
                echo 1. Abre PowerShell como Administrador
                echo 2. Ejecuta: python -m pip install opencv-contrib-python
                echo 3. Luego ejecuta este archivo de nuevo
                pause
                exit /b 1
            )
        )
    )
    echo  OpenCV instalado correctamente
) else (
    echo  OpenCV ya est? instalado
)

REM Verificar todas las dependencias
echo.
echo  Verificando instalaci?n completa...
python -c "
try:
    import cv2, numpy, pyautogui, psutil
    print('? TODAS LAS DEPENDENCIAS INSTALADAS:')
    print(f'   ? OpenCV: {cv2.__version__}')
    print(f'   ? NumPy: {numpy.__version__}')
    print(f'   ? PyAutoGUI: {pyautogui.__version__}')
    print(f'    psutil: {psutil.__version__}')
except ImportError as e:
    print(f' Error: {e}')
    print(' Faltan dependencias. Instalando...')
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-contrib-python', 'numpy', 'pyautogui', 'psutil', '--quiet'])
    print('? Dependencias instaladas. Reinicia el bot.')
"

REM Ejecutar bot
echo.
echo  Iniciando bot extremo...
echo   Presiona Ctrl+C para detener
echo ================================================
cd /d "%~dp0"

REM Verificar que el script del bot existe
if not exist "extreme_optimization\extreme_bot_simple.py" (
    echo  Error: No se encuentra el script del bot
    echo  Aseg?rate de que extreme_optimization\extreme_bot_simple.py existe
    pause
    exit /b 1
)

python "extreme_optimization\extreme_bot_simple.py"

echo.
echo  Bot finalizado
pause
