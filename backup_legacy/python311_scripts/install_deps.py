# Script de instalación para Python 3.11
import subprocess
import sys

def run_command(cmd):
    print(f"Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f" {result.stdout.strip()}")
    else:
        print(f" Error: {result.stderr}")
    return result.returncode

# Actualizar pip primero
run_command(f'"{sys.executable}" -m pip install --upgrade pip')

# Lista de dependencias
dependencies = [
    "numpy",
    "opencv-contrib-python",
    "pyautogui", 
    "PyYAML",
    "pandas",
    "scikit-learn",
    "setuptools",
    "wheel"
]

print("Instalando dependencias...")
for dep in dependencies:
    run_command(f'"{sys.executable}" -m pip install {dep}')

# Verificar instalación
print("\nVerificando instalación...")
try:
    import cv2
    import numpy as np
    import pandas as pd
    print(f"✅ OpenCV {cv2.__version__}")
    print(f"✅ NumPy {np.__version__}")
    print(f"✅ Pandas {pd.__version__}")
    print("✅ Todas las dependencias instaladas correctamente")
except ImportError as e:
    print(f" Error de importación: {e}")
