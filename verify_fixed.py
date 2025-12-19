# verify_fixed.py - Ejecutar en la raíz del proyecto
import sys
import os
import json

print("🎯 VERIFICACIÓN COMPLETA DEL SISTEMA")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

# 1. Verificar estructura
print("\n📁 VERIFICANDO ESTRUCTURA...")
required_dirs = [
    'data/card_templates/pokerstars',
    'data/card_templates/ggpoker',
    'data/card_templates/fallback',
    'debug',
    'logs',
    'hand_history',
    'config'
]

for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"✅ {dir_path}/")
    else:
        print(f"❌ {dir_path}/ (FALTANTE)")

# 2. Verificar archivos de configuración
print("\n⚙️  VERIFICANDO CONFIGURACIÓN...")
config_files = [
    'config/settings.json',
    'config/strategies.json',
    'config/platforms.json'
]

for config_file in config_files:
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✅ {config_file} (válido)")
        except json.JSONDecodeError:
            print(f"⚠️  {config_file} (JSON inválido)")
    else:
        print(f"❌ {config_file} (FALTANTE)")

# 3. Verificar módulos
print("\n🔄 VERIFICANDO MÓDULOS...")
modules = [
    ('screen_capture.stealth_capture', 'StealthScreenCapture'),
    ('screen_capture.card_recognizer', 'CardRecognizer'),
    ('screen_capture.table_detector', 'TableDetector'),
    ('screen_capture.text_ocr', 'TextOCR'),
    ('screen_capture.template_manager', 'CardTemplateManager'),
    ('platforms.pokerstars_adapter', 'PokerStarsAdapter'),
    ('platforms.ggpoker_adapter', 'GGPokerAdapter'),
    ('integration.coach_integrator', 'CoachIntegrator'),
]

all_modules_ok = True

for module_path, class_name in modules:
    try:
        module = __import__(module_path, fromlist=[class_name])
        if hasattr(module, class_name):
            # Intentar crear instancia simple
            if class_name == 'CardTemplateManager':
                obj = getattr(module, class_name)("pokerstars")
            elif class_name in ['PokerStarsAdapter', 'GGPokerAdapter']:
                obj = getattr(module, class_name)()
            else:
                obj = getattr(module, class_name)("pokerstars", 1)
            
            print(f"✅ {class_name} (instanciado correctamente)")
        else:
            print(f"❌ {class_name} (no encontrado en módulo)")
            all_modules_ok = False
    except Exception as e:
        print(f"❌ {class_name}: {str(e)[:80]}")
        all_modules_ok = False

# 4. Verificar templates
print("\n🃏 VERIFICANDO TEMPLATES DE CARTAS...")
try:
    from src.screen_capture.template_manager import CardTemplateManager
    tm = CardTemplateManager("pokerstars")
    
    # Verificar templates básicos
    test_cards = [
        ("A", "hearts"),
        ("K", "spades"),
        ("10", "diamonds"),
        ("Q", "clubs")
    ]
    
    templates_found = 0
    for value, suit in test_cards:
        template = tm.get_template(value, suit)
        if template is not None:
            templates_found += 1
    
    print(f"✅ Sistema de templates: {templates_found}/4 templates obtenidos")
    
except Exception as e:
    print(f"❌ Error en templates: {e}")

# 5. Resumen
print("\n" + "=" * 60)
print("📊 RESUMEN DE VERIFICACIÓN")

if all_modules_ok:
    print("🎉 ¡SISTEMA VERIFICADO CORRECTAMENTE!")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Ejecutar: python test_pokerstars.py")
    print("2. Abrir PokerStars en una mesa")
    print("3. Verificar captura de pantalla")
    print("4. Probar reconocimiento de cartas")
else:
    print("⚠️  SE ENCONTRARON PROBLEMAS")
    print("\n🔧 SOLUCIONES:")
    print("1. Ejecutar: python create_structure.py")
    print("2. Verificar dependencias: pip install opencv-python mss numpy")
    print("3. Revisar errores específicos arriba")

print("\n" + "=" * 60)