@echo off
echo ========================================
echo    INSTALADOR CORREGIDO - POKER COACH PRO
echo ========================================
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado en PATH
    echo.
    echo SOLUCION: Agregar Python al PATH
    echo 1. Busca "Variables de entorno" en Windows
    echo 2. Click en "Variables de entorno..."
    echo 3. En "Variables del sistema", busca "Path"
    echo 4. Click "Editar" y agrega:
    echo    C:\Users\ethan\AppData\Local\Python\pythoncore-3.14-64\Scripts\
    echo    C:\Users\ethan\AppData\Local\Python\pythoncore-3.14-64\
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo Versión: 
python --version
echo.

echo 📦 Instalando usando python -m pip...
echo (Esto evita problemas de PATH)
echo.

REM 1. Actualizar pip usando python -m
echo [1/8] Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Error actualizando pip, continuando...
)

REM 2. Instalar opencv (versión headless si hay problemas)
echo [2/8] Instalando OpenCV...
python -m pip install opencv-python-headless
if errorlevel 1 (
    echo ❌ Error crítico con OpenCV
    echo Intentando con versión normal...
    python -m pip install opencv-python
)

REM 3. Instalar numpy y pillow
echo [3/8] Instalando NumPy y Pillow...
python -m pip install numpy pillow
if errorlevel 1 (
    echo ❌ Error con numpy/pillow
    pause
    exit /b 1
)

REM 4. Instalar captura de pantalla
echo [4/8] Instalando herramientas de captura...
python -m pip install pyautogui mss
if errorlevel 1 (
    echo ⚠️  Algunas herramientas de captura fallaron
    echo Continuando con instalación básica...
)

REM 5. Instalar utilidades
echo [5/8] Instalando utilidades del sistema...
python -m pip install psutil pandas
if errorlevel 1 (
    echo ⚠️  Algunas utilidades fallaron
)

REM 6. Instalar base de datos
echo [6/8] Instalando base de datos...
python -m pip install tinydb
if errorlevel 1 (
    echo ⚠️  Base de datos falló
)

REM 7. Crear estructura de directorios
echo [7/8] Creando estructura de directorios...
if not exist "data" mkdir data
if not exist "data\logs" mkdir data\logs
if not exist "config" mkdir config
if not exist "src" mkdir src

REM 8. Crear archivo de configuración mínimo
echo [8/8] Creando configuración mínima...
(
echo {
echo     "version": "1.0",
echo     "platform": "ggpoker",
echo     "mode": "cash",
echo     "stakes": "NL10",
echo     "overlay": {
echo         "position": "top_right",
echo         "transparency": 0.9
echo     }
echo }
) > config\simple_config.json

echo.
echo 🎉 ¡INSTALACIÓN COMPLETADA!
echo.
echo Para probar el sistema:
echo   1. Ejecuta: python prueba_rapida.py
echo   2. O usa: python poker_coach_simple.py
echo.
echo Si hay errores, ejecuta estos comandos MANUALMENTE:
echo   python -m pip install opencv-python-headless
echo   python -m pip install numpy pillow
echo   python -m pip install pyautogui
echo.
pause