# install_all_deps.py
import subprocess
import sys

def run_cmd(cmd):
    """Ejecutar comando y mostrar resultado"""
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("[OK] Completado")
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line:
                    print(f"  {line}")
    else:
        print(f"[ERROR] Codigo: {result.returncode}")
        if result.stderr:
            print(f"  {result.stderr[:200]}")
    
    return result.returncode == 0

def main():
    print("=== INSTALACION COMPLETA DE DEPENDENCIAS ===")
    print("=" * 60)
    
    # 1. Dependencias esenciales
    print("\n1. Instalando dependencias esenciales...")
    
    essential_packages = [
        "numpy==1.24.4",
        "opencv-python==4.9.0.80",
        "pillow==10.3.0",
        "mss==9.0.1",
        "pyyaml==6.0.1",
        "pyautogui==0.9.54",
    ]
    
    for package in essential_packages:
        if not run_cmd(f"pip install {package}"):
            print(f"[ADVERTENCIA] Fallo instalacion de {package}")
    
    # 2. Dependencias opcionales
    print("\n2. Instalando dependencias opcionales...")
    
    optional_packages = [
        "pytesseract==0.3.10",
    ]
    
    for package in optional_packages:
        run_cmd(f"pip install {package}")
    
    # 3. Verificar instalacion
    print("\n3. Verificando instalacion...")
    
    verify_code = '''
import sys
print(f"Python: {sys.version.split()[0]}")

try:
    import numpy as np
    print(f"numpy: {np.__version__}")
except: print("numpy: ERROR")

try:
    import cv2
    print(f"opencv: {cv2.__version__}")
except: print("opencv: ERROR")

try:
    from PIL import Image
    print(f"pillow: {Image.__version__}")
except: print("pillow: ERROR")

try:
    import mss
    print(f"mss: {mss.__version__}")
except: print("mss: ERROR")
'''
    
    with open("verify_temp.py", "w", encoding="utf-8") as f:
        f.write(verify_code)
    
    run_cmd("python verify_temp.py")
    
    # Limpiar
    import os
    if os.path.exists("verify_temp.py"):
        os.remove("verify_temp.py")
    
    print("\n" + "=" * 60)
    print("[COMPLETADO] Instalacion finalizada")
    print("\n[PROXIMOS PASOS]")
    print("1. Ejecutar: python test_system_basic.py")
    print("2. Si necesitas OCR, instala Tesseract:")
    print("   https://github.com/UB-Mannheim/tesseract/wiki")
    print("3. Abre PokerStars para pruebas reales")

if __name__ == "__main__":
    main()