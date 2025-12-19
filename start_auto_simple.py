# start_auto_simple.py - Versión simplificada sin emojis problemáticos
import os
import sys

print("🎴 POKER COACH PRO - SISTEMA DE CAPTURA AUTOMÁTICA")
print("=" * 70)
print("Versión: 2.1 - Menú simplificado")
print("=" * 70)

def check_dependencies():
    """Verificar dependencias mínimas"""
    required = [
        ("cv2", "OpenCV", True),
        ("numpy", "NumPy", True),
        ("mss", "MSS", True),
        ("sklearn", "scikit-learn", False),
        ("matplotlib", "Matplotlib", False)
    ]
    
    print("\nVERIFICANDO DEPENDENCIAS:")
    all_required_ok = True
    
    for module_name, display_name, required_flag in required:
        try:
            __import__(module_name)
            version = getattr(sys.modules[module_name], "__version__", "OK")
            print(f"   OK {display_name:15} {version}")
        except ImportError:
            if required_flag:
                print(f"   ERROR {display_name:15} FALTANTE")
                all_required_ok = False
            else:
                print(f"   ADVERTENCIA {display_name:15} Faltante")
    
    return all_required_ok

def check_configuration():
    """Verificar configuración necesaria"""
    requirements = [
        ("config/pokerstars_coords.json", "Configuración PokerStars", False),
        ("data/card_templates/pokerstars_real", "Carpeta templates", False),
        ("src/card_detector.py", "Módulo detector", True),
        ("src/auto_template_capturer.py", "Capturador", True)
    ]
    
    print("\nVERIFICANDO CONFIGURACIÓN:")
    all_required_ok = True
    
    for path, description, required in requirements:
        exists = os.path.exists(path)
        status = "OK" if exists else ("ADVERTENCIA" if not required else "ERROR")
        print(f"   {status} {description}")
        
        if required and not exists:
            all_required_ok = False
    
    return all_required_ok

def show_simple_menu():
    """Menú simplificado sin caracteres problemáticos"""
    print("\n" + "=" * 60)
    print("MENU PRINCIPAL - CAPTURA AUTOMATICA")
    print("=" * 60)
    
    # Estado del sistema
    sessions_count = count_sessions()
    templates_count = count_templates()
    
    print("ESTADO DEL SISTEMA:")
    print(f"   Sesiones: {sessions_count}")
    print(f"   Templates: {templates_count}")
    
    print("\nOPCIONES DISPONIBLES:")
    print("1. Sistema Completo (recomendado)")
    print("2. Capturar Templates Basico")
    print("3. Clasificar Cartas Existentes")
    print("4. Ver Sesiones de Captura")
    print("5. Gestionar Sesiones (eliminar/limpiar)")
    print("6. Verificar/Reparar Instalacion")
    print("7. Generar Reportes")
    print("8. Ayuda y Tutorial")
    print("9. Salir")
    print("=" * 60)
    
    try:
        choice = input("\nSelecciona opcion (1-9): ")
        return int(choice.strip())
    except:
        return 0

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

def run_full_system():
    """Ejecutar sistema completo"""
    print("\n" + "=" * 60)
    print("SISTEMA COMPLETO DE CAPTURA AUTOMATICA")
    print("=" * 60)
    
    try:
        sys.path.insert(0, "src")
        from auto_capture_system import AutoCaptureSystem
        system = AutoCaptureSystem()
        system.run()
    except ImportError as e:
        print(f"ERROR: {e}")
        print("\nSolucion: Ejecuta pip install -r requirements.txt")
    except Exception as e:
        print(f"ERROR inesperado: {e}")

def run_basic_capturer():
    """Modo capturador basico"""
    print("\nCAPTURADOR BASICO")
    print("=" * 50)
    
    try:
        from src.auto_template_capturer import main as capturer_main
        capturer_main()
    except ImportError:
        print("ERROR: No se puede importar el capturador")

def run_classifier():
    """Ejecutar clasificador"""
    print("\nCLASIFICADOR DE CARTAS")
    print("=" * 50)
    
    try:
        from src.card_classifier import main as classifier_main
        classifier_main()
    except ImportError as e:
        print(f"ERROR: {e}")

