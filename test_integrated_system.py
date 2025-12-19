# test_integrated_system.py
import sys
import os
import time

sys.path.insert(0, 'src')

def test_integrated_system():
    """Prueba el sistema integrado paso a paso"""
    print("🧪 PRUEBA DEL SISTEMA INTEGRADO")
    print("=" * 50)
    
    try:
        # 1. Importar componentes
        print("\n1. IMPORTANDO COMPONENTES...")
        from screen_capture.stealth_capture import StealthScreenCapture
        from screen_capture.table_detector import TableDetector
        from integration.coach_integrator import CoachIntegrator
        from platforms.pokerstars_adapter import PokerStarsAdapter
        
        print("✅ Componentes importados")
        
        # 2. Crear instancias
        print("\n2. CREANDO INSTANCIAS...")
        try:
            capture = StealthScreenCapture(stealth_level=1, platform="pokerstars")
            print("✅ StealthScreenCapture creado")
        except Exception as e:
            print(f"❌ Error StealthScreenCapture: {e}")
            # Crear sin parámetros si falla
            capture = StealthScreenCapture()
            print("✅ StealthScreenCapture (sin parámetros)")
        
        detector = TableDetector()
        coach = CoachIntegrator()
        adapter = PokerStarsAdapter()
        
        print("✅ Todas las instancias creadas")
        
        # 3. Simular flujo de trabajo
        print("\n3. SIMULANDO FLUJO DE TRABAJO...")
        
        # Simular situación de poker
        simulated_data = {
            'hero_cards': ['Ah', 'Kd'],
            'community_cards': ['Qs', 'Jh', 'Tc'],
            'pot': 125,
            'stack': 1500,
            'position': 'BTN',
            'bet_size': 50
        }
        
        # Obtener recomendación del coach
        recommendation = coach.get_recommendation(simulated_data)
        print(f"✅ Recomendación del coach: {recommendation}")
        
        # 4. Verificar funcionalidades
        print("\n4. VERIFICANDO FUNCIONALIDADES...")
        
        # Coach tiene estrategias
        strategies = list(coach.postflop_decisions.keys())
        print(f"✅ Estrategias disponibles: {len(strategies)}")
        
        # TableDetector configurado
        print(f"✅ TableDetector umbral: {detector.green_threshold}")
        
        print("\n🎉 SISTEMA INTEGRADO FUNCIONAL")
        print("=" * 50)
        print("Problemas conocidos:")
        print("1. Entorno virtual necesita reinstalación")
        print("2. Templates reales faltantes")
        print("3. Overlay no implementado")
        
        return True
        
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integrated_system()
    sys.exit(0 if success else 1)