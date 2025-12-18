#!/usr/bin/env python3
"""
Script principal unificado para Poker Coach Pro - VERSIÓN CORREGIDA
"""
import os
import sys
import logging
from pathlib import Path

# Añadir src al path ANTES de cualquier import
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/coach_pro.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def check_imports():
    """Verificar que todos los imports funcionen"""
    print(" Verificando imports y compatibilidad...")
    print("-" * 50)
    
    # Verificar imports básicos
    try:
        from src.core.poker_engine import PokerEngine
        print(" src.core.poker_engine.PokerEngine")
    except ImportError as e:
        print(f" src.core.poker_engine.PokerEngine: {e}")
        return False
    
    try:
        from src.overlay.overlay_gui import PokerOverlay
        print(" src.overlay.overlay_gui.PokerOverlay")
    except ImportError as e:
        print(f" src.overlay.overlay_gui.PokerOverlay: {e}")
        return False
    
    try:
        from src.platforms.ggpoker_adapter import GGPokerAdapter
        print(" src.platforms.ggpoker_adapter.GGPokerAdapter")
        
        # Verificar firma del constructor
        import inspect
        sig = inspect.signature(GGPokerAdapter.__init__)
        params = list(sig.parameters.keys())
        print(f"   Parámetros constructor: {params[1:] if params else 'ninguno'}")
        
    except ImportError as e:
        print(f" src.platforms.ggpoker_adapter.GGPokerAdapter: {e}")
        return False
    
    try:
        from src.screen_capture.adaptive_recognizer import AdaptiveCardRecognizer
        print(" src.screen_capture.adaptive_recognizer.AdaptiveCardRecognizer")
    except ImportError as e:
        print(f"  src.screen_capture.adaptive_recognizer: {e}")
    
    try:
        from src.integration.coach_integrator import PokerCoachIntegrator
        print(" src.integration.coach_integrator.PokerCoachIntegrator")
    except ImportError as e:
        print(f" src.integration.coach_integrator: {e}")
        return False
    
    print("-" * 50)
    return True

def main():
    """Función principal"""
    print("=" * 60)
    print(" POKER COACH PRO v1.0 - Sistema de Asistencia")
    print("=" * 60)
    
    # Verificar imports primero
    if not check_imports():
        print("\n ERROR: Faltan imports críticos")
        print(" Solución: Verifica que los archivos existan en:")
        print("   - src/core/poker_engine.py")
        print("   - src/overlay/overlay_gui.py")
        print("   - src/platforms/ggpoker_adapter.py")
        return
    
    try:
        # Importar integrador
        from src.integration.coach_integrator import PokerCoachIntegrator
        
        # Crear logs directory si no existe
        os.makedirs("logs", exist_ok=True)
        
        # Inicializar y ejecutar
        print("\n Inicializando sistema...")
        coach = PokerCoachIntegrator()
        
        if coach.initialize():
            logger.info(" Inicialización completada")
            print("\n" + "=" * 60)
            print(" SISTEMA INICIADO CORRECTAMENTE")
            print("   Modo:", "DEMO" if coach.demo_mode else "TIEMPO REAL (GG Poker)")
            print("   Presiona Ctrl+C para detener")
            print("=" * 60 + "\n")
            
            try:
                coach.run()
            except KeyboardInterrupt:
                logger.info("Detenido por usuario")
                print("\n Saliendo de Poker Coach Pro...")
            except Exception as e:
                logger.error(f"Error durante ejecución: {e}")
                print(f"\n Error durante ejecución: {e}")
        else:
            logger.error(" Fallo en inicialización")
            print("\n Error al inicializar el sistema")
            
    except ImportError as e:
        logger.error(f" Error de importación: {e}")
        print(f"\n ERROR DE IMPORTACIÓN: {e}")
        import traceback
        traceback.print_exc()
        
    except Exception as e:
        logger.error(f" Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n ERROR: {e}")

if __name__ == "__main__":
    main()
