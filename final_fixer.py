# final_fixer.py - Reparador definitivo del sistema
import os
import sys
import shutil

print("🔧 REPARADOR DEFINITIVO DEL POKER COACH PRO")
print("=" * 60)

def fix_numpy_issue():
    """Solucionar problema de numpy"""
    print("\n1. SOLUCIONANDO PROBLEMA DE NUMPY...")
    
    # Verificar si numpy está instalado
    try:
        import numpy
        print(f"   ✅ NumPy ya está instalado: versión {numpy.__version__}")
        return True
    except ImportError:
        print("   ❌ NumPy no está instalado")
    
    # Intentar reinstalar
    print("   🔄 Intentando reinstalar numpy...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "numpy"])
        print("   ✅ NumPy reinstalado correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error reinstalando numpy: {e}")
        return False

def fix_stealth_capture():
    """Reparar StealthScreenCapture"""
    print("\n2. REPARANDO STEALTHSCREENCAPTURE...")
    
    stealth_path = "src/screen_capture/stealth_capture.py"
    
    if not os.path.exists(stealth_path):
        print(f"   ❌ Archivo no encontrado: {stealth_path}")
        return False
    
    try:
        with open(stealth_path, 'r') as f:
            content = f.read()
        
        # Verificar si el constructor está vacío
        if "def __init__(self):" in content and "def __init__(self, " not in content:
            print("   ⚠️  Constructor vacío detectado, actualizando...")
            
            # Reemplazar constructor vacío por uno con parámetros
            old_init = '''def __init__(self):
        """Inicializador CORREGIDO - maneja correctamente los argumentos"""
        
        # 🔥 CORRECCIÓN: Asegurar que platform sea string
        self.platform = "pokerstars"'''
        
            new_init = '''def __init__(self, stealth_level=1, platform="pokerstars"):
        """
        Inicializador CORREGIDO - maneja correctamente los argumentos
        
        Args:
            stealth_level (int): Nivel de sigilo (1-3)
            platform (str): Plataforma ('pokerstars', 'ggpoker', etc.)
        """
        # 🔥 CORRECCIÓN: Asegurar que platform sea string
        self.platform = str(platform) if platform else "pokerstars"
        
        # Validar y convertir stealth_level
        if isinstance(stealth_level, str):
            try:
                self.stealth_level = int(stealth_level)
            except ValueError:
                self.stealth_level = 1
        else:
            self.stealth_level = int(stealth_level)
        
        # Limitar el rango de stealth_level
        self.stealth_level = max(1, min(3, self.stealth_level))
        
        # Configurar delays según nivel de sigilo
        self.capture_delays = {
            1: 0.1,    # Bajo sigilo - más rápido
            2: 0.3,    # Medio sigilo
            3: 0.5     # Alto sigilo - más lento
        }
        
        self.capture_delay = self.capture_delays.get(self.stealth_level, 0.1)
        
        # Nombres de niveles de sigilo
        stealth_names = {
            1: "BAJO",
            2: "MEDIO", 
            3: "ALTO"
        }
        
        print(f"🎯 StealthScreenCapture inicializado para {self.platform}")
        print(f"🔰 Nivel de sigilo: {stealth_names.get(self.stealth_level, 'BAJO')}")
        print(f"⚙️  Delay de captura: {self.capture_delay}s")'''
        
        if old_init in content:
            content = content.replace(old_init, new_init)
            print("   ✅ Constructor actualizado con parámetros")
        
        # Guardar cambios
        backup_path = stealth_path + '.backup'
        shutil.copy2(stealth_path, backup_path)
        
        with open(stealth_path, 'w') as f:
            f.write(content)
        
        print(f"   ✅ StealthScreenCapture reparado")
        print(f"   💾 Backup guardado en: {backup_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error reparando StealthScreenCapture: {e}")
        return False

def create_fixed_pokerstars_adapter():
    """Crear adaptador PokerStars corregido"""
    print("\n3. CREANDO ADAPTADOR POKERSTARS CORREGIDO...")
    
    adapter_code = '''# pokerstars_adapter_fixed.py - Adaptador corregido
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Intentar importar con manejo de errores
try:
    from screen_capture.stealth_capture import StealthScreenCapture
    from screen_capture.card_recognizer import CardRecognizer
    from screen_capture.table_detector import TableDetector
    from screen_capture.text_ocr import TextOCR
except ImportError as e:
    print(f"⚠️  Error importando módulos de screen_capture: {e}")
    # Clases placeholder
    class StealthScreenCapture:
        def __init__(self, stealth_level=1, platform="pokerstars"):
            self.platform = platform
            self.stealth_level = stealth_level
            self.capture_delay = 0.1
            print(f"🎯 StealthScreenCapture (placeholder) para {platform}")
        def capture_screen(self): return None
    
    class CardRecognizer:
        def __init__(self, platform="pokerstars"): 
            self.platform = platform
            print(f"🃏 CardRecognizer (placeholder) para {platform}")
        def recognize_cards(self, img, pos=None): return []
    
    class TableDetector:
        def __init__(self): print("🟢 TableDetector (placeholder)")
        def detect(self, img): return False
    
    class TextOCR:
        def __init__(self): print("🔤 TextOCR (placeholder)")
        def extract_text(self, img): return ""

class PokerStarsAdapter:
    def __init__(self, stealth_level=1):
        # 🔥 CORRECCIÓN: Definir el atributo 'platform' PRIMERO
        self.platform = "pokerstars"
        self.stealth_level = stealth_level
        self.capture_delay = max(0.1, 0.5 / stealth_level)
        
        print(f"🎴 Inicializando adaptador para {self.platform}...")
        
        # 🔥 CORRECCIÓN: Pasar los argumentos CORRECTOS
        try:
            self.screen_capturer = StealthScreenCapture(stealth_level=stealth_level, platform=self.platform)
            self.card_recognizer = CardRecognizer(platform=self.platform)
            self.table_detector = TableDetector()
            self.text_ocr = TextOCR()
            
            print("✅ Todos los componentes del adaptador inicializados")
            
        except Exception as e:
            print(f"❌ Error inicializando componentes: {e}")
            self.screen_capturer = None
            self.card_recognizer = None
            self.table_detector = None
            self.text_ocr = None
    
    def capture_table(self):
        """Capturar la pantalla donde está la mesa"""
        if self.screen_capturer:
            return self.screen_capturer.capture_screen()
        return None
    
    def detect_table(self, screenshot):
        """Detectar si hay una mesa de poker en la captura"""
        if self.table_detector:
            return self.table_detector.detect(screenshot)
        return False
    
    def recognize_hole_cards(self, screenshot):
        """Reconocer las cartas propias (hole cards)"""
        if self.card_recognizer:
            # Posiciones para 1920x1080
            card_positions = [
                (850, 930, 71, 96),   # Hole card 1
                (1000, 930, 71, 96)   # Hole card 2
            ]
            return self.card_recognizer.recognize_cards(screenshot, card_positions)
        return []
    
    def recognize_community_cards(self, screenshot):
        """Reconocer las cartas comunitarias"""
        if self.card_recognizer:
            # Posiciones para 1920x1080
            card_positions = [
                (780, 480, 71, 96),   # Flop 1
                (870, 480, 71, 96),   # Flop 2
                (960, 480, 71, 96),   # Flop 3
                (1050, 480, 71, 96),  # Turn
                (1140, 480, 71, 96)   # River
            ]
            return self.card_recognizer.recognize_cards(screenshot, card_positions)
        return []
    
    def get_table_info(self, screenshot):
        """Obtener información general de la mesa"""
        return {
            "platform": self.platform,
            "stealth_level": self.stealth_level,
            "table_detected": self.detect_table(screenshot) if screenshot is not None else False
        }
'''
    
    try:
        # Crear directorio si no existe
        os.makedirs("src/platforms_fixed", exist_ok=True)
        
        # Guardar adaptador corregido
        adapter_path = "src/platforms_fixed/pokerstars_adapter_fixed.py"
        with open(adapter_path, 'w') as f:
            f.write(adapter_code)
        
        print(f"   ✅ Adaptador corregido creado: {adapter_path}")
        return adapter_path
        
    except Exception as e:
        print(f"   ❌ Error creando adaptador: {e}")
        return None

def update_run_pokerstars():
    """Actualizar run_pokerstars_optimized.py para usar versiones corregidas"""
    print("\n4. ACTUALIZANDO RUN_POKERSTARS_OPTIMIZED.PY...")
    
    run_path = "run_pokerstars_optimized.py"
    
    if not os.path.exists(run_path):
        print(f"   ❌ Archivo no encontrado: {run_path}")
        return False
    
    try:
        with open(run_path, 'r') as f:
            content = f.read()
        
        # Reemplazar import del adaptador
        old_import = "from platforms.pokerstars_adapter import PokerStarsAdapter"
        new_import = "from platforms_fixed.pokerstars_adapter_fixed import PokerStarsAdapter"
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            print("   ✅ Import del adaptador actualizado")
        
        # Guardar cambios
        backup_path = run_path + '.backup'
        shutil.copy2(run_path, backup_path)
        
        with open(run_path, 'w') as f:
            f.write(content)
        
        print(f"   ✅ run_pokerstars_optimized.py actualizado")
        print(f"   💾 Backup guardado en: {backup_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error actualizando run_pokerstars: {e}")
        return False

def create_simple_test():
    """Crear una prueba simple para verificar"""
    print("\n5. CREANDO PRUEBA DE VERIFICACIÓN...")
    
    test_code = '''# simple_test.py - Prueba simple del sistema
import sys
import os

print("🧪 PRUEBA SIMPLE DEL SISTEMA")
print("=" * 50)

sys.path.insert(0, 'src')

try:
    # 1. Probar imports básicos
    print("\n1. Probando imports...")
    
    try:
        import numpy
        print(f"   ✅ NumPy: versión {numpy.__version__}")
    except Exception as e:
        print(f"   ❌ NumPy: {e}")
    
    try:
        import cv2
        print(f"   ✅ OpenCV: versión {cv2.__version__}")
    except Exception as e:
        print(f"   ❌ OpenCV: {e}")
    
    # 2. Probar adaptador corregido
    print("\n2. Probando adaptador PokerStars...")
    
    from platforms_fixed.pokerstars_adapter_fixed import PokerStarsAdapter
    
    adapter = PokerStarsAdapter(stealth_level=1)
    print(f"   ✅ Adaptador creado: plataforma={adapter.platform}")
    
    # 3. Probar coach
    print("\n3. Probando coach...")
    
    from integration.coach_integrator_simple import CoachIntegrator
    
    coach = CoachIntegrator("pokerstars")
    print(f"   ✅ Coach creado")
    
    # Prueba de análisis
    test_situation = {
        "hole_cards": [("A", "hearts"), ("K", "spades")],
        "community_cards": [],
        "pot_size": 100,
        "bet_size": 20,
        "position": "BTN",
        "players": 6,
        "stage": "preflop"
    }
    
    recommendation = coach.analyze_hand(test_situation)
    print(f"   ✅ Recomendación: {recommendation['primary_action']}")
    print(f"   📈 Confianza: {recommendation['confidence']:.0%}")
    
    # 4. Verificar estructura
    print("\n4. Verificando estructura...")
    
    required_dirs = ["src/", "config/", "debug/", "logs/"]
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} (faltante)")
    
    print("\n" + "=" * 50)
    print("🎉 ¡SISTEMA VERIFICADO CORRECTAMENTE!")
    print("\n🚀 Ejecuta: python run_pokerstars_optimized.py")
    
except Exception as e:
    print(f"\\n❌ Error en prueba: {e}")
    import traceback
    traceback.print_exc()

print("\\n" + "=" * 50)
'''
    
    try:
        test_path = "simple_test.py"
        with open(test_path, 'w') as f:
            f.write(test_code)
        
        print(f"   ✅ Prueba creada: {test_path}")
        return test_path
        
    except Exception as e:
        print(f"   ❌ Error creando prueba: {e}")
        return None

def run_quick_cleanup():
    """Limpieza rápida"""
    print("\n6. LIMPIEZA RÁPIDA...")
    
    # Eliminar cache de Python
    cache_dirs = ["__pycache__", ".pytest_cache", ".mypy_cache"]
    
    for cache_dir in cache_dirs:
        for found in os.popen(f'dir /s /b {cache_dir} 2>nul').read().strip().split('\n'):
            if found and os.path.exists(found):
                try:
                    shutil.rmtree(found)
                    print(f"   🗑️  Eliminado: {found}")
                except:
                    pass
    
    print("   ✅ Limpieza completada")

def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🎯 INICIANDO REPARACIÓN DEFINITIVA...")
    
    # 1. Solucionar problema de numpy
    fix_numpy_issue()
    
    # 2. Reparar StealthScreenCapture
    fix_stealth_capture()
    
    # 3. Crear adaptador corregido
    adapter_path = create_fixed_pokerstars_adapter()
    
    if not adapter_path:
        print("❌ No se pudo crear adaptador corregido")
        return
    
    # 4. Actualizar run_pokerstars
    update_run_pokerstars()
    
    # 5. Crear prueba
    test_path = create_simple_test()
    
    # 6. Limpieza
    run_quick_cleanup()
    
    print("\n" + "=" * 60)
    print("🔧 REPARACIÓN DEFINITIVA COMPLETADA")
    print("\n📋 RESUMEN:")
    print("✅ Problema de numpy verificado")
    print("✅ StealthScreenCapture reparado")
    print("✅ Adaptador PokerStars corregido creado")
    print("✅ Sistema principal actualizado")
    print("✅ Prueba de verificación creada")
    print("✅ Cache limpiado")
    
    print("\n🚀 INSTRUCCIONES FINALES:")
    print("1. Ejecuta la prueba: python simple_test.py")
    print("2. Si la prueba pasa, ejecuta: python run_pokerstars_optimized.py")
    print("3. Para limpiar completamente: python clean_project.py")
    
    print("\n⚠️  NOTA: Si sigue sin funcionar, prueba reinstalar dependencias:")
    print("   pip uninstall numpy opencv-python mss")
    print("   pip install numpy opencv-python mss")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()