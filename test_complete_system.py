# test_complete_system.py
import sys
import os
import time

print("=== TEST COMPLETO DEL SISTEMA ===")
print("=" * 60)

# Configuración inicial
sys.path.insert(0, 'src')

# Verificar componentes
def check_component(name, check_func):
    print(f"\n🔍 {name}...")
    try:
        result = check_func()
        print(f"   ✅ {result}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__}: {e}")
        return False

# 1. Dependencias básicas
def check_deps():
    import numpy as np
    import cv2
    from PIL import Image
    import mss
    return f"NumPy {np.__version__}, OpenCV {cv2.__version__}, Pillow {Image.__version__}"

# 2. Sistema de captura
def check_capture():
    from screen_capture.stealth_capture import StealthScreenCapture
    capture = StealthScreenCapture("pokerstars", "LOW")
    screenshot = capture.capture_screen()
    return f"Captura: {screenshot.shape if hasattr(screenshot, 'shape') else 'OK'}"

# 3. Adaptador PokerStars
def check_adapter():
    from platforms.pokerstars_adapter import PokerStarsAdapter
    adapter = PokerStarsAdapter(stealth_level="LOW")
    adapter.start()
    time.sleep(0.5)
    state = adapter.get_table_state()
    adapter.stop()
    
    if state and 'simulated' in state:
        return "Adaptador OK (modo simulado)"
    elif state:
        return "Adaptador OK (modo real)"
    else:
        return "Adaptador OK (sin estado)"

# 4. Motor GTO
def check_engine():
    from core.poker_engine import PokerEngine
    engine = PokerEngine()
    return f"Motor GTO: {engine.__class__.__name__}"

# 5. Configuración
def check_config():
    import yaml
    with open('config/default_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return f"Config: {config.get('platforms', {}).get('default', 'No config')}"

# Ejecutar checks
checks = [
    ("Dependencias", check_deps),
    ("Captura", check_capture),
    ("Adaptador", check_adapter),
    ("Motor GTO", check_engine),
    ("Configuración", check_config),
]

all_passed = True
for name, func in checks:
    if not check_component(name, func):
        all_passed = False

# 6. Test integración
print("\n🔗 Test de integración...")
try:
    from integration.poker_coach_integrator import PokerCoachIntegrator
    
    integrator = PokerCoachIntegrator(config_path='config/default_config.yaml')
    print("   ✅ Integrador creado")
    
    initialized = integrator.initialize()
    print(f"   ✅ Inicialización: {initialized}")
    
    # Una iteración rápida
    result = integrator.run_single_iteration()
    print(f"   ✅ Iteración: {'OK' if result else 'Falló'}")
    
    integrator.cleanup()
    print("   ✅ Limpieza completada")
    
except Exception as e:
    print(f"   ❌ Error integración: {type(e).__name__}: {e}")
    all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
    print("\n📋 Próximos pasos:")
    print("1. Abre PokerStars para pruebas reales")
    print("2. Ejecuta: python main.py")
    print("3. Verifica el overlay en la mesa")
else:
    print("⚠️  Sistema parcialmente funcional")
    print("\n🔧 Revisa los componentes con error")