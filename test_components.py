#!/usr/bin/env python3
"""
Prueba rápida de componentes individuales
"""
import sys
import os
sys.path.insert(0, 'src')

def test_poker_engine():
    print(" Probando PokerEngine...")
    try:
        from core.poker_engine import PokerEngine
        engine = PokerEngine()
        print(f" PokerEngine creado: agresión={getattr(engine, 'aggression', 'N/A')}")
        
        # Probar decisión demo
        demo_state = {
            "hero_cards": ["Ah", "Kd"],
            "community_cards": ["Js", "8c", "2h"],
            "street": "preflop",
            "position": "BTN",
            "pot": 500,
            "stack": 2500,
            "to_call": 100,
            "actions_available": ["FOLD", "CALL", "RAISE"]
        }
        
        decision = engine.make_decision(demo_state)
        print(f" Decisión tomada: {decision.get('action', 'N/A')}")
        print(f"   Confianza: {decision.get('confidence', 'N/A')}")
        print(f"   Razón: {decision.get('reason', 'N/A')}")
        
        return True
    except Exception as e:
        print(f" Error en PokerEngine: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_overlay():
    print("\n Probando Overlay...")
    try:
        from overlay.overlay_gui import PokerOverlay
        overlay = PokerOverlay()
        print(" Overlay creado")
        
        # Iniciar en hilo separado
        import threading
        overlay_thread = threading.Thread(target=overlay.start, daemon=True)
        overlay_thread.start()
        
        # Probar actualización
        overlay.update_recommendation(
            action="RAISE",
            confidence=0.85,
            reason="Top pair + flush draw",
            alternatives=["CALL", "FOLD"]
        )
        
        print(" Overlay actualizado")
        
        # Esperar un momento y cerrar
        import time
        time.sleep(2)
        overlay.stop()
        
        return True
    except Exception as e:
        print(f" Error en Overlay: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ggpoker_adapter():
    print("\n Probando GGPokerAdapter...")
    try:
        from platforms.ggpoker_adapter import GGPokerAdapter
        
        # Probar diferentes firmas de constructor
        try:
            adapter = GGPokerAdapter()
            print(" GGPokerAdapter creado (sin parámetros)")
        except TypeError:
            try:
                adapter = GGPokerAdapter(poker_engine=None, overlay=None)
                print(" GGPokerAdapter creado (con parámetros None)")
            except Exception as e:
                print(f" Error creando adapter: {e}")
                return False
        
        # Verificar métodos disponibles
        methods = [m for m in dir(adapter) if not m.startswith('_')]
        print(f" Métodos disponibles: {', '.join(methods[:10])}...")
        
        # Verificar si tiene método de detección
        if hasattr(adapter, 'is_ggpoker_active'):
            is_active = adapter.is_ggpoker_active()
            print(f" GG Poker activo: {is_active}")
        else:
            print("  No tiene método is_ggpoker_active")
        
        return True
    except Exception as e:
        print(f" Error en GGPokerAdapter: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print(" PRUEBA DE COMPONENTES POKER COACH PRO")
    print("=" * 60)
    
    results = []
    results.append(test_poker_engine())
    results.append(test_overlay())
    results.append(test_ggpoker_adapter())
    
    print("\n" + "=" * 60)
    print(" RESUMEN DE PRUEBAS:")
    for i, (test_name, result) in enumerate(zip(
        ["PokerEngine", "Overlay", "GGPokerAdapter"], results
    )):
        status = "" if result else ""
        print(f"  {status} {test_name}")
    
    if all(results):
        print("\n Todos los componentes funcionan correctamente!")
        print(" Ejecuta: python start_coach_pro.py")
    else:
        print("\n  Algunos componentes tienen problemas")
        print(" Revisa los errores arriba")

if __name__ == "__main__":
    main()
