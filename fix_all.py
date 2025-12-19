#!/usr/bin/env python3
"""
REPARADOR COMPLETO - Poker Coach Pro
Soluciona TODOS los problemas comunes
"""
import os
import sys
import shutil

def print_header():
    print("=" * 60)
    print("🛠️  REPARADOR COMPLETO - POKER COACH PRO")
    print("=" * 60)

def fix_syntax_errors():
    """Reparar errores de sintaxis en todos los archivos"""
    print("\n🔧 Reparando errores de sintaxis...")
    
    # Lista de archivos conocidos con problemas
    files_to_check = [
        "test_system.py",
        "start_coach.py",
        "fix_imports.py",
        "fix_imports_corrected.py",
        "src/screen_capture/__init__.py",
        "src/screen_capture/stealth_capture.py",
        "src/screen_capture/card_recognizer.py",
        "src/screen_capture/table_detector.py",
        "src/screen_capture/text_ocr.py"
    ]
    
    fixed_count = 0
    
    for filepath in files_to_check:
        if not os.path.exists(filepath):
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Problemas comunes a buscar y reparar
            original_content = content
            
            # 1. Strings con \ mal formados
            content = content.replace('\\"', '"')
            content = content.replace("\\'", "'")
            
            # 2. Strings sin cerrar en print
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'print(' in line and line.count('"') % 2 != 0:
                    # Intentar arreglar string sin cerrar
                    if line.endswith('"') and not line.endswith('\\"'):
                        lines[i] = line + '"'
            
            content = '\n'.join(lines)
            
            # 3. Caracteres de escape problemáticos
            content = content.replace('\\\\', '\\')
            
            # Guardar solo si hubo cambios
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {filepath} - reparado")
                fixed_count += 1
            else:
                print(f"✓ {filepath} - OK")
                
        except Exception as e:
            print(f"❌ {filepath} - error: {e}")
    
    return fixed_count

def ensure_basic_structure():
    """Asegurar que exista la estructura básica"""
    print("\n📁 Verificando estructura de directorios...")
    
    required_dirs = [
        "src",
        "src/screen_capture",
        "src/core",
        "src/platforms", 
        "src/overlay",
        "src/integration",
        "data",
        "logs",
        "debug"
    ]
    
    created_count = 0
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Creado: {directory}/")
            created_count += 1
        else:
            print(f"✓ {directory}/ - existe")
    
    return created_count

def create_minimal_modules():
    """Crear módulos mínimos pero funcionales"""
    print("\n📄 Creando módulos esenciales...")
    
    # 1. __init__.py para screen_capture
    init_content = '''"""
Módulo de captura de pantalla - Poker Coach Pro
"""
__version__ = "1.0.0"
__author__ = "Poker Coach Pro Team"

# Las importaciones se harán de forma perezosa para evitar problemas
'''

    with open("src/screen_capture/__init__.py", "w", encoding="utf-8") as f:
        f.write(init_content)
    print("✅ src/screen_capture/__init__.py")
    
    # 2. stealth_capture.py MÍNIMO
    stealth_content = '''import mss
import cv2
import numpy as np

class StealthScreenCapture:
    """Captura básica de pantalla"""
    
    def __init__(self):
        self.sct = None
    
    def initialize(self):
        """Inicializar capturador"""
        try:
            self.sct = mss.mss()
            return True
        except Exception as e:
            print(f"Error inicializando MSS: {e}")
            return False
    
    def capture(self):
        """Capturar pantalla completa"""
        if not self.sct:
            if not self.initialize():
                return None
        
        try:
            screenshot = self.sct.grab(self.sct.monitors[1])
            img = np.array(screenshot)
            
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            return img
        except Exception as e:
            print(f"Error capturando: {e}")
            return None
'''

    with open("src/screen_capture/stealth_capture.py", "w", encoding="utf-8") as f:
        f.write(stealth_content)
    print("✅ src/screen_capture/stealth_capture.py")
    
    # 3. table_detector.py MÍNIMO
    table_content = '''import cv2
import numpy as np

class TableDetector:
    """Detector básico de mesas"""
    
    def detect(self, image):
        """Detectar si hay una mesa en la imagen"""
        if image is None:
            return False
        
        # Método simple: buscar áreas verdes grandes
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Rango para verde
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])
            
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Contar píxeles verdes
            green_pixels = np.sum(mask > 0)
            total_pixels = image.shape[0] * image.shape[1]
            green_percentage = green_pixels / total_pixels
            
            return green_percentage > 0.1  # Más del 10% verde
            
        except Exception as e:
            print(f"Error detectando mesa: {e}")
            return False
'''

    with open("src/screen_capture/table_detector.py", "w", encoding="utf-8") as f:
        f.write(table_content)
    print("✅ src/screen_capture/table_detector.py")
    
    # 4. Crear otros __init__.py
    init_files = [
        "src/__init__.py",
        "src/core/__init__.py", 
        "src/platforms/__init__.py",
        "src/overlay/__init__.py",
        "src/integration/__init__.py"
    ]
    
    for init_file in init_files:
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('"""Módulo Poker Coach Pro"""\n\n__version__ = "1.0.0"')
        print(f"✅ {init_file}")
    
    return 7  # Número de archivos creados

