# start_auto_capture.py - VERSIÓN CORREGIDA
import os
import sys

print(" POKER COACH PRO - SISTEMA DE CAPTURA AUTOMÁTICA")
print("=" * 70)
print("Versión: 2.2 - Corregido errores de indentación")
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
    
    print("\n🔍 VERIFICANDO DEPENDENCIAS:")
    all_required_ok = True
    
    for module_name, display_name, required_flag in required:
        try:
            __import__(module_name)
            version = getattr(sys.modules[module_name], "__version__", "OK")
            print(f"    {display_name:15} {version}")
        except ImportError:
            if required_flag:
                print(f"   ❌ {display_name:15} FALTANTE")
                all_required_ok = False
            else:
                print(f"     {display_name:15} Faltante")
    
    return all_required_ok

def check_configuration():
    """Verificar configuración necesaria"""
    requirements = [
        ("config/pokerstars_coords.json", "Configuración PokerStars", False),
        ("data/card_templates/pokerstars_real", "Carpeta templates", False),
        ("src/card_detector.py", "Módulo detector", True),
        ("src/auto_template_capturer.py", "Capturador", True)
    ]
    
    print("\n🔧 VERIFICANDO CONFIGURACIÓN:")
    all_required_ok = True
    
    for path, description, required in requirements:
        exists = os.path.exists(path)
        status = "" if exists else (" " if not required else "")
        print(f"   {status} {description}")
        
        if required and not exists:
            all_required_ok = False
    
    return all_required_ok

def show_menu():
    """Mostrar menú principal mejorado"""
    print("\n" + "=" * 60)
    print("🎮 MENÚ PRINCIPAL - CAPTURA AUTOMÁTICA")
    print("=" * 60)
    
    # Estado del sistema
    sessions_count = count_sessions()
    templates_count = count_templates()
    
    print(" ESTADO DEL SISTEMA:")
    print(f"    Sesiones: {sessions_count}")
    print(f"    Templates: {templates_count}")
    
    print("\n OPCIONES DISPONIBLES:")
    print("1.  Sistema Completo (recomendado)")
    print("2.  Capturar Templates Básico")
    print("3.  Clasificar Cartas Existentes")
    print("4.  Ver Sesiones de Captura")
    print("5.  Gestionar Sesiones (eliminar/limpiar)")
    print("6.  Verificar/Reparar Instalación")
    print("7. 📊 Generar Reportes")
    print("8. ❓ Ayuda y Tutorial")
    print("9. 🚪 Salir")
    print("=" * 60)
    
    try:
        choice = int(input("\n👉 Selecciona opción (1-9): "))
        return choice
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
    print(" SISTEMA COMPLETO DE CAPTURA AUTOMÁTICA")
    print("=" * 60)
    
    try:
        sys.path.insert(0, "src")
        from auto_capture_system import AutoCaptureSystem
        system = AutoCaptureSystem()
        system.run()
    except ImportError as e:
        print(f"❌ Error importando módulo: {e}")
        print("\n Soluciones:")
        print("   1. Ejecuta: pip install -r requirements.txt")
        print("   2. Verifica que los archivos en src/ existan")

def run_basic_capturer():
    """Modo capturador básico"""
    print("\n📸 MODO CAPTURADOR BÁSICO")
    print("=" * 50)
    
    try:
        from src.auto_template_capturer import main as capturer_main
        capturer_main()
    except ImportError:
        print(" No se puede importar el capturador")

def run_classifier():
    """Ejecutar clasificador"""
    print("\n CLASIFICADOR DE CARTAS")
    print("=" * 50)
    
    try:
        from src.card_classifier import main as classifier_main
        classifier_main()
    except ImportError as e:
        print(f"❌ Error: {e}")

def view_sessions():
    """Ver sesiones de captura existentes"""
    print("\n📁 SESIONES DE CAPTURA EXISTENTES")
    print("=" * 50)
    
    capture_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(capture_path):
        print(" No hay carpeta de capturas")
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
        print("📭 No hay sesiones de captura")
        return
    
    print(f"📊 Total sesiones: {len(sessions)}")
    print("\n📋 LISTA DE SESIONES:")
    print("-" * 50)
    
    for i, session in enumerate(sessions, 1):
        print(f"{i:2}. {session['date']} - {session['cards']:3} cartas")

