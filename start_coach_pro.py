#!/usr/bin/env python3
"""
Script principal unificado para Poker Coach Pro
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
    print(" Verificando imports...")
    
    modules_to_check = [
        ("src.core.poker_engine", "PokerEngine"),
        ("src.overlay.overlay_gui", "PokerOverlay"),
        ("src.platforms.ggpoker_adapter", "GGPokerAdapter"),
        ("src.integration.coach_integrator", "PokerCoachIntegrator"),
    ]
    
    for module_name, class_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[class_name])
            print(f" {module_name}.{class_name}")
        except ImportError as e:
            print(f" {module_name}.{class_name}: {e}")
            
            # Intentar importación alternativa
            try:
                # Intentar importar sin src.
                alt_module_name = module_name.replace("src.", "")
                module = __import__(alt_module_name, fromlist=[class_name])
                print(f"    Usando alternativa: {alt_module_name}.{class_name}")
            except:
                pass
    
    print()

def main():
    """Función principal"""
    print("=" * 60)
    print(" POKER COACH PRO v1.0 - Sistema de Asistencia")
    print("=" * 60)
    
    # Verificar imports primero
    check_imports()
    
    try:
        # Importar integrador
        from src.integration.coach_integrator import PokerCoachIntegrator
        
        # Crear logs directory si no existe
        os.makedirs("logs", exist_ok=True)
        
        # Inicializar y ejecutar
        print(" Inicializando sistema...")
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
        else:
            logger.error(" Fallo en inicialización")
            print(" Error al inicializar el sistema")
            
    except ImportError as e:
        logger.error(f" Error de importación: {e}")
        print(f"\n ERROR DE IMPORTACIÓN: {e}")
        print("\n SOLUCIONES POSIBLES:")
        print("1. Verifica que los archivos estén en:")
        print("   - src/core/poker_engine.py")
        print("   - src/overlay/overlay_gui.py")
        print("   - src/platforms/ggpoker_adapter.py")
        print("\n2. Verifica los imports en ggpoker_adapter.py:")
        print("   DEBE decir: from core.poker_engine import PokerEngine")
        print("   DEBE decir: from overlay.overlay_gui import PokerOverlay")
        
    except Exception as e:
        logger.error(f" Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n ERROR: {e}")

if __name__ == "__main__":
    main()
