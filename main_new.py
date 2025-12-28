#!/usr/bin/env python3
"""
POKER COACH PRO - Sistema Principal Mejorado
Usa la estructura existente en src/
"""

import os
import sys
import importlib
from pathlib import Path

# Configurar path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def explore_structure():
    """Explora y muestra la estructura real del proyecto."""
    print("🔍 EXPLORANDO ESTRUCTURA DEL PROYECTO")
    print("=" * 60)
    
    src_path = project_root / "src"
    if not src_path.exists():
        print("❌ ERROR: No se encuentra la carpeta src/")
        return {}
    
    structure = {}
    
    # Recorrer todas las carpetas en src/
    for item in src_path.iterdir():
        if item.is_dir():
            module_name = item.name
            py_files = list(item.rglob("*.py"))
            
            if py_files:
                structure[module_name] = {
                    "path": str(item.relative_to(src_path)),
                    "files": len(py_files),
                    "sample": [f.name for f in py_files[:3]]
                }
    
    # Mostrar estructura
    print(f"📁 Estructura encontrada en src/:")
    print("-" * 60)
    
    for module, info in sorted(structure.items()):
        print(f"  📂 {module}/")
        print(f"     ├── Archivos: {info['files']}")
        print(f"     ├── Muestra: {', '.join(info['sample'])}")
        if len(info['sample']) < info['files']:
            print(f"     └── ... y {info['files'] - len(info['sample'])} más")
        print()
    
    return structure

def load_key_modules():
    """Intenta cargar los módulos clave del sistema."""
    print("\n🔧 CARGANDO MÓDULOS CLAVE")
    print("-" * 60)
    
    modules_to_load = [
        # Módulos principales (de core/)
        ("core.card_recognizer", "Reconocimiento de cartas"),
        ("core.learning_system", "Sistema de aprendizaje"),
        
        # Integración
        ("integration.pokerstars_calibrator", "Calibrador PokerStars"),
        ("integration.pokerstars_assistant", "Asistente PokerStars"),
        
        # Utilidades
        ("utils.system_checker", "Verificador de sistema"),
        ("utils.window_selector", "Selector de ventanas"),
    ]
    
    loaded_modules = {}
    failed_modules = []
    
    for module_path, description in modules_to_load:
        try:
            module = importlib.import_module(module_path)
            
            # Intentar encontrar clases principales
            classes = []
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and not attr_name.startswith("_"):
                    classes.append(attr_name)
            
            loaded_modules[module_path] = {
                "module": module,
                "classes": classes[:3],  # Primeras 3 clases
                "description": description
            }
            
            print(f"  ✅ {module_path}")
            if classes:
                print(f"     └── Clases: {', '.join(classes[:3])}")
            
        except ImportError as e:
            print(f"  ❌ {module_path}: {e}")
            failed_modules.append((module_path, str(e)))
        except Exception as e:
            print(f"  ⚠️  {module_path}: Error inesperado - {e}")
            failed_modules.append((module_path, str(e)))
    
    return loaded_modules, failed_modules

