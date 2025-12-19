# emergency_start.py - Versión de emergencia ultra-simple
import os
import sys

def emergency_menu():
    """Menú de emergencia ultra-simple"""
    while True:
        print("\n" + "=" * 50)
        print("POKER COACH PRO - MODO EMERGENCIA")
        print("=" * 50)
        print("1. Capturar cartas")
        print("2. Clasificar cartas")
        print("3. Gestionar sesiones")
        print("4. Verificar sistema")
        print("5. Salir")
        print("=" * 50)
        
        try:
            choice = input("\nOpcion: ")
            
            if choice == '1':
                print("\nEjecutando capturador...")
                try:
                    sys.path.insert(0, 'src')
                    from auto_template_capturer import main
                    main()
                except:
                    print("Error: Ejecuta src/auto_template_capturer.py manualmente")
                    
            elif choice == '2':
                print("\nEjecutando clasificador...")
                try:
                    sys.path.insert(0, 'src')
                    from card_classifier import main
                    main()
                except:
                    print("Error: Ejecuta src/card_classifier.py manualmente")
                    
            elif choice == '3':
                print("\nEjecutando gestor de sesiones...")
                try:
                    sys.path.insert(0, 'src')
                    from session_manager import SessionManager
                    manager = SessionManager()
                    if manager.sessions:
                        for i, session in enumerate(manager.sessions[:5], 1):
                            print(f"{i}. {session['id']} - {session['image_count']} imagenes")
                    else:
                        print("No hay sesiones")
                except:
                    print("Error: Usa manage_sessions.py manualmente")
                    
            elif choice == '4':
                print("\nEstado del sistema:")
                print(f"Python: {sys.version}")
                print(f"Directorio: {os.getcwd()}")
                
                # Verificar archivos esenciales
                essentials = ['requirements.txt', 'main.py', 'detect_coords.py']
                for file in essentials:
                    if os.path.exists(file):
                        print(f"OK {file}")
                    else:
                        print(f"FALTA {file}")
                        
            elif choice == '5':
                print("\nSaliendo...")
                break
                
            else:
                print("Opcion no valida")
                
        except KeyboardInterrupt:
            print("\n\nInterrumpido")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print(" MODO EMERGENCIA ACTIVADO")
    print("Usa este modo si hay problemas con el menu principal")
    emergency_menu()
