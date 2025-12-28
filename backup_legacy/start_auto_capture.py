# start_auto_capture.py - VERSIÓN COMPLETAMENTE NUEVA
import os
import sys

def print_header():
    """Imprimir encabezado del sistema"""
    print(" POKER COACH PRO - SISTEMA DE CAPTURA AUTOMÁTICA")
    print("=" * 70)
    print("Versión: 3.0 - Estable y corregido")
    print("=" * 70)

def check_dependencies():
    """Verificar dependencias mínimas"""
    print("\n VERIFICANDO DEPENDENCIAS:")
    
    deps = [
        ("cv2", "OpenCV", True),
        ("numpy", "NumPy", True),
        ("mss", "MSS", True),
        ("PIL", "Pillow", True),
        ("sklearn", "scikit-learn", False),
        ("matplotlib", "Matplotlib", False)
    ]
    
    all_ok = True
    for module_name, display_name, required in deps:
        try:
            __import__(module_name)
            print(f"    {display_name}")
        except ImportError:
            if required:
                print(f"   ❌ {display_name} (REQUERIDO)")
                all_ok = False
            else:
                print(f"   ⚠️  {display_name} (opcional)")
    
    return all_ok

def check_configuration():
    """Verificar configuración necesaria"""
    print("\n VERIFICANDO CONFIGURACIÓN:")
    
    requirements = [
        ("config/pokerstars_coords.json", "Configuración PokerStars", False),
        ("data/card_templates/pokerstars_real", "Carpeta templates", False),
        ("src/card_detector.py", "Detector de cartas", True),
        ("src/auto_template_capturer.py", "Capturador", True)
    ]
    
    all_ok = True
    for path, description, required in requirements:
        exists = os.path.exists(path)
        status = "✅" if exists else ("⚠️ " if not required else "❌")
        print(f"   {status} {description}")
        
        if required and not exists:
            all_ok = False
    
    return all_ok

def count_sessions():
    """Contar sesiones disponibles"""
    base_path = "data/card_templates/auto_captured"
    if not os.path.exists(base_path):
        return 0
    
    sessions = [d for d in os.listdir(base_path) 
               if os.path.isdir(os.path.join(base_path, d))]
    return len(sessions)

def count_templates():
    """Contar templates organizados"""
    base_path = "data/card_templates/pokerstars_real"
    if not os.path.exists(base_path):
        return 0
    
    total = 0
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    for suit in suits:
        suit_path = os.path.join(base_path, suit)
        if os.path.exists(suit_path):
            count = len([f for f in os.listdir(suit_path) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))])
            total += count
    
    return total

def show_menu():
    """Mostrar menú principal"""
    print("\n" + "=" * 60)
    print(" MENÚ PRINCIPAL")
    print("=" * 60)
    
    sessions = count_sessions()
    templates = count_templates()
    
    print(" ESTADO ACTUAL:")
    print(f"    Sesiones: {sessions}")
    print(f"    Templates: {templates}")
    
    print("\n OPCIONES:")
    print("1.  Sistema Completo")
    print("2.  Captura Rápida")
    print("3.  Clasificar Cartas")
    print("4.  Ver Sesiones")
    print("5.  Gestionar Sesiones")
    print("6.  Verificar Sistema")
    print("7.  Reportes")
    print("8.  Ayuda")
    print("9.  Salir")
    print("=" * 60)
    
    try:
        choice = input("\n Selecciona opción (1-9): ")
        return int(choice)
    except:
        return 0

def run_full_system():
    """Ejecutar sistema completo"""
    print("\n" + "=" * 60)
    print(" SISTEMA COMPLETO")
    print("=" * 60)
    
    try:
        sys.path.insert(0, "src")
        from auto_capture_system import AutoCaptureSystem
        system = AutoCaptureSystem()
        system.run()
    except ImportError as e:
        print(f" Error: {e}")
        print(" Ejecuta: pip install -r requirements.txt")

def run_quick_capture():
    """Ejecutar captura rápida"""
    print("\n" + "=" * 60)
    print(" CAPTURA RÁPIDA")
    print("=" * 60)
    
    try:
        from src.auto_template_capturer import main
        main()
    except ImportError as e:
        print(f" Error: {e}")

def run_classifier():
    """Ejecutar clasificador"""
    print("\n" + "=" * 60)
    print(" CLASIFICADOR")
    print("=" * 60)
    
    try:
        from src.card_classifier import main
        main()
    except ImportError as e:
        print(f" Error: {e}")

def view_sessions():
    """Ver sesiones"""
    print("\n" + "=" * 60)
    print(" SESIONES")
    print("=" * 60)
    
    base_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(base_path):
        print(" No hay sesiones")
        return
    
    sessions = []
    for item in os.listdir(base_path):
        path = os.path.join(base_path, item)
        if os.path.isdir(path):
            # Contar imágenes
            raw_path = os.path.join(path, "raw_captures")
            count = 0
            if os.path.exists(raw_path):
                count = len([f for f in os.listdir(raw_path) if f.endswith('.png')])
            
            sessions.append({
                "id": item,
                "images": count,
                "date": item[:15] if len(item) >= 15 else item
            })
    
    if not sessions:
        print(" No hay sesiones")
        return
    
    print(f" Total: {len(sessions)} sesiones")
    print("\n LISTA:")
    for i, session in enumerate(sessions[:10], 1):
        print(f"{i:2}. {session['date']} - {session['images']} imágenes")
    
    if len(sessions) > 10:
        print(f"   ... y {len(sessions) - 10} más")

