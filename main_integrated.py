# main_integrated.py - Sistema principal completo de Poker Coach Pro
import os
import sys
import json
import time
from datetime import datetime

def print_header(title):
    """Imprimir encabezado con estilo"""
    print("\n" + "=" * 70)
    print(f"🎴 {title}")
    print("=" * 70)

def check_system_status():
    """Verificar estado del sistema"""
    print_header("VERIFICACIÓN DEL SISTEMA")
    
    status = {
        'pokerstars_config': False,
        'dataset_balanced': False,
        'templates_organized': False,
        'scripts_working': False
    }
    
    # Verificar configuración de PokerStars
    config_file = "config/pokerstars_coords.json"
    if os.path.exists(config_file):
        print(" Configuración PokerStars: PRESENTE")
        status['pokerstars_config'] = True
    else:
        print("❌ Configuración PokerStars: FALTANTE")
        print("    Ejecuta: python detect_coords.py")
    
    # Verificar dataset balanceado
    sessions_path = "data/card_templates/auto_captured"
    if os.path.exists(sessions_path):
        sessions = [d for d in os.listdir(sessions_path) 
                   if os.path.isdir(os.path.join(sessions_path, d))]
        
        if sessions:
            # Analizar la sesión más reciente
            latest = max(sessions)
            results_file = os.path.join(sessions_path, latest, "classification_results.json")
            
            if os.path.exists(results_file):
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    
                    if 'distribution' in data:
                        dist = data['distribution']
                        total = sum(dist.values())
                        red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                        red_percentage = (red_cards / total * 100) if total > 0 else 0
                        
                        print(f"✅ Dataset: {total} cartas totales")
                        print(f"   🔴 Cartas rojas: {red_cards} ({red_percentage:.1f}%)")
                        
                        if red_percentage >= 30:
                            status['dataset_balanced'] = True
                            print("    Balance: ACEPTABLE")
                        else:
                            print(f"     Balance: Necesitas más cartas rojas ({red_percentage:.1f}%)")
                except:
                    print("⚠️  Dataset: Error leyendo resultados")
        else:
            print(" Dataset: No hay sesiones de captura")
            print("    Ejecuta: python smart_capture_fixed.py")
    else:
        print(" Dataset: No existe directorio")
    
    # Verificar templates organizados
    templates_path = "data/card_templates/pokerstars_real"
    if os.path.exists(templates_path):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        total_templates = 0
        
        for suit in suits:
            suit_path = os.path.join(templates_path, suit)
            if os.path.exists(suit_path):
                count = len([f for f in os.listdir(suit_path) 
                           if f.endswith(('.png', '.jpg'))])
                total_templates += count
        
        if total_templates > 0:
            print(f" Templates organizados: {total_templates}")
            status['templates_organized'] = True
        else:
            print("  Templates: Directorio vacío")
            print("    Ejecuta: python session_manager.py -> Opción 2")
    else:
        print(" Templates: No existe directorio")
    
    # Verificar scripts funcionando
    required_scripts = ["session_manager.py", "verify_balance.py", "smart_capture_fixed.py"]
    working_scripts = 0
    
    for script in required_scripts:
        if os.path.exists(script):
            working_scripts += 1
    
    if working_scripts == len(required_scripts):
        print(" Scripts principales: TODOS FUNCIONAN")
        status['scripts_working'] = True
    else:
        print(f"  Scripts: {working_scripts}/{len(required_scripts)} funcionando")
    
    return status

def show_main_menu():
    """Mostrar menú principal"""
    print_header("POKER COACH PRO - MENÚ PRINCIPAL")
    
    print(" ESTADO DEL SISTEMA:")
    status = check_system_status()
    
    print("\n MENÚ DE OPCIONES:")
    print("1.  Modo interactivo (recomendado)")
    print("2.  Capturar dataset balanceado")
    print("3.  Configurar PokerStars")
    print("4.  Gestionar sesiones/templates")
    print("5.  Verificar balance del dataset")
    print("6.  Sistema automático completo")
    print("7.  Dashboard del sistema")
    print("8.  Salir")
    
    return status

