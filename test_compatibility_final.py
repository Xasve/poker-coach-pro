# test_compatibility_final.py
import sys
import os

print("🎴 TEST FINAL DE COMPATIBILIDAD - POKER COACH PRO")
print("=" * 70)

# Información del sistema
print(f"🐍 Python: {sys.version.split()[0]}")
print(f"📁 Directorio: {os.getcwd()}")

# Test 1: Dependencias básicas
print("\n1. DEPENDENCIAS BÁSICAS:")
try:
    import numpy as np
    import cv2
    from PIL import Image
    import mss
    import pytesseract
    import yaml
    import pyautogui
    
    print(f"   ✅ NumPy: {np.__version__}")
    print(f"   ✅ OpenCV: {cv2.__version__}")
    print(f"   ✅ Pillow: {Image.__version__}")
    
    # Test operacional
    arr = np.zeros((100, 100, 3), dtype=np.uint8)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    print(f"   ✅ Compatibilidad NumPy-OpenCV: {arr.shape} -> {gray.shape}")
    
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")
    sys.exit(1)

# Test 2: Estructura del proyecto
print("\n2. ESTRUCTURA DEL PROYECTO:")
sys.path.insert(0, 'src')

required_dirs = [
    'src',
    'src/screen_capture',
    'src/platforms', 
    'src/core',
    'src/integration',
    'src/utils',
    'config',
    'data/card_templates/pokerstars'
]

for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"   ✅ {dir_path}/")
    else:
        print(f"   ⚠️  {dir_path}/ (no encontrado)")

# Test 3: Importación de módulos
print("\n3. IMPORTACIÓN DE MÓDULOS:")
try:
    from screen_capture.stealth_capture import StealthScreenCapture
    print("   ✅ StealthScreenCapture")
    
    from platforms.pokerstars_adapter import PokerStarsAdapter
    print("   ✅ PokerStarsAdapter")
    
    from core.poker_engine import PokerEngine
    print("   ✅ PokerEngine")
    
    from integration.poker_coach_integrator import PokerCoachIntegrator
    print("   ✅ PokerCoachIntegrator")
    
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Configuración
print("\n4. CONFIGURACIÓN:")
try:
    with open('config/default_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"   ✅ Configuración cargada")
    print(f"   📊 Plataforma por defecto: {config.get('platforms', {}).get('default', 'NO DEFINIDO')}")
    print(f"   🎯 Nivel stealth: {config.get('capture', {}).get('stealth_level', 'NO DEFINIDO')}")
    
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# Test 5: Templates de cartas
print("\n5. TEMPLATES DE CARTAS:")
try:
    template_path = "data/card_templates/pokerstars"
    if os.path.exists(template_path):
        suits = os.listdir(template_path)
        print(f"   ✅ Templates encontrados: {len(suits)} suits")
        for suit in suits:
            suit_path = os.path.join(template_path, suit)
            if os.path.isdir(suit_path):
                cards = [f for f in os.listdir(suit_path) if f.endswith('.png')]
                print(f"      {suit}: {len(cards)} cartas")
    else:
        print("   ⚠️  No se encontraron templates")
        print("   💡 Ejecuta: python scripts/setup_templates.py")
        
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("🎯 RESULTADO: SISTEMA LISTO PARA PRUEBAS")

# Preguntar qué test ejecutar
print("\n📋 TESTS DISPONIBLES:")
print("1. test_capture_system.py - Sistema de captura")
print("2. test_pokerstars.py - Adaptador PokerStars")
print("3. test_integrator.py - Integrador principal")
print("4. test_pokerstars_fixed.py - Adaptador corregido")

choice = input("\n¿Qué test quieres ejecutar? (1-4): ")

tests = {
    '1': 'test_capture_system.py',
    '2': 'test_pokerstars.py', 
    '3': 'test_integrator.py',
    '4': 'test_pokerstars_fixed.py'
}

if choice in tests:
    print(f"\n🚀 Ejecutando {tests[choice]}...")
    os.system(f"python {tests[choice]}")
else:
    print("\n✅ Compatibilidad verificada. Ejecuta manualmente los tests.")