def manage_sessions():
    """Gestionar sesiones"""
    print("\n" + "=" * 60)
    print(" GESTIÓN DE SESIONES")
    print("=" * 60)
    
    try:
        from src.session_manager import SessionManager
        manager = SessionManager()
        
        print("\n1.  Listar sesiones")
        print("2.  Eliminar sesión")
        print("3.  Limpiar vacías")
        print("4.  Volver")
        
        choice = input("\n Opción: ")
        
        if choice == "1":
            manager.list_sessions(show_all=True)
        elif choice == "2":
            sessions = manager.list_sessions(show_all=False, max_display=10)
            if sessions:
                try:
                    num = int(input("\nNúmero de sesión: "))
                    if 1 <= num <= len(sessions):
                        manager.delete_session(sessions[num-1]["id"])
                except:
                    print(" Número inválido")
        elif choice == "3":
            manager.delete_empty_sessions()
        elif choice == "4":
            return
        else:
            print(" Opción inválida")
    
    except ImportError as e:
        print(f" Error: {e}")
        print(" Ejecuta: python manage_sessions.py")

def verify_system():
    """Verificar sistema"""
    print("\n" + "=" * 60)
    print(" VERIFICACIÓN DEL SISTEMA")
    print("=" * 60)
    
    print("\n1.  Instalar dependencias")
    print("2.  Crear carpetas")
    print("3.  Verificar archivos")
    print("4.  Configurar PokerStars")
    print("5.  Volver")
    
    choice = input("\n Opción: ")
    
    if choice == "1":
        print("\nInstalando dependencias...")
        os.system("pip install -r requirements.txt")
    elif choice == "2":
        print("\nCreando carpetas...")
        folders = [
            "data/card_templates/pokerstars_real",
            "data/card_templates/auto_captured",
            "config", "logs", "debug"
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            print(f" {folder}")
    elif choice == "3":
        print("\nVerificando archivos...")
        files = [
            "requirements.txt", "main.py", "detect_coords.py",
            "src/card_detector.py", "src/auto_template_capturer.py"
        ]
        for file in files:
            if os.path.exists(file):
                print(f" {file}")
            else:
                print(f" {file}")
    elif choice == "4":
        print("\nConfigurando PokerStars...")
        os.system("python detect_coords.py")
    elif choice == "5":
        return
    else:
        print(" Opción inválida")

def show_reports():
    """Mostrar reportes"""
    print("\n" + "=" * 60)
    print(" REPORTES")
    print("=" * 60)
    
    # Templates
    templates = count_templates()
    print(f"\n TEMPLATES: {templates}")
    
    if templates > 0:
        base_path = "data/card_templates/pokerstars_real"
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        for suit in suits:
            path = os.path.join(base_path, suit)
            if os.path.exists(path):
                count = len([f for f in os.listdir(path) if f.endswith(('.png', '.jpg'))])
                print(f"   {suit.upper():10} {count}")
    
    # Sesiones
    sessions = count_sessions()
    print(f"\n SESIONES: {sessions}")
    
    if sessions > 0:
        base_path = "data/card_templates/auto_captured"
        total_images = 0
        for item in os.listdir(base_path)[:5]:
            path = os.path.join(base_path, item)
            if os.path.isdir(path):
                raw_path = os.path.join(path, "raw_captures")
                if os.path.exists(raw_path):
                    count = len([f for f in os.listdir(raw_path) if f.endswith('.png')])
                    total_images += count
        
        print(f" Total imágenes: {total_images}")
        print(f" Promedio: {total_images//sessions if sessions > 0 else 0} por sesión")

def show_help():
    """Mostrar ayuda"""
    print("\n" + "=" * 70)
    print(" AYUDA - POKER COACH PRO")
    print("=" * 70)
    
    print("\n QUÉ HACE ESTE SISTEMA?")
    print("Captura cartas de PokerStars y las organiza para reconocimiento.")
    
    print("\n FLUJO RECOMENDADO:")
    print("1. Verificar sistema (opción 6)")
    print("2. Configurar PokerStars")
    print("3. Capturar cartas (opción 2)")
    print("4. Clasificar (opción 3)")
    print("5. Gestionar sesiones (opción 5)")
    
    print("\n ESTRUCTURA:")
    print("data/card_templates/pokerstars_real/ - Templates organizados")
    print("data/card_templates/auto_captured/   - Sesiones de captura")
    print("config/                              - Configuración")
    
    input("\nPresiona Enter para continuar...")

def main():
    """Función principal"""
    print_header()
    
    print("Bienvenido al sistema de captura automática.")
    print("Selecciona una opción para comenzar.")
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n Faltan dependencias importantes")
        resp = input("Instalar ahora? (s/n): ")
        if resp.lower() == "s":
            os.system("pip install -r requirements.txt")
    
    # Verificar configuración
    check_configuration()
    
    # Bucle principal
    while True:
        choice = show_menu()
        
        if choice == 1:
            run_full_system()
        elif choice == 2:
            run_quick_capture()
        elif choice == 3:
            run_classifier()
        elif choice == 4:
            view_sessions()
        elif choice == 5:
            manage_sessions()
        elif choice == 6:
            verify_system()
        elif choice == 7:
            show_reports()
        elif choice == 8:
            show_help()
        elif choice == 9:
            print("\n Gracias por usar Poker Coach Pro!")
            print("Hasta pronto!")
            break
        else:
            print("\n Opción inválida. Usa 1-9.")
        
        if choice != 9:
            input("\n Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido")
    except Exception as e:
        print(f"\n Error: {e}")
        print(" Ejecuta la opción 6 para verificar el sistema")