def interactive_mode():
    """Modo interactivo principal"""
    print_header("MODO INTERACTIVO")
    
    print(" Este modo te permite controlar todo el sistema.")
    print(" Comandos disponibles:")
    print("    'capture' - Iniciar captura automática")
    print("    'analyze' - Analizar mesa actual")
    print("    'status' - Ver estado del sistema")
    print("    'sessions' - Gestionar sesiones")
    print("    'templates' - Ver templates organizados")
    print("    'balance' - Verificar balance")
    print("    'config' - Configurar PokerStars")
    print("    'back' - Volver al menú principal")
    print("    'exit' - Salir del sistema")
    
    while True:
        try:
            command = input("\n Comando: ").strip().lower()
            
            if command == 'capture':
                print("\n Iniciando captura balanceada...")
                os.system("python smart_capture_fixed.py")
                
            elif command == 'analyze':
                print("\n Analizando mesa...")
                if os.path.exists("start_auto_simple.py"):
                    os.system("python start_auto_simple.py")
                else:
                    print(" Script de análisis no disponible")
                    print(" Usa: python session_manager.py -> Opción 3")
                    
            elif command == 'status':
                check_system_status()
                
            elif command == 'sessions':
                print("\n Gestionando sesiones...")
                os.system("python session_manager.py")
                
            elif command == 'templates':
                print("\n Mostrando templates organizados...")
                templates_path = "data/card_templates/pokerstars_real"
                if os.path.exists(templates_path):
                    suits = ['hearts', 'diamonds', 'clubs', 'spades']
                    for suit in suits:
                        suit_path = os.path.join(templates_path, suit)
                        if os.path.exists(suit_path):
                            count = len([f for f in os.listdir(suit_path) 
                                       if f.endswith(('.png', '.jpg'))])
                            suit_symbol = {'hearts': '', 'diamonds': '', 
                                         'clubs': '', 'spades': ''}[suit]
                            print(f"   {suit_symbol} {suit}: {count} templates")
                else:
                    print(" No hay templates organizados")
                    
            elif command == 'balance':
                print("\n Verificando balance...")
                os.system("python verify_balance.py")
                
            elif command == 'config':
                print("\n Configurando PokerStars...")
                os.system("python detect_coords.py")
                
            elif command == 'back':
                print("\n Volviendo al menú principal...")
                break
                
            elif command == 'exit':
                print("\n Hasta pronto!")
                sys.exit(0)
                
            else:
                print(" Comando no reconocido")
                print(" Usa: capture, analyze, status, sessions, templates, balance, config, back, exit")
                
        except KeyboardInterrupt:
            print("\n\n Comando interrumpido")
        except Exception as e:
            print(f" Error: {e}")

def capture_balanced_dataset():
    """Función para capturar dataset balanceado"""
    print_header("CAPTURA DE DATASET BALANCEADO")
    
    print(" Esta función capturará cartas balanceadas automáticamente.")
    print(" Objetivo: 30-40% cartas rojas ()")
    
    try:
        target = input("\nCuántas cartas capturar? (default: 100): ").strip()
        target_count = int(target) if target.isdigit() else 100
        
        print(f"\n Configuración:")
        print(f"    Cartas a capturar: {target_count}")
        print(f"    Objetivo rojas: 35% mínimo")
        print(f"    Duración estimada: {target_count * 0.3:.0f} segundos")
        
        confirm = input("\nIniciar captura? (s/n): ").strip().lower()
        
        if confirm == 's':
            os.system(f'python smart_capture_fixed.py')
        else:
            print(" Captura cancelada")
            
    except ValueError:
        print(" Número inválido")
    except Exception as e:
        print(f" Error: {e}")

def configure_pokerstars():
    """Configurar PokerStars"""
    print_header("CONFIGURACIÓN DE POKERSTARS")
    
    print(" Esta función configurará las coordenadas para PokerStars.")
    print(" Asegúrate de tener PokerStars abierto en una mesa 'Classic'.")
    
    confirm = input("\nIniciar configuración? (s/n): ").strip().lower()
    
    if confirm == 's':
        os.system("python detect_coords.py")
    else:
        print(" Configuración cancelada")

def manage_sessions():
    """Gestionar sesiones y templates"""
    print_header("GESTIÓN DE SESIONES Y TEMPLATES")
    
    print(" Esta función te permite gestionar tu dataset.")
    print(" Opciones disponibles:")
    print("   1. Listar todas las sesiones")
    print("   2. Clasificar cartas en templates")
    print("   3. Limpiar sesiones antiguas")
    print("   4. Ver templates organizados")
    
    os.system("python session_manager.py")