def create_unified_system(loaded_modules):
    """Crea un sistema unificado usando los módulos cargados."""
    print("\n🧩 CREANDO SISTEMA UNIFICADO")
    print("-" * 60)
    
    class PokerCoachPro:
        """Sistema principal unificado de Poker Coach Pro."""
        
        def __init__(self):
            self.modules = {}
            self.initialize_modules()
        
        def initialize_modules(self):
            """Inicializa todos los módulos disponibles."""
            print("  Inicializando módulos...")
            
            # Intentar inicializar cada módulo
            for module_path, info in loaded_modules.items():
                module_name = module_path.split(".")[-1]
                
                try:
                    # Crear instancia de la primera clase encontrada
                    if info["classes"]:
                        main_class_name = info["classes"][0]
                        main_class = getattr(info["module"], main_class_name)
                        
                        # Intentar crear instancia
                        instance = main_class()
                        self.modules[module_name] = instance
                        
                        print(f"    ✅ {module_name}: {main_class_name}")
                    else:
                        # Si no hay clases, guardar el módulo directamente
                        self.modules[module_name] = info["module"]
                        print(f"    📦 {module_name}: (módulo)")
                        
                except Exception as e:
                    print(f"    ⚠️  {module_name}: No se pudo instanciar - {e}")
                    self.modules[module_name] = info["module"]
        
        def get_module(self, name):
            """Obtiene un módulo por nombre."""
            return self.modules.get(name)
        
        def list_modules(self):
            """Lista todos los módulos disponibles."""
            print("\n  📋 MÓDULOS DISPONIBLES:")
            for name, instance in self.modules.items():
                module_type = type(instance).__name__
                print(f"    • {name:20} ({module_type})")
        
        def run_diagnostic(self):
            """Ejecuta diagnóstico del sistema."""
            print("\n  🩺 DIAGNÓSTICO DEL SISTEMA:")
            print("  " + "-" * 40)
            
            # Verificar componentes críticos
            critical_components = [
                ("card_recognizer", "Reconocimiento de cartas"),
                ("pokerstars_calibrator", "Calibración PokerStars"),
                ("system_checker", "Verificación de sistema"),
            ]
            
            for comp_name, description in critical_components:
                if comp_name in self.modules:
                    print(f"    ✅ {description}")
                else:
                    print(f"    ❌ {description} (FALTANTE)")
            
            print(f"\n  📊 Total módulos cargados: {len(self.modules)}")
    
    system = PokerCoachPro()
    return system

def display_main_menu():
    """Muestra el menú principal mejorado."""
    print("\n" + "=" * 60)
    print("🎯 POKER COACH PRO - MENÚ PRINCIPAL")
    print("=" * 60)
    print("1. 🔍 Explorar estructura del proyecto")
    print("2. 🧪 Probar módulos individuales")
    print("3. 🃏 Probar reconocimiento de cartas")
    print("4. ⚙️  Calibrar sistema PokerStars")
    print("5. 📊 Ejecutar diagnóstico completo")
    print("6. 🚀 Iniciar modo asistente (Beta)")
    print("7. 📁 Mostrar archivos del proyecto")
    print("0. 🚪 Salir")
    print("=" * 60)
    
    try:
        choice = input("\nSelecciona una opción (0-7): ").strip()
        return choice
    except (KeyboardInterrupt, EOFError):
        return "0"

