#!/usr/bin/env python3
"""
POKER COACH PRO - SISTEMA ADAPTATIVO
Descubre automáticamente las clases y funciones disponibles.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

# Configurar paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

class AdaptivePokerCoach:
    """Sistema que se adapta a lo que realmente tienes."""
    
    def __init__(self):
        self.discovered_modules = {}
        self.discover_available_code()
    
    def discover_available_code(self):
        """Descubre automáticamente qué código está disponible."""
        print("🔍 DESCUBRIENDO CÓDIGO DISPONIBLE")
        print("=" * 60)
        
        # Explorar todos los archivos .py en src/
        src_path = project_root / "src"
        
        for py_file in src_path.rglob("*.py"):
            if py_file.name.startswith("__") or "pycache" in str(py_file):
                continue
            
            # Convertir ruta a módulo Python
            rel_path = py_file.relative_to(src_path)
            module_path = str(rel_path).replace("\\", ".").replace("/", ".").replace(".py", "")
            
            self.analyze_module(module_path, py_file)
    
    def analyze_module(self, module_path, file_path):
        """Analiza un módulo específico."""
        try:
            module = importlib.import_module(module_path)
            module_info = {
                "module": module,
                "file": file_path,
                "classes": [],
                "functions": [],
                "importable": True
            }
            
            # Encontrar clases
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    module_info["classes"].append(name)
                elif inspect.isfunction(obj) and obj.__module__ == module.__name__:
                    module_info["functions"].append(name)
            
            if module_info["classes"] or module_info["functions"]:
                self.discovered_modules[module_path] = module_info
                print(f"\n✅ {module_path}")
                
                if module_info["classes"]:
                    print(f"   📦 Clases: {', '.join(module_info['classes'][:3])}")
                    if len(module_info["classes"]) > 3:
                        print(f"   ... y {len(module_info['classes']) - 3} más")
                
                if module_info["functions"]:
                    print(f"   🔧 Funciones: {', '.join(module_info['functions'][:3])}")
                    if len(module_info["functions"]) > 3:
                        print(f"   ... y {len(module_info['functions']) - 3} más")
            
        except ImportError as e:
            print(f"\n❌ {module_path}: {str(e)[:50]}")
        except SyntaxError as e:
            print(f"\n❌ {module_path}: ERROR DE SINTAXIS - {e}")
        except Exception as e:
            print(f"\n⚠️  {module_path}: {str(e)[:50]}...")
    
    def create_dynamic_system(self):
        """Crea un sistema dinámico basado en lo descubierto."""
        print("\n" + "=" * 60)
        print("🧩 CREANDO SISTEMA DINÁMICO")
        print("=" * 60)
        
        system_components = {}
        
        # Mapear módulos descubiertos a funcionalidades
        for module_path, info in self.discovered_modules.items():
            if not info["classes"]:
                continue
            
            # Intentar determinar qué tipo de módulo es
            module_type = self.determine_module_type(module_path, info["classes"])
            
            if module_type:
                # Intentar crear instancia de la primera clase
                try:
                    first_class = info["classes"][0]
                    class_obj = getattr(info["module"], first_class)
                    instance = class_obj()
                    
                    system_components[module_type] = {
                        "instance": instance,
                        "class_name": first_class,
                        "module": module_path
                    }
                    
                    print(f"✅ {module_type}: {first_class}")
                    
                except Exception as e:
                    system_components[module_type] = {
                        "module": info["module"],
                        "error": str(e),
                        "type": "module_only"
                    }
                    print(f"⚠️  {module_type}: No se pudo instanciar ({str(e)[:30]}...)")
        
        return system_components
    
    def determine_module_type(self, module_path, classes):
        """Determina el tipo de módulo basado en su nombre y clases."""
        module_lower = module_path.lower()
        
        # Patrones para identificar tipos de módulos
        if any(x in module_lower for x in ["card", "ocr", "recogn"]):
            return "card_recognizer"
        elif any(x in module_lower for x in ["learn", "gto", "system"]):
            return "learning_system"
        elif any(x in module_lower for x in ["calibrat", "pokerstar"]):
            return "pokerstars_calibrator"
        elif any(x in module_lower for x in ["assist", "helper"]):
            return "pokerstars_assistant"
        elif any(x in module_lower for x in ["window", "select"]):
            return "window_selector"
        elif any(x in module_lower for x in ["check", "system"]):
            return "system_checker"
        elif any(x in module_lower for x in ["util", "helper"]):
            return "utility"
        
        return None
    
    def run_adaptive_menu(self, system_components):
        """Ejecuta menú adaptativo basado en componentes disponibles."""
        while True:
            print("\n" + "=" * 60)
            print("🎯 POKER COACH PRO - SISTEMA ADAPTATIVO")
            print("=" * 60)
            
            # Mostrar opciones basadas en lo disponible
            options = []
            
            if "system_checker" in system_components:
                options.append(("1", "🩺 Verificar sistema", self.check_system))
            
            if "window_selector" in system_components:
                options.append(("2", "🪟 Probar selector de ventanas", self.test_window_selector))
            
            if "card_recognizer" in system_components:
                options.append(("3", "🎴 Probar reconocimiento de cartas", self.test_card_recognition))
            
            if "pokerstars_calibrator" in system_components:
                options.append(("4", "⚙️ Calibrar PokerStars", self.calibrate_pokerstars))
            
            if "learning_system" in system_components:
                options.append(("5", "🧠 Modo práctica GTO", self.practice_gto))
            
            options.append(("6", "📊 Mostrar componentes disponibles", self.show_components))
            options.append(("0", "🚪 Salir", None))
            
            # Mostrar menú
            for key, label, _ in options:
                print(f"{key}. {label}")
            
            print("=" * 60)
            
            choice = input("\nSelección: ").strip()
            
            if choice == "0":
                print("\n👋 ¡Hasta luego!")
                break
            
            # Ejecutar función correspondiente
            for key, label, func in options:
                if choice == key and func:
                    func(system_components)
                    break
            else:
                print("❌ Opción inválida")
            
            input("\nPresiona Enter para continuar...")
    
    def check_system(self, components):
        """Verificación básica del sistema."""
        print("\n🩺 VERIFICACIÓN DEL SISTEMA")
        print("-" * 40)
        print(f"✅ Componentes cargados: {len(components)}")
        print(f"✅ Python: {sys.version.split()[0]}")
        print(f"✅ Directorio: {project_root}")
        
        # Verificar dependencias básicas
        basic_deps = ["cv2", "numpy", "pyautogui"]
        for dep in basic_deps:
            try:
                __import__(dep)
                print(f"✅ {dep}")
            except ImportError:
                print(f"❌ {dep}")
    
    def test_window_selector(self, components):
        """Prueba el selector de ventanas."""
        print("\n🪟 PRUEBA SELECTOR DE VENTANAS")
        print("-" * 40)
        
        if "window_selector" in components:
            comp = components["window_selector"]
            if "instance" in comp:
                instance = comp["instance"]
                print(f"Instancia: {comp['class_name']}")
                
                # Verificar métodos disponibles
                methods = [m for m in dir(instance) if not m.startswith("_") and callable(getattr(instance, m))]
                print(f"Métodos: {', '.join(methods[:5])}")
            else:
                print("Módulo disponible pero no instanciable")
        else:
            print("Componente no disponible")
    
    def test_card_recognition(self, components):
        """Prueba reconocimiento de cartas."""
        print("\n🎴 PRUEBA RECONOCIMIENTO DE CARTAS")
        print("-" * 40)
        
        if "card_recognizer" in components:
            print("Componente disponible")
            # Aquí iría la lógica de prueba
        else:
            print("ℹ️  Para reconocimiento de cartas necesitas:")
            print("1. Tesseract OCR instalado")
            print("2. Archivo card_recognizer.py funcional")
    
    def calibrate_pokerstars(self, components):
        """Calibra PokerStars."""
        print("\n⚙️ CALIBRACIÓN POKERSTARS")
        print("-" * 40)
        
        if "pokerstars_calibrator" in components:
            print("Componente disponible")
        else:
            print("ℹ️  Para calibrar PokerStars:")
            print("1. Necesitas pokerstars_calibrator.py")
            print("2. Sin errores de sintaxis")
    
    def practice_gto(self, components):
        """Modo práctica GTO."""
        print("\n🧠 MODO PRÁCTICA GTO")
        print("-" * 40)
        
        if "learning_system" in components:
            comp = components["learning_system"]
            print(f"✅ Sistema GTO disponible: {comp.get('class_name', 'Módulo')}")
            
            # Ejemplo de práctica
            print("\n📊 Ejercicio: Hero en BU con A♠ K♠")
            print("Acción: MP raise 3bb, folds to hero")
            print("\nDecisiones GTO recomendadas:")
            print("• 3-bet (70% de las veces)")
            print("• Call (25% de las veces)")
            print("• Fold (5% de las veces)")
        else:
            print("Sistema GTO no disponible")
            print("\n💡 Decisiones básicas:")
            print("AKs desde BU vs MP raise: 3-bet o call")
    
    def show_components(self, components):
        """Muestra componentes disponibles."""
        print("\n📊 COMPONENTES DISPONIBLES")
        print("-" * 40)
        
        for name, info in components.items():
            if "instance" in info:
                print(f"✅ {name}: {info['class_name']} (instanciado)")
            else:
                print(f"⚠️  {name}: módulo disponible")

def main():
    """Función principal."""
    print("=" * 60)
    print("POKER COACH PRO - SISTEMA ADAPTATIVO")
    print("=" * 60)
    
    coach = AdaptivePokerCoach()
    
    if not coach.discovered_modules:
        print("\n❌ NO SE ENCONTRÓ CÓDIGO FUNCIONAL")
        print("\n💡 Soluciones:")
        print("1. Ejecuta el comando de diagnóstico primero")
        print("2. Revisa que los archivos en src/ tengan código válido")
        print("3. Corrige errores de sintaxis")
        return
    
    print(f"\n📈 Módulos descubiertos: {len(coach.discovered_modules)}")
    
    system_components = coach.create_dynamic_system()
    
    if system_components:
        coach.run_adaptive_menu(system_components)
    else:
        print("\n❌ No se pudieron crear componentes del sistema")

if __name__ == "__main__":
    main()