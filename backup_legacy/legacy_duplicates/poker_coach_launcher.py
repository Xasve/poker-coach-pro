# poker_coach_launcher.py - Lanzador de emergencia
import subprocess
import os
import sys

def run_safe():
    """Ejecutar de forma segura"""
    print(" POKER COACH PRO - LANZADOR DE EMERGENCIA")
    print("=" * 60)
    
    options = [
        ("1", "start_auto_capture.py", "Sistema completo"),
        ("2", "manage_sessions.py", "Gestión de sesiones"),
        ("3", "src/auto_template_capturer.py", "Capturador"),
        ("4", "src/card_classifier.py", "Clasificador"),
        ("5", "diagnose_sessions.py", "Diagnóstico"),
        ("6", "detect_coords.py", "Configurar PokerStars"),
        ("7", "emergency_start.py", "Modo emergencia"),
        ("8", "test_simple.py", "Prueba simple"),
        ("9", "exit", "Salir")
    ]
    
    while True:
        print("\n SELECCIONA UNA OPCIÓN:")
        for key, script, desc in options:
            print(f"{key}. {desc}")
        
        choice = input("\n Opción: ")
        
        if choice == "9":
            print("\n Hasta pronto!")
            break
        
        for key, script, desc in options:
            if choice == key and script != "exit":
                print(f"\n Ejecutando: {desc}")
                try:
                    if script.endswith('.py') and os.path.exists(script):
                        subprocess.run([sys.executable, script])
                    else:
                        print(f" Archivo no encontrado: {script}")
                except Exception as e:
                    print(f" Error: {e}")
                break
        else:
            print(" Opción inválida")
        
        input("\n Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        run_safe()
    except KeyboardInterrupt:
        print("\n\n Interrumpido por usuario")
