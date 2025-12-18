"""
start_full_coach.py - Sistema completo integrado con overlay y motor de decisiones
"""

import sys
import os
import time
import logging
import threading
from pathlib import Path
import numpy as np

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def main():
    """Función principal del sistema completo"""
    print("🎴 POKER COACH PRO - SISTEMA COMPLETO")
    print("=" * 70)
    
    try:
        # Importar todos los componentes
        print("🚀 Cargando módulos...")
        from platforms.ggpoker_adapter import GGPokerAdapter, GameState
        from core.poker_engine import PokerEngine
        from overlay.overlay_gui import PokerOverlay, Recommendation
        
        print("✅ Módulos cargados correctamente")
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/full_session.log'),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger(__name__)
        
        # Inicializar componentes
        print("\n⚙️  Inicializando componentes...")
        
        # 1. Adaptador GG Poker (captura y análisis)
        adapter = GGPokerAdapter(stealth_level="MEDIUM", learning_mode=True)
        
        # 2. Motor de decisiones
        engine = PokerEngine(aggression_factor=1.0, tightness_factor=1.0)
        
        # 3. Overlay GUI
        overlay = PokerOverlay(position="top_right", theme="dark")
        
        print("✅ Todos los componentes inicializados")
        
        # Iniciar overlay en hilo separado
        overlay_thread = threading.Thread(target=overlay.start, daemon=True)
        overlay_thread.start()
        
        print("\n" + "=" * 70)
        print("🔄 SISTEMA ACTIVO - Esperando análisis de mesa...")
        print("   Ctrl+C para detener")
        print("=" * 70)
        
        # Variables de sesión
        hand_counter = 0
        session_stats = {
            "hands_analyzed": 0,
            "decisions_made": 0,
            "average_confidence": 0.0
        }
        
        # Bucle principal
        while True:
            try:
                # 1. Capturar y analizar mesa
                game_state = adapter.capture_and_analyze()
                
                if game_state and game_state.action_on_hero:
                    hand_counter += 1
                    
                    # 2. Convertir GameState a dict para el motor
                    game_dict = game_state.to_dict()
                    
                    # 3. Tomar decisión con el motor
                    decision = engine.make_decision(game_dict)
                    
                    # 4. Crear recomendación para el overlay
                    recommendation = Recommendation(
                        action=decision["action"],
                        amount=decision.get("amount", 0),
                        confidence=decision["confidence"],
                        reason=decision["reason"],
                        alternatives=decision.get("alternatives", [])
                    )
                    
                    # 5. Actualizar overlay
                    overlay.update_recommendation(recommendation, hand_counter)
                    
                    # 6. Mostrar información en consola
                    print(f"\n🃏 MANO #{hand_counter} - {game_state.current_street.upper()}")
                    print(f"   Hero: {game_state.hero_cards} | Board: {game_state.board_cards}")
                    print(f"   Pot: ${game_state.pot_amount:.2f} | Stack: ${game_state.hero_stack:.2f}")
                    print(f"   Posición: {game_state.hero_position}")
                    
                    # Mostrar acciones disponibles
                    available = [a.upper() for a, avail in game_state.available_actions.items() if avail]
                    print(f"   ⏰ ACCIONES DISPONIBLES: {', '.join(available)}")
                    
                    # Mostrar decisión
                    print(f"   🤖 DECISIÓN: {decision['action']} (${decision.get('amount', 0):.2f})")
                    print(f"      Confianza: {decision['confidence']:.1%}")
                    print(f"      Razón: {decision['reason']}")
                    print(f"      Fuerza de mano: {decision['hand_strength']}")
                    
                    # Actualizar estadísticas
                    session_stats["hands_analyzed"] = hand_counter
                    session_stats["decisions_made"] = engine.decisions_made
                    session_stats["average_confidence"] = engine.average_confidence
                    
                    # Pausa para no saturar
                    time.sleep(2.0)  # 2 segundos entre decisiones
                else:
                    # No es nuestro turno o error en análisis
                    if hand_counter > 0:
                        overlay.show_waiting_message()
                    
                    # Pausa más corta entre chequeos
                    time.sleep(1.0)
                
                # Auto-guardar cada 20 manos
                if hand_counter > 0 and hand_counter % 20 == 0:
                    print(f"\n💾 Auto-guardando datos...")
                    adapter.save_hand_history()
                    engine.save_config()
                    overlay.save_config()
                    
                    # Mostrar estadísticas
                    print(f"📊 Estadísticas actuales:")
                    print(f"   Manos analizadas: {session_stats['hands_analyzed']}")
                    print(f"   Decisiones tomadas: {session_stats['decisions_made']}")
                    print(f"   Confianza promedio: {session_stats['average_confidence']:.3f}")
                    
                    # Estadísticas de aprendizaje
                    learning_stats = adapter.card_recognizer.get_learning_stats()
                    print(f"   Cartas aprendidas: {learning_stats.get('total_learned_cards', 0)}")
                
            except KeyboardInterrupt:
                print("\n⏹️  Deteniendo sistema...")
                break
            except Exception as e:
                logger.error(f"Error en bucle principal: {e}")
                overlay.show_error_message(str(e)[:100])
                time.sleep(3)  # Pausa más larga en error
        
        # Guardar al finalizar
        print("\n💾 Guardando datos finales de sesión...")
        adapter.save_hand_history()
        engine.save_config()
        overlay.save_config()
        
        # Mostrar resumen final
        print("\n📈 RESUMEN FINAL DE SESIÓN:")
        print(f"   Manos analizadas: {session_stats['hands_analyzed']}")
        print(f"   Decisiones tomadas: {session_stats['decisions_made']}")
        print(f"   Confianza promedio: {session_stats['average_confidence']:.3f}")
        
        # Estadísticas de aprendizaje finales
        final_learning_stats = adapter.card_recognizer.get_learning_stats()
        print(f"   Cartas aprendidas: {final_learning_stats.get('total_learned_cards', 0)}")
        
        print("\n✅ Sesión guardada. ¡Hasta la próxima!")
        
        # Detener overlay
        overlay.stop()
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\n🔧 VERIFICA LA ESTRUCTURA:")
        print("   ¿Tienes estos archivos en src/?")
        print("   - platforms/ggpoker_adapter.py")
        print("   - core/poker_engine.py")
        print("   - overlay/overlay_gui.py")
        print("   - screen_capture/ [todos los módulos]")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())