def view_sessions():
    """Ver sesiones de captura existentes"""
    print("\nSESIONES DE CAPTURA EXISTENTES")
    print("=" * 50)
    
    capture_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(capture_path):
        print("No hay carpeta de capturas")
        return
    
    sessions = []
    for item in os.listdir(capture_path):
        session_path = os.path.join(capture_path, item)
        if os.path.isdir(session_path):
            raw_path = os.path.join(session_path, "raw_captures")
            card_count = 0
            if os.path.exists(raw_path):
                card_count = len([f for f in os.listdir(raw_path) 
                                if f.endswith('.png')])
            
            sessions.append({
                "id": item,
                "cards": card_count,
                "date": item[:15]
            })
    
    if not sessions:
        print("No hay sesiones de captura")
        return
    
    print(f"Total sesiones: {len(sessions)}")
    print("\nLISTA DE SESIONES:")
    print("-" * 50)
    
    for i, session in enumerate(sessions, 1):
        print(f"{i:2}. {session['date']} - {session['cards']:3} cartas")

def manage_sessions():
    """Gestionar sesiones"""
    print("\nGESTION DE SESIONES")
    print("=" * 50)
    
    try:
        from src.session_manager import SessionManager
        manager = SessionManager()
        
        print("\nMENU GESTION DE SESIONES:")
        print("1. Listar todas las sesiones")
        print("2. Eliminar sesion especifica")
        print("3. Eliminar sesiones vacias (< 5 imagenes)")
        print("4. Eliminar sesiones antiguas")
        print("5. Ver uso de disco")
        print("6. Limpieza completa")
        print("7. Volver al menu principal")
        
        try:
            choice = int(input("\nSelecciona opcion (1-7): "))
            
            if choice == 1:
                manager.list_sessions(show_all=True)
            elif choice == 2:
                sessions = manager.list_sessions(show_all=False, max_display=15)
                if sessions:
                    try:
                        num = int(input("\nNumero de sesion a eliminar (0 para cancelar): "))
                        if 1 <= num <= len(sessions):
                            manager.delete_session(sessions[num-1]["id"])
                    except ValueError:
                        print("Entrada no valida")
            elif choice == 3:
                manager.delete_empty_sessions()
            elif choice == 4:
                days = input("Dias de antiguedad (default 30): ")
                days = int(days) if days.isdigit() else 30
                manager.delete_old_sessions(days_old=days)
            elif choice == 5:
                manager.show_disk_usage()
            elif choice == 6:
                manager.cleanup_system()
            elif choice == 7:
                return
            else:
                print("Opcion no valida")
                
        except Exception as e:
            print(f"Error: {e}")
            
    except ImportError as e:
        print(f"Error importando gestor de sesiones: {e}")
        print("\nUsando gestion basica...")
        basic_session_management()

def basic_session_management():
    """Gestion basica de sesiones"""
    print("\nGESTION BASICA DE SESIONES")
    print("=" * 50)
    
    base_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(base_path):
        print("No hay sesiones de captura")
        return
    
    sessions = []
    for item in sorted(os.listdir(base_path), reverse=True):
        session_path = os.path.join(base_path, item)
        if os.path.isdir(session_path):
            raw_path = os.path.join(session_path, "raw_captures")
            image_count = 0
            if os.path.exists(raw_path):
                image_count = len([f for f in os.listdir(raw_path) 
                                 if f.endswith('.png')])
            
            sessions.append({
                "id": item,
                "image_count": image_count
            })
    
    if not sessions:
        print("No hay sesiones")
        return
    
    print(f"\nSESIONES DISPONIBLES ({len(sessions)}):")
    print("-" * 50)
    
    for i, session in enumerate(sessions[:10], 1):
        print(f"{i:2}. {session['id']} - {session['image_count']} imagenes")

