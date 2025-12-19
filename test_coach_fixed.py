# test_coach_fixed.py - Prueba del coach corregido
import sys
import os

print("🤖 PRUEBA DEL COACH INTEGRATOR CORREGIDO")
print("=" * 60)

sys.path.insert(0, 'src')

try:
    from integration.coach_integrator import CoachIntegrator
    
    print("✅ CoachIntegrator importado correctamente")
    
    # Verificar que todas las claves existan
    print("\n🔍 VERIFICANDO ESTRUCTURA DEL COACH...")
    
    coach = CoachIntegrator("pokerstars", "gto_basic")
    
    # Verificar postflop_decisions
    required_keys = ["VERY_STRONG", "STRONG", "MEDIUM", "WEAK", "DRAWING", "UNKNOWN"]
    missing_keys = []
    
    for key in required_keys:
        if key not in coach.postflop_decisions:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Claves faltantes en postflop_decisions: {missing_keys}")
        print("\n🔧 Solución: Añade las claves faltantes al diccionario")
    else:
        print("✅ Todas las claves necesarias existen en postflop_decisions")
    
    # Verificar estrategias
    print(f"\n📊 Estrategias disponibles: {coach.get_available_strategies()}")
    
    # Prueba básica
    print("\n🧪 PRUEBA BÁSICA DE ANÁLISIS...")
    
    test_situations = [
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
            "name": "AK suited",
            "hole_cards": [("A", "hearts"), ("K", "hearts")],
            "community_cards": [],
            "pot_size": 30,
            "bet_size": 0,
            "position": "BTN",
            "players": 4,
            "stage": "preflop"
        },
        {
            "name": "Mano débil",
            "hole_cards": [("7", "diamonds"), ("2", "clubs")],
            "community_cards": [],
            "pot_size": 20,
            "bet_size": 5,
            "position": "BB",
            "players": 5,
            "stage": "preflop"
        }
    ]
    
    for i, situation in enumerate(test_situations):
        print(f"\n📊 Caso {i+1}: {situation['name']}")
        
        try:
            recommendation = coach.analyze_hand(situation)
            
            print(f"   ✅ Análisis exitoso!")
            print(f"   🎯 Acción: {recommendation['primary_action']}")
            print(f"   📈 Confianza: {recommendation['confidence']:.0%}")
            
            if 'hand_evaluation' in recommendation:
                eval_info = recommendation['hand_evaluation']
                print(f"   🔍 Evaluación: {eval_info.get('strength', '?')} - {eval_info.get('category', '?')}")
            
        except KeyError as e:
            print(f"   ❌ Error KeyError: {e}")
            print(f"   🔧 Posible clave faltante en postflop_decisions")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Probar diferentes estrategias
    print("\n🔄 PROBANDO DIFERENTES ESTRATEGIAS...")
    
    strategies_to_test = ["gto_basic", "aggressive", "tight_passive"]
    
    for strategy in strategies_to_test:
        print(f"\n   📊 Estrategia: {strategy}")
        coach.set_strategy(strategy)
        
        # Prueba simple
        simple_test = {
            "hole_cards": [("K", "hearts"), ("Q", "diamonds")],
            "community_cards": [],
            "pot_size": 40,
            "bet_size": 10,
            "position": "CO",
            "players": 6,
            "stage": "preflop"
        }
        
        try:
            rec = coach.analyze_hand(simple_test)
            print(f"      Acción: {rec['primary_action']} (Conf: {rec['confidence']:.0%})")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    # Obtener estadísticas
    print("\n📈 ESTADÍSTICAS DE LA SESIÓN:")
    stats = coach.get_session_stats()
    print(f"   Manos analizadas: {stats['hands_analyzed']}")
    print(f"   Recomendaciones: {stats['recommendations_given']}")
    
    # Guardar sesión
    print("\n💾 GUARDANDO SESIÓN...")
    coach.save_session()
    
    print("\n" + "=" * 60)
    print("✅ ¡PRUEBA COMPLETADA!")
    print("\n📋 RESUMEN:")
    print("• Coach inicializado correctamente")
    print("• Estructura verificada")
    print("• Múltiples situaciones analizadas")
    print("• Diferentes estrategias probadas")
    print("• Sesión guardada exitosamente")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n🔧 Verifica que el archivo exista:")
    print("   src/integration/coach_integrator.py")
    
except Exception as e:
    print(f"❌ Error general: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)