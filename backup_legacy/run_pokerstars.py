# run_pokerstars.py - Sistema principal para PokerStars
import sys
import os
import time
import cv2

print("🚀 POKER COACH PRO - SISTEMA PRINCIPAL")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

def main():
    """Función principal del sistema"""
    try:
        from platforms.pokerstars_adapter import PokerStarsAdapter
        from integration.coach_integrator import CoachIntegrator
        
        print("🎴 Inicializando Poker Coach Pro...")
        
        # Inicializar componentes
        adapter = PokerStarsAdapter()
        coach = CoachIntegrator(platform="pokerstars")
        
        print("✅ Sistema inicializado")
        print(f"🔄 Modo sigilo: Nivel {adapter.stealth_level}")
        
        # Contadores para estadísticas
        frames_captured = 0
        tables_detected = 0
        hands_analyzed = 0
        
        print("\n📡 Esperando mesa de PokerStars...")
        print("💡 Asegúrate de tener PokerStars abierto en una mesa")
        print("📌 Presiona Ctrl+C para detener\n")
        
        try:
            while True:
                # Capturar pantalla
                screenshot = adapter.capture_table()
                
                if screenshot is not None:
                    frames_captured += 1
                    
                    # Detectar mesa
                    table_detected = adapter.detect_table(screenshot)
                    
                    if table_detected:
                        tables_detected += 1
                        
                        if tables_detected == 1:
                            print(f"✅ Mesa detectada! Iniciando análisis...")
                        
                        # Obtener información de la mesa
                        table_info = adapter.get_table_info(screenshot)
                        
                        # Reconocer cartas
                        hole_cards = adapter.recognize_hole_cards(screenshot)
                        community_cards = adapter.recognize_community_cards(screenshot)
                        
                        # Reconocer montos
                        pot_size = adapter.recognize_pot_size(screenshot)
                        stack_sizes = adapter.recognize_stack_sizes(screenshot)
                        
                        # Crear situación para análisis
                        situation = {
                            "hole_cards": hole_cards,
                            "community_cards": community_cards,
                            "pot_size": pot_size,
                            "stack_sizes": stack_sizes,
                            "table_info": table_info
                        }
                        
                        # Analizar con coach
                        recommendation = coach.analyze_hand(situation)
                        
                        if recommendation:
                            hands_analyzed += 1
                            
                            # Mostrar recomendación
                            print(f"\n📊 Análisis #{hands_analyzed}")
                            print(f"   Tus cartas: {hole_cards}")
                            print(f"   Mesa: {community_cards}")
                            print(f"   Bote: ${pot_size}")
                            print(f"   💡 Recomendación: {recommendation.get('action', 'CHECK')}")
                            print(f"   📈 Confianza: {recommendation.get('confidence', 0):.0%}")
                            
                            # Mostrar overlay (simulado)
                            if 'overlay' in recommendation:
                                print(f"   🎯 {recommendation['overlay']}")
                        
                        # Delay sigiloso
                        time.sleep(adapter.capture_delay)
                        
                    else:
                        if frames_captured % 10 == 0:
                            print(f"🔍 Buscando mesa... ({frames_captured} capturas)")
                
                else:
                    print("⚠️  Error en captura, reintentando...")
                
                # Pequeño delay entre iteraciones
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Sistema detenido por el usuario")
            
        finally:
            # Mostrar estadísticas
            print("\n" + "=" * 60)
            print("📊 ESTADÍSTICAS DE LA SESIÓN:")
            print(f"   Capturas totales: {frames_captured}")
            print(f"   Mesas detectadas: {tables_detected}")
            print(f"   Manos analizadas: {hands_analyzed}")
            
            if frames_captured > 0:
                detection_rate = (tables_detected / frames_captured) * 100
                print(f"   Tasa de detección: {detection_rate:.1f}%")
            
            print("\n🎯 Poker Coach Pro - Sesión finalizada")
            print("=" * 60)
    
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\n🔧 Solución:")
        print("1. Ejecuta: python create_structure.py")
        print("2. Verifica que todos los módulos existan")
        print("3. Instala dependencias: pip install opencv-python mss numpy")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()