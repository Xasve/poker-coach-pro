# src/core/main_system.py - Sistema principal corregido
import os
import sys
import time
import json
from datetime import datetime

# Añadir el directorio padre al path para importar otros módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class PokerCoachProV2:
    """Versión corregida del sistema principal"""
    
    def __init__(self):
        self.version = "2.0"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.is_running = False
        
        print(f" POKER COACH PRO v{self.version}")
        print("=" * 70)
        print("Sistema principal - Modo de prueba")
        print("=" * 70)
    
    def check_dependencies(self):
        """Verificar dependencias disponibles"""
        print("\n VERIFICANDO DEPENDENCIAS...")
        
        dependencies = {
            "OpenCV (cv2)": self._try_import("cv2"),
            "PyAutoGUI": self._try_import("pyautogui"),
            "NumPy": self._try_import("numpy"),
            "Pillow (PIL)": self._try_import("PIL"),
            "scikit-learn": self._try_import("sklearn")
        }
        
        available = sum(dependencies.values())
        total = len(dependencies)
        
        print(f"\n Disponibles: {available}/{total}")
        
        if available >= 3:
            print(" Dependencias suficientes para funcionamiento básico")
            return True
        else:
            print("⚠️  Algunas dependencias faltan")
            print("💡 Ejecuta: pip install -r requirements.txt")
            return False
    
    def _try_import(self, module_name):
        """Intentar importar un módulo"""
        try:
            __import__(module_name)
            print(f"    {module_name}")
            return True
        except ImportError:
            print(f"   ❌ {module_name}")
            return False
    
    def simulate_analysis(self):
        """Simular análisis de mesa (para pruebas)"""
        print("\n SIMULANDO ANÁLISIS DE MESA...")
        
        # Manos de ejemplo para simulación
        sample_hands = [
            ("A", "K", "Mano premium - Subir fuerte"),
            ("Q", "Q", "Pareja media - Subir moderado"),
            ("J", "T", "Dibujos conectados - Pagar"),
            ("7", "2", "Mano débil - Retirarse")
        ]
        
        positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        
        for i in range(5):
            hand_idx = i % len(sample_hands)
            position_idx = i % len(positions)
            
            card1, card2, analysis = sample_hands[hand_idx]
            position = positions[position_idx]
            
            print(f"\n🔄 Iteración {i+1}:")
            print(f"   Posición: {position}")
            print(f"   Mano: {card1} {card2}")
            print(f"   Análisis: {analysis}")
            
            # Decisión basada en posición y mano
            if "premium" in analysis:
                action = "RAISE"
                confidence = 0.85
            elif "Pareja" in analysis:
                action = "RAISE" if position in ["CO", "BTN"] else "CALL"
                confidence = 0.7
            elif "Dibujos" in analysis:
                action = "CALL"
                confidence = 0.6
            else:
                action = "FOLD"
                confidence = 0.8
            
            print(f"    Decisión: {action} (Confianza: {confidence*100:.0f}%)")
            
            time.sleep(1)  # Pausa para simular procesamiento
        
        print("\n✅ Simulación completada")
    
    def capture_test(self):
        """Probar captura de pantalla básica"""
        print("\n PROBANDO CAPTURA DE PANTALLA...")
        
        try:
            import pyautogui
            
            print("   Tomando captura de pantalla...")
            screenshot = pyautogui.screenshot()
            
            print(f"    Captura exitosa")
            print(f"    Tamaño: {screenshot.size}")
            print(f"    Modo: {screenshot.mode}")
            
            # Guardar captura de prueba
            test_dir = "logs/test_captures"
            os.makedirs(test_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_file = os.path.join(test_dir, f"test_capture_{timestamp}.png")
            screenshot.save(test_file)
            
            print(f"    Guardado en: {test_file}")
            
            return True
            
        except Exception as e:
            print(f"    Error en captura: {e}")
            return False
    
    def interactive_mode_v2(self):
        """Modo interactivo mejorado"""
        print("\n" + "=" * 70)
        print("🎮 MODO INTERACTIVO - POKER COACH PRO")
        print("=" * 70)
        
        # Verificar dependencias primero
        if not self.check_dependencies():
            print("\n  No se pueden cargar todas las dependencias")
            print(" Usando modo de simulación...")
        
        self.is_running = True
        
        while self.is_running:
            try:
                print("\n🔧 OPCIONES DEL SISTEMA:")
                print("1. Simular análisis de mesa")
                print("2. Probar captura de pantalla")
                print("3. Verificar configuración")
                print("4. Ejecutar diagnóstico rápido")
                print("5. Volver al menú principal")
                
                choice = input("\n Selecciona opción (1-5): ").strip()
                
                if choice == "1":
                    self.simulate_analysis()
                    
                elif choice == "2":
                    self.capture_test()
                    
                elif choice == "3":
                    self.check_configuration()
                    
                elif choice == "4":
                    self.run_quick_diagnostic()
                    
                elif choice == "5":
                    print("\n👋 Regresando al menú principal...")
                    self.is_running = False
                    
                else:
                    print(" Opción no válida")
                    
            except KeyboardInterrupt:
                print("\n\n  Operación interrumpida")
                self.is_running = False
            except Exception as e:
                print(f" Error: {e}")
    
    def check_configuration(self):
        """Verificar configuración del sistema"""
        print("\n  VERIFICANDO CONFIGURACIÓN...")
        
        config_files = {
            "Configuración principal": "config/system_config.yaml",
            "Coordenadas PokerStars": "config/pokerstars_coords.json",
            "Perfiles de color": "config/color_profiles.json"
        }
        
        for name, path in config_files.items():
            if os.path.exists(path):
                print(f"   ✅ {name}: {path}")
            else:
                print(f"   ❌ {name}: NO ENCONTRADO")
        
        # Verificar directorios de datos
        data_dirs = [
            "data/templates/cards",
            "data/datasets",
            "logs/sessions"
        ]
        
        print("\n DIRECTORIOS DE DATOS:")
        for dir_path in data_dirs:
            if os.path.exists(dir_path):
                # Contar archivos si es relevante
                if "templates" in dir_path:
                    files = len([f for f in os.listdir(dir_path) if f.endswith(('.png', '.jpg'))])
                    print(f"    {dir_path} ({files} archivos)")
                else:
                    print(f"    {dir_path}")
            else:
                print(f"    {dir_path}: NO EXISTE")
    
    def run_quick_diagnostic(self):
        """Ejecutar diagnóstico rápido"""
        print("\n EJECUTANDO DIAGNÓSTICO RÁPIDO...")
        
        tests = [
            ("Python version", self._check_python),
            ("OpenCV import", self._check_opencv),
            ("Directorio de trabajo", self._check_working_dir),
            ("Permisos de escritura", self._check_write_permissions)
        ]
        
        for test_name, test_func in tests:
            try:
                result, message = test_func()
                status = "" if result else ""
                print(f"   {status} {test_name}: {message}")
            except Exception as e:
                print(f"    {test_name}: ERROR - {e}")
    
    def _check_python(self):
        """Verificar versión de Python"""
        import platform
        version = platform.python_version()
        return True, f"Python {version}"
    
    def _check_opencv(self):
        """Verificar OpenCV"""
        try:
            import cv2
            return True, f"OpenCV {cv2.__version__}"
        except ImportError:
            return False, "No instalado"
    
    def _check_working_dir(self):
        """Verificar directorio de trabajo"""
        cwd = os.getcwd()
        return True, cwd
    
    def _check_write_permissions(self):
        """Verificar permisos de escritura"""
        test_file = "test_permissions.tmp"
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return True, "OK"
        except:
            return False, "Sin permisos"

def main():
    """Función principal para ejecutar directamente"""
    system = PokerCoachProV2()
    system.interactive_mode_v2()

if __name__ == "__main__":
    main()