def create_working_start_script():
    """Crear script de inicio FUNCIONAL"""
    print("\n🚀 Creando script de inicio funcional...")
    
    start_content = '''#!/usr/bin/env python3
"""
POKER COACH PRO - VERSIÓN FUNCIONAL
Sistema básico pero operativo
"""
import sys
import os
import time

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 60)
    print("🎴 POKER COACH PRO - SISTEMA BÁSICO")
    print("=" * 60)
    
    try:
        # Importar módulos
        print("\n🔧 Importando módulos...")
        from screen_capture.stealth_capture import StealthScreenCapture
        from screen_capture.table_detector import TableDetector
        
        print("✅ Módulos importados correctamente")
        
        # Crear componentes
        print("\n🛠️  Creando componentes...")
        capture = StealthScreenCapture()
        detector = TableDetector()
        
        print("✅ Componentes creados")
        
        # Menú simple
        while True:
            print("\n" + "=" * 60)
            print("🎮 MENÚ PRINCIPAL")
            print("=" * 60)
            print("\n1. Probar captura de pantalla")
            print("2. Buscar mesa de poker")
            print("3. Salir")
            
            try:
                option = input("\n👉 Selecciona una opción (1-3): ").strip()
                
                if option == "1":
                    test_capture(capture)
                elif option == "2":
                    find_table(capture, detector)
                elif option == "3":
                    print("\n👋 ¡Hasta pronto!")
                    break
                else:
                    print("❌ Opción no válida")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Operación cancelada")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    except ImportError as e:
        print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
        print("\n💡 Ejecuta: python fix_all.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_capture(capture):
    """Probar la captura de pantalla"""
    print("\n" + "=" * 60)
    print("📸 PRUEBA DE CAPTURA")
    print("=" * 60)
    
    print("\nInicializando captura...")
    if capture.initialize():
        print("✅ Captura inicializada")
    else:
        print("❌ No se pudo inicializar la captura")
        return
    
    print("\nCapturando pantalla...")
    screenshot = capture.capture()
    
    if screenshot is not None:
        print(f"✅ Captura exitosa!")
        print(f"   Tamaño: {screenshot.shape}")
        print(f"   Tipo: {screenshot.dtype}")
        
        # Guardar para revisión
        os.makedirs("debug", exist_ok=True)
        import cv2
        filename = "debug/test_capture.png"
        cv2.imwrite(filename, screenshot)
        print(f"   💾 Guardado como: {filename}")
        
        # Mostrar información básica
        print(f"\n📊 Información de la imagen:")
        print(f"   Ancho: {screenshot.shape[1]} px")
        print(f"   Alto: {screenshot.shape[0]} px")
        print(f"   Canales: {screenshot.shape[2]}")
        
    else:
        print("❌ No se pudo capturar la pantalla")

def find_table(capture, detector):
    """Buscar mesa de poker"""
    print("\n" + "=" * 60)
    print("🎯 BUSCANDO MESA DE POKER")
    print("=" * 60)
    
    print("\n1. Inicializando captura...")
    if not capture.initialize():
        print("❌ No se pudo inicializar la captura")
        return
    
    print("2. Capturando pantalla...")
    screenshot = capture.capture()
    
    if screenshot is None:
        print("❌ No se pudo capturar la pantalla")
        return
    
    print("3. Analizando imagen...")
    has_table = detector.detect(screenshot)
    
    if has_table:
        print("\n✅ ¡MESA DETECTADA!")
        print("\n💡 Consejos:")
        print("   - El sistema encontró una posible mesa de poker")
        print("   - Basado en la detección de áreas verdes")
        print("   - Asegúrate de que PokerStars/GG Poker esté visible")
    else:
        print("\n❌ No se detectó mesa de poker")
        print("\n💡 Posibles causas:")
        print("   - No hay ventana de poker visible")
        print("   - La mesa no es verde")
        print("   - La captura falló")
    
    # Guardar captura siempre
    os.makedirs("debug", exist_ok=True)
    import cv2
    filename = "debug/table_search.png"
    cv2.imwrite(filename, screenshot)
    print(f"\n💾 Captura guardada: {filename}")

if __name__ == "__main__":
    main()
'''

    with open("poker_coach.py", "w", encoding="utf-8") as f:
        f.write(start_content)
    
    print("✅ Script principal creado: poker_coach.py")
    return True