def manage_sessions():
    """Gestión completa de sesiones"""
    print("\n" + "=" * 60)
    print("🗑️ GESTIÓN DE SESIONES DE CAPTURA")
    print("=" * 60)
    
    try:
        from src.session_manager import SessionManager
        manager = SessionManager()
        
        if not manager.sessions:
            print("\n No hay sesiones de captura")
            return
        
        while True:
            print("\n🎮 MENÚ GESTIÓN DE SESIONES:")
            print("1. 📋 Listar todas las sesiones")
            print("2. 🗑️ Eliminar sesión específica")
            print("3. 🗑️ Eliminar sesiones vacías (< 5 imágenes)")
            print("4.  Eliminar sesiones antiguas")
            print("5.  Ver uso de disco")
            print("6.  Limpieza completa")
            print("7.  Volver al menú principal")
            
            try:
                choice = int(input("\n Selecciona opción (1-7): "))
                
                if choice == 1:
                    manager.list_sessions(show_all=True)
                elif choice == 2:
                    sessions = manager.list_sessions(show_all=False, max_display=15)
                    if sessions:
                        try:
                            num = int(input("\nNúmero de sesión a eliminar (0 para cancelar): "))
                            if 1 <= num <= len(sessions):
                                manager.delete_session(sessions[num-1]["id"])
                            elif num != 0:
                                print("❌ Número fuera de rango")
                        except ValueError:
                            print("❌ Entrada no válida")
                elif choice == 3:
                    manager.delete_empty_sessions()
                elif choice == 4:
                    days = input("Días de antigüedad (default 30): ")
                    days = int(days) if days.isdigit() else 30
                    manager.delete_old_sessions(days_old=days)
                elif choice == 5:
                    manager.show_disk_usage()
                elif choice == 6:
                    manager.cleanup_system()
                elif choice == 7:
                    print("\n Volviendo al menú principal...")
                    break
                else:
                    print(" Opción no válida")
                
                if choice != 7:
                    input("\n Presiona Enter para continuar...")
                    
            except Exception as e:
                print(f" Error: {e}")
                
    except ImportError as e:
        print(f" Error importando gestor de sesiones: {e}")
        print("\n💡 El módulo session_manager.py no está disponible")
        basic_session_management()

def basic_session_management():
    """Gestión básica de sesiones"""
    print("\n🗑️ GESTIÓN BÁSICA DE SESIONES")
    print("=" * 50)
    
    base_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(base_path):
        print(" No hay sesiones de captura")
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
        print(" No hay sesiones")
        return
    
    print(f"\n SESIONES DISPONIBLES ({len(sessions)}):")
    print("-" * 50)
    
    for i, session in enumerate(sessions[:10], 1):
        print(f"{i:2}. {session['id']} - {session['image_count']} imágenes")

def repair_installation():
    """Reparar instalación"""
    print("\n HERRAMIENTAS DE REPARACIÓN")
    print("=" * 50)
    
    print("1. Instalar dependencias básicas")
    print("2. Crear estructura de carpetas")
    print("3. Verificar archivos esenciales")
    print("4. Configurar PokerStars")
    print("5. Volver al menú principal")
    
    try:
        subchoice = int(input("\n Opción (1-5): "))
        
        if subchoice == 1:
            install_dependencies()
        elif subchoice == 2:
            create_folders()
        elif subchoice == 3:
            verify_files()
        elif subchoice == 4:
            setup_pokerstars()
        elif subchoice == 5:
            return
        else:
            print(" Opción inválida")
    
    except:
        print(" Entrada inválida")

def install_dependencies():
    """Instalar dependencias"""
    print("\n INSTALANDO DEPENDENCIAS...")
    
    packages = [
        "opencv-python==4.9.0.80",
        "numpy==1.24.4",
        "mss==9.0.1",
        "pillow==10.3.0",
        "pyyaml==6.0.1"
    ]
    
    print("Paquetes básicos (siempre necesarios):")
    for pkg in packages:
        print(f"    {pkg}")
    
    response = input("\nInstalar TODAS las dependencias? (s/n): ")
    
    if response.lower() == 's':
        print("\n Instalando... Esto puede tomar unos minutos.")
        import subprocess
        for pkg in packages:
            print(f"Instalando {pkg}...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"])

