# test_capture_simple.py
import sys
sys.path.insert(0, 'src')

print("=== TEST CAPTURA SIMPLE ===")
print("=" * 50)

# Test solo MSS (sin OpenCV para captura basica)
try:
    import mss
    import numpy as np
    from PIL import Image
    
    print("[OK] Dependencias de captura cargadas")
    
    # Capturar pantalla
    with mss.mss() as sct:
        # Capturar monitor principal
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        print(f"[OK] Captura exitosa")
        print(f"  - Tamaño: {screenshot.width}x{screenshot.height}")
        print(f"  - Formato: {screenshot.raw}")
        
        # Convertir a PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        
        # Guardar para verificar
        img.save("debug/simple_capture.jpg")
        print(f"[OK] Imagen guardada: debug/simple_capture.jpg")
        
        # Convertir a numpy array si OpenCV funciona
        try:
            import cv2
            img_array = np.array(img)
            print(f"[OK] Convertido a array NumPy: {img_array.shape}")
            
            # Procesamiento simple con OpenCV
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            print(f"[OK] Procesado con OpenCV: {gray.shape}")
            
        except Exception as e:
            print(f"[INFO] OpenCV no disponible para procesamiento: {e}")
    
except Exception as e:
    print(f"[ERROR] Captura fallo: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("[COMPLETADO] Test de captura finalizado")