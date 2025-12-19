# start_auto_capture.py - Script de inicio unificado
import os
import sys

print(" POKER COACH PRO - CAPTURA AUTOMÁTICA")
print("=" * 60)

def check_dependencies():
    """Verificar dependencias necesarias"""
    try:
        import cv2
        import numpy as np
        import mss
        from sklearn.cluster import KMeans
        
        print(" Dependencias principales: OK")
        print(f"   OpenCV: {cv2.__version__}")
        print(f"   NumPy: {np.__version__}")
        
        return True
    except ImportError as e:
        print(f" Dependencia faltante: {e}")
        return False

def check_configuration():
    """Verificar configuración necesaria"""
    requirements = [
        ("config/pokerstars_coords.json", "Configuración de PokerStars"),
        ("data/card_templates/pokerstars_real/", "Carpeta de templates"),
        ("src/card_detector.py", "Módulo detector"),
        ("src/auto_capture_system.py", "Sistema de captura")
    ]
    
    all_ok = True
    print("\n VERIFICANDO CONFIGURACIÓN:")
    
    for path, description in requirements:
        exists = os.path.exists(path)
        status = "" if exists else ""
        print(f"   {status} {description}")
        
        if not exists:
            all_ok = False
    
    return all_ok

def show_menu():
    """Mostrar menú principal"""
    print("\n" + "=" * 60)
    print("MENÚ PRINCIPAL - CAPTURA AUTOMÁTICA")
    print("=" * 60)
    print("1.  Sistema de Captura Automática Completo")
    print("2.  Solo Detector de Cartas (pruebas)")
    print("3.  Solo Capturador de Templates")
    print("4.  Solo Clasificador de Cartas")
    print("5.   Verificar/Reparar Instalación")
    print("6.  Generar Reportes del Sistema")
    print("7.  Salir")
    
    try:
        choice = int(input("\nSelecciona opción (1-7): "))
        return choice
    except:
        return 0

def run_full_system():
    """Ejecutar sistema completo"""
    print("\n� INICIANDO SISTEMA COMPLETO")
    print("=" * 50)
    
    # Importar después de verificar dependencias
    from src.auto_capture_system import AutoCaptureSystem
    
    system = AutoCaptureSystem()
    system.run()

def run_detector_only():
    """Ejecutar solo detector"""
    print("\n🔍 MODO DETECTOR SOLO")
    print("=" * 50)
    
    from src.card_detector import CardDetector
    
    detector = CardDetector()
    print(" Detector inicializado")
    
    # Aquí podrías añadir pruebas específicas
    input("\nPresiona Enter para volver al menú...")

def run_capturer_only():
    """Ejecutar solo capturador"""
    print("\n MODO CAPTURADOR SOLO")
    print("=" * 50)
    
    from src.auto_template_capturer import main as capturer_main
    capturer_main()

def run_classifier_only():
    """Ejecutar solo clasificador"""
    print("\n🎯 MODO CLASIFICADOR SOLO")
    print("=" * 50)
    
    from src.card_classifier import main as classifier_main
    classifier_main()

def repair_installation():
    """Reparar instalación si es necesario"""
    print("\n⚙️  REPARANDO INSTALACIÓN")
    print("=" * 50)
    
    # Verificar y crear estructura si no existe
    folders = [
        "data/card_templates/pokerstars_real",
        "data/card_templates/auto_captured",
        "config",
        "logs",
        "debug"
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            print(f" Creado: {folder}")
        else:
            print(f"✅ Existe: {folder}")
    
    # Verificar archivos esenciales
    essential_files = [
        "requirements.txt",
        "main.py",
        "detect_coords.py"
    ]
    
    for file in essential_files:
        if not os.path.exists(file):
            print(f"❌ Faltante: {file}")
        else:
            print(f" Presente: {file}")
    
    print("\n Si hay problemas, ejecuta:")
    print("   pip install -r requirements.txt")
    print("   python detect_coords.py (para configuración)")

def main():
    """Función principal"""
    
    if not check_dependencies():
        print("\n  Instala las dependencias faltantes:")
        print("   pip install opencv-python numpy mss scikit-learn")
        return
    
    if not check_configuration():
        print("\n  Configuración incompleta")
        print("   Ejecuta primero: python detect_coords.py")
        response = input("Ejecutar detect_coords.py ahora? (s/n): ")
        if response.lower() == 's':
            os.system("python detect_coords.py")
    
    while True:
        choice = show_menu()
        
        if choice == 1:
            run_full_system()
        elif choice == 2:
            run_detector_only()
        elif choice == 3:
            run_capturer_only()
        elif choice == 4:
            run_classifier_only()
        elif choice == 5:
            repair_installation()
        elif choice == 6:
            from src.auto_capture_system import AutoCaptureSystem
            system = AutoCaptureSystem()
            system.generate_reports()
        elif choice == 7:
            print("\n Hasta pronto!")
            break
        else:
            print("\n Opción inválida")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
