import sys
import os

print(" POKER COACH PRO - SISTEMA PRINCIPAL")
print("=" * 60)

sys.path.insert(0, 'src')

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    from core.poker_engine import PokerEngine
    
    print("✅ Sistema listo")
    adapter = PokerStarsAdapter(stealth_level="LOW")
    engine = PokerEngine()
    
    print("\n Iniciando... Presiona Ctrl+C para detener")
    print("=" * 60)
    
    adapter.start()
    import time
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n Iteración {iteration}")
        
        state = adapter.get_table_state()
        if state:
            print(f"   📊 Mesa: {state.get('simulated', 'REAL')}")
            print(f"    Cartas: {state.get('cards', {})}")
            print(f"    Pozo: {state.get('pot', '0')}")
        
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n  Detenido")
    adapter.stop()
    
except Exception as e:
    print(f" Error: {e}")

print("\n Fin del programa")
