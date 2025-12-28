@echo off
echo 🔧 REINSTALANDO DEPENDENCIAS DEL POKER COACH PRO
echo ================================================
echo.

echo 1. SALIENDO DEL ENTORNO VIRTUAL...
call deactivate 2>nul

echo.
echo 2. ELIMINANDO ENTORNO VIRTUAL CORRUPTO...
if exist venv rmdir /s /q venv

echo.
echo 3. CREANDO NUEVO ENTORNO VIRTUAL...
python -m venv venv

echo.
echo 4. ACTIVANDO NUEVO ENTORNO...
call venv\Scripts\activate.bat

echo.
echo 5. ACTUALIZANDO PIP...
python -m pip install --upgrade pip

echo.
echo 6. INSTALANDO DEPENDENCIAS...
pip install numpy opencv-python mss pillow

echo.
echo 7. VERIFICANDO INSTALACIÓN...
python -c "import numpy; print('✅ NumPy:', numpy.__version__)"
python -c "import cv2; print('✅ OpenCV:', cv2.__version__)"
python -c "import mss; print('✅ MSS instalado')"

echo.
echo ================================================
echo ✅ REINSTALACIÓN COMPLETADA
echo.
echo 🚀 EJECUTA: python run_minimal.py
echo.
pause