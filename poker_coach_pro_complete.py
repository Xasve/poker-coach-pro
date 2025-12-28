#!/usr/bin/env python3
"""
POKER COACH PRO - SISTEMA COMPLETO FUNCIONAL
Integra todos los módulos disponibles.
"""

import os
import sys
import json
import time
import traceback
from pathlib import Path

# Configurar paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

class PokerCoachProComplete:
    """Sistema completo de Poker Coach Pro."""
    
    def __init__(self):
        self.modules = {}
        self.config = self.load_config()
        self.initialize_system()
    
    def load_config(self):
        """Carga la configuración del sistema."""
        config_path = project_root / "config" / "system_config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuración por defecto
        return {
            "pokerstars": {
                "table_position": {"x": 100, "y": 100, "width": 800, "height": 600},
                "calibrated": False
            },
            "ocr": {
                "tesseract_path": None,
                "confidence_threshold": 0.8
            },
            "gto": {
                "ranges_path": "data/gto_ranges",
                "aggression_level": "medium"
            }
        }
    
    def save_config(self):
        """Guarda la configuración."""
        config_path = project_root / "config" / "system_config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✅ Configuración guardada en: {config_path}")
    
    def initialize_system(self):
        """Inicializa todos los módulos del sistema."""
        print("🔧 INICIALIZANDO SISTEMA COMPLETO")
        print("=" * 60)
        
        # 1. Verificador del sistema
        print("\n1. 📋 Verificando sistema...")
        try:
            from utils.system_checker import check_system, SystemChecker
            check_system()
            self.modules['system_checker'] = SystemChecker()
            print("   ✅ Verificador del sistema listo")
        except Exception as e:
            print(f"   ⚠️  Verificador: {str(e)[:50]}...")
        
        # 2. Selector de ventanas
        print("\n2. 🪟 Cargando selector de ventanas...")
        try:
            from utils.window_selector import WindowSelector
            self.modules['window_selector'] = WindowSelector()
            print("   ✅ Selector de ventanas listo")
        except Exception as e:
            print(f"   ⚠️  Selector: {str(e)[:50]}...")
        
        # 3. Reconocedor de cartas (OCR)
        print("\n3. 🎴 Cargando reconocedor de cartas...")
        try:
            from core.card_recognizer import CardRecognizer
            self.modules['card_recognizer'] = CardRecognizer()
            print("   ✅ Reconocedor de cartas listo")
        except Exception as e:
            print(f"   ❌ Reconocedor: {str(e)[:50]}...")
            print("   ℹ️  Este módulo requiere pytesseract instalado")
        
        # 4. Calibrador PokerStars
        print("\n4. ⚙️  Cargando calibrador PokerStars...")
        try:
            from integration.pokerstars_calibrator import PokerStarsCalibrator
            self.modules['pokerstars_calibrator'] = PokerStarsCalibrator()
            print("   ✅ Calibrador PokerStars listo")
        except Exception as e:
            print(f"   ⚠️  Calibrador: {str(e)[:50]}...")
        
        # 5. Sistema de aprendizaje GTO
        print("\n5. 🧠 Cargando sistema de aprendizaje GTO...")
        try:
            from core.learning_system import PokerCoachProCompleteSystem
            self.modules['learning_system'] = PokerCoachProCompleteSystem()
            print("   ✅ Sistema de aprendizaje GTO listo")
        except Exception as e:
            print(f"   ⚠️  Sistema GTO: {str(e)[:50]}...")
        
        # 6. Asistente PokerStars
        print("\n6. 🤖 Cargando asistente PokerStars...")
        try:
            from integration.pokerstars_assistant import PokerStarsAssistant
            self.modules['pokerstars_assistant'] = PokerStarsAssistant()
            print("   ✅ Asistente PokerStars listo")
        except Exception as e:
            print(f"   ⚠️  Asistente: {str(e)[:50]}...")
        
        print("\n" + "=" * 60)
        print(f"✅ SISTEMA INICIALIZADO: {len(self.modules)}/6 módulos cargados")
    
    def run_system_check(self):
        """Ejecuta verificación completa del sistema."""
        print("\n🩺 VERIFICACIÓN COMPLETA DEL SISTEMA")
        print("=" * 60)
        
        checks = [
            ("Entorno Python", self._check_python),
            ("Dependencias críticas", self._check_dependencies),
            ("Estructura de carpetas", self._check_folder_structure),
            ("Archivos de configuración", self._check_config_files),
            ("Módulos funcionales", self._check_functional_modules),
        ]
        
        all_ok = True
        for check_name, check_func in checks:
            try:
                status, message = check_func()
                icon = "✅" if status else "❌"
                print(f"{icon} {check_name}: {message}")
                if not status:
                    all_ok = False
            except Exception as e:
                print(f"❌ {check_name}: Error - {e}")
                all_ok = False
        
        print("\n" + "=" * 60)
        if all_ok:
            print("🎉 ¡SISTEMA LISTO PARA USO!")
        else:
            print("⚠️  Algunos componentes necesitan atención")
        
        return all_ok
    
    def _check_python(self):
        import platform
        version = platform.python_version()
        return True, f"Python {version}"
    
    def _check_dependencies(self):
        critical_deps = ["cv2", "numpy", "pyautogui", "PIL"]
        missing = []
        
        for dep in critical_deps:
            try:
                if dep == "cv2":
                    import cv2
                elif dep == "PIL":
                    from PIL import Image
                else:
                    __import__(dep)
            except ImportError:
                missing.append(dep)
        
        if missing:
            return False, f"Faltan: {', '.join(missing)}"
        return True, "Todas instaladas"
    
    def _check_folder_structure(self):
        required_folders = [
            "src/core",
            "src/integration", 
            "src/utils",
            "config",
            "data/card_templates",
            "logs"
        ]
        
        missing = []
        for folder in required_folders:
            if not (project_root / folder).exists():
                missing.append(folder)
        
        if missing:
            return False, f"Faltan: {', '.join(missing[:3])}"
        return True, "Completa"
    
    def _check_config_files(self):
        config_files = ["config/system_config.json"]
        missing = []
        
        for file in config_files:
            if not (project_root / file).exists():
                missing.append(file)
        
        if missing:
            return False, "Archivos de configuración faltantes"
        return True, "Configurados"
    
    def _check_functional_modules(self):
        loaded = len(self.modules)
        total = 6  # Número total de módulos que intentamos cargar
        return loaded >= 3, f"{loaded}/{total} módulos funcionales"
    
    def calibrate_pokerstars(self):
        """Ejecuta calibración de PokerStars."""
        print("\n🎯 CALIBRACIÓN POKERSTARS")
        print("=" * 60)
        
        if 'pokerstars_calibrator' not in self.modules:
            print("❌ Módulo de calibración no disponible")
            return False
        
        print("Este proceso calibrará las posiciones de la mesa de PokerStars.")
        print("Necesitas:")
        print("1. PokerStars abierto en una mesa")
        print("2. La mesa visible en pantalla")
        print("3. Seguir las instrucciones paso a paso")
        print()
        
        confirm = input("¿Continuar con la calibración? (s/n): ").lower()
        if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
            print("Calibración cancelada.")
            return False
        
        try:
            calibrator = self.modules['pokerstars_calibrator']
            
            if hasattr(calibrator, 'run_interactive_calibration'):
                calibrator.run_interactive_calibration()
            elif hasattr(calibrator, 'calibrate_table'):
                calibrator.calibrate_table()
            else:
                print("⚠️  Método de calibración no encontrado")
                return False
            
            self.config['pokerstars']['calibrated'] = True
            self.save_config()
            return True
            
        except Exception as e:
            print(f"❌ Error durante la calibración: {e}")
            traceback.print_exc()
            return False
    
    def test_card_recognition(self):
        """Prueba el reconocimiento de cartas."""
        print("\n🃏 PRUEBA DE RECONOCIMIENTO DE CARTAS")
        print("=" * 60)
        
        if 'card_recognizer' not in self.modules:
            print("❌ Módulo de reconocimiento no disponible")
            print("ℹ️  Instala pytesseract: https://github.com/UB-Mannheim/tesseract/wiki")
            return False
        
        print("Opciones de prueba:")
        print("1. Usar imagen de prueba (si existe)")
        print("2. Capturar pantalla actual")
        print("3. Probar con imagen personalizada")
        print()
        
        choice = input("Selecciona opción (1-3): ").strip()
        
        try:
            recognizer = self.modules['card_recognizer']
            
            if choice == "1":
                # Buscar imagen de prueba
                test_images = list((project_root / "data" / "card_templates").glob("*.png"))
                if test_images:
                    test_image = test_images[0]
                    print(f"🔍 Analizando: {test_image.name}")
                    
                    if hasattr(recognizer, 'recognize_from_file'):
                        result = recognizer.recognize_from_file(str(test_image))
                    elif hasattr(recognizer, 'process_image'):
                        import cv2
                        img = cv2.imread(str(test_image))
                        result = recognizer.process_image(img)
                    else:
                        print("⚠️  Método de reconocimiento no encontrado")
                        return False
                    
                    print(f"✅ Resultado: {result}")
                    return True
                else:
                    print("❌ No hay imágenes de prueba en data/card_templates/")
                    return False
            
            elif choice == "2":
                print("📸 Capturando pantalla...")
                
                if 'window_selector' in self.modules:
                    selector = self.modules['window_selector']
                    if hasattr(selector, 'capture_region_interactive'):
                        region = selector.capture_region_interactive("test_capture")
                        if region:
                            print("✅ Región capturada")
                            return True
                
                print("⚠️  Usando captura completa de pantalla...")
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save("test_screenshot.png")
                print("✅ Captura guardada como test_screenshot.png")
                return True
            
            else:
                print("ℹ️  Coloca una imagen en la raíz del proyecto y ejecuta de nuevo.")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
            return False
    
    def practice_gto_decisions(self):
        """Modo práctica de decisiones GTO."""
        print("\n🧠 MODO PRÁCTICA - DECISIONES GTO")
        print("=" * 60)
        
        print("Este modo te permite practicar decisiones basadas en GTO.")
        print()
        print("Ejemplo de situación:")
        print("  Posición: BU (Button)")
        print("  Mano: A♠ K♠")
        print("  Acción: MP raise 3bb, folds to you")
        print()
        print("¿Qué harías?")
        print("1. Fold")
        print("2. Call")
        print("3. 3-bet to 9bb")
        print("4. All-in")
        print()
        
        choice = input("Tu decisión (1-4): ").strip()
        
        # Respuestas GTO simplificadas
        gto_answers = {
            "1": "❌ Fold - Mala decisión con AKo desde BU",
            "2": "⚠️  Call - Aceptable pero no óptimo",
            "3": "✅ 3-bet - Decisión GTO óptima",
            "4": "❌ All-in - Demasiado agresivo"
        }
        
        result = gto_answers.get(choice, "❌ Opción inválida")
        print(f"\n📊 Análisis GTO: {result}")
        
        if 'learning_system' in self.modules:
            print("\n🔍 Análisis detallado disponible en sistema de aprendizaje")
        
        return True
    
    def realtime_assistant_mode(self):
        """Modo asistente en tiempo real."""
        print("\n🤖 ASISTENTE EN TIEMPO REAL")
        print("=" * 60)
        
        if 'pokerstars_assistant' not in self.modules:
            print("❌ Módulo de asistente no disponible")
            return False
        
        print("⚠️  MODO AVANZADO - REQUIERE CONFIGURACIÓN COMPLETA")
        print()
        print("Prerrequisitos:")
        print("1. PokerStars abierto y calibrado")
        print("2. Mesa de poker visible")
        print("3. Reconocimiento de cartas funcional")
        print("4. Sistema GTO configurado")
        print()
        
        confirm = input("¿Tienes todo configurado? (s/n): ").lower()
        if confirm not in ['s', 'si', 'sí']:
            print("Modo cancelado. Configura primero el sistema.")
            return False
        
        print("\n🚀 Iniciando asistente...")
        print("Presiona Ctrl+C para detener.")
        
        try:
            assistant = self.modules['pokerstars_assistant']
            
            if hasattr(assistant, 'run'):
                assistant.run()
            elif hasattr(assistant, 'start_monitoring'):
                assistant.start_monitoring()
            else:
                print("⚠️  Método de ejecución no encontrado")
                return False
            
            return True
            
        except KeyboardInterrupt:
            print("\n⏹️  Asistente detenido por el usuario.")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
            return False
    
    def show_main_menu(self):
        """Muestra el menú principal del sistema completo."""
        while True:
            print("\n" + "=" * 60)
            print("🎯 POKER COACH PRO - SISTEMA COMPLETO")
            print("=" * 60)
            print("1. 🩺 Verificación completa del sistema")
            print("2. ⚙️  Calibrar PokerStars")
            print("3. 🃏 Probar reconocimiento de cartas")
            print("4. 🧠 Modo práctica (decisiones GTO)")
            print("5. 🤖 Asistente en tiempo real (Beta)")
            print("6. 📊 Estado de módulos")
            print("7. 💾 Guardar configuración")
            print("0. 🚪 Salir")
            print("=" * 60)
            
            try:
                choice = input("\nSelecciona opción (0-7): ").strip()
                
                if choice == "1":
                    self.run_system_check()
                elif choice == "2":
                    self.calibrate_pokerstars()
                elif choice == "3":
                    self.test_card_recognition()
                elif choice == "4":
                    self.practice_gto_decisions()
                elif choice == "5":
                    self.realtime_assistant_mode()
                elif choice == "6":
                    self.show_module_status()
                elif choice == "7":
                    self.save_config()
                elif choice == "0":
                    print("\n👋 ¡Gracias por usar Poker Coach Pro!")
                    print("   ¡Buena suerte en las mesas! 🍀")
                    break
                else:
                    print("❌ Opción inválida. Usa 0-7.")
            
            except KeyboardInterrupt:
                print("\n\n⚠️  Operación cancelada.")
            except Exception as e:
                print(f"\n❌ Error: {e}")
            
            input("\nPresiona Enter para continuar...")
    
    def show_module_status(self):
        """Muestra el estado de todos los módulos."""
        print("\n📊 ESTADO DE MÓDULOS")
        print("=" * 60)
        
        module_info = [
            ("system_checker", "✅", "Verificador del sistema"),
            ("window_selector", "✅", "Selector de ventanas"),
            ("card_recognizer", "⚠️", "Reconocimiento de cartas (requiere pytesseract)"),
            ("pokerstars_calibrator", "✅", "Calibrador PokerStars"),
            ("learning_system", "✅", "Sistema de aprendizaje GTO"),
            ("pokerstars_assistant", "✅", "Asistente PokerStars"),
        ]
        
        for module_name, status, description in module_info:
            if module_name in self.modules:
                print(f"{status} {description}: CARGADO")
            else:
                print(f"❌ {description}: NO DISPONIBLE")
        
        print(f"\n📈 Total: {len(self.modules)}/6 módulos funcionales")

def main():
    """Función principal."""
    print("=" * 60)
    print("POKER COACH PRO - SISTEMA COMPLETO FUNCIONAL")
    print("=" * 60)
    
    try:
        coach = PokerCoachProComplete()
        coach.show_main_menu()
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        print("\n💡 Soluciones rápidas:")
        print("1. Ejecuta como Administrador")
        print("2. Verifica que Python 3.11 esté instalado")
        print("3. Ejecuta: pip install -r requirements.txt")
        traceback.print_exc()

if __name__ == "__main__":
    main()