def repair_installation():
    """Reparar instalacion"""
    print("\nHERRAMIENTAS DE REPARACION")
    print("=" * 50)
    print("1. Instalar dependencias basicas")
    print("2. Crear estructura de carpetas")
    print("3. Verificar archivos esenciales")
    print("4. Configurar PokerStars")
    print("5. Volver al menu principal")
    
    try:
        subchoice = int(input("\nOpcion (1-5): "))
        
        if subchoice == 1:
            print("\nInstalando dependencias...")
            os.system("pip install -r requirements.txt")
        elif subchoice == 2:
            print("\nCreando estructura...")
            folders = [
                "data/card_templates/pokerstars_real",
                "data/card_templates/auto_captured",
                "config", "logs", "debug"
            ]
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
                print(f"   {folder}")
        elif subchoice == 3:
            print("\nVerificando archivos...")
            essential_files = [
                "requirements.txt", "main.py", "detect_coords.py",
                "src/card_detector.py", "src/auto_template_capturer.py"
            ]
            for file in essential_files:
                if os.path.exists(file):
                    print(f"   OK {file}")
                else:
                    print(f"   ERROR {file}")
        elif subchoice == 4:
            print("\nConfigurando PokerStars...")
            os.system("python detect_coords.py")
        elif subchoice == 5:
            return
        else:
            print("Opcion invalida")
    
    except:
        print("Entrada invalida")

def generate_reports():
    """Generar reportes"""
    print("\nGENERANDO REPORTES...")
    
    # Contar templates
    templates_path = "data/card_templates/pokerstars_real"
    total_templates = 0
    suit_counts = {}
    
    if os.path.exists(templates_path):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        for suit in suits:
            suit_path = os.path.join(templates_path, suit)
            if os.path.exists(suit_path):
                count = len([f for f in os.listdir(suit_path) 
                           if f.endswith(('.png', '.jpg', '.jpeg'))])
                suit_counts[suit] = count
                total_templates += count
    
    print("\nESTADISTICAS DE TEMPLATES:")
    print("=" * 40)
    
    if total_templates > 0:
        for suit, count in suit_counts.items():
            if count > 0:
                print(f"   {suit.upper():10} {count:3}")
        
        print(f"\n   TOTAL:      {total_templates:3}")
    else:
        print("   No hay templates capturados")

def show_help():
    """Mostrar ayuda"""
    print("\n" + "=" * 70)
    print("AYUDA Y TUTORIAL - POKER COACH PRO")
    print("=" * 70)
    
    print("\nQUE HACE ESTE SISTEMA?")
    print("   Captura automaticamente cartas de PokerStars mientras juegas,")
    print("   las clasifica por palo y las guarda como templates.")
    
    print("\nFLUJO DE TRABAJO RECOMENDADO:")
    print("   1. Verificar/Reparar Instalacion (opcion 6)")
    print("   2. Configurar PokerStars")
    print("   3. Usar Sistema Completo (opcion 1) para capturar")
    print("   4. Usar Clasificar Cartas (opcion 3) para organizar")
    
    input("\nPresiona Enter para volver al menu...")

def main():
    """Funcion principal"""
    
    print("Bienvenido al sistema de captura automatica de Poker Coach Pro!")
    
    # Verificar dependencias minimas
    if not check_dependencies():
        print("\nFaltan dependencias REQUERIDAS")
        response = input("Instalar automaticamente? (s/n): ")
        if response.lower() == 's':
            os.system("pip install -r requirements.txt")
        else:
            print("No se puede continuar sin dependencias basicas")
            return
    
    # Verificar configuracion
    config_ok = check_configuration()
    
    if not config_ok:
        print("\nConfiguracion incompleta")
        response = input("Ejecutar configuracion basica? (s/n): ")
        if response.lower() == 's':
            folders = [
                "data/card_templates/pokerstars_real",
                "data/card_templates/auto_captured",
                "config", "logs", "debug"
            ]
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
            os.system("python detect_coords.py")
    
    # Bucle principal del menu
    while True:
        choice = show_simple_menu()
        
        if choice == 1:
            run_full_system()
        elif choice == 2:
            run_basic_capturer()
        elif choice == 3:
            run_classifier()
        elif choice == 4:
            view_sessions()
        elif choice == 5:
            manage_sessions()
        elif choice == 6:
            repair_installation()
        elif choice == 7:
            generate_reports()
        elif choice == 8:
            show_help()
        elif choice == 9:
            print("\nGracias por usar Poker Coach Pro!")
            print("Hasta pronto!")
            break
        else:
            print("\nOpcion invalida. Por favor, selecciona 1-9.")
        
        if choice != 9:
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
