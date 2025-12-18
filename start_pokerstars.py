#!/usr/bin/env python3
"""
Poker Coach Pro - Script principal para PokerStars
"""
import os
import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    print("=" * 60)
    print(" POKER COACH PRO - POKERSTARS EDITION")
    print("=" * 60)
    
    print("\n Iniciando sistema...")
    
    try:
        # Verificar si PokerStars está disponible
        from platforms.pokerstars_adapter import PokerStarsAdapter
        
        adapter = PokerStarsAdapter()
        
        print("\n Verificando PokerStars...")
        if adapter.is_pokerstars_active():
            print(" PokerStars detectado - Modo tiempo real")
            
            # Importar y ejecutar coach
            from integration.improved_integrator import ImprovedPokerCoach
            coach = ImprovedPokerCoach()
            coach.start()
            
        else:
            print("  PokerStars no detectado")
            print("\n Activando modo demo...")
            
            from integration.improved_integrator import ImprovedPokerCoach
            coach = ImprovedPokerCoach()
            coach.start()
            
    except ImportError as e:
        print(f"\n Error: {e}")
        print("\n Ejecuta el instalador primero: python install_pokerstars.py")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
