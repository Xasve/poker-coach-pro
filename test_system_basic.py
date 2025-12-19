# test_system_basic.py
import sys
import os

print("=== TEST SISTEMA BASICO POKER COACH ===")
print("=" * 50)

# Informacion basica
print(f"Python: {sys.version.split()[0]}")
print(f"Directorio: {os.getcwd()}")

# Test 1: Dependencias core
print("\n--- Dependencias Core ---")
deps_status = {}

try:
    import numpy as np
    deps_status['numpy'] = f"OK (v{np.__version__})"
except ImportError:
    deps_status['numpy'] = "FALLO"

try:
    import cv2
    deps_status['opencv'] = f"OK (v{cv2.__version__})"
except ImportError:
    deps_status['opencv'] = "FALLO"

try:
    from PIL import Image
    deps_status['pillow'] = f"OK (v{Image.__version__})"
except ImportError:
    deps_status['pillow'] = "FALLO"

try:
    import mss
    deps_status['mss'] = f"OK (v{mss.__version__})"
except ImportError:
    deps_status['mss'] = "FALLO"

try:
    import yaml
    deps_status['yaml'] = "OK"
except ImportError:
    deps_status['yaml'] = "FALLO"

try:
    import pyautogui
    deps_status['pyautogui'] = "OK"
except ImportError:
    deps_status['pyautogui'] = "FALLO"

# Mostrar resultados
for dep, status in deps_status.items():
    print(f"{dep:15} : {status}")

# Test 2: OCR (opcional)
print("\n--- OCR (Opcional) ---")
try:
    import pytesseract
    print("pytesseract     : OK")
    
    # Configurar si es posible
    paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    configured = False
    for path in paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            print(f"Tesseract exe   : {path}")
            configured = True
            break
    
    if not configured:
        print("Tesseract exe   : NO ENCONTRADO")
        print("[INFO] Para OCR real, instala Tesseract")
        
except ImportError:
    print("pytesseract     : NO INSTALADO")
    print("[INFO] pip install pytesseract==0.3.10")

# Test 3: Estructura del proyecto
print("\n--- Estructura del Proyecto ---")
sys.path.insert(0, 'src')

required_files = [
    ('src/__init__.py', True),
    ('src/screen_capture/__init__.py', True),
    ('src/platforms/pokerstars_adapter.py', True),
    ('src/core/poker_engine.py', True),
    ('config/default_config.yaml', True),
    ('data/card_templates/pokerstars/', False),  # Directorio
]

for file_path, is_file in required_files:
    if os.path.exists(file_path):
        if is_file:
            size = os.path.getsize(file_path)
            print(f"OK  : {file_path} ({size} bytes)")
        else:
            count = len([f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))])
            print(f"OK  : {file_path} ({count} archivos)")
    else:
        print(f"FALT: {file_path}")

# Test 4: Importacion de modulos principales
print("\n--- Importacion de Modulos ---")
try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    print("PokerStarsAdapter: OK")
    
    # Crear instancia de prueba
    adapter = PokerStarsAdapter(stealth_level="LOW")
    print("Instancia adapter: OK")
    
    # Probar ciclo basico
    print("\n--- Test Ciclo Basico ---")
    adapter.start()
    
    import time
    time.sleep(0.5)
    
    state = adapter.get_table_state()
    if state:
        print(f"Estado mesa: {len(state)} elementos")
        if 'simulated' in state:
            print("Modo: SIMULADO (PokerStars no detectado)")
        else:
            print("Modo: REAL")
    
    adapter.stop()
    print("Ciclo completo: OK")
    
except Exception as e:
    print(f"ERROR importacion: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)

# Resumen
all_core_ok = all(status.startswith('OK') for dep, status in deps_status.items() 
                  if dep in ['numpy', 'opencv', 'pillow', 'mss'])

if all_core_ok:
    print("[RESULTADO] SISTEMA BASICO FUNCIONAL")
    print("[SIGUIENTE] Ejecutar tests especificos:")
    print("  python test_capture_system.py")
    print("  python test_pokerstars.py")
else:
    print("[RESULTADO] PROBLEMAS CON DEPENDENCIAS")
    print("[SOLUCION] Instala dependencias faltantes:")
    missing = [dep for dep, status in deps_status.items() 
               if status == "FALLO" and dep in ['numpy', 'opencv', 'pillow', 'mss']]
    if missing:
        print(f"  pip install {' '.join(missing)}")