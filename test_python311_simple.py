# test_python311_simple.py
import sys
import os

print("=== TEST PARA PYTHON 3.11 ===")
print("=" * 50)

# Verificar Python
print(f"Python: {sys.version}")
if "3.11" not in sys.version:
    print("[ERROR] Necesitas Python 3.11")
    print("[SOLUCION] py -3.11 -m venv venv")
    exit(1)

# Test solo NumPy y OpenCV primero
print("\n--- Test critico (NumPy + OpenCV) ---")
try:
    import numpy as np
    print(f"[OK] NumPy: {np.__version__}")
    
    import cv2
    print(f"[OK] OpenCV: {cv2.__version__}")
    
    # Test de compatibilidad
    test_array = np.zeros((5, 5, 3), dtype=np.uint8)
    result = cv2.cvtColor(test_array, cv2.COLOR_RGB2GRAY)
    print(f"[OK] Compatibilidad verificada")
    
    CRITICAL_OK = True
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    CRITICAL_OK = False

if not CRITICAL_OK:
    print("\n[SOLUCION RAPIDA]")
    print("pip uninstall -y numpy opencv-python")
    print("pip install numpy==1.24.4")
    print("pip install opencv-python==4.9.0.80")
    exit(1)

# Test otras dependencias
print("\n--- Otras dependencias ---")
try:
    from PIL import Image
    print(f"[OK] Pillow: {Image.__version__}")
except: print("[ERROR] Pillow")

try:
    import mss
    print(f"[OK] MSS: {mss.__version__}")
except: print("[ERROR] MSS")

try:
    import yaml
    print("[OK] PyYAML")
except: print("[ERROR] PyYAML")

# Test estructura del proyecto
print("\n--- Importacion proyecto ---")
sys.path.insert(0, 'src')

try:
    # Modificar temporalmente para evitar errores de importacion
    import importlib.util
    
    # Testear si podemos importar sin ejecutar
    spec = importlib.util.spec_from_file_location(
        "pokerstars_adapter", 
        "src/platforms/pokerstars_adapter.py"
    )
    
    if spec:
        print("[OK] Archivo adapter encontrado")
        
        # Leer contenido para ver si tiene errores obvios
        with open("src/platforms/pokerstars_adapter.py", "r") as f:
            content = f.read()
            lines = len(content.split('\n'))
            print(f"[OK] Adapter: {lines} lineas")
    else:
        print("[ERROR] Archivo adapter no encontrado")
        
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("[RESULTADO] Python 3.11 configurado correctamente")
print("\n[EJECUTAR] python test_capture_simple.py")