#!/usr/bin/env python3
"""
POKER COACH PRO - SCRIPT PRINCIPAL
Versión simplificada y funcional
"""
import sys
import os
import time

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 60)
    print("🎴 POKER COACH PRO - SISTEMA DEFINITIVO")
    print("=" * 60)
    
    print("\n🚀 Inicializando sistema...")
    
    try:
        # 1. Verificar que podemos importar screen_capture
        print("\n🔍 Probando importación de screen_capture...")
        from screen_capture.stealth_capture import StealthScreenCapture
        
        print("✅ Módulo screen_capture importado correctamente")
        
        # 2. Crear capturador
        capturador = StealthScreenCapture()
        print("✅ Capturador de pantalla creado")
        
        # 3. Intentar capturar pantalla
        print("\n📷 Probando captura de pantalla...")
        screenshot = capturador.capture_screen()
        
        if screenshot is not None and screenshot.size > 0:
            print(f"✅ Captura exitosa - Tamaño: {screenshot.shape}")
        else:
            print("⚠️  Captura vacía o nula")
        
        # 4. Verificar si hay mesa de poker
        print("\n🎯 Buscando mesa de poker...")
        
        # Importar detector de mesa
        try:
            from screen_capture.table_detector import TableDetector
            detector = TableDetector()
            mesa = detector.detect_table(screenshot)
            
            if mesa:
                print(f"✅ Mesa detectada en: {mesa}")
            else:
                print("⚠️  No se detectó mesa de poker")
                
        except ImportError:
            print("⚠️  TableDetector no disponible, continuando...")
        
        # 5. Mostrar opciones
        print("\n" + "=" * 60)
        print("🎮 SISTEMA LISTO - ELIGE UN MODO:")
        print("=" * 60)
        print("\n1. Modo TIEMPO REAL (PokerStars/GG Poker)")
        print("   - Necesitas tener el casino abierto")
        print("   - Detecta mesa automáticamente")
        print("   - Analiza y recomienda en tiempo real")
        
        print("\n2. Modo DEMOSTRACIÓN")
        print("   - Funciona sin casino real")
        print("   - Muestra decisiones GTO de ejemplo")
        print("   - Perfecto para probar el sistema")
        
        print("\n3. Modo CAPTURA SOLA")
        print("   - Solo captura y guarda pantallas")
        print("   - Para debugging y calibración")
        
        print("\n4. SALIR")
        
        # 6. Esperar selección
        print("\n" + "-" * 60)
        opcion = input("👉 Selecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            modo_tiempo_real()
        elif opcion == "2":
            modo_demostracion()
        elif opcion == "3":
            modo_captura()
        else:
            print("\n👋 ¡Hasta pronto!")
        
    except ImportError as e:
        print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
        print("\n💡 SOLUCIÓN RÁPIDA:")
        print("   1. Ejecuta: python fix_imports.py")
        print("   2. Verifica que existe: src/screen_capture/__init__.py")
        print("   3. Intenta de nuevo")
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()

def modo_tiempo_real():
    """Modo para usar con PokerStars/GG Poker real"""
    print("\n" + "=" * 60)
    print("🎮 MODO TIEMPO REAL ACTIVADO")
    print("=" * 60)
    
    print("\n📋 INSTRUCCIONES:")
    print("   1. Abre PokerStars o GG Poker")
    print("   2. Abre una mesa de cash o torneo")
    print("   3. Asegúrate de que la mesa sea visible")
    print("   4. El sistema empezará a analizar automáticamente")
    print("\n⏳ Iniciando en 5 segundos...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🔍 Analizando mesa...")
    
    try:
        from screen_capture.stealth_capture import StealthScreenCapture
        from screen_capture.table_detector import TableDetector
        
        capturador = StealthScreenCapture()
        detector = TableDetector()
        
        print("\n🔄 Capturando y analizando (Ctrl+C para detener)...")
        
        contador = 0
        while True:
            contador += 1
            
            # Capturar pantalla
            screenshot = capturador.capture_screen()
            
            # Detectar mesa
            mesa = detector.detect_table(screenshot)
            
            if mesa:
                print(f"✅ Iteración {contador}: Mesa detectada")
                
                # Aquí iría el análisis GTO completo
                # Por ahora solo mostramos que funciona
                
                # Guardar captura de debug cada 10 iteraciones
                if contador % 10 == 0:
                    debug_dir = "debug"
                    os.makedirs(debug_dir, exist_ok=True)
                    import cv2
                    cv2.imwrite(f"{debug_dir}/captura_{contador}.png", screenshot)
                    print(f"   📸 Captura guardada: debug/captura_{contador}.png")
            else:
                print(f"⚠️  Iteración {contador}: No se detecta mesa")
                print("   💡 Asegúrate de tener PokerStars/GG visible")
            
            # Pequeña pausa
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Detenido por usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def modo_demostracion():
    """Modo de demostración sin casino real"""
    print("\n" + "=" * 60)
    print("🎮 MODO DEMOSTRACIÓN ACTIVADO")
    print("=" * 60)
    
    print("\n📊 Mostrando decisiones GTO de ejemplo...")
    
    # Decisiones de ejemplo
    decisiones = [
        {"mano": "A♠ K♠", "mesa": "J♥ 8♦ 2♣", "accion": "RAISE", "confianza": 85},
        {"mano": "Q♦ Q♣", "mesa": "Q♥ 7♠ 2♦ 9♣", "accion": "BET", "confianza": 92},
        {"mano": "J♣ T♣", "mesa": "9♣ 8♦ 2♥", "accion": "CALL", "confianza": 78},
        {"mano": "7♠ 7♥", "mesa": "A♦ K♥ Q♠", "accion": "FOLD", "confianza": 95},
    ]
    
    for i, decision in enumerate(decisiones, 1):
        print(f"\n📋 Ejemplo {i}:")
        print(f"   🃏 Mano: {decision['mano']}")
        print(f"   🎴 Mesa: {decision['mesa']}")
        print(f"   🎯 Decisión: {decision['accion']}")
        print(f"   📊 Confianza: {decision['confianza']}%")
        
        if i < len(decisiones):
            print("\n   ⏳ Siguiente ejemplo en 3 segundos...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print("✅ Demostración completada")
    print("\n🚀 Para usar con PokerStars real:")
    print("   Ejecuta de nuevo y selecciona 'Modo TIEMPO REAL'")

def modo_captura():
    """Solo captura y guarda pantallas"""
    print("\n" + "=" * 60)
    print("📸 MODO CAPTURA ACTIVADO")
    print("=" * 60)
    
    try:
        from screen_capture.stealth_capture import StealthScreenCapture
        
        capturador = StealthScreenCapture()
        
        print("\n🔄 Capturando pantallas (Ctrl+C para detener)...")
        print("   Las capturas se guardan en: debug/")
        
        contador = 0
        debug_dir = "debug"
        os.makedirs(debug_dir, exist_ok=True)
        import cv2
        
        while True:
            contador += 1
            
            screenshot = capturador.capture_screen()
            
            if screenshot is not None and screenshot.size > 0:
                filename = f"{debug_dir}/captura_{contador:04d}.png"
                cv2.imwrite(filename, screenshot)
                print(f"✅ Captura {contador} guardada: {filename}")
            else:
                print(f"⚠️  Captura {contador} fallida")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Captura detenida")
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("💡 Ejecuta: python fix_imports.py")

if __name__ == "__main__":
    main()