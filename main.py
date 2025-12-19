import sys,os,time
sys.path.insert(0,"src")
from platforms.pokerstars_adapter import PokerStarsAdapter
from core.poker_engine import PokerEngine
a=PokerStarsAdapter("LOW")
e=PokerEngine()
a.start()
print(" Sistema iniciado. Ctrl+C para detener")
try:
    while 1:
        s=a.get_table_state()
        if s:
            modo="REAL" if not s.get("simulated") else "SIMULADA"
            print(f"\n Mesa: {modo}")
            print(f" Cartas: {s.get('cards',{})}")
            print(f" Pozo: {s.get('pot',0)}")
            if s.get("cards"):
                pot=s.get("pot","0")
                pot_int=int(pot) if isinstance(pot,str) and pot.isdigit() else 0
                d=e.analyze_hand(s["cards"].get("hero",[]),s["cards"].get("community",[]),pot_int,"middle")
                print(f" Recomendación: {d.get('action')} ({d.get('confidence',0)*100:.0f}%)")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n Deteniendo...")
except Exception as ex:
    print(f"\n Error: {ex}")
finally:
    a.stop()
    print(" Sistema detenido")
