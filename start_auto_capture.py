# start_auto_capture.py - Versión corregida y mejorada
import os
import sys

print("🎴 POKER COACH PRO - SISTEMA DE CAPTURA AUTOMÁTICA")
print("=" * 70)
print("Versión: 2.0 - Corregido y optimizado")
print("=" * 70)

def check_dependencies():
    """Verificar dependencias mínimas"""
    required = [
        ("cv2", "OpenCV", True),
        ("numpy", "NumPy", True),
        ("mss", "MSS", True),
        ("sklearn", "scikit-learn", False),  # Opcional
        ("matplotlib", "Matplotlib", False)  # Opcional
    ]
    
    print("\n🔍 VERIFICANDO DEPENDENCIAS:")
    all_required_ok = True
    
    for module_name, display_name, required_flag in required:
        try:
            __import__(module_name)
            version = getattr(sys.modules[module_name], "__version__", "OK")
            print(f"   ✅ {display_name:15} {version}")
        except ImportError:
            if required_flag:
                print(f"   ❌ {display_name:15} FALTANTE (REQUERIDO)")
                all_required_ok = False
            else:
                print(f"   ⚠️  {display_name:15} Faltante (algunas funciones limitadas)")
    
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
        status = "✅" if exists else ("⚠️ " if not required else "❌")
        print(f"   {status} {description}")
        
        if required and not exists:
            all_required_ok = False
    
    return all_required_ok

def show_menu():
    """Mostrar menú principal mejorado"""
    print("\n" + "=" * 60)
    print("MENÚ PRINCIPAL - CAPTURA AUTOMÁTICA")
    print("=" * 60)
    
    # Estado del sistema
    sessions_count = count_sessions()
    templates_count = count_templates()
    
    print(" ESTADO DEL SISTEMA:")
    print(f"   📁 Sesiones: {sessions_count}")
    print(f"   🎴 Templates: {templates_count}")
    
    print("\nOPCIONES DISPONIBLES:")
    print("1. Sistema Completo (recomendado)")
    print("2. Capturar Templates Básico")
    print("3. Clasificar Cartas Existentes")
    print("4. Ver Sesiones de Captura")
    print("5. Gestionar Sesiones (eliminar/limpiar)")
    print("6. Verificar/Reparar Instalación")
    print("7. Generar Reportes")
    print("8. Ayuda y Tutorial")
    print("9. Salir")
    print("=" * 60)
    
    try:
        choice = int(input("\n Selecciona opción (1-9): "))
        return choice
    except:
        return 0
    except:
        return 0
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

def manage_sessions():
    """Gestión completa de sesiones - VERSIÓN CORREGIDA"""
    print("\n" + "=" * 60)
    print("  GESTIÓN DE SESIONES DE CAPTURA")
    print("=" * 60)
    
    try:
        from src.session_manager import SessionManager
        manager = SessionManager()
        
        if not manager.sessions:
            print("\n No hay sesiones de captura")
            print(" Ejecuta primero una captura")
            return
        
        while True:
            print("\n MENÚ GESTIÓN DE SESIONES:")
            print("1.  Listar todas las sesiones")
            print("2.   Eliminar sesión específica")
            print("3.   Eliminar sesiones vacías (< 5 imágenes)")
            print("4.   Eliminar sesiones antiguas")
            print("5.  Ver uso de disco")
            print("6.  Limpieza completa")
            print("7.  Volver al menú principal")
            
            try:
                choice = int(input("\n Selecciona opción (1-7): "))
                
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
    print("\n Opción inválida. Por favor, selecciona 1-9.")("\n❌ Opción inválida. Por favor, selecciona 1-9.")("❌ Opción no válida")
                
                if choice != 7:
                    input("\n�� Presiona Enter para continuar...")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except ImportError as e:
        print(f" Error importando gestor de sesiones: {e}")
        print("\n El módulo session_manager.py no está disponible")
        print("   Usando gestión básica...")
        basic_session_management()

