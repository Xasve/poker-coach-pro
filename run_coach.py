#!/usr/bin/env python3
"""
Poker Coach Pro - Versión estable y funcional
"""
import os
import sys
import time
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def print_header():
    """Imprimir encabezado del programa"""
    print("\n" + "=" * 60)
    print(" POKER COACH PRO - ASISTENTE INTELIGENTE")
    print("=" * 60)
    print(" Versión: 1.0 - Modo Demo")
    print(" Motor: PokerEngine GTO")
    print(" Objetivo: Mejorar tu juego en tiempo real")
    print("=" * 60)

def check_environment():
    """Verificar entorno"""
    print("\n Verificando entorno...")
    
    required_files = [
        "src/core/poker_engine.py",
        "src/integration/improved_integrator.py"
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f" {file}")
        else:
            print(f" {file} - NO ENCONTRADO")
            all_ok = False
    
    # Verificar imports
    try:
        from src.core.poker_engine import PokerEngine
        print(" PokerEngine - IMPORT OK")
    except ImportError as e:
        print(f" Error importando PokerEngine: {e}")
        all_ok = False
    
    return all_ok

def main():
    """Función principal"""
    print_header()
    
    if not check_environment():
        print("\n ERROR: Problemas en el entorno")
        print(" Solución: Ejecuta 'python fix_all_problems.py' primero")
        return
    
    print("\n Iniciando sistema...")
    
    try:
        # Importar el coach mejorado
        from src.integration.improved_integrator import ImprovedPokerCoach
        
        # Crear y ejecutar coach
        coach = ImprovedPokerCoach()
        
        print("\n" + "=" * 60)
        print(" MODO DEMO ACTIVADO")
        print("=" * 60)
        print("\nEl sistema generará manos de poker aleatorias y")
        print("te dará recomendaciones basadas en estrategia GTO.")
        print("\nPresiona Ctrl+C en cualquier momento para salir.")
        print("=" * 60)
        
        time.sleep(2)  # Pausa para leer
        
        if coach.start():
            print("\n" + "=" * 60)
            print(" SESIÓN TERMINADA")
            print("=" * 60)
            print(f" Manos jugadas: {coach.hand_number - 1}")
            print(" Gracias por usar Poker Coach Pro!")
        else:
            print("\n Error al iniciar el sistema")
            
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido por el usuario")
    except ImportError as e:
        print(f"\n Error de importación: {e}")
        print("\n Intenta ejecutar:")
        print("   python fix_all_problems.py")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
