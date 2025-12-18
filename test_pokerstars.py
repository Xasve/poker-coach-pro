#!/usr/bin/env python3
"""
Script de prueba para PokerStars
"""
import sys
import os
sys.path.insert(0, 'src')

print(" Probando PokerStars Adapter...")

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    adapter = PokerStarsAdapter()
    print(" PokerStarsAdapter creado")
    
    # Verificar PokerStars
    is_active = adapter.is_pokerstars_active()
    print(f" PokerStars activo: {is_active}")
    
    # Probar captura
    if is_active:
        print("\n Probando captura...")
        state = adapter.capture_and_analyze()
        if state:
            print(f" Estado capturado:")
            print(f"   Cartas: {state.hero_cards}")
            print(f"   Calle: {state.street}")
            print(f"   Pot: {state.pot}")
        else:
            print(" No se pudo capturar estado")
    else:
        print("  Ejecuta este script con PokerStars abierto")
        
except ImportError as e:
    print(f" Error de importación: {e}")
except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()
