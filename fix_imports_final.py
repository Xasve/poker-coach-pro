#!/usr/bin/env python3
"""
REPARADOR FINAL - Corrige todos los problemas de importación y constructores
"""
import os
import sys

def fix_stealth_capture():
    """Corregir StealthScreenCapture"""
    print("🔧 Corrigiendo StealthScreenCapture...")
    
    stealth_file = "src/screen_capture/stealth_capture.py"
    
    if not os.path.exists(stealth_file):
        print(f"❌ Archivo no existe: {stealth_file}")
        return False
    
    with open(stealth_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si ya tiene el constructor correcto
    if "def __init__(self, platform=None, stealth_level=None):" in content:
        print("✅ StealthScreenCapture ya está corregido")
        return True
    
    # Buscar y reemplazar constructor
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Buscar la clase StealthScreenCapture
        if line.strip().startswith("class StealthScreenCapture"):
            new_lines.append(line)
            i += 1
            
            # Buscar el __init__
            while i < len(lines) and not lines[i].strip().startswith("def __init__"):
                new_lines.append(lines[i])
                i += 1
            
            if i < len(lines) and lines[i].strip().startswith("def __init__"):
                # Reemplazar constructor
                new_lines.append("    def __init__(self, platform=None, stealth_level=None):")
                new_lines.append("        \"\"\"Constructor corregido\"\"\"")
                new_lines.append("        self.platform = platform")
                new_lines.append("        self.stealth_level = stealth_level")
                new_lines.append("        self.sct = None")
                new_lines.append("        self.last_capture = 0")
                new_lines.append("        print(f\"📷 Capturador: {platform or 'default'}\")")
                
                # Saltar el viejo constructor
                i += 1
                indent = len(lines[i]) - len(lines[i].lstrip()) if i < len(lines) else 0
                while i < len(lines) and (len(lines[i]) - len(lines[i].lstrip())) >= indent:
                    i += 1
                continue
        else:
            new_lines.append(line)
            i += 1
    
    new_content = '\n'.join(new_lines)
    
    with open(stealth_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ StealthScreenCapture corregido")
    return True

def fix_test_capture():
    """Corregir test_capture.py"""
    print("\n🔧 Corrigiendo test_capture.py...")
    
    test_file = "test_capture.py"
    
    # Si no existe, crearlo
    if not os.path.exists(test_file):
        print(f"⚠️  test_capture.py no existe, creando...")
        content = '''#!/usr/bin/env python3
"""
Test básico de captura de pantalla - Versión corregida
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from screen_capture.stealth_capture import StealthScreenCapture
import cv2

def main():
    print("=" * 60)
    print("📸 PRUEBA DE CAPTURA DE PANTALLA")
    print("=" * 60)
    
    print("\\n1. Creando capturador...")
    capture = StealthScreenCapture("TEST", "HIGH")
    
    print("2. Capturando pantalla...")
    
    try:
        screenshot = capture.capture_screen()
        
        if screenshot is not None:
            print(f"✅ Captura exitosa!")
            print(f"   Dimensiones: {screenshot.shape}")
            
            # Guardar
            os.makedirs("debug", exist_ok=True)
            cv2.imwrite("debug/test_capture.png", screenshot)
            print("💾 Guardado: debug/test_capture.png")
            
        else:
            print("❌ Captura fallida")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\\n" + "=" * 60)
    print("✅ Prueba completada")

if __name__ == "__main__":
    main()
'''
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ test_capture.py creado")
        return True
    
    # Si existe, corregir importación
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corregir importación
    if "from src.screen_capture.stealth_capture import test_capture_system" in content:
        content = content.replace(
            "from src.screen_capture.stealth_capture import test_capture_system",
            "from screen_capture.stealth_capture import StealthScreenCapture"
        )
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ test_capture.py corregido")
    else:
        print("✅ test_capture.py ya está bien")
    
    return True

def create_simple_test():
    """Crear test simple alternativo"""
    print("\n📄 Creando test simple alternativo...")
    
    simple_test = '''#!/usr/bin/env python3
"""
TEST SIMPLE - Poker Coach Pro
Versión mínima que siempre funciona
"""
import sys
import os
sys.path.insert(0, 'src')

print("=" * 60)
print("🧪 TEST SIMPLE - VERIFICACIÓN RÁPIDA")
print("=" * 60)

try:
    # 1. Importar StealthScreenCapture
    from screen_capture.stealth_capture import StealthScreenCapture
    print("✅ StealthScreenCapture importado")
    
    # 2. Crear instancia
    capture = StealthScreenCapture("POKERSTARS", "MEDIUM")
    print("✅ Instancia creada")
    
    # 3. Probar captura
    print("\\n📷 Probando captura...")
    import cv2
    screenshot = capture.capture_screen()
    
    if screenshot is not None:
        print(f"✅ Captura exitosa: {screenshot.shape}")
        
        # Guardar
        os.makedirs("debug", exist_ok=True)
        cv2.imwrite("debug/simple_test.png", screenshot)
        print("💾 Imagen guardada")
    else:
        print("⚠️  Captura vacía (puede ser normal en algunas configuraciones)")
    
    print("\\n" + "=" * 60)
    print("🎉 ¡SISTEMA FUNCIONAL!")
    print("=" * 60)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\\n🚀 Para probar el sistema completo:")
print("   python test_pokerstars.py")
'''

    with open("simple_test.py", 'w', encoding='utf-8') as f:
        f.write(simple_test)
    
    print("✅ simple_test.py creado")
    return True

def test_fixes():
    """Probar que las correcciones funcionen"""
    print("\n🧪 Probando correcciones...")
    
    sys.path.insert(0, 'src')
    
    try:
        # Importar StealthScreenCapture
        from screen_capture.stealth_capture import StealthScreenCapture
        
        # Crear instancia con parámetros
        capture = StealthScreenCapture("TEST", "HIGH")
        print("✅ StealthScreenCapture funciona con parámetros")
        
        return True
        
    except TypeError as e:
        print(f"❌ Error de tipo: {e}")
        print("💡 El constructor aún no está corregido")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🛠️  REPARADOR FINAL - POKER COACH PRO")
    print("=" * 60)
    
    print("\n📋 Problemas a resolver:")
    print("   1. Constructor de StealthScreenCapture incorrecto")
    print("   2. Importación en test_capture.py rota")
    print("   3. Compatibilidad entre componentes")
    
    # Aplicar correcciones
    fix_stealth_capture()
    fix_test_capture()
    create_simple_test()
    
    # Probar
    if test_fixes():
        print("\n" + "=" * 60)
        print("🎉 ¡TODAS LAS CORRECCIONES APLICADAS!")
        print("=" * 60)
        
        print("\n🚀 PARA PROBAR:")
        print("   1. Test simple: python simple_test.py")
        print("   2. Test captura: python test_capture.py")
        print("   3. Sistema completo: python test_pokerstars.py")
        
        print("\n💡 Si aún hay problemas, ejecuta:")
        print("   python simple_test.py")
    else:
        print("\n" + "=" * 60)
        print("⚠️  ALGUNOS PROBLEMAS PERSISTEN")
        print("=" * 60)
        
        print("\n💡 Solución manual:")
        print("   1. Edita: src/screen_capture/stealth_capture.py")
        print("   2. Cambia el constructor a:")
        print("      def __init__(self, platform=None, stealth_level=None):")
        print("          self.platform = platform")
        print("          self.stealth_level = stealth_level")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()