#!/usr/bin/env python3
"""
POKER COACH PRO - VERSIÓN FUNCIONAL
Sistema básico pero operativo
"""
import sys
import os
import time

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 60)
    print("🎴 POKER COACH PRO - SISTEMA BÁSICO")
    print("=" * 60)
    
    try:
        # Importar módulos
        print("
🔧 Importando módulos...")
        from screen_capture.stealth_capture import StealthScreenCapture
        from screen_capture.table_detector import TableDetector
        
        print("✅ Módulos importados correctamente")
        
        # Crear componentes
        print("
🛠️  Creando componentes...")
        capture = StealthScreenCapture()
        detector = TableDetector()
        
        print("✅ Componentes creados")
        
        # Menú simple
        while True:
            print("
" + "=" * 60)
            print("🎮 MENÚ PRINCIPAL")
            print("=" * 60)
            print("
1. Probar captura de pantalla")
            print("2. Buscar mesa de poker")
            print("3. Salir")
            
            try:
                option = input("
👉 Selecciona una opción (1-3): ").strip()
                
                if option == "1":
                    test_capture(capture)
                elif option == "2":
                    find_table(capture, detector)
                elif option == "3":
                    print("
👋 ¡Hasta pronto!")
                    break
                else:
                    print("❌ Opción no válida")
                    
            except KeyboardInterrupt:
                print("

🛑 Operación cancelada")
                break
            except Exception as e:
                print(f"
❌ Error: {e}")
                
    except ImportError as e:
        print(f"
❌ ERROR DE IMPORTACIÓN: {e}")
        print("
💡 Ejecuta: python fix_all.py")
    except Exception as e:
        print(f"
❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_capture(capture):
    """Probar la captura de pantalla"""
    print("
" + "=" * 60)
    print("📸 PRUEBA DE CAPTURA")
    print("=" * 60)
    
    print("
Inicializando captura...")
    if capture.initialize():
        print("✅ Captura inicializada")
    else:
        print("❌ No se pudo inicializar la captura")
        return
    
    print("
Capturando pantalla...")
    screenshot = capture.capture()
    
    if screenshot is not None:
        print(f"✅ Captura exitosa!")
        print(f"   Tamaño: {screenshot.shape}")
        print(f"   Tipo: {screenshot.dtype}")
        
        # Guardar para revisión
        os.makedirs("debug", exist_ok=True)
        import cv2
        filename = "debug/test_capture.png"
        cv2.imwrite(filename, screenshot)
        print(f"   💾 Guardado como: {filename}")
        
        # Mostrar información básica
        print(f"
📊 Información de la imagen:")
        print(f"   Ancho: {screenshot.shape[1]} px")
        print(f"   Alto: {screenshot.shape[0]} px")
        print(f"   Canales: {screenshot.shape[2]}")
        
    else:
        print("❌ No se pudo capturar la pantalla")

def find_table(capture, detector):
    """Buscar mesa de poker"""
    print("
" + "=" * 60)
    print("🎯 BUSCANDO MESA DE POKER")
    print("=" * 60)
    
    print("
1. Inicializando captura...")
    if not capture.initialize():
        print("❌ No se pudo inicializar la captura")
        return
    
    print("2. Capturando pantalla...")
    screenshot = capture.capture()
    
    if screenshot is None:
        print("❌ No se pudo capturar la pantalla")
        return
    
    print("3. Analizando imagen...")
    has_table = detector.detect(screenshot)
    
    if has_table:
        print("
✅ ¡MESA DETECTADA!")
        print("
💡 Consejos:")
        print("   - El sistema encontró una posible mesa de poker")
        print("   - Basado en la detección de áreas verdes")
        print("   - Asegúrate de que PokerStars/GG Poker esté visible")
    else:
        print("
❌ No se detectó mesa de poker")
        print("
💡 Posibles causas:")
        print("   - No hay ventana de poker visible")
        print("   - La mesa no es verde")
        print("   - La captura falló")
    
    # Guardar captura siempre
    os.makedirs("debug", exist_ok=True)
    import cv2
    filename = "debug/table_search.png"
    cv2.imwrite(filename, screenshot)
    print(f"
💾 Captura guardada: {filename}")

if __name__ == "__main__":
    main()
