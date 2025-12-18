"""
start_full_coach.py - Sistema completo con manejo de errores mejorado
"""

import sys
import os
import time
import logging
from pathlib import Path
import traceback

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def setup_logging():
    """Configurar logging con manejo de errores"""
    try:
        # Crear directorio logs si no existe
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Configurar logging básico primero
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        return True
    except Exception as e:
        print(f"⚠️  No se pudo configurar logging: {e}")
        print("✅ Continuando sin logging a archivo...")
        return False

def check_module_imports():
    """Verificar que todos los módulos necesarios existen"""
    print("\n🔍 Verificando módulos...")
    
    required_modules = {
        "platforms.ggpoker_adapter": ["GGPokerAdapter", "GameState"],
        "core.poker_engine": ["PokerEngine"],
        "overlay.overlay_gui": ["PokerOverlay", "Recommendation"],
        "screen_capture.adaptive_recognizer": ["AdaptiveCardRecognizer"],
        "screen_capture.text_ocr": ["TextOCR"],
        "screen_capture.table_detector": ["TableDetector"],
        "screen_capture.stealth_capture": ["StealthScreenCapture"],
        "screen_capture.card_recognizer": ["CardRecognizer", "Card"]
    }
    
    all_ok = True
    
    for module_path, classes in required_modules.items():
        try:
            # Intentar importar
            exec(f"from {module_path} import {', '.join(classes)}")
            print(f"  ✅ {module_path}")
        except ImportError as e:
            print(f"  ❌ {module_path}: {e}")
            all_ok = False
    
    return all_ok

def create_missing_files():
    """Crear archivos faltantes si es necesario"""
    print("\n📁 Verificando archivos faltantes...")
    
    missing_files = []
    
    # Verificar archivos críticos
    critical_files = [
        "src/screen_capture/adaptive_recognizer.py",
        "src/screen_capture/text_ocr.py",
        "src/core/poker_engine.py",
        "src/overlay/overlay_gui.py",
        "src/platforms/ggpoker_adapter.py"
    ]
    
    for file_path in critical_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"  ⚠️  Faltante: {file_path}")
        else:
            print(f"  ✅ Existe: {file_path}")
    
    return missing_files

def simple_test_mode():
    """Modo de prueba simple sin componentes complejos"""
    print("\n🎮 MODO DE PRUEBA SIMPLE ACTIVADO")
    print("=" * 50)
    
    try:
        print("🧪 Probando imports básicos...")
        
        # Intentar importar lo básico
        try:
            from platforms.ggpoker_adapter import GGPokerAdapter
            print("  ✅ GGPokerAdapter importado")
        except:
            print("  ⚠️  No se pudo importar GGPokerAdapter")
            print("  🔧 Creando versión mínima...")
            # Crear versión mínima
            exec(open("src/platforms/ggpoker_adapter.py").read())
        
        print("\n🎯 Sistema listo para pruebas básicas")
        print("\n📋 COMANDOS DISPONIBLES:")
        print("   1. python test_ggpoker_simple.py  - Prueba básica")
        print("   2. python start_coach.py          - Sistema simple")
        print("   3. python test_capture.py         - Prueba captura")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en modo prueba: {e}")
        return False

