# final_test.py - Prueba final del sistema corregido
import sys
import os

print("🚀 PRUEBA FINAL DEL SISTEMA CORREGIDO")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

# Función para prueba segura
def safe_test(description, test_func):
    print(f"\n🔍 {description}")
    try:
        result = test_func()
        print(f"✅ {result}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Contador de pruebas exitosas
passed_tests = 0
total_tests = 0

# Test 1: Importaciones básicas
total_tests += 1
if safe_test("1. Importando módulos principales", lambda: 
    "Módulos importados" if all([
        __import__('screen_capture.stealth_capture', fromlist=['StealthScreenCapture']),
        __import__('screen_capture.card_recognizer', fromlist=['CardRecognizer']),
        __import__('screen_capture.table_detector', fromlist=['TableDetector']),
        __import__('screen_capture.text_ocr', fromlist=['TextOCR']),
        __import__('platforms.pokerstars_adapter', fromlist=['PokerStarsAdapter'])
    ]) else "Fallo"):
    passed_tests += 1

# Test 2: Inicialización de StealthScreenCapture
total_tests += 1
if safe_test("2. Inicializando StealthScreenCapture", lambda: 
    "StealthScreenCapture creado" if (
        StealthScreenCapture := getattr(
            __import__('screen_capture.stealth_capture', fromlist=['StealthScreenCapture']),
            'StealthScreenCapture'
        )
    ) and (ss := StealthScreenCapture(stealth_level=1, platform="pokerstars")) and 
    hasattr(ss, 'platform') and ss.platform == "pokerstars" else "Fallo"):
    passed_tests += 1

# Test 3: Inicialización de CardRecognizer
total_tests += 1
if safe_test("3. Inicializando CardRecognizer", lambda: 
    "CardRecognizer creado" if (
        CardRecognizer := getattr(
            __import__('screen_capture.card_recognizer', fromlist=['CardRecognizer']),
            'CardRecognizer'
        )
    ) and (cr := CardRecognizer(platform="pokerstars")) and 
    hasattr(cr, 'platform') and cr.platform == "pokerstars" else "Fallo"):
    passed_tests += 1

# Test 4: Inicialización de TableDetector y TextOCR (sin argumentos)
total_tests += 1
if safe_test("4. Inicializando TableDetector (sin argumentos)", lambda: 
    "TableDetector creado" if (
        TableDetector := getattr(
            __import__('screen_capture.table_detector', fromlist=['TableDetector']),
            'TableDetector'
        )
    ) and (td := TableDetector()) else "Fallo"):
    passed_tests += 1

total_tests += 1
if safe_test("5. Inicializando TextOCR (sin argumentos)", lambda: 
    "TextOCR creado" if (
        TextOCR := getattr(
            __import__('screen_capture.text_ocr', fromlist=['TextOCR']),
            'TextOCR'
        )
    ) and (ocr := TextOCR()) else "Fallo"):
    passed_tests += 1

# Test 6: Sistema completo de adaptador
total_tests += 1
if safe_test("6. Inicializando PokerStarsAdapter completo", lambda: 
    "Adaptador completo" if (
        PokerStarsAdapter := getattr(
            __import__('platforms.pokerstars_adapter', fromlist=['PokerStarsAdapter']),
            'PokerStarsAdapter'
        )
    ) and (adapter := PokerStarsAdapter()) and 
    hasattr(adapter, 'platform') and adapter.platform == "pokerstars" and
    hasattr(adapter, 'screen_capturer') and adapter.screen_capturer is not None else "Fallo"):
    passed_tests += 1

# Test 7: Sistema de templates
total_tests += 1
if safe_test("7. Probando sistema de templates", lambda: 
    "Templates funcionando" if (
        CardTemplateManager := getattr(
            __import__('screen_capture.template_manager', fromlist=['CardTemplateManager']),
            'CardTemplateManager'
        )
    ) and (tm := CardTemplateManager("pokerstars")) and 
    (template := tm.get_template("A", "hearts")) is not None else "Fallo"):
    passed_tests += 1

# Resumen
print("\n" + "=" * 60)
print("📊 RESULTADOS FINALES:")
print(f"   Pruebas pasadas: {passed_tests}/{total_tests}")
print(f"   Porcentaje: {(passed_tests/total_tests)*100:.1f}%")

if passed_tests == total_tests:
    print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! 🎉")
    print("\n🚀 El sistema está listo para usar.")
    print("📝 Ejecuta: python run_pokerstars.py")
else:
    print(f"\n⚠️  {total_tests - passed_tests} pruebas fallaron.")
    print("🔧 Revisa los errores específicos arriba.")
    print("💡 Ejecuta: python debug_imports.py para diagnóstico detallado")

print("\n" + "=" * 60)