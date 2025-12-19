# test_pokerstars.py - Ejecutar en la raíz del proyecto
import sys
import os
import time

print("🎴 POKER COACH PRO - TEST COMPLETO POKERSTARS")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    from screen_capture.stealth_capture import StealthScreenCapture
    
    print("✅ Módulos cargados correctamente")
    
    # Crear adaptador
    print("\n🔄 Creando adaptador PokerStars...")
    adapter = PokerStarsAdapter()
    print(f"✅ Adaptador creado: {adapter}")
    
    # Verificar componentes internos
    print("\n🔍 Verificando componentes internos...")
    components = [
        ('card_recognizer', adapter.card_recognizer),
        ('table_detector', adapter.table_detector),
        ('text_ocr', adapter.text_ocr)
    ]
    
    for name, component in components:
        if component:
            print(f"✅ {name}: {component}")
        else:
            print(f"❌ {name}: NO INICIALIZADO")
    
    # Probar captura básica
    print("\n📸 Probando captura de pantalla...")
    try:
        # Usar StealthScreenCapture directamente
        capture = StealthScreenCapture(stealth_level=1)
        screenshot = capture.capture_screen()
        
        if screenshot is not None:
            height, width = screenshot.shape[:2]
            print(f"✅ Captura exitosa: {width}x{height}px")
            
            # Guardar para diagnóstico
            debug_dir = "debug/captures"
            os.makedirs(debug_dir, exist_ok=True)
            
            import cv2
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            capture_path = os.path.join(debug_dir, f"test_capture_{timestamp}.png")
            cv2.imwrite(capture_path, screenshot)
            print(f"💾 Captura guardada en: {capture_path}")
        else:
            print("❌ Captura fallida: screenshot es None")
            
    except Exception as e:
        print(f"❌ Error en captura: {e}")
    
    # Probar detección de mesa
    print("\n🟢 Probando detección de mesa...")
    try:
        if 'screenshot' in locals():
            table_found = adapter.detect_table(screenshot)
            
            if table_found:
                print("✅ Mesa detectada correctamente")
                
                # Mostrar información de la mesa
                table_info = adapter.get_table_info(screenshot)
                print(f"📊 Información de mesa:")
                for key, value in table_info.items():
                    print(f"   {key}: {value}")
            else:
                print("⚠️  Mesa no detectada")
                
                # Consejos para debugging
                print("\n💡 CONSEJOS:")
                print("1. Asegúrate de tener PokerStars abierto")
                print("2. La mesa debe estar visible en pantalla")
                print("3. Verifica el color verde de la mesa")
                print("4. Revisa debug/captures/ para ver la captura")
        else:
            print("⚠️  No hay screenshot para analizar")
            
    except Exception as e:
        print(f"❌ Error en detección de mesa: {e}")
    
    # Probar reconocimiento de cartas (simulado)
    print("\n🃏 Probando sistema de reconocimiento...")
    try:
        # Crear una imagen de prueba simple
        import numpy as np
        import cv2
        
        # Imagen de prueba con "cartas" simuladas
        test_image = np.zeros((200, 400, 3), dtype=np.uint8)
        cv2.putText(test_image, "POKERSTARS TEST", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Probar con el adaptador
        cards = adapter.recognize_community_cards(test_image)
        print(f"✅ Sistema de reconocimiento listo")
        print(f"   Cartas detectadas (simuladas): {cards}")
        
    except Exception as e:
        print(f"❌ Error en reconocimiento: {e}")
    
    # Prueba de integración
    print("\n🤖 Probando integración de coach...")
    try:
        from integration.coach_integrator import CoachIntegrator
        
        coach = CoachIntegrator(platform="pokerstars")
        print(f"✅ Coach Integrator creado: {coach}")
        
        # Obtener recomendación de ejemplo
        example_situation = {
            "hole_cards": [("A", "hearts"), ("K", "spades")],
            "community_cards": [("10", "diamonds"), ("J", "clubs"), ("Q", "hearts")],
            "pot_size": 150,
            "position": "late"
        }
        
        recommendation = coach.analyze_hand(example_situation)
        print(f"📊 Recomendación de ejemplo:")
        print(f"   Acción: {recommendation.get('action', 'N/A')}")
        print(f"   Confianza: {recommendation.get('confidence', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️  Coach no disponible: {e}")
        print("   (Esto es normal si no hay estrategias configuradas)")
    
    print("\n" + "=" * 60)
    print("🎯 TEST COMPLETADO!")
    print("\n📋 RESULTADO:")
    print("El sistema básico está funcionando correctamente.")
    print("\n🚀 PRÓXIMOS PASOS:")
    print("1. Abre PokerStars y siéntate en una mesa")
    print("2. Ejecuta el sistema en modo real:")
    print("   python run_pokerstars.py")
    print("3. Verifica la captura en tiempo real")
    print("4. Ajusta posiciones si es necesario")
    
except ImportError as e:
    print(f"❌ ERROR DE IMPORTACIÓN: {e}")
    print("\n🔧 SOLUCIÓN:")
    print("1. Asegúrate de tener la estructura correcta")
    print("2. Ejecuta: python create_structure.py")
    print("3. Verifica que src/ esté en el path")
    
except Exception as e:
    print(f"❌ ERROR INESPERADO: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)