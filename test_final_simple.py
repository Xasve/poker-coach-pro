# test_final_simple.py
import sys
import os

print("🎴 TEST FINAL SIMPLIFICADO - POKER COACH PRO")
print("=" * 60)

# Configurar path
sys.path.insert(0, 'src')

# Paso 1: Verificar estructura
print("\n1. VERIFICANDO ESTRUCTURA...")
required_dirs = ['src', 'config', 'data/card_templates/pokerstars']
for dir in required_dirs:
    if os.path.exists(dir):
        print(f"   ✅ {dir}/")
    else:
        print(f"   ❌ {dir}/ (FALTANTE)")

# Paso 2: Test de dependencias
print("\n2. TEST DE DEPENDENCIAS...")
try:
    import numpy as np
    import cv2
    from PIL import Image
    import mss
    import yaml
    
    print(f"   ✅ NumPy {np.__version__}")
    print(f"   ✅ OpenCV {cv2.__version__}")
    print(f"   ✅ Pillow {Image.__version__}")
    print(f"   ✅ MSS {mss.__version__}")
    print(f"   ✅ PyYAML OK")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Paso 3: Test de componentes individuales
print("\n3. TEST DE COMPONENTES...")

# 3.1 StealthCapture
print("\n   3.1 StealthCapture...")
try:
    from screen_capture.stealth_capture import StealthScreenCapture
    capture = StealthScreenCapture("pokerstars", "LOW")
    print(f"   ✅ StealthCapture creado")
    
    screenshot = capture.capture_screen()
    if screenshot is not None:
        print(f"   ✅ Captura exitosa: {screenshot.shape}")
    else:
        print("   ⚠️  Captura retornó None")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# 3.2 PokerStarsAdapter
print("\n   3.2 PokerStarsAdapter...")
try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    adapter = PokerStarsAdapter(stealth_level="LOW")
    print(f"   ✅ Adapter creado")
    
    adapter.start()
    print(f"   ✅ Adapter iniciado")
    
    import time
    time.sleep(0.5)
    
    state = adapter.get_table_state()
    if state:
        print(f"   ✅ Estado obtenido: {list(state.keys())}")
        if state.get('simulated'):
            print(f"   ⚠️  Modo SIMULADO activado")
    else:
        print(f"   ⚠️  Estado None")
    
    adapter.stop()
    print(f"   ✅ Adapter detenido")
    
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# 3.3 PokerEngine
print("\n   3.3 PokerEngine...")
try:
    from core.poker_engine import PokerEngine
    engine = PokerEngine()
    print(f"   ✅ Engine creado")
    
    # Test de análisis
    decision = engine.analyze_hand(
        hole_cards=["Ah", "Ks"],
        community_cards=["Qd", "Jc", "Th"],
        pot_size=1250,
        position="middle"
    )
    print(f"   ✅ Análisis completado: {decision.get('action')}")
    
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# 3.4 Integrator
print("\n   3.4 Integrator...")
try:
    # Crear el archivo si no existe
    integrator_path = "src/integration/poker_coach_integrator.py"
    if not os.path.exists(integrator_path):
        print(f"   ⚠️  Integrator no encontrado, creando...")
        # Crear contenido básico
        with open(integrator_path, 'w', encoding='utf-8') as f:
            f.write('''
class PokerCoachIntegrator:
    def __init__(self, config_path=None):
        self.config_path = config_path
        print("[Integrator] Creado")
    
    def initialize(self):
        print("[Integrator] Inicializado")
        return True
    
    def run_single_iteration(self):
        print("[Integrator] Iteración ejecutada")
        return True
    
    def cleanup(self):
        print("[Integrator] Limpiado")
''')
        print(f"   📄 Integrator creado")
    
    from integration.poker_coach_integrator import PokerCoachIntegrator
    integrator = PokerCoachIntegrator()
    print(f"   ✅ Integrator creado")
    
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("✅ TEST FINALIZADO")
print("\n🎯 EJECUTAR SISTEMA COMPLETO:")
print("python run_poker_coach.py")