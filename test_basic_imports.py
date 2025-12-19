# test_basic_imports.py

print("🧪 TEST DE IMPORTACIONES BÁSICAS")
print("=" * 50)

try:
    # Test 1: NumPy
    print("1. Probando NumPy...")
    import numpy as np
    print(f"   ✅ NumPy {np.__version__} importado")
    
    # Test 2: OpenCV
    print("2. Probando OpenCV...")
    import cv2
    print(f"   ✅ OpenCV {cv2.__version__} importado")
    
    # Test 3: Otras dependencias
    print("3. Probando otras dependencias...")
    from PIL import Image
    import mss
    print("   ✅ PIL y mss importados")
    
    print("=" * 50)
    print("🎉 ¡Todas las importaciones funcionan!")
    
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()