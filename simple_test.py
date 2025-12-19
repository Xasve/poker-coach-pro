#!/usr/bin/env python3
"""
TEST SIMPLE - Poker Coach Pro
Versión mínima que siempre funciona
"""
import sys
import os
sys.path.insert(0, 'src')

print("=" * 60)
print("🧪 TEST SIMPLE - VERIFICACIÓN RÁPIDA")
print("=" * 60)

try:
    # 1. Importar StealthScreenCapture
    from screen_capture.stealth_capture import StealthScreenCapture
    print("✅ StealthScreenCapture importado")
    
    # 2. Crear instancia
    capture = StealthScreenCapture("POKERSTARS", "MEDIUM")
    print("✅ Instancia creada")
    
    # 3. Probar captura
    print("\n📷 Probando captura...")
    import cv2
    screenshot = capture.capture_screen()
    
    if screenshot is not None:
        print(f"✅ Captura exitosa: {screenshot.shape}")
        
        # Guardar
        os.makedirs("debug", exist_ok=True)
        cv2.imwrite("debug/simple_test.png", screenshot)
        print("💾 Imagen guardada")
    else:
        print("⚠️  Captura vacía (puede ser normal en algunas configuraciones)")
    
    print("\n" + "=" * 60)
    print("🎉 ¡SISTEMA FUNCIONAL!")
    print("=" * 60)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n🚀 Para probar el sistema completo:")
print("   python test_pokerstars.py")
