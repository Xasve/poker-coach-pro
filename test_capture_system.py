# test_capture_system.py
import sys
sys.path.insert(0, 'src')

from screen_capture.stealth_capture import StealthScreenCapture

def test_stealth_capture():
    print("🎥 TEST SISTEMA DE CAPTURA")
    print("=" * 50)
    
    try:
        # Crear capturador
        capture = StealthScreenCapture("pokerstars", "MEDIUM")
        print("✅ StealthScreenCapture creado")
        
        # Probar captura simple
        screenshot = capture.capture_screen()
        
        if screenshot is not None:
            print(f"✅ Captura exitosa - Tamaño: {screenshot.shape}")
            # Guardar para verificación
            import cv2
            cv2.imwrite("debug/test_capture.png", screenshot)
            print("📁 Captura guardada en debug/test_capture.png")
        else:
            print("⚠️  No se pudo capturar pantalla")
            
        return screenshot is not None
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_stealth_capture()
    print("=" * 50)
    print("✅ TEST COMPLETADO" if success else "❌ TEST FALLÓ")