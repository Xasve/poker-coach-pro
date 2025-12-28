#!/usr/bin/env python3
"""
POKER COACH PRO - SISTEMA MÍNIMO VIABLE
Versión simplificada para integración rápida.
"""

import sys
import os
from pathlib import Path

# Configurar paths
sys.path.insert(0, str(Path(__file__).parent / "src"))

class PokerCoachSimple:
    """Sistema mínimo de Poker Coach."""
    
    def __init__(self):
        self.modules = {}
        self.load_available_modules()
    
    def load_available_modules(self):
        """Carga solo los módulos que funcionan."""
        print("🔧 CARGANDO MÓDULOS DISPONIBLES")
        print("-" * 40)
        
        # Intentar cargar en este orden
        modules_to_try = [
            ("utils.system_checker", "Verificador"),
            ("integration.pokerstars_assistant", "Asistente"),
            ("utils.window_selector", "Selector"),
        ]
        
        for module_path, name in modules_to_try:
            try:
                module = __import__(module_path)
                self.modules[name] = module
                print(f"✅ {name}")
            except Exception as e:
                print(f"❌ {name}: {str(e)[:50]}...")
    
    def show_menu(self):
        """Menú simple y claro."""
        while True:
            print("\n" + "=" * 50)
            print("🎯 POKER COACH PRO - MENÚ SIMPLIFICADO")
            print("=" * 50)
            print("1. Verificar sistema")
            print("2. Probar selector de ventana")
            print("3. Iniciar modo práctica")
            print("4. Explorar módulos disponibles")
            print("0. Salir")
            print("=" * 50)
            
            choice = input("\nOpción: ").strip()
            
            if choice == "1":
                self.check_system()
            elif choice == "2":
                self.test_window_selector()
            elif choice == "3":
                self.practice_mode()
            elif choice == "4":
                self.explore_modules()
            elif choice == "0":
                print("\n¡Hasta luego! 🍀")
                break
    
    def check_system(self):
        """Verifica el estado del sistema."""
        print("\n🩺 VERIFICACIÓN DEL SISTEMA")
        print("-" * 40)
        
        checks = [
            ("Python 3.11", self._check_python),
            ("Dependencias instaladas", self._check_deps),
            ("Estructura de carpetas", self._check_folders),
            ("Módulos cargados", self._check_modules),
        ]
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                print(f"✅ {check_name}: {result}")
            except Exception as e:
                print(f"❌ {check_name}: Error - {e}")
    
    def _check_python(self):
        import platform
        return platform.python_version()
    
    def _check_deps(self):
        try:
            import cv2, numpy, pyautogui, PIL
            return "OK"
        except ImportError as e:
            return f"Falta: {e.name}"
    
    def _check_folders(self):
        folders = ["src", "data", "config"]
        missing = [f for f in folders if not os.path.exists(f)]
        return "OK" if not missing else f"Faltan: {missing}"
    
    def _check_modules(self):
        return f"{len(self.modules)} módulos"
    
    def test_window_selector(self):
        """Prueba el selector de ventanas."""
        print("\n🪟 SELECTOR DE VENTANAS")
        print("-" * 40)
        
        if "Selector" in self.modules:
            try:
                # Verificar si tiene clase WindowSelector
                module = self.modules["Selector"]
                if hasattr(module, "WindowSelector"):
                    print("✅ Clase WindowSelector disponible")
                    print("ℹ️  Para usar: from utils.window_selector import WindowSelector")
                else:
                    print("⚠️  No se encontró clase WindowSelector")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ Módulo no disponible")
    
    def practice_mode(self):
        """Modo práctica sin PokerStars."""
        print("\n🧪 MODO PRÁCTICA")
        print("-" * 40)
        print("Funcionalidades disponibles:")
        print("1. Analizar decisiones GTO (próximamente)")
        print("2. Estudiar rangos (próximamente)")
        print("3. Simular situaciones (próximamente)")
        print("\n⚠️  En desarrollo...")
    
    def explore_modules(self):
        """Explora qué módulos hay disponibles."""
        print("\n📁 EXPLORAR MÓDULOS")
        print("-" * 40)
        
        src_path = Path("src")
        for item in src_path.rglob("*.py"):
            if item.is_file() and not item.name.startswith("__"):
                rel_path = item.relative_to(src_path)
                print(f"• {rel_path}")

def main():
    """Función principal."""
    print("=" * 60)
    print("POKER COACH PRO - SISTEMA MÍNIMO")
    print("=" * 60)
    
    coach = PokerCoachSimple()
    coach.show_menu()

if __name__ == "__main__":
    main()