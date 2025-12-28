# continue_development.py - Script para continuar desarrollo
import os
import sys
import json
from datetime import datetime

def show_development_menu():
    """Mostrar menú de desarrollo"""
    print("🎴 CONTINUACIÓN DE DESARROLLO - POKER COACH PRO")
    print("=" * 60)
    
    # Analizar estado actual
    print("\n🔍 ESTADO ACTUAL DEL PROYECTO:")
    
    # Verificar archivos clave
    key_files = [
        ("color_optimizer.py", "Optimizador de color"),
        ("detect_coords.py", "Configurador PokerStars"),
        ("smart_capture_fixed_v2.py", "Captura de dataset"),
        ("ocr_enhancer.py", "Mejorador OCR"),
        ("poker_coach_pro.py", "Sistema principal")
    ]
    
    for file_name, description in key_files:
        if os.path.exists(file_name):
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}")
    
    # Verificar dataset
    dataset_path = "data/templates/cards"
    if os.path.exists(dataset_path):
        images = [f for f in os.listdir(dataset_path) if f.endswith(('.png', '.jpg'))]
        print(f"   📊 Dataset: {len(images)} imágenes")
    else:
        print(f"   📊 Dataset: No existe")
    
    print("\n🚀 OPCIONES DE CONTINUACIÓN:")
    print("1. 🎨 Ejecutar optimizador de color")
    print("2. ⚙️  Configurar PokerStars (detectar coordenadas)")
    print("3. 📸 Capturar dataset de cartas")
    print("4. 🔍 Mejorar OCR con data augmentation")
    print("5. 🎮 Probar sistema completo")
    print("6.  Ejecutar pruebas automáticas")
    print("7. 📊 Ver estadísticas del proyecto")
    print("8.  Salir")
    print("=" * 60)

def run_option(choice):
    """Ejecutar opción seleccionada"""
    scripts = {
        "1": "color_optimizer.py",
        "2": "detect_coords.py",
        "3": "smart_capture_fixed_v2.py",
        "4": "ocr_enhancer.py",
        "5": "poker_coach_pro.py",
        "6": "final_tests.py"
    }
    
    if choice in scripts:
        script = scripts[choice]
        if os.path.exists(script):
            print(f"\n🚀 Ejecutando: {script}")
            os.system(f"python {script}")
        else:
            print(f" Script no encontrado: {script}")
    elif choice == "7":
        show_project_stats()
    elif choice == "8":
        print("\n Hasta luego!")
        sys.exit(0)
    else:
        print(" Opción no válida")

def show_project_stats():
    """Mostrar estadísticas del proyecto"""
    print("\n ESTADÍSTICAS DEL PROYECTO:")
    print("-" * 40)
    
    # Contar archivos Python
    py_files = [f for f in os.listdir(".") if f.endswith(".py")]
    print(f" Archivos Python: {len(py_files)}")
    
    # Tamaño del proyecto
    total_size = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.startswith(".") and not root.startswith(".\\venv"):
                try:
                    total_size += os.path.getsize(os.path.join(root, file))
                except:
                    pass
    
    print(f" Tamaño total: {total_size/1024/1024:.2f} MB")
    
    # Verificar logs
    if os.path.exists("logs"):
        log_files = [f for f in os.listdir("logs") if f.endswith(".log")]
        print(f" Archivos de log: {len(log_files)}")
    
    # Última modificación
    if py_files:
        latest_file = max(py_files, key=lambda f: os.path.getmtime(f))
        mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
        print(f" Última modificación: {mod_time.strftime('%Y-%m-%d %H:%M')}")

def main():
    """Función principal"""
    while True:
        try:
            show_development_menu()
            choice = input("\n Selecciona opción (1-8): ").strip()
            run_option(choice)
            
            input("\n Presiona Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n  Interrumpido")
            break
        except Exception as e:
            print(f" Error: {e}")

if __name__ == "__main__":
    main()
