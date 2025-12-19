#!/usr/bin/env python3
"""
Test básico de captura de pantalla
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from screen_capture.stealth_capture import StealthScreenCapture
import cv2
import time

def test_capture():
    print("=" * 60)
    print("📸 PRUEBA DE CAPTURA DE PANTALLA")
    print("=" * 60)
    
    print("\n1. Creando capturador...")
    capture = StealthScreenCapture()
    
    print("2. Capturando pantalla...")
    
    try:
        # Intentar capturar
        screenshot = capture.capture_screen()
        
        if screenshot is not None and screenshot.size > 0:
            print(f"✅ Captura exitosa!")
            print(f"   Tamaño: {screenshot.shape}")
            print(f"   Tipo: {screenshot.dtype}")
            
            # Guardar para revisión
            debug_dir = "debug_captures"
            os.makedirs(debug_dir, exist_ok=True)
            
            filename = os.path.join(debug_dir, "test_capture.png")
            cv2.imwrite(filename, screenshot)
            print(f"💾 Guardado como: {filename}")
            
            # Mostrar info adicional
            height, width, channels = screenshot.shape
            print(f"\n📊 Información:")
            print(f"   Ancho: {width} px")
            print(f"   Alto: {height} px")
            print(f"   Canales: {channels}")
            print(f"   Tamaño: {screenshot.nbytes / 1024:.1f} KB")
            
        else:
            print("❌ Captura fallida o vacía")
            
    except Exception as e:
        print(f"❌ Error durante la captura: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Prueba completada")
    print("=" * 60)

if __name__ == "__main__":
    test_capture()