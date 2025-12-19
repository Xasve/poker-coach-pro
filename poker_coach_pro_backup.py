#!/usr/bin/env python3
"""
POKER COACH PRO - LAUNCHER DEFINITIVO
Interfaz principal para acceder a todos los componentes del sistema
"""
import os
import sys
import subprocess
import time

def print_header():
    """Imprimir cabecera del programa"""
    print("=" * 60)
    print("🎴 POKER COACH PRO - SISTEMA DEFINITIVO")
    print("=" * 60)

def scan_project():
    """Escanear el proyecto para encontrar todos los scripts disponibles"""
    print("\n🔍 Escaneando proyecto...")
    
    scripts_by_category = {
        "🎯 SISTEMAS COMPLETOS": [],
        "🃏 POKERSTARS": [],
        "🎴 GG POKER": [],
        "🔧 PRUEBAS Y DIAGNOSTICO": [],
        "🛠️ HERRAMIENTAS": []
    }
    
    # Buscar todos los archivos .py
    for root, dirs, files in os.walk("."):
        # Ignorar carpetas especiales
        ignore_dirs = {'__pycache__', '.git', 'venv', '.idea'}
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ".")
                
                # Clasificar por nombre
                file_lower = file.lower()
                
                if any(x in file_lower for x in ['poker_coach', 'definitive', 'final', 'main']):
                    scripts_by_category["🎯 SISTEMAS COMPLETOS"].append(rel_path)
                elif 'pokerstars' in file_lower:
                    scripts_by_category["🃏 POKERSTARS"].append(rel_path)
                elif 'ggpoker' in file_lower or 'gg_' in file_lower:
                    scripts_by_category["🎴 GG POKER"].append(rel_path)
                elif file.startswith('test_'):
                    scripts_by_category["🔧 PRUEBAS Y DIAGNOSTICO"].append(rel_path)
                elif file in ['check.py', 'cleanup.py', 'setup_folders.py']:
                    scripts_by_category["🛠️ HERRAMIENTAS"].append(rel_path)
                elif root == '.' and not file.startswith('.'):
                    scripts_by_category["🛠️ HERRAMIENTAS"].append(rel_path)
    
    return scripts_by_category

def display_menu(scripts_by_category):
    """Mostrar menú con todas las opciones disponibles"""
    print_header()
    
    print("\n📁 COMPONENTES DISPONIBLES:")
    print("-" * 50)
    
    all_scripts = []
    option_number = 1
    
    # Mostrar scripts por categoría
    for category, scripts in scripts_by_category.items():
        if scripts:
            print(f"\n{category}:")
            for script in sorted(scripts):
                print(f"  [{option_number:2}] {script}")
                all_scripts.append(script)
                option_number += 1
    
    print(f"\n  [{option_number:2}] 🔄 Re-escanear proyecto")
    print(f"  [{option_number + 1:2}] 🚪 Salir")
    
    return all_scripts, option_number

def run_script(script_path):
    """Ejecutar un script específico"""
    if not os.path.exists(script_path):
        print(f"\n❌ ERROR: El archivo no existe: {script_path}")
        return False
    
    print(f"\n🚀 EJECUTANDO: {script_path}")
    print("═" * 60)
    
    try:
        # Cambiar al directorio del script si es necesario
        script_dir = os.path.dirname(script_path)
        original_dir = os.getcwd()
        
        if script_dir:
            os.chdir(script_dir)
            script_name = os.path.basename(script_path)
        else:
            script_name = script_path
        
        # Ejecutar el script
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Mostrar output en tiempo real
        print("\n📝 SALIDA DEL SCRIPT:\n")
        
        # Leer salida línea por línea
        for line in process.stdout:
            print(line.rstrip())
        
        # Esperar a que termine
        process.wait()
        
        # Volver al directorio original
        os.chdir(original_dir)
        
        if process.returncode == 0:
            print(f"\n✅ {script_path} - EJECUTADO EXITOSAMENTE")
        else:
            print(f"\n⚠️  {script_path} - FINALIZÓ CON CÓDIGO {process.returncode}")
            
        return True
        
    except FileNotFoundError:
        print(f"\n❌ ERROR: Python no encontrado o script no existe")
        return False
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        return False
    finally:
        print("\n" + "═" * 60)

