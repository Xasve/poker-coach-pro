# test_real_capture.py - Prueba con PokerStars real
import sys
import os
import time
import cv2
import json

print("🎴 POKER COACH PRO - PRUEBA CON POKERSTARS REAL")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    print("🔧 Inicializando sistema...")
    
    # Crear adaptador con nivel de sigilo medio
    adapter = PokerStarsAdapter(stealth_level=2)
    
    print("\n🎯 INSTRUCCIONES:")
    print("1. Abre PokerStars y siéntate en una mesa de cash o torneo")
    print("2. Asegúrate de que la mesa sea visible en pantalla")
    print("3. El sistema intentará detectar la mesa automáticamente")
    print("4. Presiona Ctrl+C para detener la prueba")
    print("\n⏳ Iniciando en 5 segundos...")
    
    time.sleep(5)
    
    # Contadores
    capture_count = 0
    table_detected_count = 0
    capture_errors = 0
    
    # Directorio para debug
    debug_dir = "debug/real_test"
    os.makedirs(debug_dir, exist_ok=True)
    
    print("\n📡 INICIANDO CAPTURA EN TIEMPO REAL...")
    print("-" * 40)
    
    try:
        while True:
            capture_count += 1
            print(f"\n🔄 Captura #{capture_count}")
            
            # 1. Capturar pantalla
            print("   📸 Capturando pantalla...")
            screenshot = adapter.capture_table()
            
            if screenshot is None:
                print("   ❌ Error: No se pudo capturar pantalla")
                capture_errors += 1
                time.sleep(1)
                continue
            
            # Mostrar info de la captura
            height, width = screenshot.shape[:2]
            print(f"   ✅ Captura: {width}x{height}px")
            
            # 2. Guardar primera captura para análisis
            if capture_count == 1:
                first_capture_path = os.path.join(debug_dir, "first_capture.png")
                cv2.imwrite(first_capture_path, screenshot)
                print(f"   💾 Primera captura guardada: {first_capture_path}")
            
            # 3. Detectar mesa
            print("   🔍 Detectando mesa...")
            table_detected = adapter.detect_table(screenshot)
            
            if table_detected:
                table_detected_count += 1
                print("   🟢 ¡MESA DETECTADA!")
                
                # 4. Obtener información de la mesa
                table_info = adapter.get_table_info(screenshot)
                print(f"   📊 Info mesa: {table_info}")
                
                # 5. Probar reconocimiento de cartas (si hay mesa)
                print("   🃏 Probando reconocimiento de cartas...")
                
                # Cartas del jugador
                hole_cards = adapter.recognize_hole_cards(screenshot)
                print(f"   👤 Tus cartas: {hole_cards}")
                
                # Cartas comunitarias
                community_cards = adapter.recognize_community_cards(screenshot)
                print(f"   🎯 Cartas comunitarias: {community_cards}")
                
                # 6. Guardar captura con mesa detectada
                if table_detected_count <= 3:  # Solo guardar primeras 3
                    capture_path = os.path.join(debug_dir, f"table_detected_{table_detected_count}.png")
                    cv2.imwrite(capture_path, screenshot)
                    print(f"   💾 Captura guardada: {capture_path}")
                
                # 7. Mostrar estadísticas
                detection_rate = (table_detected_count / capture_count) * 100
                print(f"   📈 Tasa de detección: {detection_rate:.1f}%")
                
            else:
                print("   ❌ Mesa no detectada")
                
                # Guardar algunas capturas sin mesa para debugging
                if capture_count % 10 == 0:
                    capture_path = os.path.join(debug_dir, f"no_table_{capture_count}.png")
                    cv2.imwrite(capture_path, screenshot)
                    print(f"   💾 Captura sin mesa guardada")
            
            # 8. Delay entre capturas (configurable por sigilo)
            delay = adapter.capture_delay
            print(f"   ⏳ Esperando {delay}s...")
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Prueba detenida por el usuario")
        
    finally:
        # Mostrar estadísticas finales
        print("\n" + "=" * 60)
        print("📊 ESTADÍSTICAS FINALES DE LA PRUEBA:")
        print(f"   Capturas totales: {capture_count}")
        print(f"   Mesas detectadas: {table_detected_count}")
        print(f"   Errores de captura: {capture_errors}")
        
        if capture_count > 0:
            detection_rate = (table_detected_count / capture_count) * 100
            success_rate = ((capture_count - capture_errors) / capture_count) * 100
            
            print(f"   Tasa de detección: {detection_rate:.1f}%")
            print(f"   Tasa de éxito captura: {success_rate:.1f}%")
        
        print(f"   Archivos guardados en: {debug_dir}/")
        
        # Guardar configuración usada
        config_data = {
            "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "capture_count": capture_count,
            "table_detected_count": table_detected_count,
            "capture_errors": capture_errors,
            "adapter_config": {
                "platform": adapter.platform,
                "stealth_level": adapter.stealth_level,
                "capture_delay": adapter.capture_delay
            }
        }
        
        config_path = os.path.join(debug_dir, "test_config.json")
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"   Configuración guardada: {config_path}")
        
        print("\n🎯 RECOMENDACIONES:")
        if table_detected_count == 0:
            print("   ❌ No se detectaron mesas. Verifica que:")
            print("      1. PokerStars esté abierto y visible")
            print("      2. La mesa tenga fondo verde característico")
            print("      3. Revisa las capturas en debug/real_test/")
        elif detection_rate < 50:
            print("   ⚠️  Baja tasa de detección. Posibles soluciones:")
            print("      1. Ajustar umbrales en TableDetector")
            print("      2. Verificar iluminación/colores de pantalla")
            print("      3. Probar diferentes mesas/torneos")
        else:
            print("   ✅ ¡Sistema funcionando correctamente!")
            print("      Procede a probar el sistema completo con:")
            print("      python run_pokerstars.py")
        
        print("\n" + "=" * 60)

except ImportError as e:
    print(f"❌ ERROR DE IMPORTACIÓN: {e}")
    print("\n🔧 Solución: Ejecuta primero:")
    print("   python final_test.py")
    
except Exception as e:
    print(f"❌ ERROR INESPERADO: {e}")
    import traceback
    traceback.print_exc()