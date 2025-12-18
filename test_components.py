#!/usr/bin/env python3
"""
Prueba rápida de componentes individuales CON WRAPPERS
"""
import sys
import os
sys.path.insert(0, 'src')

def test_poker_engine():
    print(" Probando PokerEngine...")
    try:
        from core.poker_engine import PokerEngine
        engine = PokerEngine()
        print(f" PokerEngine creado")
        
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
        
        # Probar wrapper
        from integration.compatibility_wrappers import PokerEngineWrapper
        wrapper = PokerEngineWrapper(engine)
        wrapped_decision = wrapper.make_decision(demo_state)
        print(f" Wrapper funcionando: {wrapped_decision.get('action', 'N/A')}")
        
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
        
        # Probar wrapper
        from integration.compatibility_wrappers import OverlayWrapper
        wrapper = OverlayWrapper(overlay)
        print(f" Wrapper creado - tipo detectado: {wrapper.method_type}")
        
        # Iniciar en hilo separado
        import threading
        overlay_thread = threading.Thread(target=overlay.start, daemon=True)
        overlay_thread.start()
        
        # Probar actualización con wrapper
        wrapper.update_recommendation(
            action="RAISE",
            confidence=0.85,
            reason="Top pair + flush draw",
            alternatives=["CALL", "FOLD"]
        )
        
        print(" Overlay actualizado via wrapper")
        
        # Probar diferentes tipos de actualización
        wrapper.update_recommendation(
            action="CALL",
            confidence=0.65,
            reason="Pot odds favorables",
            alternatives=["RAISE", "FOLD"]
        )
        
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
        
        # Crear adapter
        adapter = GGPokerAdapter()
        print(" GGPokerAdapter creado")
        
        # Probar wrapper
        from integration.compatibility_wrappers import GGAdapterWrapper
        wrapper = GGAdapterWrapper(adapter)
        print(" Wrapper creado")
        
        # Verificar si GG Poker está activo
        is_active = wrapper.is_ggpoker_active()
        print(f" GG Poker activo (wrapper): {is_active}")
        
        # Verificar métodos
        print(f" Métodos wrapper: is_ggpoker_active, capture_and_analyze")
        
        return True
    except Exception as e:
        print(f" Error en GGPokerAdapter: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integrator():
    print("\n Probando Integrador...")
    try:
        from integration.coach_integrator import PokerCoachIntegrator
        
        integrator = PokerCoachIntegrator()
        print(" Integrador creado")
        
        # Inicializar (pero no ejecutar bucle completo)
        initialized = integrator.initialize()
        print(f" Inicialización: {initialized}")
        print(f"   Modo demo: {integrator.demo_mode}")
        print(f"   Wrappers creados: {bool(integrator.overlay_wrapper)}")
        
        # Limpiar
        integrator.shutdown()
        
        return initialized
    except Exception as e:
        print(f" Error en Integrador: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print(" PRUEBA DE COMPONENTES CON WRAPPERS")
    print("=" * 60)
    
    results = []
    results.append(test_poker_engine())
    results.append(test_overlay())
    results.append(test_ggpoker_adapter())
    results.append(test_integrator())
    
    print("\n" + "=" * 60)
    print(" RESUMEN DE PRUEBAS:")
    tests = ["PokerEngine", "Overlay", "GGPokerAdapter", "Integrador"]
    for i, (test_name, result) in enumerate(zip(tests, results)):
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