def show_quick_guide():
    """Mostrar guía rápida de los scripts principales"""
    print("\n📋 GUÍA RÁPIDA DE SCRIPTS PRINCIPALES:")
    print("-" * 50)
    
    guides = {
        "test_pokerstars.py": "Sistema COMPLETO para PokerStars. Incluye captura, análisis GTO y overlay.",
        "test_ggpoker_simple.py": "Sistema para GG Poker con funcionalidad similar a PokerStars.",
        "src/integration/pokerstars_coach.py": "Integrador principal del sistema (más avanzado).",
        "test_capture.py": "Prueba básica de captura de pantalla.",
        "test_components.py": "Prueba individual de componentes del sistema.",
        "check.py": "Verificador completo del sistema.",
        "cleanup.py": "Limpia archivos duplicados y organiza el proyecto."
    }
    
    for script, description in guides.items():
        if os.path.exists(script):
            print(f"\n🎯 {script}:")
            print(f"   📖 {description}")
    
    print("\n💡 CONSEJO: Usa los números entre corchetes [] para seleccionar.")

def main():
    """Función principal"""
    print("Inicializando Poker Coach Pro...")
    time.sleep(0.5)
    
    # Primer escaneo
    scripts_by_category = scan_project()
    
    while True:
        try:
            # Mostrar menú
            all_scripts, last_option = display_menu(scripts_by_category)
            
            print("\n" + "=" * 60)
            print("🎮 MENÚ PRINCIPAL - Selecciona una opción")
            print("=" * 60)
            
            # Mostrar guía rápida si es la primera vez o si se solicita
            show_quick_guide()
            
            # Obtener selección del usuario
            try:
                selection = input(f"\n👉 Ingresa el número (1-{last_option + 1}) o 'q' para salir: ").strip().lower()
                
                if selection == 'q':
                    print("\n👋 ¡Hasta pronto!")
                    break
                
                if selection == '?':
                    show_quick_guide()
                    continue
                
                option_num = int(selection)
                
                if 1 <= option_num <= len(all_scripts):
                    # Ejecutar script seleccionado
                    script_to_run = all_scripts[option_num - 1]
                    run_script(script_to_run)
                    
                    # Preguntar si quiere volver al menú
                    print("\n¿Qué quieres hacer ahora?")
                    print("  1. Volver al menú principal")
                    print("  2. Ejecutar otro script")
                    print("  3. Salir")
                    
                    choice = input("\n👉 Selección (1-3): ").strip()
                    
                    if choice == '3':
                        print("\n👋 ¡Hasta pronto!")
                        break
                    elif choice == '2':
                        continue  # Volver a mostrar menú
                    # Si es 1, continuará automáticamente
                    
                elif option_num == len(all_scripts) + 1:  # Re-escanear
                    print("\n🔄 Re-escaneando proyecto...")
                    scripts_by_category = scan_project()
                    print("✅ Proyecto re-escaneado")
                    
                elif option_num == len(all_scripts) + 2:  # Salir
                    print("\n👋 ¡Hasta pronto!")
                    break
                else:
                    print(f"\n❌ Opción inválida. Por favor ingresa un número entre 1 y {last_option + 1}")
                    
            except ValueError:
                print("\n❌ Entrada inválida. Por favor ingresa un número.")
            except KeyboardInterrupt:
                print("\n\n🛑 Operación cancelada por el usuario")
                break
            
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {e}")
            import traceback
            traceback.print_exc()
            
            print("\n💡 Intentando recuperar...")
            time.sleep(2)

if __name__ == "__main__":
    main()