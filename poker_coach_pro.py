# poker_coach_pro.py - Actualizado para estructura correcta
import os
import sys
import argparse

# Añadir src al path
sys.path.insert(0, "src")

class PokerCoachPro:
    """Sistema principal unificado - Versión corregida"""
    
    def __init__(self):
        self.version = "4.0"
        self.project_name = "Poker Coach Pro"
        
        print(f" {self.project_name} v{self.version}")
        print("=" * 70)
        print(" Sistema organizado y optimizado")
        print("=" * 70)
        
        # Verificar estructura
        self.check_structure()
    
    def check_structure(self):
        """Verificar estructura básica"""
        print("\n VERIFICANDO ESTRUCTURA...")
        
        required_files = [
            ("src/core/main_system.py", "Módulo principal"),
            ("config/system_config.yaml", "Configuración"),
            ("requirements.txt", "Dependencias")
        ]
        
        for file_path, description in required_files:
            if os.path.exists(file_path):
                print(f"    {description}")
            else:
                print(f"   ❌ {description} - FALTANTE")
    
    def show_menu(self):
        """Mostrar menú principal"""
        print("\n🎮 MENÚ PRINCIPAL:")
        print("=" * 50)
        print("1.  Sistema Principal - Análisis en tiempo real")
        print("2.  Optimizar - Calibración y configuración")
        print("3.  Herramientas - Utilidades del sistema")
        print("4.  Pruebas - Verificación y testing")
        print("5.  Documentación - Guías y ayuda")
        print("6.   Configuración - Ajustes del sistema")
        print("7.  Salir")
        print("=" * 50)
    
    def run_main_system(self):
        """Ejecutar sistema principal de análisis - CORREGIDO"""
        try:
            # Importar desde la ubicación correcta
            from core.main_system import PokerCoachProV2
            
            print("\n CARGANDO SISTEMA PRINCIPAL...")
            system = PokerCoachProV2()
            system.interactive_mode_v2()
            
        except ImportError as e:
            print(f"\n Error cargando sistema principal: {e}")
            print("\n SOLUCIÓN RÁPIDA:")
            print("1. Verifica que src/core/main_system.py existe")
            print("2. Ejecuta este comando para probar:")
            print('   python -c "import sys; sys.path.insert(0, \"src\"); from core.main_system import PokerCoachProV2; print(\" Importación exitosa\")"')
    
    def run_optimization(self):
        """Ejecutar herramientas de optimización"""
        print("\n HERRAMIENTAS DE OPTIMIZACIÓN:")
        print("=" * 50)
        
        # Buscar archivos de optimización
        optimization_files = [
            "color_optimizer.py",
            "ocr_enhancer.py",
            "smart_capture_fixed_v2.py",
            "detect_coords.py"
        ]
        
        found_tools = []
        for i, tool in enumerate(optimization_files, 1):
            if os.path.exists(tool):
                found_tools.append((i, tool))
                print(f"{i}.   {tool}")
        
        print(f"{len(found_tools)+1}.   Volver al menú principal")
        
        if not found_tools:
            print("\n  No se encontraron herramientas de optimización")
            return
        
        try:
            choice = input("\n Selecciona opción: ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(found_tools):
                tool_index = choice_num - 1
                script_name = found_tools[tool_index][1]
                self.run_script(script_name)
            elif choice_num == len(found_tools) + 1:
                return
            else:
                print(" Opción no válida")
        except ValueError:
            print(" Ingresa un número válido")
    
    def run_tools(self):
        """Ejecutar herramientas del sistema"""
        print("\n HERRAMIENTAS DEL SISTEMA:")
        print("=" * 50)
        
        # Buscar herramientas comunes
        tool_files = [
            "verify_balance.py",
            "diagnostic.py", 
            "session_manager.py",
            "pokerstars_assistant.py"
        ]
        
        found_tools = []
        for i, tool in enumerate(tool_files, 1):
            if os.path.exists(tool):
                found_tools.append((i, tool))
                
                # Nombres amigables
                friendly_names = {
                    "verify_balance.py": " Verificador de balance",
                    "diagnostic.py": " Diagnóstico del sistema",
                    "session_manager.py": " Gestor de sesiones",
                    "pokerstars_assistant.py": " Asistente PokerStars"
                }
                
                name = friendly_names.get(tool, tool)
                print(f"{i}. {name}")
        
        print(f"{len(found_tools)+1}.   Volver al menú principal")
        
        if not found_tools:
            print("\n  No se encontraron herramientas")
            return
        
        try:
            choice = input("\n Selecciona opción: ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(found_tools):
                tool_index = choice_num - 1
                script_name = found_tools[tool_index][1]
                self.run_script(script_name)
            elif choice_num == len(found_tools) + 1:
                return
            else:
                print(" Opción no válida")
        except ValueError:
            print(" Ingresa un número válido")
    
    def run_script(self, script_name):
        """Ejecutar un script específico"""
        if os.path.exists(script_name):
            print(f"\n Ejecutando: {script_name}")
            os.system(f"python {script_name}")
        else:
            print(f" Script no encontrado: {script_name}")
    
    def run_tests(self):
        """Ejecutar pruebas del sistema"""
        print("\n PRUEBAS DEL SISTEMA:")
        print("=" * 50)
        
        test_files = [
            "final_tests.py",
            "quick_test.py",
            "startup_check.py"
        ]
        
        found_tests = []
        for i, test in enumerate(test_files, 1):
            if os.path.exists(test):
                found_tests.append((i, test))
                
                friendly_names = {
                    "final_tests.py": " Pruebas completas",
                    "quick_test.py": " Pruebas rápidas", 
                    "startup_check.py": " Verificación inicial"
                }
                
                name = friendly_names.get(test, test)
                print(f"{i}. {name}")
        
        print(f"{len(found_tests)+1}.   Volver al menú principal")
        
        if not found_tests:
            print("\n  No se encontraron pruebas")
            return
        
        try:
            choice = input("\n Selecciona opción: ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(found_tests):
                test_index = choice_num - 1
                script_name = found_tests[test_index][1]
                self.run_script(script_name)
            elif choice_num == len(found_tests) + 1:
                return
            else:
                print(" Opción no válida")
        except ValueError:
            print(" Ingresa un número válido")
    
    def show_documentation(self):
        """Mostrar documentación"""
        print("\n DOCUMENTACIÓN:")
        print("=" * 50)
        
        doc_files = [
            "README.md",
            "POKERSTARS_GUIDE.txt",
            "SOLUCIÓN_DEFINITIVA.txt"
        ]
        
        print("\n Documentación disponible:")
        for doc in doc_files:
            if os.path.exists(doc):
                print(f"    {doc}")
            else:
                print(f"    {doc} (no encontrado)")
        
        print("\n Directorio docs/:")
        if os.path.exists("docs"):
            $docs = Get-ChildItem "docs" -File | Select-Object -ExpandProperty Name
            foreach ($doc in $docs) {
                print(f"    docs/{$doc}")
            }
        
        input("\n Presiona Enter para continuar...")
    
    def show_configuration(self):
        """Mostrar configuración del sistema"""
        print("\n  CONFIGURACIÓN DEL SISTEMA:")
        print("=" * 50)
        
        print("\n ESTRUCTURA ACTUAL:")
        
        $dirs = @("src", "data", "config", "logs", "docs", "tests")
        foreach ($dir in $dirs) {
            if (Test-Path $dir) {
                $itemCount = (Get-ChildItem $dir -Recurse -File | Measure-Object).Count
                Write-Host "    $dir ($itemCount archivos)"
            } else {
                Write-Host "    $dir (no existe)"
            }
        }
        
        print("\n  ARCHIVOS DE CONFIGURACIÓN:")
        $configFiles = @("config/system_config.yaml", "requirements.txt")
        foreach ($file in $configFiles) {
            if (Test-Path $file) {
                Write-Host "    $file"
            } else {
                Write-Host "    $file (no encontrado)"
            }
        }
        
        input("\n Presiona Enter para continuar...")
    
    def interactive_mode(self):
        """Modo interactivo principal"""
        while True:
            try:
                self.show_menu()
                choice = input("\n Selecciona opción (1-7): ").strip()
                
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
                    print("\n Hasta luego! ")
                    break
                else:
                    print(" Opción no válida")
            
            except KeyboardInterrupt:
                print("\n\n  Interrumpido por usuario")
                break
            except Exception as e:
                print(f" Error: {e}")
    
    def cli_mode(self, args):
        """Modo línea de comandos"""
        if args.mode == "main":
            self.run_main_system()
        elif args.mode == "optimize":
            self.run_optimization()
        elif args.mode == "test":
            self.run_tests()
        elif args.mode == "tools":
            self.run_tools()
        elif args.mode == "config":
            self.show_configuration()

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Poker Coach Pro - Sistema organizado")
    parser.add_argument("--mode", choices=["main", "optimize", "test", "tools", "config", "interactive"],
                       default="interactive", help="Modo de ejecución")
    parser.add_argument("--version", action="store_true", help="Mostrar versión")
    
    args = parser.parse_args()
    
    # Crear instancia
    poker_coach = PokerCoachPro()
    
    if args.version:
        print(f" Poker Coach Pro v{poker_coach.version}")
        return
    
    if args.mode == "interactive":
        poker_coach.interactive_mode()
    else:
        poker_coach.cli_mode(args)

if __name__ == "__main__":
    main()
