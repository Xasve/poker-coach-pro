#!/usr/bin/env python3
"""
Script principal unificado para Poker Coach Pro - VERSIÓN MEJORADA
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

def check_dependencies():
    """Verificar dependencias y estructura"""
    print(" Verificando sistema...")
    
    # Verificar directorios necesarios
    dirs = ["logs", "data/card_templates", "src", "src/integration"]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            print(f"  Creando directorio: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    # Verificar archivos críticos
    critical_files = [
        "src/core/poker_engine.py",
        "src/overlay/overlay_gui.py",
        "src/platforms/ggpoker_adapter.py",
        "src/integration/compatibility_wrappers.py"
    ]
    
    for file in critical_files:
        if os.path.exists(file):
            print(f" {file}")
        else:
            print(f" {file} - NO ENCONTRADO")
            return False
    
    return True

def main():
    """Función principal"""
    print("=" * 60)
    print(" POKER COACH PRO v1.0 - Sistema de Asistencia")
    print("=" * 60)
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n ERROR: Faltan archivos críticos")
        return
    
    try:
        # Importar integrador
        from src.integration.coach_integrator import PokerCoachIntegrator
        
        print("\n Inicializando sistema...")
        coach = PokerCoachIntegrator()
        
        if coach.initialize():
            logger.info(" Inicialización completada")
            print("\n" + "=" * 60)
            print(" SISTEMA INICIADO CORRECTAMENTE")
            print(f"   Modo: {'DEMO' if coach.demo_mode else 'TIEMPO REAL (GG Poker)'}")
            print("   Componentes activos:")
            print(f"     - PokerEngine: {'' if coach.poker_engine else ''}")
            print(f"     - Overlay: {'' if coach.overlay else ''}")
            print(f"     - GGPokerAdapter: {'' if coach.ggpoker_adapter else ''}")
            print("\n   Presiona Ctrl+C para detener")
            print("=" * 60 + "\n")
            
            try:
                coach.run()
            except KeyboardInterrupt:
                logger.info("Detenido por usuario")
                print("\n Saliendo de Poker Coach Pro...")
            except Exception as e:
                logger.error(f"Error durante ejecución: {e}")
                print(f"\n Error durante ejecución: {e}")
                import traceback
                traceback.print_exc()
        else:
            logger.error(" Fallo en inicialización")
            print("\n Error al inicializar el sistema")
            print(" Intenta ejecutar: python test_components.py")
            
    except ImportError as e:
        logger.error(f" Error de importación: {e}")
        print(f"\n ERROR DE IMPORTACIÓN: {e}")
        import traceback
        traceback.print_exc()
        print("\n Solución: Ejecuta primero: python test_components.py")
        
    except Exception as e:
        logger.error(f" Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n ERROR: {e}")

if __name__ == "__main__":
    main()
