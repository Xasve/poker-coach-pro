#!/usr/bin/env python3
"""
POKER COACH PRO - VERSIÓN SIMPLIFICADA Y FUNCIONAL
"""
import sys
import os
import time

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 60)
    print("🎴 POKER COACH PRO - SISTEMA SIMPLIFICADO")
    print("=" * 60)
    
    try:
        # Importar módulos básicos
        print("\n🔧 Importando módulos...")
        from screen_capture.stealth_capture import StealthScreenCapture
        from screen_capture.table_detector import TableDetector
        
        print("✅ Módulos importados correctamente")
        
        # Crear instancias
        print("\n🛠️  Creando componentes...")
        capture = StealthScreenCapture()
        detector = TableDetector()
        
        # Inicializar captura
        print("\n📷 Inicializando captura de pantalla...")
        if capture.initialize():
            print("✅ Captura lista")
        else:
            print("⚠️  Captura tuvo problemas, continuando...")
        
        # Menú principal
        while True:
            print("\n" + "=" * 60)
            print("🎮 MENÚ PRINCIPAL")
            print("=" * 60)
            print("\n1. Probar captura de pantalla")
            print("2. Detectar mesa de poker")
            print("3. Modo demostración GTO")
            print("4. Salir")
            
            choice = input("\n👉 Selecciona una opción (1-4): ").strip()
            
            if choice == "1":
                test_capture(capture)
            elif choice == "2":
                test_table_detection(capture, detector)
            elif choice == "3":
                demo_mode()
            elif choice == "4":
                print("\n👋 ¡Hasta pronto!")
                break
            else:
                print("❌ Opción no válida")
                
    except ImportError as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Ejecuta: python fix_imports_corrected.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_capture(capture):
    """Probar captura de pantalla"""
    print("\n" + "=" * 60)
    print("📸 PRUEBA DE CAPTURA")
    print("=" * 60)
    
    print("\n⚠️  Presiona Ctrl+C para detener")
    print("📷 Capturando pantalla cada 2 segundos...")
    
    try:
        for i in range(1, 6):
            print(f"\n📸 Captura {i}/5...")
            screenshot = capture.capture_screen()
            
            if screenshot is not None:
                print(f"   ✅ Tamaño: {screenshot.shape}")
                print(f"   ✅ Tipo: {screenshot.dtype}")
                
                # Guardar para revisión
                debug_dir = "debug"
                os.makedirs(debug_dir, exist_ok=True)
                
                import cv2
                filename = f"{debug_dir}/test_capture_{i}.png"
                cv2.imwrite(filename, screenshot)
                print(f"   💾 Guardado como: {filename}")
            else:
                print("   ❌ Captura fallida")
            
            if i < 5:
                time.sleep(2)
        
        print("\n✅ Prueba de captura completada")
        
    except KeyboardInterrupt:
        print("\n🛑 Prueba interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_table_detection(capture, detector):
    """Probar detección de mesa"""
    print("\n" + "=" * 60)
    print("🎯 DETECCIÓN DE MESA")
    print("=" * 60)
    
    print("\n📷 Capturando pantalla...")
    screenshot = capture.capture_screen()
    
    if screenshot is None:
        print("❌ No se pudo capturar pantalla")
        return
    
    print("🔍 Analizando imagen...")
    table_region = detector.detect_table(screenshot)
    
    if table_region:
        x1, y1, x2, y2 = table_region
        width = x2 - x1
        height = y2 - y1
        
        print(f"\n✅ MESA DETECTADA!")
        print(f"   📍 Posición: ({x1}, {y1}) a ({x2}, {y2})")
        print(f"   📏 Tamaño: {width} x {height} píxeles")
        print(f"   📐 Área: {width * height:,} píxeles")
        
        # Guardar imagen con rectángulo
        debug_dir = "debug"
        os.makedirs(debug_dir, exist_ok=True)
        
        import cv2
        # Dibujar rectángulo
        img_with_box = screenshot.copy()
        cv2.rectangle(img_with_box, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        filename = f"{debug_dir}/table_detected.png"
        cv2.imwrite(filename, img_with_box)
        print(f"   💾 Imagen guardada: {filename}")
        
    else:
        print("\n❌ No se detectó mesa de poker")
        print("\n💡 Consejos:")
        print("   - Asegúrate de tener PokerStars/GG Poker abierto")
        print("   - La mesa debe ser visible")
        print("   - Intenta ajustar la ventana")
        
        # Guardar captura para diagnóstico
        debug_dir = "debug"
        os.makedirs(debug_dir, exist_ok=True)
        
        import cv2
        cv2.imwrite(f"{debug_dir}/no_table_detected.png", screenshot)
        print(f"   💾 Captura guardada para diagnóstico")

def demo_mode():
    """Modo demostración GTO"""
    print("\n" + "=" * 60)
    print("🧠 DEMOSTRACIÓN GTO")
    print("=" * 60)
    
    print("\n📊 Mostrando decisiones de poker avanzadas...")
    
    # Ejemplos de decisiones GTO
    examples = [
        {
            "situation": "Pre-flop, posición BU (Button)",
            "hand": "A♠ K♥",
            "action": "RAISE 3x",
            "reason": "Mano premium, posición favorable"
        },
        {
            "situation": "Flop, mesa seca",
            "hand": "Q♦ Q♣",
            "board": "Q♥ 7♠ 2♦",
            "action": "BET 2/3 del bote",
            "reason": "Top set, extraer valor"
        },
        {
            "situation": "Turn, draw flush",
            "hand": "J♣ T♣",
            "board": "9♣ 8♦ 2♥ A♠",
            "action": "CHECK-CALL",
            "reason": "Draw fuerte, pot odds favorables"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📋 Ejemplo {i}:")
        print(f"   📍 Situación: {example['situation']}")
        print(f"   🃏 Mano: {example['hand']}")
        
        if 'board' in example:
            print(f"   🎴 Mesa: {example['board']}")
        
        print(f"   🎯 Acción: {example['action']}")
        print(f"   📖 Razón: {example['reason']}")
        
        if i < len(examples):
            print("\n   ⏳ Siguiente en 3 segundos...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print("✅ Demostración completada")
    print("\n🚀 Para análisis en tiempo real:")
    print("   Usa las opciones 1 y 2 del menú principal")

if __name__ == "__main__":
    main()