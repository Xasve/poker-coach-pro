#!/usr/bin/env python3
"""
Script para verificar la estructura del proyecto
"""
import os
import sys

def check_structure():
    """Verificar estructura de archivos"""
    print(" Verificando estructura de Poker Coach Pro...")
    print("-" * 60)
    
    checks = [
        ("src/", " Directorio src", " Falta directorio src"),
        ("src/core/poker_engine.py", " Motor de poker", " Falta poker_engine.py"),
        ("src/core/__init__.py", " Init core", "  Falta __init__.py en core"),
        ("src/overlay/overlay_gui.py", " Overlay GUI", " Falta overlay_gui.py"),
        ("src/overlay/__init__.py", " Init overlay", "  Falta __init__.py en overlay"),
        ("src/platforms/ggpoker_adapter.py", " Adaptador GG", " Falta ggpoker_adapter.py"),
        ("src/__init__.py", " Init principal", "  Falta __init__.py en src"),
        ("logs/", " Directorio logs", "  Falta directorio logs"),
        ("data/card_templates/", " Templates cartas", "  Falta templates"),
    ]
    
    all_ok = True
    for path, ok_msg, error_msg in checks:
        if os.path.exists(path):
            print(f"{ok_msg:40} {path}")
        else:
            print(f"{error_msg:40} {path}")
            if "" in error_msg:
                all_ok = False
    
    print("-" * 60)
    
    if all_ok:
        print(" Estructura correcta")
        
        # Probar imports
        print("\n Probando imports...")
        try:
            sys.path.insert(0, 'src')
            
            # Test 1: Import básico
            from core.poker_engine import PokerEngine
            print(" Import PokerEngine: OK")
            
            # Test 2: Import overlay
            from overlay.overlay_gui import PokerOverlay
            print(" Import PokerOverlay: OK")
            
            # Test 3: Import adaptador
            from platforms.ggpoker_adapter import GGPokerAdapter
            print(" Import GGPokerAdapter: OK")
            
            print("\n Ejecuta: python start_coach_pro.py")
            
        except ImportError as e:
            print(f"\n Error en imports: {e}")
            print("\n Probable causa: Imports incorrectos en ggpoker_adapter.py")
            print("   Abre el archivo y verifica que diga:")
            print("   from core.poker_engine import PokerEngine")
            print("   from overlay.overlay_gui import PokerOverlay")
    else:
        print(" Problemas en la estructura - Revisa arriba")

if __name__ == "__main__":
    check_structure()