def create_folders():
    """Crear estructura de carpetas"""
    print("\n CREANDO ESTRUCTURA...")
    
    folders = [
        "data/card_templates/pokerstars_real",
        "data/card_templates/pokerstars_real/hearts",
        "data/card_templates/pokerstars_real/diamonds",
        "data/card_templates/pokerstars_real/clubs",
        "data/card_templates/pokerstars_real/spades",
        "data/card_templates/auto_captured",
        "config",
        "logs",
        "debug",
        "models"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"    {folder}")

def verify_files():
    """Verificar archivos esenciales"""
    print("\n VERIFICANDO ARCHIVOS...")
    
    essential_files = [
        ("requirements.txt", "Lista de dependencias"),
        ("main.py", "Sistema principal"),
        ("detect_coords.py", "Configurador PokerStars"),
        ("src/card_detector.py", "Detector de cartas"),
        ("src/auto_template_capturer.py", "Capturador")
    ]
    
    missing = []
    for file, description in essential_files:
        if os.path.exists(file):
            print(f"    {description}")
        else:
            print(f"    {description}")
            missing.append(file)
    
    if missing:
        print(f"\n Faltan {len(missing)} archivos esenciales")

def setup_pokerstars():
    """Configurar PokerStars"""
    print("\n CONFIGURANDO POKERSTARS...")
    print("\n Asegúrate de:")
    print("   1. Tener PokerStars ABIERTO")
    print("   2. La mesa debe estar VISIBLE")
    print("   3. No minimizado")
    
    response = input("\nPokerStars está abierto y visible? (s/n): ")
    
    if response.lower() == 's':
        print("\n Detectando coordenadas...")
        os.system("python detect_coords.py")

def generate_reports():
    """Generar reportes"""
    print("\n GENERANDO REPORTES...")
    
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
    
    print("\n ESTADÍSTICAS DE TEMPLATES:")
    print("=" * 40)
    
    if total_templates > 0:
        for suit, count in suit_counts.items():
            if count > 0:
                percentage = (count / total_templates) * 100
                print(f"   {suit.upper():10} {count:3} ({percentage:.1f}%)")
        
        print(f"\n   TOTAL:      {total_templates:3}")
    else:
        print("    No hay templates capturados")

def show_help():
    """Mostrar ayuda y tutorial"""
    print("\n" + "=" * 70)
    print(" AYUDA Y TUTORIAL - POKER COACH PRO")
    print("=" * 70)
    
    print("\n QUÉ HACE ESTE SISTEMA?")
    print("   Captura automáticamente cartas de PokerStars mientras juegas,")
    print("   las clasifica por palo y las guarda como templates.")
    
    print("\n FLUJO DE TRABAJO RECOMENDADO:")
    print("   1.  Ejecuta 'Verificar/Reparar Instalación' (opción 6)")
    print("   2.  Configura PokerStars (dentro de la opción 6)")
    print("   3.  Usa 'Sistema Completo' (opción 1) para capturar")
    print("   4.  Usa 'Clasificar Cartas' (opción 3) para organizar")
    
    input("\nPresiona Enter para volver al menú...")

def main():
    """Función principal"""
    
    print("Bienvenido al sistema de captura automática de Poker Coach Pro!")
    print("\nEste sistema te ayudará a crear una base de datos de cartas")
    print("para entrenar el sistema de reconocimiento.")
    
    # Verificar dependencias mínimas
    if not check_dependencies():
        print("\n Faltan dependencias REQUERIDAS")
        response = input("Instalar automáticamente? (s/n): ")
        if response.lower() == 's':
            install_dependencies()
        else:
            print(" No se puede continuar sin dependencias básicas")
            return
    
    # Verificar configuración
    config_ok = check_configuration()
    
    if not config_ok:
        print("\n Configuración incompleta")
        response = input("Ejecutar configuración básica? (s/n): ")
        if response.lower() == 's':
            create_folders()
            setup_pokerstars()
    
    # Bucle principal del menú
    while True:
        choice = show_menu()
        
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
            print("\n Gracias por usar Poker Coach Pro!")
            print("Hasta pronto!")
            break
        else:
            print("\n Opción inválida. Por favor, selecciona 1-9.")
        
        if choice != 9:
            input("\n Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        print(" Intenta ejecutar la opción 6 (Reparar instalación)")
