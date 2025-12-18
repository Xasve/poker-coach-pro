#!/usr/bin/env python3
"""
Script de prueba mejorado para PokerStars
"""
import sys
import os
sys.path.insert(0, 'src')

print(" PROBANDO POKERSTARS ADAPTER")
print("=" * 50)

# Primero probar importaciones básicas
print("\n Probando imports...")
try:
    from core.poker_engine import PokerEngine
    print(" PokerEngine importado")
    
    engine = PokerEngine()
    print(" PokerEngine instanciado")
    
except ImportError as e:
    print(f" Error importando PokerEngine: {e}")

# Probar adaptador simple
print("\n Probando adaptador simple...")
try:
    from platforms.simple_pokerstars_adapter import SimplePokerStarsAdapter
    
    adapter = SimplePokerStarsAdapter()
    print(" SimplePokerStarsAdapter creado")
    
    # Verificar si PokerStars está activo
    is_active = adapter.is_pokerstars_active()
    print(f" PokerStars activo: {is_active}")
    
    # Probar captura
    print("\n Probando captura simulada...")
    state = adapter.capture_and_analyze()
    
    if state:
        print(f" Estado simulado capturado:")
        print(f"   Cartas: {state['hero_cards']}")
        print(f"   Calle: {state['street']}")
        print(f"   Posición: {state['position']}")
        print(f"   Pot: ")
        print(f"   Para igualar: ")
        
        # Probar decisión del motor
        print("\n Probando decisión del motor...")
        decision = engine.make_decision(state)
        print(f" Decisión tomada:")
        print(f"   Acción: {decision.get('action', 'N/A')}")
        print(f"   Confianza: {decision.get('confidence', 0)*100:.0f}%")
        print(f"   Razón: {decision.get('reason', 'N/A')}")
    else:
        print(" No se pudo capturar estado")
        
except ImportError as e:
    print(f" Error importando adaptador simple: {e}")

# Intentar con adaptador completo si existe
print("\n Intentando con adaptador completo...")
try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    print(" PokerStarsAdapter importado (archivo existe)")
    
    try:
        adapter = PokerStarsAdapter()
        print(" PokerStarsAdapter instanciado")
        
        is_active = adapter.is_pokerstars_active()
        print(f" PokerStars activo (completo): {is_active}")
        
    except Exception as e:
        print(f"  Error instanciando adaptador completo: {e}")
        
except ImportError as e:
    print(f"  No se pudo importar adaptador completo: {e}")

print("\n" + "=" * 50)
print(" PRUEBA COMPLETADA")
print("=" * 50)
