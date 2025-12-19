# run_minimal.py - Sistema mínimo funcional
import time
import sys
import os

print("🚀 POKER COACH PRO - VERSIÓN MÍNIMA")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

try:
    # Importar componentes mínimos
    from platforms.pokerstars_adapter_minimal import PokerStarsAdapter
    from integration.coach_integrator_minimal import CoachIntegrator
    
    print("✅ Componentes mínimos cargados")
    
    # Inicializar
    adapter = PokerStarsAdapter(stealth_level=1)
    coach = CoachIntegrator("pokerstars")
    
    print("\n🎯 SISTEMA INICIALIZADO CORRECTAMENTE")
    print("\n📡 MODO DE PRUEBA ACTIVADO")
    print("-" * 50)
    
    # Simular partida
    for i in range(5):
        print(f"\n🔄 Mano #{i+1}")
        
        # Simular captura
        screenshot = adapter.capture_table()
        
        # Detectar mesa
        table_detected = adapter.detect_table(screenshot)
        
        if table_detected:
            # Obtener cartas
            hole_cards = adapter.recognize_hole_cards(screenshot)
            print(f"   👤 Tus cartas: {hole_cards}")
            
            # Analizar
            situation = {
                "hole_cards": hole_cards,
                "community_cards": [],
                "pot_size": 100,
                "bet_size": 20,
                "position": "BTN",
                "players": 6,
                "stage": "preflop"
            }
            
            recommendation = coach.analyze_hand(situation)
            print(f"   💡 Recomendación: {recommendation['primary_action']}")
            print(f"   📈 Confianza: {recommendation['confidence']:.0%}")
            print(f"   🧠 Razón: {recommendation['reasoning']}")
        
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("\n🎯 El sistema base funciona correctamente")
    print("\n🔧 Para la versión completa, instala:")
    print("   pip install numpy opencv-python mss")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
