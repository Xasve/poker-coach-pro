import sys
import os
import time
sys.path.insert(0, "src")
from platforms.pokerstars_adapter import PokerStarsAdapter
from core.poker_engine import PokerEngine

adapter = PokerStarsAdapter("LOW")
engine = PokerEngine()
adapter.start()

print(" Sistema iniciado. Analizando PokerStars...")
print("   Presiona Ctrl+C para detener")

try:
    while True:
        estado = adapter.get_table_state()
        if estado:
            print(f"\n Mesa: {"REAL" if not estado.get("simulated") else "SIMULADA"}")
            print(f" Cartas: {estado.get("cards", {})}")
            print(f" Pozo: {estado.get("pot", 0)}")
            
            if estado.get("cards"):
                decision = engine.analyze_hand(
                    estado["cards"].get("hero", []),
                    estado["cards"].get("community", []),
                    int(estado.get("pot", 0)) if str(estado.get("pot", "0")).isdigit() else 0,
                    "middle"
                )
                print(f" Recomendación: {decision.get("action")} ({decision.get("confidence"):.0%})")
        
        time.sleep(2)
except KeyboardInterrupt:
    print("\n Deteniendo...")
finally:
    adapter.stop()