def main():
    """Función principal"""
    print("🎴 POKER COACH PRO - SISTEMA COMPLETO")
    print("=" * 70)
    
    # Configurar logging
    if not setup_logging():
        print("⚠️  Continuando con logging básico...")
    
    logger = logging.getLogger(__name__)
    
    try:
        # 1. Verificar módulos
        modules_ok = check_module_imports()
        
        if not modules_ok:
            print("\n⚠️  Algunos módulos faltan. Creando archivos básicos...")
            
            # Verificar archivos faltantes
            missing = create_missing_files()
            
            if missing:
                print(f"\n❌ Faltan {len(missing)} archivos críticos.")
                print("📋 Ejecuta estos comandos para crearlos:")
                
                for file in missing:
                    print(f"   New-Item -Path \"{file}\" -ItemType File -Force")
                
                print("\n🎮 Activando modo de prueba simple...")
                return simple_test_mode()
        
        # 2. Importar componentes
        print("\n🚀 Importando componentes...")
        
        from platforms.ggpoker_adapter import GGPokerAdapter
        from core.poker_engine import PokerEngine
        from overlay.overlay_gui import PokerOverlay, Recommendation
        
        print("✅ Componentes importados correctamente")
        
        # 3. Inicializar sistema
        print("\n⚙️  Inicializando sistema...")
        
        adapter = GGPokerAdapter(stealth_level="MINIMUM", learning_mode=True)
        engine = PokerEngine(aggression_factor=1.0, tightness_factor=1.0)
        overlay = PokerOverlay(position="top_right", theme="dark")
        
        print("✅ Sistema inicializado")
        
        # 4. Mostrar información
        print("\n" + "=" * 70)
        print("🎯 SISTEMA ACTIVO - POKER COACH PRO")
        print("=" * 70)
        
        print("\n📊 COMPONENTES CARGADOS:")
        print(f"   • Adaptador GG Poker: {adapter.config.get('platform', 'N/A')}")
        print(f"   • Motor de decisiones: {engine.aggression_factor} agresión")
        print(f"   • Overlay: {overlay.position} ({overlay.theme} theme)")
        
        # Estadísticas de aprendizaje
        learning_stats = adapter.card_recognizer.get_learning_stats()
        print(f"   • Cartas aprendidas: {learning_stats.get('total_learned_cards', 0)}")
        
        print("\n🔄 Ejecutando en modo demostración...")
        print("   Presiona Ctrl+C para detener")
        
        # Bucle de demostración simple
        hand_counter = 0
        
        try:
            while True:
                # Estado de juego simulado
                test_states = [
                    {
                        "hero_cards": ["Ah", "Ks"],
                        "board_cards": ["Jc", "Th", "2d"],
                        "current_street": "flop",
                        "hero_position": "BTN",
                        "pot_amount": 25.50,
                        "hero_stack": 100.0,
                        "available_actions": {"fold": True, "call": True, "raise": True}
                    },
                    {
                        "hero_cards": ["Qd", "Qh"],
                        "board_cards": ["9s", "8d", "2c"],
                        "current_street": "flop",
                        "hero_position": "CO",
                        "pot_amount": 15.0,
                        "hero_stack": 85.0,
                        "available_actions": {"fold": True, "check": True, "bet": True}
                    }
                ]
                
                for state in test_states:
                    hand_counter += 1
                    
                    # Tomar decisión
                    decision = engine.make_decision(state)
                    
                    # Crear recomendación
                    recommendation = Recommendation(
                        action=decision["action"],
                        amount=decision.get("amount", 0),
                        confidence=decision["confidence"],
                        reason=decision["reason"],
                        alternatives=decision.get("alternatives", [])
                    )
                    
                    # Actualizar overlay
                    overlay.update_recommendation(recommendation, hand_counter)
                    
                    # Mostrar en consola
                    print(f"\n🃏 MANO #{hand_counter} - Demo")
                    print(f"   Hero: {state['hero_cards']} | Board: {state['board_cards']}")
                    print(f"   Pot: ${state['pot_amount']:.2f} | Calle: {state['current_street']}")
                    print(f"   🤖 DECISIÓN: {decision['action']}")
                    print(f"      Confianza: {decision['confidence']:.1%}")
                    print(f"      Razón: {decision['reason']}")
                    
                    time.sleep(3)  # Esperar 3 segundos
                
                # Mostrar estadísticas cada 4 manos
                if hand_counter % 4 == 0:
                    print(f"\n📊 Estadísticas: {hand_counter} manos simuladas")
                    
        except KeyboardInterrupt:
            print("\n\n⏹️  Demostración detenida por el usuario")
        
        print("\n✅ Demostración completada")
        
        # Guardar datos
        print("\n💾 Guardando datos de sesión...")
        try:
            adapter.save_hand_history()
            print("  ✅ Historial de manos guardado")
        except:
            print("  ⚠️  No se pudo guardar historial")
        
        print("\n🎯 Para uso real con GG Poker:")
        print("   1. Abre GG Poker en una mesa")
        print("   2. Ejecuta: python start_coach.py")
        print("   3. El sistema analizará automáticamente")
        
        return 0
        
    except ImportError as e:
        print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
        print("\n🔧 SOLUCIÓN RÁPIDA:")
        print("   1. Verifica que los archivos existan:")
        print("      - src/platforms/ggpoker_adapter.py")
        print("      - src/core/poker_engine.py")
        print("      - src/overlay/overlay_gui.py")
        print("   2. Crea los archivos faltantes con:")
        print("      python setup_folders.py")
        
        # Intentar modo simple
        return simple_test_mode()
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        print("\n🔧 DIAGNÓSTICO:")
        print(traceback.format_exc())
        
        # Intentar modo simple como último recurso
        print("\n🔄 Intentando modo de recuperación...")
        return simple_test_mode()

if __name__ == "__main__":
    # Ejecutar con manejo de errores
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO: {e}")
        sys.exit(1)