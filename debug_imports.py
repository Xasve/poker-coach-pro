# debug_imports.py - Diagnóstico profundo de importaciones
import sys
import os
import traceback

print("🔍 DIAGNÓSTICO PROFUNDO DE IMPORTACIONES")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

# Test 1: Importar StealthScreenCapture con diferentes argumentos
print("\n1. Probando StealthScreenCapture con diferentes argumentos:")
test_cases = [
    ("Argumentos normales", lambda: __import__('screen_capture.stealth_capture', fromlist=['StealthScreenCapture'])),
    ("Solo stealth_level", lambda: None),  # No aplica
    ("Solo platform", lambda: None),  # No aplica
]

for test_name, import_func in test_cases:
    try:
        module = import_func()
        StealthScreenCapture = getattr(module, 'StealthScreenCapture')
        
        # Probar diferentes combinaciones de inicialización
        print(f"\n   Probando: {test_name}")
        
        # Caso 1: Ambos argumentos
        try:
            ss1 = StealthScreenCapture(stealth_level=2, platform="pokerstars")
            print(f"   ✅ StealthScreenCapture(2, 'pokerstars') - OK")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Caso 2: Solo stealth_level (debería usar default para platform)
        try:
            ss2 = StealthScreenCapture(stealth_level=1)
            print(f"   ✅ StealthScreenCapture(1) - OK")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Caso 3: Solo platform (debería usar default para stealth_level)
        try:
            ss3 = StealthScreenCapture(platform="ggpoker")
            print(f"   ✅ StealthScreenCapture('ggpoker') - OK")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        # Caso 4: Sin argumentos
        try:
            ss4 = StealthScreenCapture()
            print(f"   ✅ StealthScreenCapture() - OK")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
    except Exception as e:
        print(f"   ❌ Error en import: {e}")

# Test 2: Verificar la estructura de parámetros real
print("\n" + "=" * 60)
print("2. Analizando firma de constructores...")

import inspect

modules_to_check = [
    ('screen_capture.stealth_capture', 'StealthScreenCapture'),
    ('screen_capture.card_recognizer', 'CardRecognizer'),
    ('screen_capture.table_detector', 'TableDetector'),
    ('screen_capture.text_ocr', 'TextOCR'),
    ('platforms.pokerstars_adapter', 'PokerStarsAdapter'),
]

for module_path, class_name in modules_to_check:
    try:
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        
        # Obtener la firma del constructor
        sig = inspect.signature(cls.__init__)
        params = list(sig.parameters.keys())
        
        # Remover 'self'
        if 'self' in params:
            params.remove('self')
        
        print(f"\n   {class_name}.__init__({', '.join(params)})")
        
        # Mostrar valores por defecto
        for param_name, param in sig.parameters.items():
            if param_name != 'self' and param.default != inspect.Parameter.empty:
                print(f"      {param_name} = {param.default}")
                
    except Exception as e:
        print(f"   ❌ Error analizando {class_name}: {e}")

# Test 3: Prueba de integración completa
print("\n" + "=" * 60)
print("3. Prueba de integración completa:")

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    print("\n   Creando PokerStarsAdapter...")
    adapter = PokerStarsAdapter(stealth_level=2)
    
    print(f"   ✅ Adaptador creado exitosamente")
    print(f"   - Platform: {adapter.platform}")
    print(f"   - Stealth level: {adapter.stealth_level}")
    print(f"   - Capture delay: {adapter.capture_delay}")
    
    # Verificar componentes internos
    print("\n   Verificando componentes internos:")
    components = [
        ('screen_capturer', adapter.screen_capturer),
        ('card_recognizer', adapter.card_recognizer),
        ('table_detector', adapter.table_detector),
        ('text_ocr', adapter.text_ocr)
    ]
    
    for name, component in components:
        if component is not None:
            print(f"   ✅ {name}: {type(component).__name__}")
        else:
            print(f"   ❌ {name}: None")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("\n   Traceback completo:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("🎯 DIAGNÓSTICO COMPLETADO")
print("\n📋 RESUMEN:")
print("Si ves 'OK' en todas las pruebas, el sistema está listo.")
print("Si hay errores, revisa las firmas de los constructores.")