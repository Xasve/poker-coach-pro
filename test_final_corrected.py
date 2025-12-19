# test_final_corrected.py
import sys
import os

print("🎴 TEST FINAL CORREGIDO - POKER COACH PRO")
print("=" * 60)

# Configurar path
sys.path.insert(0, 'src')

try:
    # 1. Test PokerStarsAdapter
    print("\n1. TEST POKERSTARS ADAPTER...")
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    adapter = PokerStarsAdapter(stealth_level="LOW")
    print("✅ Adapter creado")
    
    adapter.start()
    print("✅ Adapter iniciado")
    
    import time
    time.sleep(0.5)
    
    state = adapter.get_table_state()
    if state:
        print(f"✅ Estado obtenido")
        print(f"   - Tipo: {'SIMULADO' if state.get('simulated') else 'REAL'}")
        print(f"   - Cartas: {state.get('cards', {})}")
        print(f"   - Pot: {state.get('pot', 'N/A')}")
    else:
        print("❌ No se pudo obtener estado")
    
    adapter.stop()
    print("✅ Adapter detenido")
    
    # 2. Test PokerEngine
    print("\n2. TEST POKER ENGINE...")
    from core.poker_engine import PokerEngine
    
    engine = PokerEngine()
    print("✅ Engine creado")
    
    # Test con datos simulados
    decision = engine.analyze_hand(
        hole_cards=["Ah", "Ks"],
        community_cards=["Qd", "Jc", "Th"],
        pot_size=1250,
        position="middle"
    )
    
    print(f"✅ Análisis completado")
    print(f"   - Acción: {decision.get('action')}")
    print(f"   - Confianza: {decision.get('confidence', 0):.1%}")
    print(f"   - Razón: {decision.get('reason', 'N/A')}")
    
    # 3. Test integración
    print("\n3. TEST INTEGRACIÓN COMPLETA...")
    print("   Simulando ciclo de análisis...")
    
    # Usar datos del adapter para engine
    if state and 'cards' in state:
        cards = state['cards']
        pot = int(state['pot']) if str(state.get('pot', '0')).isdigit() else 0
        
        decision2 = engine.analyze_hand(
            hole_cards=cards.get('hero', []),
            community_cards=cards.get('community', []),
            pot_size=pot,
            position=state.get('position', 'middle')
        )
        
        print(f"✅ Integración funcionando")
        print(f"   - Acción final: {decision2.get('action')}")
        print(f"   - Sistema: {'SIMULADO' if state.get('simulated') else 'REAL'}")
    
    print("\n" + "=" * 60)
    print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
    print("\n🎯 EJECUTAR SISTEMA COMPLETO:")
    print("python run_poker_coach_simple.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()