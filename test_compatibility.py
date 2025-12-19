# test_compatibility.py
print("🔍 TEST DE COMPATIBILIDAD")
print("=" * 50)

try:
    # Test 1: NumPy
    import numpy as np
    print(f"✅ NumPy: {np.__version__}")
    print(f"   Esperado: 1.x.x, Actual: {np.__version__}")
    
    # Test 2: OpenCV
    import cv2
    print(f"✅ OpenCV: {cv2.__version__}")
    
    # Test 3: Crear array y procesar
    test_array = np.zeros((100, 100, 3), dtype=np.uint8)
    processed = cv2.cvtColor(test_array, cv2.COLOR_RGB2GRAY)
    print(f"✅ NumPy + OpenCV compatibles: array {test_array.shape} -> {processed.shape}")
    
    # Test 4: Otras dependencias
    from PIL import Image
    import mss
    import pytesseract
    import yaml
    import pyautogui
    
    print("✅ Todas las dependencias importadas")
    
    print("\n📊 RESUMEN:")
    print(f"NumPy: {np.__version__}")
    print(f"OpenCV: {cv2.__version__}")
    print(f"Python: {sys.version.split()[0]}")
    
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()