# poker_coach_pro.py - Sistema principal unificado y organizado
"""
🎴 POKER COACH PRO - SISTEMA PRINCIPAL UNIFICADO
Versión: 4.0 (Organizada y Limpia)
"""

import os
import sys
import argparse
from pathlib import Path

# Añadir src al path
sys.path.insert(0, "src")

class PokerCoachPro:
    """Sistema principal unificado de Poker Coach Pro"""
    
    def __init__(self):
        self.version = "4.0"
        self.project_name = "Poker Coach Pro"
        self.author = "Poker Coach Team"
        
        print(f"🎴 {self.project_name} v{self.version}")
        print("=" * 70)
        print("📦 Sistema organizado y optimizado")
        print("=" * 70)
    
    def show_menu(self):
        """Mostrar menú principal"""
        print("\n🎮 MENÚ PRINCIPAL:")
        print("=" * 50)
        print("1. 🎴 Sistema Principal - Análisis en tiempo real")
        print("2. 🎨 Optimizar - Calibración y configuración")
        print("3. 📊 Herramientas - Utilidades del sistema")
        print("4. 🧪 Pruebas - Verificación y testing")
        print("5. 📚 Documentación - Guías y ayuda")
        print("6. ⚙️  Configuración - Ajustes del sistema")
        print("7. 🚪 Salir")
        print("=" * 50)
    
    def run_main_system(self):
        """Ejecutar sistema principal de análisis"""
        try:
            from core.main_system import PokerCoachProV2
            system = PokerCoachProV2()
            system.interactive_mode_v2()
        except ImportError as e:
            print(f"❌ Error cargando sistema principal: {e}")
            print("💡 Ejecuta: python -m src.core.main_system")
    
    def run_optimization(self):
        """Ejecutar herramientas de optimización"""
        print("\n🔧 HERRAMIENTAS DE OPTIMIZACIÓN:")
        print("=" * 50)
        print("1. 🎨 Optimizador de color")
        print("2. 🔍 Mejorador OCR")
        print("3. 📸 Calibración de captura")
        print("4. ⚙️  Configuración PokerStars")
        print("5. ↩️  Volver al menú principal")
        
        choice = input("\n👉 Selecciona opción (1-5): ").strip()
        
        if choice == "1":
            self.run_color_optimizer()
        elif choice == "2":
            self.run_ocr_enhancer()
        elif choice == "3":
            self.run_capture_calibration()
        elif choice == "4":
            self.run_pokerstars_config()
        elif choice == "5":
            return
        else:
            print("❌ Opción no válida")
    
    def run_color_optimizer(self):
        """Ejecutar optimizador de color"""
        try:
            from analysis.color_optimizer import ColorOptimizer
            optimizer = ColorOptimizer()
            optimizer.interactive_calibration()
        except ImportError as e:
            print(f"❌ Error cargando optimizador: {e}")
            print("💡 Asegúrate de que src/analysis/color_optimizer.py existe")
    
    def run_ocr_enhancer(self):
        """Ejecutar mejorador OCR"""
        try:
            from analysis.ocr_enhancer import OCR_Enhancer
            enhancer = OCR_Enhancer()
            
            # Verificar si hay dataset
            dataset_path = "data/templates/cards"
            if not os.path.exists(dataset_path):
                print(f"❌ Dataset no encontrado: {dataset_path}")
                print("💡 Captura dataset primero con: python -m src.capture.smart_capture")
                return
            
            # Analizar dataset
            stats = enhancer.analyze_dataset(dataset_path)
            
            print(f"\n📊 Dataset actual: {stats['total_images']} imágenes")
            
            # Preguntar qué hacer
            print("\n🎯 OPCIONES OCR:")
            print("1. Analizar dataset actual")
            print("2. Balancear con data augmentation")
            print("3. Crear split entrenamiento/validación")
            
            choice = input("\n👉 Selecciona opción (1-3): ").strip()
            
            if choice == "1":
                print(f"\n📈 Distribución:")
                for suit, count in stats['by_suit'].items():
                    if count > 0:
                        percentage = stats['suit_distribution'].get(suit, 0)
                        print(f"   {suit:10} {count:4} imágenes ({percentage:5.1f}%)")
            
            elif choice == "2":
                target_path = "data/datasets/augmented"
                target_count = int(input("Objetivo por clase (default 50): ") or "50")
                enhancer.balance_dataset(dataset_path, target_path, target_count)
            
            elif choice == "3":
                enhancer.create_training_validation_split(dataset_path)
            
        except ImportError as e:
            print(f"❌ Error cargando mejorador OCR: {e}")
    
    def run_capture_calibration(self):
        """Ejecutar calibración de captura"""
        print("\n📸 CALIBRACIÓN DE CAPTURA")
        print("=" * 50)
        
        try:
            from capture.smart_capture import main as smart_capture_main
            print("Ejecutando captura inteligente...")
            smart_capture_main()
        except ImportError:
            print("💡 Ejecuta: python -m src.capture.smart_capture")
    
    def run_pokerstars_config(self):
        """Configurar PokerStars"""
        try:
            from utils.coordinates_detector import main as coords_main
            coords_main()
        except ImportError:
            print("💡 Ejecuta: python -m src.utils.coordinates_detector")
    
    def run_tools(self):
        """Ejecutar herramientas del sistema"""
        print("\n🔧 HERRAMIENTAS DEL SISTEMA:")
        print("=" * 50)
        print("1. 📊 Verificador de balance")
        print("2. 🩺 Diagnóstico del sistema")
        print("3. 📁 Gestor de sesiones")
        print("4. 🎯 Asistente PokerStars")
        print("5. ↩️  Volver al menú principal")
        
        choice = input("\n👉 Selecciona opción (1-5): ").strip()
        
        tool_mappings = {
            "1": ("utils.balance_checker", "main"),
            "2": ("utils.diagnostic", "main"),
            "3": ("utils.session_manager", "main"),
            "4": ("utils.pokerstars_assistant", "main")
        }
        
        if choice in tool_mappings:
            module_path, func_name = tool_mappings[choice]
            try:
                module = __import__(f"src.{module_path}", fromlist=[func_name])
                getattr(module, func_name)()
            except ImportError as e:
                print(f"❌ Error cargando herramienta: {e}")
        elif choice == "5":
            return
        else:
            print("❌ Opción no válida")
    
    def run_tests(self):
        """Ejecutar pruebas del sistema"""
        print("\n🧪 PRUEBAS DEL SISTEMA:")
        print("=" * 50)
        print("1. 🧪 Pruebas rápidas (unitarias)")
        print("2. 🔍 Pruebas de integración")
        print("3. ⚡ Pruebas de rendimiento")
        print("4. 📋 Verificación inicial")
        print("5. ↩️  Volver al menú principal")
        
        choice = input("\n👉 Selecciona opción (1-5): ").strip()
        
        test_mappings = {
            "1": ("tests.unit.quick_test", "run_quick_tests"),
            "2": ("tests.integration.final_tests", "run_comprehensive_tests"),
            "4": ("tests.integration.startup_check", "main")
        }
        
        if choice in test_mappings:
            module_path, func_name = test_mappings[choice]
            try:
                # Importar dinámicamente
                import importlib.util
                
                script_path = f"{module_path.replace('.', '/')}.py"
                if not os.path.exists(script_path):
                    print(f"❌ Archivo no encontrado: {script_path}")
                    return
                
                spec = importlib.util.spec_from_file_location(module_path, script_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, func_name):
                    getattr(module, func_name)()
                else:
                    module.main()  # Intentar llamar a main()
                    
            except Exception as e:
                print(f"❌ Error ejecutando pruebas: {e}")
                import traceback
                traceback.print_exc()
        
        elif choice == "3":
            print("🚧 Pruebas de rendimiento en desarrollo...")
        
        elif choice == "5":
            return
        
        else:
            print("❌ Opción no válida")
    
    def show_documentation(self):
        """Mostrar documentación"""
        print("\n📚 DOCUMENTACIÓN:")
        print("=" * 50)
        
        docs = {
            "Guía Principal": "docs/README.md",
            "Guía de Continuación": "docs/guides/CONTINUATION_GUIDE.md",
            "Guía Final": "docs/guides/FINAL_GUIDE.md"
        }
        
        print("\n📖 Documentación disponible:")
        for i, (title, path) in enumerate(docs.items(), 1):
            if os.path.exists(path):
                print(f"{i}. {title}")
            else:
                print(f"{i}. {title} (no disponible)")
        
        choice = input("\n👉 Selecciona documento (1-3) o Enter para volver: ").strip()
        
        if choice == "1" and os.path.exists(docs["Guía Principal"]):
            os.system(f"type {docs['Guía Principal']} | more")
        elif choice == "2" and os.path.exists(docs["Guía de Continuación"]):
            os.system(f"type {docs['Guía de Continuación']} | more")
        elif choice == "3" and os.path.exists(docs["Guía Final"]):
            os.system(f"type {docs['Guía Final']} | more")
    
    def show_configuration(self):
        """Mostrar configuración del sistema"""
        print("\n⚙️  CONFIGURACIÓN DEL SISTEMA:")
        print("=" * 50)
        
        config_path = "config/system_config.yaml"
        if os.path.exists(config_path):
            print("📄 Configuración actual:")
            with open(config_path, 'r') as f:
                content = f.readlines()[:20]  # Mostrar primeras 20 líneas
                for line in content:
                    print(f"   {line.rstrip()}")
            
            print("\n💡 Para editar configuración completa:")
            print(f"   Edita el archivo: {config_path}")
        else:
            print("❌ Archivo de configuración no encontrado")
            print("💡 Crea uno con: cp config/system_config.example.yaml config/system_config.yaml")
        
        input("\n👉 Presiona Enter para continuar...")
    
    def interactive_mode(self):
        """Modo interactivo principal"""
        while True:
            try:
                self.show_menu()
                choice = input("\n👉 Selecciona opción (1-7): ").strip()
                
                if choice == "1":
                    self.run_main_system()
                elif choice == "2":
                    self.run_optimization()
                elif choice == "3":
                    self.run_tools()
                elif choice == "4":
                    self.run_tests()
                elif choice == "5":
                    self.show_documentation()
                elif choice == "6":
                    self.show_configuration()
                elif choice == "7":
                    print("\n👋 ¡Hasta luego! 🎴")
                    break
                else:
                    print("❌ Opción no válida")
            
            except KeyboardInterrupt:
                print("\n\n⏹️  Interrumpido por usuario")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
    
    def cli_mode(self, args):
        """Modo línea de comandos"""
        if args.mode == "main":
            self.run_main_system()
        elif args.mode == "optimize":
            self.run_optimization()
        elif args.mode == "test":
            self.run_tests()
        elif args.mode == "capture":
            self.run_capture_calibration()
        elif args.mode == "config":
            self.show_configuration()

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Poker Coach Pro - Sistema organizado")
    parser.add_argument("--mode", choices=["main", "optimize", "test", "capture", "config", "interactive"],
                       default="interactive", help="Modo de ejecución")
    parser.add_argument("--version", action="store_true", help="Mostrar versión")
    
    args = parser.parse_args()
    
    # Crear instancia
    poker_coach = PokerCoachPro()
    
    if args.version:
        print(f"🎴 Poker Coach Pro v{poker_coach.version}")
        return
    
    if args.mode == "interactive":
        poker_coach.interactive_mode()
    else:
        poker_coach.cli_mode(args)

if __name__ == "__main__":
    main()
