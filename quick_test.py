# quick_test.py - Prueba rápida después de las correcciones
import sys
import os
sys.path.insert(0, 'src')

print("🔧 PRUEBA RÁPIDA POST-CORRECCIONES")
print("=" * 50)

# Test 1: Importaciones básicas
print("\n1. Probando importaciones críticas...")
try:
    from screen_capture.stealth_capture import StealthScreenCapture
    from screen_capture.card_recognizer import CardRecognizer
    from screen_capture.table_detector import TableDetector
    from screen_capture.text_ocr import TextOCR
    print("✅ Todas las importaciones funcionan")
except ImportError as e:
    print(f"❌ Error de importación: {e}")

# Test 2: Inicialización de componentes
print("\n2. Probando inicialización...")
try:
    # Inicializar con los argumentos CORRECTOS
    capturer = StealthScreenCapture(stealth_level=1, platform="pokerstars")
    recognizer = CardRecognizer(platform="pokerstars")
    detector = TableDetector()  # Sin argumentos
    ocr = TextOCR()  # Sin argumentos
    
    print("✅ Todos los componentes inicializados")
    print(f"   - Capturer: {type(capturer).__name__}")
    print(f"   - Recognizer: {type(recognizer).__name__}")
    print(f"   - Detector: {type(detector).__name__}")
    print(f"   - OCR: {type(ocr).__name__}")
    
except TypeError as e:
    print(f"❌ Error de tipo (argumentos incorrectos): {e}")
except Exception as e:
    print(f"❌ Error general: {e}")

# Test 3: Adaptador PokerStars
print("\n3. Probando adaptador PokerStars...")
try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    adapter = PokerStarsAdapter()
    print(f"✅ Adaptador creado: {adapter}")
    print(f"   - Plataforma: {adapter.platform}")
    print(f"   - Nivel sigilo: {adapter.stealth_level}")
    
except Exception as e:
    print(f"❌ Error con adaptador: {e}")

# Test 4: Sistema de templates
print("\n4. Probando sistema de templates...")
try:
    from screen_capture.template_manager import CardTemplateManager
    tm = CardTemplateManager("pokerstars")
    template = tm.get_template("A", "hearts")
    print(f"✅ Template manager funciona")
    print(f"   - Template obtenido: {'Sí' if template is not None else 'No'}")
    
except Exception as e:
    print(f"❌ Error con templates: {e}")

print("\n" + "=" * 50)
print("🎯 PRUEBA COMPLETADA")
print("\nSiguiente paso: Ejecutar 'python test_pokerstars.py'")