def check_python_environment():
    """Verificar el entorno Python"""
    print("\n🐍 Verificando entorno Python...")
    
    info = {
        "Python version": sys.version,
        "Python executable": sys.executable,
        "Current directory": os.getcwd(),
        "Platform": sys.platform
    }
    
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    return True

def run_quick_test():
    """Ejecutar prueba rápida"""
    print("\n🧪 Ejecutando prueba rápida...")
    
    # Añadir src al path
    sys.path.insert(0, 'src')
    
    try:
        # Intentar importar
        import screen_capture
        print("✅ screen_capture importado")
        
        from screen_capture.stealth_capture import StealthScreenCapture
        print("✅ StealthScreenCapture importado")
        
        from screen_capture.table_detector import TableDetector
        print("✅ TableDetector importado")
        
        print("\n🎉 ¡TODAS LAS IMPORTACIONES FUNCIONAN!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_requirements_file():
    """Crear archivo de dependencias"""
    print("\n📦 Creando requirements.txt...")
    
    requirements = '''# DEPENDENCIAS BÁSICAS
opencv-python>=4.8.0
mss>=9.0.1
numpy>=1.24.0

# DEPENDENCIAS OPCIONALES
# pygame>=2.5.0        # Para overlay
# pytesseract>=0.3.10  # Para OCR
# Pillow>=10.0.0       # Para imágenes
# pyautogui>=0.9.54    # Para automatización

# UTILIDADES
colorama>=0.4.6        # Colores en consola
'''
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements)
    
    print("✅ requirements.txt creado")
    return True

def main():
    print_header()
    
    # 1. Verificar entorno
    check_python_environment()
    
    # 2. Reparar errores de sintaxis
    fixed_files = fix_syntax_errors()
    
    # 3. Crear estructura
    created_dirs = ensure_basic_structure()
    
    # 4. Crear módulos mínimos
    created_modules = create_minimal_modules()
    
    # 5. Crear script de inicio
    create_working_start_script()
    
    # 6. Crear requirements
    create_requirements_file()
    
    # 7. Probar
    test_passed = run_quick_test()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA REPARACIÓN")
    print("=" * 60)
    print(f"\n✅ Archivos reparados: {fixed_files}")
    print(f"✅ Directorios creados/verificados: {created_dirs}")
    print(f"✅ Módulos creados: {created_modules}")
    print(f"✅ Prueba de importación: {'PASADA' if test_passed else 'FALLADA'}")
    
    print("\n🚀 INSTRUCCIONES FINALES:")
    print("=" * 60)
    
    if test_passed:
        print("\n🎉 ¡SISTEMA REPARADO CON ÉXITO!")
        print("\n📋 PARA USAR EL SISTEMA:")
        print("   1. Instala dependencias: pip install -r requirements.txt")
        print("   2. Ejecuta el sistema: python poker_coach.py")
        print("   3. Sigue las instrucciones en pantalla")
    else:
        print("\n⚠️  REPARACIÓN PARCIAL")
        print("\n💡 PROBLEMAS PERSISTENTES:")
        print("   1. Verifica que Python esté instalado correctamente")
        print("   2. Asegúrate de tener permisos de escritura")
        print("   3. Intenta ejecutar en una nueva terminal")
    
    print("\n🆘 PARA MÁS AYUDA:")
    print("   - Revisa la carpeta 'debug/' para capturas")
    print("   - Verifica los logs si hay errores")
    print("   - Ejecuta 'python poker_coach.py' para comenzar")
    print("=" * 60)

if __name__ == "__main__":
    main()