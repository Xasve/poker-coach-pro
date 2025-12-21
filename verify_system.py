#  SCRIPT DE VERIFICACIÓN DEL SISTEMA

import os
import sys

def verify_system():
    """Verificar que todo el sistema está correctamente instalado"""
    
    print(" VERIFICANDO INSTALACIÓN DEL SISTEMA...")
    print("=" * 50)
    
    # Verificar archivos esenciales
    essential_files = [
        "complete_poker_learning_system.py",
        "quick_start.py",
        "color_calibration/",
        "rapid_learning_system/",
        "training_plans/"
    ]
    
    all_ok = True
    
    for file in essential_files:
        if os.path.exists(file):
            print(f" {file}")
        else:
            print(f" {file} - NO ENCONTRADO")
            all_ok = False
    
    # Verificar dependencias
    print("\n VERIFICANDO DEPENDENCIAS...")
    
    dependencies = [
        ("cv2", "opencv-python"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("yaml", "PyYAML"),
        ("pyautogui", "pyautogui")
    ]
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f" {package_name}")
        except ImportError:
            print(f" {package_name} - NO INSTALADO")
            all_ok = False
    
    # Verificar funcionalidad básica
    print("\n VERIFICANDO FUNCIONALIDAD...")
    
    try:
        # Intentar importar el sistema principal
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from complete_poker_learning_system import PokerCoachProCompleteSystem
        print(" Sistema principal importado correctamente")
        
        # Crear instancia
        system = PokerCoachProCompleteSystem()
        print(" Instancia del sistema creada")
        
    except Exception as e:
        print(f" Error importando sistema: {e}")
        all_ok = False
    
    # Resultado final
    print("\n" + "=" * 50)
    if all_ok:
        print(" SISTEMA VERIFICADO CORRECTAMENTE!")
        print(" Todo está listo para comenzar el aprendizaje acelerado")
        
        # Mostrar comandos
        print("\n COMANDOS PARA COMENZAR:")
        print("   python quick_start.py          # Inicio rápido con menú")
        print("   python complete_poker_learning_system.py  # Sistema completo")
        
    else:
        print("  HAY PROBLEMAS CON LA INSTALACIÓN")
        print(" Soluciones:")
        print("   1. Ejecuta: pip install opencv-python numpy pandas pyautogui PyYAML")
        print("   2. Asegúrate de que todos los archivos están en el mismo directorio")
        print("   3. Si hay errores de importación, reinicia PowerShell/CMD")
    
    return all_ok

if __name__ == "__main__":
    verify_system()