def basic_session_management():
    """Gestión básica de sesiones (fallback)"""
    print("\n  GESTIÓN BÁSICA DE SESIONES")
    print("=" * 50)
    
    base_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(base_path):
        print(" No hay sesiones de captura")
        return
    
    sessions = []
    for item in sorted(os.listdir(base_path), reverse=True):
        session_path = os.path.join(base_path, item)
        if os.path.isdir(session_path):
            # Contar imágenes
            raw_path = os.path.join(session_path, "raw_captures")
            image_count = 0
            if os.path.exists(raw_path):
                image_count = len([f for f in os.listdir(raw_path) 
                                 if f.endswith(('.png', '.jpg'))])
            
            # Calcular tamaño
            size_mb = 0
            if os.path.exists(session_path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(session_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                size_mb = round(total_size / (1024 * 1024), 2)
            
            sessions.append({
                "id": item,
                "image_count": image_count,
                "size_mb": size_mb
            })
    
    if not sessions:
        print(" No hay sesiones de captura")
        return
    
    print(f"\n SESIONES DISPONIBLES ({len(sessions)}):")
    print("-" * 60)
    
    for i, session in enumerate(sessions[:15], 1):
        print(f"{i:2}. {session['id']} - {session['image_count']} imágenes ({session['size_mb']} MB)")
    
    if len(sessions) > 15:
        print(f"   ... y {len(sessions) - 15} sesiones más")
    
    print("\n🎯 OPCIONES:")
    print("   d [número] - Eliminar sesión específica")
    print("   v - Ver todas las sesiones")
    print("   c - Ver espacio total usado")
    print("   Enter - Volver")
    
    choice = input("\n Opción: ").strip().lower()
    
    if choice.startswith('d ') and choice[2:].isdigit():
        idx = int(choice[2:]) - 1
        if 0 <= idx < len(sessions):
            delete_session(sessions[idx]["id"])
    elif choice == 'v':
        for session in sessions:
            print(f"    {session['id']}: {session['image_count']} imágenes, {session['size_mb']} MB")
    elif choice == 'c':
        total_size = sum(s["size_mb"] for s in sessions)
        total_images = sum(s["image_count"] for s in sessions)
        print(f"\n USO TOTAL:")
        print(f"   Sesiones: {len(sessions)}")
        print(f"   Imágenes: {total_images}")
        print(f"   Espacio: {total_size:.1f} MB")

def delete_session(session_id):
    """Eliminar una sesión específica"""
    session_path = f"data/card_templates/auto_captured/{session_id}"
    
    if not os.path.exists(session_path):
        print(f"❌ Sesión no encontrada: {session_id}")
        return
    
    print(f"\n⚠️  ELIMINAR SESIÓN: {session_id}")
    print(f"   Ruta: {session_path}")
    
    # Contar imágenes
    raw_path = os.path.join(session_path, "raw_captures")
    image_count = 0
    if os.path.exists(raw_path):
        image_count = len([f for f in os.listdir(raw_path) if f.endswith(('.png', '.jpg'))])
    
    print(f"   Imágenes: {image_count}")
    
    confirm = input("\n Estás SEGURO? (escribe 'ELIMINAR' para confirmar): ")
    
    if confirm != "ELIMINAR":
        print(" Eliminación cancelada")
        return
    
    try:
        import shutil
        # Crear carpeta de backup
        backup_base = "data/card_templates/deleted_sessions"
        os.makedirs(backup_base, exist_ok=True)
        backup_path = os.path.join(backup_base, session_id)
        
        # Mover a backup en lugar de eliminar
        shutil.move(session_path, backup_path)
        print(f" Sesión movida a backup: {backup_path}")
        
    except Exception as e:
        print(f" Error eliminando sesión: {e}")
        print(" Intenta eliminar manualmente la carpeta")
    except:
        return 0

def run_full_system():
    """Ejecutar sistema completo con manejo de errores"""
    print("\n" + "=" * 60)
    print("🚀 SISTEMA COMPLETO DE CAPTURA AUTOMÁTICA")
    print("=" * 60)
    
    try:
        # Importar con manejo de errores
        sys.path.insert(0, "src")
        
        try:
            from auto_capture_system import AutoCaptureSystem
        except ImportError as e:
            print(f"❌ Error importando módulo: {e}")
            print("\n💡 Soluciones:")
            print("   1. Ejecuta: pip install -r requirements.txt")
            print("   2. Verifica que los archivos en src/ existan")
            return
        
        # Crear carpeta de templates si no existe
        os.makedirs("data/card_templates/pokerstars_real", exist_ok=True)
        
        system = AutoCaptureSystem()
        system.run()
        
    except Exception as e:
        print(f"\n❌ Error ejecutando sistema: {e}")
        print("\n🔧 Intentando modo básico...")
        run_basic_capturer()

def run_basic_capturer():
    """Modo capturador básico (sin dependencias complejas)"""
    print("\n📸 MODO CAPTURADOR BÁSICO")
    print("=" * 50)
    
    try:
        from src.auto_template_capturer import main as capturer_main
        capturer_main()
    except ImportError:
        print("❌ No se puede importar el capturador")
        print("💡 Instala dependencias: pip install mss opencv-python")

def run_classifier():
    """Ejecutar clasificador"""
    print("\n🎯 CLASIFICADOR DE CARTAS")
    print("=" * 50)
    
    try:
        from src.card_classifier import main as classifier_main
        classifier_main()
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("💡 Instala: pip install scikit-learn matplotlib")

def view_sessions():
    """Ver sesiones de captura existentes"""
    print("\n📁 SESIONES DE CAPTURA EXISTENTES")
    print("=" * 50)
    
    capture_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(capture_path):
        print("❌ No hay carpeta de capturas")
        print("💡 Ejecuta primero el capturador")
        return
    
    sessions = []
    for item in os.listdir(capture_path):
        session_path = os.path.join(capture_path, item)
        if os.path.isdir(session_path):
            # Contar cartas
            raw_path = os.path.join(session_path, "raw_captures")
            card_count = 0
            if os.path.exists(raw_path):
                card_count = len([f for f in os.listdir(raw_path) 
                                if f.endswith('.png')])
            
            sessions.append({
                "id": item,
                "path": session_path,
                "cards": card_count,
                "date": item[:15]  # Extraer fecha del ID
            })
    
    if not sessions:
        print("📭 No hay sesiones de captura")
        return
    
    print(f"📊 Total sesiones: {len(sessions)}")
    print("\n📋 LISTA DE SESIONES:")
    print("-" * 50)
    
    for i, session in enumerate(sessions, 1):
        print(f"{i:2}. {session['date']} - {session['cards']:3} cartas")
    
    print("\n💡 Usa el clasificador (opción 3) para procesar estas sesiones")

def repair_installation():
    """Reparar instalación"""
    print("\n⚙️  HERRAMIENTAS DE REPARACIÓN")
    print("=" * 50)
    
    print("1. Instalar dependencias básicas")
    print("2. Crear estructura de carpetas")
    print("3. Verificar archivos esenciales")
    print("4. Configurar PokerStars")
    print("5. Volver al menú principal")
    
    try:
        subchoice = int(input("\n👉 Opción (1-5): "))
        
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
            print("❌ Opción inválida")
    
    except:
        print("❌ Entrada inválida")

def install_dependencies():
    """Instalar dependencias"""
    print("\n📦 INSTALANDO DEPENDENCIAS...")
    
    # Lista de paquetes
    packages = [
        "opencv-python==4.9.0.80",
        "numpy==1.24.4",
        "mss==9.0.1",
        "pillow==10.3.0",
        "pyyaml==6.0.1"
    ]
    
    print("Paquetes básicos (siempre necesarios):")
    for pkg in packages:
        print(f"   📦 {pkg}")
    
    print("\nPaquetes opcionales (para funciones avanzadas):")
    print("   📦 scikit-learn==1.3.2 (clasificación ML)")
    print("   📦 matplotlib==3.8.2 (gráficos y reportes)")
    
    response = input("\n¿Instalar TODAS las dependencias? (s/n): ")
    
    if response.lower() == 's':
        print("\n🔄 Instalando... Esto puede tomar unos minutos.")
        
        # Instalar básicos primero
        import subprocess
        for pkg in packages:
            print(f"Instalando {pkg}...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"])
        
        # Preguntar por opcionales
        opt_response = input("\n¿Instalar scikit-learn y matplotlib? (s/n): ")
        if opt_response.lower() == 's':
            subprocess.run([sys.executable, "-m", "pip", "install", 
                          "scikit-learn==1.3.2", "matplotlib==3.8.2", "-q"])
        
        print("\n✅ Dependencias instaladas")
    else:
        print("\n⚠️  Instalación cancelada")

def create_folders():
    """Crear estructura de carpetas"""
    print("\n📁 CREANDO ESTRUCTURA...")
    
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
        print(f"   📂 {folder}")
    
    print("\n✅ Estructura creada")

def verify_files():
    """Verificar archivos esenciales"""
    print("\n🔍 VERIFICANDO ARCHIVOS...")
    
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
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Faltan {len(missing)} archivos esenciales")
        print("💡 Clona el repositorio completo o descarga los archivos faltantes")
    else:
        print("\n✅ Todos los archivos esenciales presentes")

def setup_pokerstars():
    """Configurar PokerStars"""
    print("\n🎴 CONFIGURANDO POKERSTARS...")
    print("\n💡 Asegúrate de:")
    print("   1. Tener PokerStars ABIERTO")
    print("   2. La mesa debe estar VISIBLE")
    print("   3. No minimizado")
    
    response = input("\n¿PokerStars está abierto y visible? (s/n): ")
    
    if response.lower() == 's':
        print("\n🔍 Detectando coordenadas...")
        os.system("python detect_coords.py")
    else:
        print("\n⚠️  Abre PokerStars primero y luego vuelve a intentar")

def generate_reports():
    """Generar reportes básicos"""
    print("\n📊 GENERANDO REPORTES...")
    
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
    
    print("\n📈 ESTADÍSTICAS DE TEMPLATES:")
    print("=" * 40)
    
    if total_templates > 0:
        for suit, count in suit_counts.items():
            if count > 0:
                percentage = (count / total_templates) * 100
                print(f"   {suit.upper():10} {count:3} ({percentage:.1f}%)")
        
        print(f"\n   TOTAL:      {total_templates:3} templates")
        
        # Evaluar si hay suficientes templates
        if total_templates < 20:
            print("\n⚠️  POCO DATOS: Menos de 20 templates")
            print("💡 Ejecuta el capturador para obtener más cartas")
        elif total_templates >= 100:
            print("\n✅ BUENOS DATOS: Más de 100 templates")
        else:
            print("\n📊 DATOS MODERADOS: Podría mejorar con más capturas")
    else:
        print("   📭 No hay templates capturados")
        print("\n💡 Ejecuta el capturador primero (opción 1 o 2)")
    
    # Información del sistema
    print("\n💻 INFORMACIÓN DEL SISTEMA:")
    print("=" * 40)
    
    import platform
    print(f"   Sistema: {platform.system()} {platform.release()}")
    print(f"   Python: {platform.python_version()}")
    
    try:
        import cv2
        print(f"   OpenCV: {cv2.__version__}")
    except:
        print("   OpenCV: No disponible")
    
    try:
        import mss
        print("   MSS: Disponible")
    except:
        print("   MSS: No disponible")

def show_help():
    """Mostrar ayuda y tutorial"""
    print("\n" + "=" * 70)
    print("❓ AYUDA Y TUTORIAL - POKER COACH PRO")
    print("=" * 70)
    
    print("\n🎯 ¿QUÉ HACE ESTE SISTEMA?")
    print("   Captura automáticamente cartas de PokerStars mientras juegas,")
    print("   las clasifica por palo (corazones, diamantes, tréboles, picas)")
    print("   y las guarda como templates para reconocimiento futuro.")
    
    print("\n🚀 FLUJO DE TRABAJO RECOMENDADO:")
    print("   1. ⚙️  Ejecuta 'Verificar/Reparar Instalación' (opción 5)")
    print("   2. 🎴 Configura PokerStars (dentro de la opción 5)")
    print("   3. 📸 Usa 'Sistema Completo' (opción 1) para capturar")
    print("   4. 🎯 Usa 'Clasificar Cartas' (opción 3) para organizar")
    print("   5. 🔄 Repite para obtener más datos")
    
    print("\n📂 ESTRUCTURA DE ARCHIVOS:")
    print("   data/card_templates/pokerstars_real/ - Templates organizados")
    print("   data/card_templates/auto_captured/   - Capturas crudas")
    print("   config/pokerstars_coords.json        - Configuración")
    print("   logs/                                - Registros del sistema")
    
    print("\n🔧 SOLUCIÓN DE PROBLEMAS COMUNES:")
    print("   ❌ 'No module named X'")
    print("      → Ejecuta opción 5 > Instalar dependencias")
    
    print("\n   ❌ 'PokerStars no detectado'")
    print("      → Asegúrate que PokerStars esté ABIERTO y VISIBLE")
    print("      → Ejecuta opción 5 > Configurar PokerStars")
    
    print("\n   ❌ 'No hay cartas para clasificar'")
    print("      → Primero captura cartas con opción 1 o 2")
    
    print("\n📞 SOPORTE:")
    print("   Revisa README.md para más información")
    print("   Reporta problemas en el repositorio GitHub")
    
    input("\nPresiona Enter para volver al menú...")

def main():
    """Función principal"""
    
    print("Bienvenido al sistema de captura automática de Poker Coach Pro!")
    print("\nEste sistema te ayudará a crear una base de datos de cartas")
    print("para entrenar el sistema de reconocimiento.")
    
    # Verificar dependencias mínimas
    if not check_dependencies():
        print("\n⚠️  Faltan dependencias REQUERIDAS")
        response = input("¿Instalar automáticamente? (s/n): ")
        if response.lower() == 's':
            install_dependencies()
        else:
            print("❌ No se puede continuar sin dependencias básicas")
            return
    
    # Verificar configuración
    config_ok = check_configuration()
    
    if not config_ok:
        print("\n⚠️  Configuración incompleta")
        response = input("¿Ejecutar configuración básica? (s/n): ")
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
    print("\n Opción inválida. Por favor, selecciona 1-9.")("\n❌ Opción inválida. Por favor, selecciona 1-9.")("\n❌ Opción inválida. Por favor, selecciona 1-8.")
        
        if choice != 8:
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💡 Intenta ejecutar la opción 5 (Reparar instalación)")




