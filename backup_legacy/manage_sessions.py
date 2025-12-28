# manage_sessions.py - Gestión independiente de sesiones (VERSIÓN CORREGIDA)
import sys
import os

# Añadir src al path
sys.path.insert(0, "src")

def show_menu():
    """Mostrar menú del gestor"""
    print("\n" + "=" * 60)
    print("GESTOR DE SESIONES - POKER COACH PRO")
    print("=" * 60)
    print("1. Listar todas las sesiones")
    print("2. Eliminar sesión específica")
    print("3. Eliminar sesiones vacías (< 5 imágenes)")
    print("4. Eliminar sesiones antiguas (> 30 días)")
    print("5. Ver uso de disco")
    print("6. Limpieza completa")
    print("7. Salir")
    print("=" * 60)
    
    try:
        choice = int(input("\n Selecciona opción (1-7): "))
        return choice
    except:
        return 0
    except:
        return 0
    except:
        return 0

def main():
    """Función principal corregida"""
    print("  GESTOR INDEPENDIENTE DE SESIONES - POKER COACH PRO")
    print("=" * 70)
    
    try:
        from session_manager import SessionManager
        manager = SessionManager()
        
        if not manager.sessions:
            print("\n📭 No hay sesiones de captura")
            print("💡 Ejecuta primero el capturador automático")
            return
        
        while True:
            choice = show_menu()
            
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
                print("\n Saliendo del gestor de sesiones...")
                break
            else:
                print(" Opción no válida")
            
            if choice != 7:
                input("\n Presiona Enter para continuar...")
                
    except ImportError as e:
        print(f" Error importando gestor de sesiones: {e}")
        print("\n El módulo session_manager.py no está disponible")
        print("   Verifica que el archivo exista en src/")
    except Exception as e:
        print(f" Error inesperado: {e}")
        print("\n Usa start_auto_capture.py (opción 5) como alternativa")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Gestión de sesiones interrumpida")


