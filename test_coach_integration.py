# test_coach_integration.py - Verificar integración del coach
import sys
import os

print("🤖 VERIFICANDO INTEGRACIÓN DEL COACH")
print("=" * 60)

sys.path.insert(0, 'src')

# Test 1: Verificar que CoachIntegrator existe
print("\n1. Verificando importación de CoachIntegrator...")
try:
    from integration.coach_integrator import CoachIntegrator
    print("✅ CoachIntegrator importado correctamente")
    
    # Test 2: Crear instancia
    print("\n2. Creando instancia del coach...")
    coach = CoachIntegrator("pokerstars")
    print(f"✅ Coach creado: {coach}")
    print(f"   Plataforma: {coach.platform}")
    print(f"   Estrategia: {coach.strategy}")
    
    # Test 3: Probar análisis de situación
    print("\n3. Probando análisis de situación...")
    test_situations = [
        {
            "name": "Pocket Aces preflop",
            "hole_cards": [("A", "hearts"), ("A", "spades")],
            "community_cards": [],
            "pot_size": 100,
            "position": "BTN",
            "stage": "preflop"
        },
        {
            "name": "Dibujo de color flop",
            "hole_cards": [("K", "hearts"), ("Q", "hearts")],
            "community_cards": [("10", "hearts"), ("J", "clubs"), ("2", "diamonds")],
            "pot_size": 200,
            "position": "CO",
            "stage": "flop"
        },
        {
            "name": "Mano débil",
            "hole_cards": [("7", "diamonds"), ("2", "clubs")],
            "community_cards": [("K", "hearts"), ("Q", "spades"), ("J", "diamonds")],
            "pot_size": 150,
            "position": "UTG",
            "stage": "flop"
        }
    ]
    
    for situation in test_situations:
        print(f"\n   📊 Situación: {situation['name']}")
        recommendation = coach.analyze_hand(situation)
        
        print(f"   🎯 Recomendación: {recommendation['action']}")
        print(f"   📈 Confianza: {recommendation['confidence']:.0%}")
        print(f"   🧠 Razón: {recommendation['reasoning']}")
    
    # Test 4: Verificar estrategias disponibles
    print("\n4. Verificando estrategias disponibles...")
    strategies = coach.get_available_strategies()
    print(f"   Estrategias: {', '.join(strategies)}")
    
    # Test 5: Cambiar estrategia
    print("\n5. Probando cambio de estrategia...")
    for strategy in strategies:
        coach.set_strategy(strategy)
        print(f"   Estrategia actual: {coach.strategy}")
    
    print("\n" + "=" * 60)
    print("🎉 ¡TODAS LAS PRUEBAS DEL COACH PASARON!")
    print("\n🚀 El sistema está listo para usar.")
    print("📝 Ejecuta: python run_pokerstars_optimized.py")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n🔧 Verifica que el archivo existe:")
    print("   src/integration/coach_integrator.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)