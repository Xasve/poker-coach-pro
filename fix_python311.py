# fix_python311.py
import subprocess
import sys
import os

def run(cmd):
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("[OK]")
        if result.stdout:
            for line in result.stdout.strip().split('\n')[:3]:  # Mostrar primeras 3 líneas
                if line:
                    print(f"  {line}")
    else:
        print(f"[ERROR] {result.stderr[:200]}")
    
    return result.returncode == 0

def main():
    print("=== CONFIGURACION PARA PYTHON 3.11 ===")
    print("=" * 60)
    
    # Verificar Python version
    print("\n1. Verificando version de Python...")
    version_result = subprocess.run("python --version", shell=True, capture_output=True, text=True)
    
    if "3.11" in version_result.stdout:
        print(f"[OK] Python correcto: {version_result.stdout.strip()}")
    else:
        print(f"[ERROR] Python incorrecto: {version_result.stdout.strip()}")
        print("\n[SOLUCION] Usa Python 3.11:")
        print("  py -3.11 -m venv venv")
        print("  .\\venv\\Scripts\\Activate.ps1")
        return False
    
    # 2. Desinstalar NumPy 2.x si existe
    print("\n2. Limpiando instalaciones conflictivas...")
    run("pip uninstall -y numpy opencv-python opencv-contrib-python")
    
    # 3. Instalar NumPy 1.x (compatible con OpenCV)
    print("\n3. Instalando NumPy 1.x...")
    run("pip install numpy==1.24.4")
    
    # 4. Instalar OpenCV compatible
    print("\n4. Instalando OpenCV compatible...")
    run("pip install opencv-python==4.9.0.80")
    
    # 5. Instalar otras dependencias
    print("\n5. Instalando otras dependencias...")
    
    packages = [
        "pillow==10.3.0",
        "mss==9.0.1",
        "pyyaml==6.0.1",
        "pyautogui==0.9.54",
        "pytesseract==0.3.10",
    ]
    
    for package in packages:
        run(f"pip install {package}")
    
    # 6. Verificar compatibilidad
    print("\n6. Verificando compatibilidad...")
    
    test_code = '''
import numpy as np
import cv2
print(f"NumPy: {np.__version__}")
print(f"OpenCV: {cv2.__version__}")

# Test de compatibilidad
arr = np.zeros((10, 10, 3), dtype=np.uint8)
gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
print(f"Compatibilidad: OK - {arr.shape} -> {gray.shape}")
'''
    
    with open("test_compat_temp.py", "w") as f:
        f.write(test_code)
    
    run("python test_compat_temp.py")
    
    # Limpiar
    if os.path.exists("test_compat_temp.py"):
        os.remove("test_compat_temp.py")
    
    print("\n" + "=" * 60)
    print("[COMPLETADO] Sistema configurado para Python 3.11")
    print("\n[PROXIMOS PASOS]")
    print("1. python test_system_basic.py")
    print("2. Si hay errores, reinicia PowerShell")
    
    return True

if __name__ == "__main__":
    main()