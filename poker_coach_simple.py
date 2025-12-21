# poker_coach_simple.py - Sistema principal simplificado
import os
import sys
import subprocess
from pathlib import Path

class PokerCoachSimple:
    """Sistema simplificado para empezar"""
    
    def __init__(self):
        print(" POKER COACH PRO - SISTEMA SIMPLIFICADO")
        print("=" * 60)
        self.check_environment()
    
    def check_environment(self):
        """Verificar entorno"""
        print("\n🔍 VERIFICANDO ENTORNO...")
        
        checks = [
            ("Python", self.check_python),
            ("OpenCV", self.check_opencv),
            ("PyAutoGUI", self.check_pyautogui),
            ("Estructura", self.check_structure)
        ]
        
        all_ok = True
        for name, check_func in checks:
            try:
                result, message = check_func()
                status = "" if result else ""
                print(f"   {status} {name}: {message}")
                if not result:
                    all_ok = False
            except Exception as e:
                print(f"   ❌ {name}: Error - {e}")
                all_ok = False
        
        return all_ok
    
    def check_python(self):
        """Verificar Python"""
        import platform
        return True, f"Python {platform.python_version()}"
    
    def check_opencv(self):
        """Verificar OpenCV"""
        try:
            import cv2
            return True, f"OpenCV {cv2.__version__}"
        except ImportError:
            return False, "No instalado. Ejecuta: pip install opencv-python"
    
    def check_pyautogui(self):
        """Verificar PyAutoGUI"""
        try:
            import pyautogui
            return True, "Instalado"
        except ImportError:
            return False, "No instalado"
    
    def check_structure(self):
        """Verificar estructura"""
        required = ["src/", "data/", "config/", "logs/"]
        missing = []
        
        for dir_path in required:
            if not os.path.exists(dir_path):
                missing.append(dir_path)
        
        if missing:
            return False, f"Faltan: {', '.join(missing)}"
        return True, "OK"
    
    def show_menu(self):
        """Mostrar menú principal"""
        print("\n MENÚ PRINCIPAL:")
        print("=" * 50)
        print("1.  Optimizar detección de color")
        print("2.  Capturar dataset de cartas")
        print("3.   Configurar PokerStars")
        print("4.  Probar captura de pantalla")
        print("5.  Ejecutar diagnóstico")
        print("6.  Salir")
        print("=" * 50)
    
    def run_color_optimizer(self):
        """Ejecutar optimizador de color"""
        print("\n EJECUTANDO OPTIMIZADOR DE COLOR...")
        
        if os.path.exists("color_optimizer.py"):
            os.system("python color_optimizer.py")
        else:
            print("❌ color_optimizer.py no encontrado")
            print("💡 Buscando en legacy_duplicates/...")
            
            legacy_path = "legacy_duplicates/color_optimizer.py"
            if os.path.exists(legacy_path):
                os.system(f"python {legacy_path}")
            else:
                print("  No se encontró en ningún lugar")
    
    def run_capture(self):
        """Ejecutar captura"""
        print("\n EJECUTANDO CAPTURA...")
        
        capture_scripts = [
            "smart_capture_fixed_v2.py",
            "smart_capture_fixed.py",
            "quick_capture.py",
            "legacy_duplicates/smart_capture_fixed_v2.py"
        ]
        
        for script in capture_scripts:
            if os.path.exists(script):
                print(f"   Ejecutando: {script}")
                os.system(f"python {script}")
                return
        
        print(" No se encontró ningún script de captura")
    
    def run_pokerstars_config(self):
        """Configurar PokerStars"""
        print("\n  CONFIGURANDO POKERSTARS...")
        
        if os.path.exists("detect_coords.py"):
            os.system("python detect_coords.py")
        else:
            print(" detect_coords.py no encontrado")
    
    def test_capture(self):
        """Probar captura básica"""
        print("\n🔍 PROBANDO CAPTURA BÁSICA...")
        
        test_code = '''
import pyautogui
from PIL import Image
import os

print(" Tomando captura de pantalla...")
try:
    screenshot = pyautogui.screenshot()
    print(f" Captura exitosa")
    print(f"   Tamaño: {screenshot.size}")
    print(f"   Modo: {screenshot.mode}")
    
    # Guardar prueba
    os.makedirs("logs/test", exist_ok=True)
    test_file = "logs/test/test_capture.png"
    screenshot.save(test_file)
    print(f" Guardado en: {test_file}")
    
    return True
except Exception as e:
    print(f" Error: {e}")
    return False
'''
        
        # Crear y ejecutar script temporal
        with open("test_capture_temp.py", "w") as f:
            f.write(test_code)
        
        os.system("python test_capture_temp.py")
        os.remove("test_capture_temp.py")
    
    def run_diagnostic(self):
        """Ejecutar diagnóstico"""
        print("\n EJECUTANDO DIAGNÓSTICO...")
        
        if os.path.exists("diagnostic.py"):
            os.system("python diagnostic.py")
        elif os.path.exists("check_system.py"):
            os.system("python check_system.py")
        else:
            print("❌ No se encontró script de diagnóstico")
            print("\n🔧 DIAGNÓSTICO MANUAL:")
            self.check_environment()
    
    def run(self):
        """Ejecutar sistema"""
        if not self.check_environment():
            print("\n  Hay problemas con el entorno")
            print(" Corrígelos antes de continuar")
        
        while True:
            try:
                self.show_menu()
                choice = input("\n👉 Selecciona opción (1-6): ").strip()
                
                if choice == "1":
                    self.run_color_optimizer()
                elif choice == "2":
                    self.run_capture()
                elif choice == "3":
                    self.run_pokerstars_config()
                elif choice == "4":
                    self.test_capture()
                elif choice == "5":
                    self.run_diagnostic()
                elif choice == "6":
                    print("\n👋 ¡Hasta luego!")
                    break
                else:
                    print("❌ Opción no válida")
            
            except KeyboardInterrupt:
                print("\n\n  Interrumpido")
                break
            except Exception as e:
                print(f" Error: {e}")

def main():
    """Función principal"""
    coach = PokerCoachSimple()
    coach.run()

if __name__ == "__main__":
    main()
