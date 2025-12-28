#!/usr/bin/env python3
"""
POKER COACH PRO - SISTEMA FUNCIONAL
Versión corregida sin errores de sintaxis.
"""

import os
import sys
import json
from pathlib import Path

# Configurar paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

class PokerCoachWorking:
    """Sistema funcional que SÍ funciona."""
    
    def __init__(self):
        self.modules = {}
        self.config = self.load_config()
        self.setup_system()
    
    def load_config(self):
        """Carga la configuración."""
        config_path = project_root / "config" / "system_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"system": {"name": "Poker Coach Pro"}}
    
    def setup_system(self):
        """Configura los módulos que SÍ funcionan."""
        print("🔧 CONFIGURANDO SISTEMA")
        print("=" * 50)
        
        # 1. Sistema de aprendizaje GTO
        try:
            from core.learning_system import PokerCoachProCompleteSystem
            self.modules['gto_system'] = PokerCoachProCompleteSystem()
            print("✅ Sistema GTO: PokerCoachProCompleteSystem")
        except Exception as e:
            print(f"⚠️  Sistema GTO: {str(e)[:40]}")
        
        # 2. Selector de ventanas
        try:
            from utils.window_selector import WindowSelector
            self.modules['window_selector'] = WindowSelector()
            print("✅ Selector de ventanas: WindowSelector")
        except Exception as e:
            print(f"⚠️  Selector: {str(e)[:40]}")
        
        # 3. Verificador de sistema
        try:
            from utils import system_checker
            self.modules['checker'] = system_checker
            print("✅ Verificador de sistema")
        except Exception as e:
            print(f"⚠️  Verificador: {str(e)[:40]}")
        
        print(f"\n📊 Módulos cargados: {len(self.modules)}")
    
    def show_menu(self):
        """Menú principal funcional."""
        while True:
            print("\n" + "=" * 50)
            print("🎯 POKER COACH PRO - MENÚ PRINCIPAL")
            print("=" * 50)
            print("1. 🧠 Modo práctica GTO (decisiones)")
            print("2. 🪟 Probar selector de ventanas")
            print("3. 📋 Verificar sistema")
            print("4. ⚙️  Configurar")
            print("5. 📊 Información del sistema")
            print("0. 🚪 Salir")
            print("=" * 50)
            
            try:
                choice = input("\nOpción: ").strip()
                
                if choice == "1":
                    self.practice_gto()
                elif choice == "2":
                    self.test_window_selector()
                elif choice == "3":
                    self.check_system()
                elif choice == "4":
                    self.configure_system()
                elif choice == "5":
                    self.system_info()
                elif choice == "0":
                    print("\n👋 ¡Hasta luego! 🍀")
                    break
                else:
                    print("❌ Opción inválida")
            
            except KeyboardInterrupt:
                print("\n⚠️  Operación cancelada")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            if choice != "0":
                input("\nPresiona Enter para continuar...")
    
    def practice_gto(self):
        """Modo práctica de decisiones GTO."""
        print("\n🧠 MODO PRÁCTICA GTO")
        print("=" * 40)
        
        print("Ejercicio 1: Hero en BTN con A♠ K♠")
        print("Situación: MP raise 3bb, folds to hero")
        print("Stack: 100bb efectivos")
        print()
        
        print("Opciones:")
        print("1. Fold (0bb)")
        print("2. Call (3bb)")
        print("3. 3-bet to 9bb")
        print("4. 3-bet to 12bb")
        print("5. All-in (100bb)")
        print()
        
        user_choice = input("Tu decisión (1-5): ").strip()
        
        # Análisis GTO
        analysis = {
            "1": "❌ Fold - AKs es demasiado fuerte para fold desde BTN",
            "2": "⚠️  Call - Aceptable, pero 3-bet es mejor",
            "3": "✅  3-bet 9bb - Tamaño óptimo GTO",
            "4": "⚠️  3-bet 12bb - Demasiado grande para este spot",
            "5": "❌ All-in - Solo vs jugadores muy tight"
        }
        
        result = analysis.get(user_choice, "❌ Opción inválida")
        print(f"\n📊 Resultado: {result}")
        
        if 'gto_system' in self.modules:
            print("\n💡 Análisis avanzado disponible en el sistema GTO")
    
    def test_window_selector(self):
        """Prueba el selector de ventanas."""
        print("\n🪟 PRUEBA SELECTOR DE VENTANAS")
        print("=" * 40)
        
        if 'window_selector' in self.modules:
            print("✅ Selector disponible")
            print("Opciones:")
            print("1. Mostrar información")
            print("2. Probar captura básica")
            print("3. Volver al menú")
            
            choice = input("\nOpción: ").strip()
            
            if choice == "1":
                selector = self.modules['window_selector']
                methods = [m for m in dir(selector) if not m.startswith('_')]
                print(f"\nMétodos disponibles: {', '.join(methods[:8])}")
            
            elif choice == "2":
                print("\n🖱️  Para usar el selector:")
                print("1. Debe tener una ventana visible")
                print("2. Usa el método capture_region_interactive()")
                print("3. Sigue las instrucciones en pantalla")
        
        else:
            print("❌ Selector no disponible")
    
    def check_system(self):
        """Verifica el sistema."""
        print("\n📋 VERIFICACIÓN DEL SISTEMA")
        print("=" * 40)
        
        print(f"✅ Python: {sys.version.split()[0]}")
        print(f"✅ Directorio: {project_root}")
        print(f"✅ Módulos cargados: {len(self.modules)}")
        print(f"✅ Configuración: {'✅' if self.config else '❌'}")
        
        # Verificar carpetas importantes
        folders = ["src", "config", "data"]
        for folder in folders:
            path = project_root / folder
            status = "✅" if path.exists() else "❌"
            print(f"{status} {folder}/")
    
    def configure_system(self):
        """Configuración básica."""
        print("\n⚙️  CONFIGURACIÓN")
        print("=" * 40)
        
        print("Opciones:")
        print("1. Crear carpetas necesarias")
        print("2. Ver archivos disponibles")
        print("3. Probar imports de módulos")
        
        choice = input("\nOpción: ").strip()
        
        if choice == "1":
            folders = ["data/card_templates", "config", "logs", "exports"]
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
                print(f"✅ {folder}")
        
        elif choice == "2":
            print("\n📁 Archivos principales:")
            src_path = project_root / "src"
            if src_path.exists():
                for item in src_path.rglob("*.py"):
                    if not item.name.startswith("__") and "pycache" not in str(item):
                        rel_path = item.relative_to(src_path)
                        print(f"  • {rel_path}")
            else:
                print("❌ Carpeta src/ no encontrada")
        
        elif choice == "3":
            print("\n🔍 Probando imports...")
            modules_to_test = [
                "core.learning_system",
                "utils.window_selector",
                "utils.system_checker"
            ]
            
            for module in modules_to_test:
                try:
                    __import__(module)
                    print(f"✅ {module}")
                except Exception as e:
                    print(f"❌ {module}: {str(e)[:50]}")
    
    def system_info(self):
        """Información del sistema."""
        print("\n📊 INFORMACIÓN DEL SISTEMA")
        print("=" * 40)
        
        info = {
            "Proyecto": self.config.get('system', {}).get('name', 'Poker Coach Pro'),
            "Módulos cargados": len(self.modules),
            "Python": sys.version.split()[0],
            "Directorio": str(project_root),
            "Sistema GTO": "✅" if 'gto_system' in self.modules else "❌",
            "Selector": "✅" if 'window_selector' in self.modules else "❌",
            "Verificador": "✅" if 'checker' in self.modules else "❌"
        }
        
        for key, value in info.items():
            print(f"{key}: {value}")

def main():
    """Función principal."""
    print("=" * 60)
    print("🎯 POKER COACH PRO - SISTEMA FUNCIONAL")
    print("=" * 60)
    
    try:
        coach = PokerCoachWorking()
        coach.show_menu()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Soluciones rápidas:")
        print("1. Verifica que tengas Python 3.11")
        print("2. Ejecuta: pip install -r requirements.txt")
        print("3. Asegúrate de que src/ tenga los archivos correctos")

if __name__ == "__main__":
    main()