def main():
    """Función principal."""
    print("=" * 60)
    print("POKER COACH PRO - Sistema Reestructurado")
    print("=" * 60)
    
    # 1. Explorar estructura
    structure = explore_structure()
    
    if not structure:
        print("❌ No se pudo cargar la estructura. Saliendo...")
        return
    
    # 2. Cargar módulos clave
    loaded_modules, failed = load_key_modules()
    
    if not loaded_modules:
        print("❌ No se pudieron cargar módulos críticos.")
        print("   Errores encontrados:")
        for module_path, error in failed:
            print(f"   • {module_path}: {error}")
        return
    
    # 3. Crear sistema unificado
    system = create_unified_system(loaded_modules)
    
    # 4. Menú interactivo
    while True:
        choice = display_main_menu()
        
        if choice == "1":
            explore_structure()
        
        elif choice == "2":
            system.list_modules()
            
            # Preguntar qué módulo probar
            module_name = input("\n  Nombre del módulo a probar (o Enter para cancelar): ").strip()
            if module_name and module_name in system.modules:
                module = system.modules[module_name]
                print(f"\n  Probando módulo: {module_name}")
                print(f"  Tipo: {type(module).__name__}")
                print(f"  Métodos disponibles:")
                
                # Mostrar métodos públicos
                methods = [m for m in dir(module) if not m.startswith("_") and callable(getattr(module, m))]
                for method in methods[:10]:  # Primeros 10 métodos
                    print(f"    • {method}()")
                if len(methods) > 10:
                    print(f"    ... y {len(methods) - 10} más")
        
        elif choice == "3":
            print("\n🃏 PROBANDO RECONOCIMIENTO DE CARTAS")
            print("-" * 40)
            
            if "card_recognizer" in system.modules:
                try:
                    # Intentar usar el reconocedor
                    recognizer = system.modules["card_recognizer"]
                    print("  ✅ Módulo cargado")
                    
                    # Verificar si tiene métodos útiles
                    if hasattr(recognizer, "recognize_cards"):
                        print("  🔍 Método 'recognize_cards' disponible")
                    if hasattr(recognizer, "process_image"):
                        print("  🖼️  Método 'process_image' disponible")
                    
                    print("\n  ℹ️  Para pruebas reales, necesitas:")
                    print("    1. Una captura de pantalla de una mesa")
                    print("    2. Configurar las coordenadas")
                    print("    3. Plantillas de cartas en data/card_templates/")
                    
                except Exception as e:
                    print(f"  ❌ Error: {e}")
            else:
                print("  ❌ Módulo 'card_recognizer' no disponible")
        
        elif choice == "4":
            print("\n⚙️  CALIBRACIÓN POKERSTARS")
            print("-" * 40)
            
            if "pokerstars_calibrator" in system.modules:
                print("  ✅ Módulo de calibración disponible")
                print("\n  📝 Instrucciones:")
                print("    1. Abre PokerStars en una mesa")
                print("    2. Ejecuta el calibrador")
                print("    3. Sigue las instrucciones en pantalla")
                print("    4. Guarda la configuración")
                
                run_cal = input("\n  ¿Ejecutar calibrador ahora? (s/n): ").lower()
                if run_cal in ['s', 'si', 'sí']:
                    print("  🚧 Funcionalidad en desarrollo...")
            else:
                print("  ❌ Módulo 'pokerstars_calibrator' no disponible")
        
        elif choice == "5":
            print("\n📊 DIAGNÓSTICO COMPLETO")
            print("-" * 40)
            system.run_diagnostic()
            
            # Verificar carpetas importantes
            print("\n  📁 VERIFICACIÓN DE CARPETAS:")
            important_dirs = ["data/card_templates", "config", "logs", "src/core", "src/integration"]
            for dir_path in important_dirs:
                full_path = project_root / dir_path
                if full_path.exists():
                    print(f"    ✅ {dir_path}")
                else:
                    print(f"    ❌ {dir_path} (FALTANTE)")
        
        elif choice == "6":
            print("\n🚀 MODO ASISTENTE (Beta)")
            print("-" * 40)
            print("  ⚠️  Esta funcionalidad está en desarrollo.")
            print("  Se requiere:")
            print("  • PokerStars abierto y visible")
            print("  • Mesa de poker activa")
            print("  • Calibración previa completada")
            print("\n  🎯 Objetivo: Analizar manos en tiempo real")
            print("  y sugerir decisiones basadas en GTO")
        
        elif choice == "7":
            print("\n📁 ARCHIVOS DEL PROYECTO")
            print("-" * 40)
            
            # Mostrar archivos principales
            root_files = list(project_root.glob("*.py"))
            print(f"  📄 Archivos en raíz ({len(root_files)}):")
            for file in root_files[:10]:
                size_kb = file.stat().st_size / 1024
                print(f"    • {file.name} ({size_kb:.1f} KB)")
            if len(root_files) > 10:
                print(f"    ... y {len(root_files) - 10} más")
        
        elif choice == "0":
            print("\n🚪 Saliendo de Poker Coach Pro.")
            print("   ¡Buena suerte en las mesas! 🍀")
            break
        
        else:
            print("\n❌ Opción inválida. Por favor, selecciona 0-7.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido.")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()