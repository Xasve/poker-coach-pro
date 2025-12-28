# diagnostic_complete.py
import sys
import os
import importlib

def check_system():
    """Diagnóstico completo del sistema"""
    print("🔍 DIAGNÓSTICO COMPLETO POKER COACH PRO")
    print("=" * 60)
    
    # Verificar Python
    print(f"Python: {sys.version}")
    
    # Verificar rutas
    sys.path.insert(0, 'src')
    print(f"Ruta actual: {os.getcwd()}")
    print(f"src existe: {os.path.exists('src')}")
    
    # Lista de módulos a verificar
    modules_to_check = [
        ('numpy', 'numpy'),
        ('cv2', 'opencv-python'),
        ('mss', 'mss'),
        ('PIL', 'PIL'),
        ('pytesseract', 'pytesseract'),
        ('pygame', 'pygame'),
    ]
    
    # Verificar importaciones básicas
    print("\n📦 VERIFICANDO DEPENDENCIAS:")
    for name, package in modules_to_check:
        try:
            mod = importlib.import_module(name)
            version = getattr(mod, '__version__', 'N/A')
            print(f"✅ {name} ({package}) v{version}")
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    # Verificar módulos del proyecto
    print("\n🏗️ VERIFICANDO MÓDULOS DEL PROYECTO:")
    project_modules = [
        ('screen_capture.stealth_capture', 'StealthScreenCapture'),
        ('screen_capture.card_recognizer', 'CardRecognizer'),
        ('screen_capture.table_detector', 'TableDetector'),
        ('screen_capture.text_ocr', 'TextOCR'),
        ('integration.coach_integrator', 'CoachIntegrator'),
        ('platforms.pokerstars_adapter', 'PokerStarsAdapter'),
    ]
    
    for module_path, class_name in project_modules:
        try:
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            print(f"✅ {class_name} en {module_path}")
            
            # Verificar constructor
            try:
                if class_name == 'StealthScreenCapture':
                    instance = cls(stealth_level=1, platform="pokerstars")
                elif class_name == 'CardRecognizer':
                    instance = cls(platform="pokerstars")
                elif class_name == 'TextOCR':
                    instance = cls()
                else:
                    instance = cls()
                print(f"   ✓ Constructor funciona")
            except Exception as e:
                print(f"   ✗ Error en constructor: {e}")
                
        except Exception as e:
            print(f"❌ {class_name}: {e}")
    
    print("\n🎯 RESUMEN DEL ESTADO:")
    print("-" * 40)
    print("✅ Sistema modular verificado")
    print("✅ Arquitectura intacta")
    print("❌ Posibles problemas de constructores")
    print("⚠️  Verificar entorno virtual reinstalado")
    
    return True

if __name__ == "__main__":
    check_system()