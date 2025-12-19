# test_coach_improved.py - Prueba del coach mejorado
import sys
import os

print("🤖 PRUEBA COMPLETA DEL COACH MEJORADO")
print("=" * 60)

sys.path.insert(0, 'src')

try:
    from integration.coach_integrator import CoachIntegrator
    
    # 1. Inicializar coach con diferentes estrategias
    print("\n1. INICIALIZANDO COACH CON DIFERENTES ESTRATEGIAS:")
    
    strategies = ["gto_basic", "aggressive", "balanced", "tight_passive", "loose_aggressive"]
    
    for strategy in strategies:
        print(f"\n   🔄 Probando estrategia: {strategy}")
        coach = CoachIntegrator("pokerstars", strategy)
        
        # Test rápido
        test_situation = {
            "hole_cards": [("A", "hearts"), ("K", "spades")],
            "community_cards": [],
            "pot_size": 100,
            "bet_size": 20,
            "position": "BTN",
            "players": 6,
            "stage": "preflop"
        }
        
        recommendation = coach.analyze_hand(test_situation)
        print(f"      Acción: {recommendation['primary_action']}")
        print(f"      Confianza: {recommendation['confidence']:.0%}")
    
    # 2. Probar situaciones complejas
    print("\n2. SITUACIONES COMPLEJAS DE PRUEBA:")
    
    coach = CoachIntegrator("pokerstars", "balanced")
    
    test_cases = [
        {
            "name": "AA preflop UTG",
            "hole_cards": [("A", "hearts"), ("A", "spades")],
            "community_cards": [],
            "pot_size": 50,
            "bet_size": 10,
            "position": "UTG",
            "players": 6,
            "stage": "preflop"
        },
        {
            "name": "AK suited flop monocolor",
            "hole_cards": [("A", "hearts"), ("K", "hearts")],
            "community_cards": [("Q", "hearts"), ("J", "hearts"), ("2", "diamonds")],
            "pot_size": 200,
            "bet_size": 50,
            "position": "CO",
            "players": 4,
            "stage": "flop"
        },
        {
            "name": "Mano débil river con pot grande",
            "hole_cards": [("7", "diamonds"), ("2", "clubs")],
            "community_cards": [("K", "hearts"), ("Q", "spades"), ("J", "diamonds"), ("10", "clubs"), ("9", "hearts")],
            "pot_size": 500,
            "bet_size": 150,
            "position": "BB",
            "players": 3,
            "stage": "river"
        },
        {
            "name": "Drawing hand turn",
            "hole_cards": [("8", "hearts"), ("9", "hearts")],
            "community_cards": [("6", "hearts"), ("7", "clubs"), ("2", "diamonds"), ("K", "spades")],
            "pot_size": 180,
            "bet_size": 40,
            "position": "BTN",
            "players": 2,
            "stage": "turn"
        },
        {
            "name": "Mano marginal flop",
            "hole_cards": [("J", "diamonds"), ("10", "clubs")],
            "community_cards": [("9", "hearts"), ("8", "spades"), ("2", "diamonds")],
            "pot_size": 120,
            "bet_size": 30,
            "position": "MP",
            "players": 5,
            "stage": "flop"
        }
    ]
    
    for i, situation in enumerate(test_cases):
        print(f"\n   📊 Caso {i+1}: {situation['name']}")
        recommendation = coach.analyze_hand(situation)
        
        print(f"      🎯 Acción: {recommendation['primary_action']}")
        print(f"      📈 Confianza: {recommendation['confidence']:.0%}")
        print(f"      💰 Apuesta: ${recommendation['bet_amount']:.2f}")
        print(f"      🧠 Razón: {recommendation['reasoning'][:70]}...")
        
        if recommendation['alternatives']:
            print(f"      🔄 Alternativas:")
            for alt in recommendation['alternatives']:
                print(f"         • {alt['action']} ({alt['confidence']:.0%}): {alt['reason']}")
    
    # 3. Obtener estadísticas
    print("\n3. ESTADÍSTICAS DEL COACH:")
    stats = coach.get_session_stats()
    print(f"   Manos analizadas: {stats['hands_analyzed']}")
    print(f"   Recomendaciones: {stats['recommendations_given']}")
    print(f"   Distribución acciones: {stats['actions_taken']}")
    
    # 4. Historial de manos
    print("\n4. HISTORIAL RECIENTE:")
    history = coach.get_hand_history(3)
    for i, hand in enumerate(history):
        print(f"   Mano {i+1}: {hand['hole_cards']} - {hand['recommendation']['primary_action']}")
    
    # 5. Guardar sesión
    print("\n5. GUARDANDO SESIÓN DE PRUEBA...")
    coach.save_session("logs/coach_test_session.json")
    
    print("\n" + "=" * 60)
    print("✅ ¡PRUEBA DEL COACH COMPLETADA EXITOSAMENTE!")
    print("\n📋 RESUMEN:")
    print("• Coach mejorado inicializado correctamente")
    print("• 5 estrategias diferentes probadas")
    print("• 5 situaciones complejas analizadas")
    print("• Estadísticas y historial funcionando")
    print("• Sesión guardada en logs/coach_test_session.json")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n🔧 Verifica que el archivo exista:")
    print("   src/integration/coach_integrator.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)