def show_dashboard():
    """Mostrar dashboard del sistema"""
    print_header("DASHBOARD DEL SISTEMA")
    
    # Información general
    print(" INFORMACIÓN GENERAL:")
    print(f"    Hora actual: {datetime.now().strftime('%H:%M:%S')}")
    print(f"    Directorio: {os.getcwd()}")
    print(f"    Python: {sys.version.split()[0]}")
    
    # Sesiones de captura
    sessions_path = "data/card_templates/auto_captured"
    if os.path.exists(sessions_path):
        sessions = [d for d in os.listdir(sessions_path) 
                   if os.path.isdir(os.path.join(sessions_path, d))]
        
        if sessions:
            print(f"\n SESIONES DE CAPTURA: {len(sessions)}")
            
            # Total de cartas
            total_cards = 0
            total_red = 0
            
            for session in sessions[:3]:  # Solo 3 más recientes
                results_file = os.path.join(sessions_path, session, "classification_results.json")
                if os.path.exists(results_file):
                    try:
                        with open(results_file, 'r') as f:
                            data = json.load(f)
                        
                        if 'distribution' in data:
                            dist = data['distribution']
                            cards = sum(dist.values())
                            red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                            
                            total_cards += cards
                            total_red += red_cards
                            
                            red_percentage = (red_cards / cards * 100) if cards > 0 else 0
                            
                            status = "" if red_percentage >= 30 else " " if red_percentage >= 10 else ""
                            
                            print(f"   {status} {session}: {cards} cartas ({red_percentage:.1f}% rojas)")
                    except:
                        pass
            
            if total_cards > 0:
                overall_red = (total_red / total_cards * 100)
                print(f"\n TOTAL: {total_cards} cartas ({overall_red:.1f}% rojas)")
    
    # Templates organizados
    templates_path = "data/card_templates/pokerstars_real"
    if os.path.exists(templates_path):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        total_templates = 0
        
        print(f"\n TEMPLATES ORGANIZADOS:")
        for suit in suits:
            suit_path = os.path.join(templates_path, suit)
            if os.path.exists(suit_path):
                count = len([f for f in os.listdir(suit_path) 
                           if f.endswith(('.png', '.jpg'))])
                total_templates += count
                
                suit_symbol = {'hearts': '', 'diamonds': '', 
                             'clubs': '', 'spades': ''}[suit]
                print(f"   {suit_symbol} {suit}: {count}")
        
        if total_templates > 0:
            print(f"    Total: {total_templates} templates")
    
    # Scripts disponibles
    print(f"\n SCRIPTS DISPONIBLES:")
    scripts = [
        ("session_manager.py", "Gestión de sesiones"),
        ("smart_capture_fixed.py", "Captura balanceada"),
        ("verify_balance.py", "Verificación de balance"),
        ("detect_coords.py", "Configuración PokerStars"),
        ("start_auto_simple.py", "Análisis automático")
    ]
    
    for script, description in scripts:
        if os.path.exists(script):
            print(f"    {script}: {description}")
        else:
            print(f"    {script}: NO DISPONIBLE")
    
    input("\n Presiona Enter para continuar...")

def auto_complete_system():
    """Sistema automático completo"""
    print_header("SISTEMA AUTOMÁTICO COMPLETO")
    
    print(" Este modo ejecutará todo el sistema automáticamente.")
    print("  Duración estimada: 3-5 minutos")
    print("\n PROCESO:")
    print("   1. Verificar estado del sistema")
    print("   2. Configurar PokerStars (si es necesario)")
    print("   3. Capturar dataset balanceado")
    print("   4. Clasificar cartas en templates")
    print("   5. Iniciar análisis automático")
    
    confirm = input("\nIniciar sistema automático completo? (s/n): ").strip().lower()
    
    if confirm == 's':
        print("\n INICIANDO PROCESO...")
        
        # 1. Verificar estado
        print("\n1 VERIFICANDO ESTADO...")
        status = check_system_status()
        
        # 2. Configurar PokerStars si es necesario
        if not status['pokerstars_config']:
            print("\n2 CONFIGURANDO POKERSTARS...")
            configure_pokerstars()
        
        # 3. Capturar dataset si es necesario
        if not status['dataset_balanced']:
            print("\n3 CAPTURANDO DATASET...")
            capture_balanced_dataset()
        
        # 4. Clasificar templates si es necesario
        if not status['templates_organized']:
            print("\n4 CLASIFICANDO TEMPLATES...")
            print(" Ejecuta manualmente: python session_manager.py -> Opción 2")
        
        # 5. Iniciar análisis
        print("\n5 INICIANDO ANÁLISIS...")
        if os.path.exists("start_auto_simple.py"):
            os.system("python start_auto_simple.py")
        else:
            print(" Script de análisis no disponible")
            print(" Puedes usar el modo interactivo")
        
        print("\n PROCESO COMPLETADO")
    else:
        print(" Proceso cancelado")

def main():
    """Función principal"""
    print_header("POKER COACH PRO - SISTEMA PRINCIPAL")
    print("Versión: 3.0 | Sistema completo integrado")
    print("Estado: Listo para uso")
    
    while True:
        try:
            # Mostrar menú y obtener estado
            status = show_main_menu()
            
            # Obtener selección del usuario
            choice = input("\n Selecciona opción (1-8): ").strip()
            
            if choice == "1":
                interactive_mode()
                
            elif choice == "2":
                capture_balanced_dataset()
                
            elif choice == "3":
                configure_pokerstars()
                
            elif choice == "4":
                manage_sessions()
                
            elif choice == "5":
                print("\n Verificando balance...")
                os.system("python verify_balance.py")
                
            elif choice == "6":
                auto_complete_system()
                
            elif choice == "7":
                show_dashboard()
                
            elif choice == "8":
                print("\n Gracias por usar Poker Coach Pro!")
                print("Hasta pronto! ")
                break
                
            else:
                print(" Opción no válida. Por favor, selecciona 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n Programa interrumpido")
            break
        except Exception as e:
            print(f" Error: {e}")
            print(" Intenta reiniciar el programa")

if __name__ == "__main__":
    # Añadir src al path si existe
    if os.path.exists("src"):
        sys.path.insert(0, "src")
    
    main()
