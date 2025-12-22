# ============================================================================
# INTEGRACIÓN DEL SISTEMA PROFESIONAL - VERSIÓN REPARADA Y FUNCIONAL
# ============================================================================

import sys
import os
import time
from datetime import datetime

def print_header():
    """Imprimir encabezado del sistema"""
    
    print("\n" + "="*70)
    print(" POKER BOT PROFESIONAL - SISTEMA INTEGRADO")
    print("="*70)
    print(" Sistema completo con:")
    print("    Conocimiento de 10+ años de experiencia")
    print("    Validación profesional en tiempo real")
    print("    Aprendizaje y mejora continuos")
    print("    Psicología y metacognición integradas")
    print("="*70)

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    
    print("\n VERIFICANDO DEPENDENCIAS...")
    
    dependencies = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("pyautogui", "PyAutoGUI")
    ]
    
    missing = []
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"    {name}")
        except ImportError:
            print(f"    {name}")
            missing.append(module)
    
    if missing:
        print(f"\n  Dependencias faltantes: {', '.join(missing)}")
        print(" Instala con: python -m pip install " + " ".join(missing))
        return False
    
    print("\n Todas las dependencias están instaladas")
    return True

def load_professional_system():
    """Cargar el sistema profesional"""
    
    print("\n CARGANDO SISTEMA PROFESIONAL...")
    
    # Verificar que los archivos existan
    required_files = [
        "professional_system/professional_monitoring_FIXED.py",
        "professional_system/professional_poker_system.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"    {os.path.basename(file)}")
        else:
            print(f"     {os.path.basename(file)} no encontrado")
    
    try:
        # Intentar cargar el sistema de monitoreo
        sys.path.insert(0, "professional_system")
        from professional_monitoring_FIXED import ProfessionalMonitor, real_time_monitoring_demo
        
        print("    Sistema de monitoreo cargado")
        return True, ProfessionalMonitor
        
    except ImportError as e:
        print(f"    Error cargando sistema: {e}")
        return False, None

def professional_demo():
    """Demostración del sistema profesional"""
    
    print("\n DEMOSTRACIÓN DEL SISTEMA PROFESIONAL")
    print("="*60)
    
    try:
        from professional_monitoring_FIXED import real_time_monitoring_demo
        real_time_monitoring_demo()
        
    except Exception as e:
        print(f" Error en demostración: {e}")
        print("\n Solución alternativa: Ejecutar monitoreo básico")
        
        # Ejecutar versión simplificada
        simple_monitoring_demo()

def simple_monitoring_demo():
    """Demostración simplificada si el sistema completo falla"""
    
    print("\n MONITOREO SIMPLIFICADO")
    print("="*60)
    
    # Datos de prueba
    decisions = [
        {"action": "RAISE", "size": 3.0, "quality": 0.92},
        {"action": "CALL", "size": 1.0, "quality": 0.85},
        {"action": "FOLD", "quality": 0.78},
        {"action": "BLUFF", "size": 2.5, "quality": 0.65},
        {"action": "VALUE_BET", "size": 0.75, "quality": 0.88}
    ]
    
    print("\n DECISIONES SIMULADAS:")
    for i, decision in enumerate(decisions, 1):
        action = decision["action"]
        quality = decision["quality"]
        
        # Asignar calificación
        if quality >= 0.9:
            rating = "ELITE "
        elif quality >= 0.8:
            rating = "PROFESSIONAL "
        elif quality >= 0.7:
            rating = "COMPETENT "
        else:
            rating = "NEEDS WORK "
        
        print(f"\n{i}. {action}")
        print(f"   Calidad: {quality:.1%}")
        print(f"   Calificación: {rating}")
        
        # Recomendación basada en calidad
        if quality < 0.7:
            print(f"    Recomendación: Revisar estrategia de {action.lower()}")
        elif quality < 0.8:
            print(f"    Recomendación: Mejorar sizing en {action.lower()}")
    
    print("\n" + "="*60)
    print(" RESUMEN DE RENDIMIENTO:")
    avg_quality = sum(d["quality"] for d in decisions) / len(decisions)
    print(f"   Calidad promedio: {avg_quality:.1%}")
    
    if avg_quality >= 0.85:
        print("    Nivel: PROFESSIONAL")
    elif avg_quality >= 0.75:
        print("    Nivel: ADVANCED")
    else:
        print("    Nivel: DEVELOPING")

def training_mode():
    """Modo de entrenamiento profesional"""
    
    print("\n MODO DE ENTRENAMIENTO PROFESIONAL")
    print("="*60)
    
    training_modules = [
        "1. Análisis de rangos preflop",
        "2. Estrategias postflop",
        "3. Gestión de bankroll",
        "4. Psicología del poker",
        "5. Análisis de oponentes",
        "6. Torneos vs Cash Games"
    ]
    
    print("\n MÓDULOS DISPONIBLES:")
    for module in training_modules:
        print(f"   {module}")
    
    try:
        choice = input("\nSelecciona módulo (1-6) o Enter para salir: ").strip()
        
        if choice == "1":
            print("\n ANÁLISIS DE RANGOS PREFLOP")
            print("-"*40)
            print("Rangos profesionales por posición:")
            print("   UTG:  22+, A2s+, K9s+, QTs+, JTs, ATo+, KTo+")
            print("   MP:   22+, A2s+, K8s+, Q9s+, J9s+, T9s, A9o+, KTo+, QTo+")
            print("   CO:   22+, A2s+, K6s+, Q8s+, J8s+, T8s, 98s, A7o+, K9o+, Q9o+, J9o+")
            print("   BTN:  22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 96s+, 85s+, A2o+, K6o+, Q8o+, J8o+, T8o+, 98o")
            print("\n Ajusta según dinámica de mesa y stacks")
            
        elif choice == "2":
            print("\n ESTRATEGIAS POSTFLOP")
            print("-"*40)
            print("Principios clave:")
            print("   1. Continuar con manos que tienen equity")
            print("   2. Bluff en boards que completan tu range")
            print("   3. Controlar el tamaño de la olla")
            print("   4. Balancear frecuencia de acciones")
            print("   5. Ajustar según tipo de oponente")
            
        elif choice == "3":
            print("\n GESTIÓN DE BANKROLL")
            print("-"*40)
            print("Reglas profesionales:")
            print("    Cash Games: 20-30 buy-ins mínimo")
            print("    Torneos: 100+ buy-ins")
            print("    Stop loss: 3-5 buy-ins por sesión")
            print("    Move up: Después de 10,000+ manos con winrate positivo")
            
        elif choice in ["4", "5", "6"]:
            print(f"\n Módulo {choice} en desarrollo...")
            print("Contenido profesional disponible próximamente")
            
        else:
            print("\n Entrenamiento finalizado")
            return
        
        input("\nPresiona Enter para continuar...")
        
    except KeyboardInterrupt:
        print("\n\n Entrenamiento interrumpido")

def main_menu():
    """Menú principal del sistema profesional - VERSIÓN FUNCIONAL"""
    
    system_loaded, MonitorClass = load_professional_system()
    
    while True:
        print_header()
        
        print("\n MENÚ PRINCIPAL:")
        print("   1.  Sistema de monitoreo profesional")
        print("   2.   Modo de entrenamiento")
        print("   3.  Verificar dependencias")
        print("   4.  Diagnóstico del sistema")
        print("   5.  Ejecutar bot extremo")
        print("   6.  Salir")
        print("="*70)
        
        try:
            choice = input("\n Selecciona opción (1-6): ").strip()
            
            if choice == "1":
                if system_loaded:
                    professional_demo()
                else:
                    print("\n  El sistema profesional no está completamente cargado")
                    print(" Ejecutando versión simplificada...")
                    simple_monitoring_demo()
            
            elif choice == "2":
                training_mode()
            
            elif choice == "3":
                check_dependencies()
                input("\nPresiona Enter para continuar...")
            
            elif choice == "4":
                print("\n DIAGNÓSTICO DEL SISTEMA")
                print("-"*40)
                
                print(f"Python: {sys.version.split()[0]}")
                print(f"Directorio: {os.getcwd()}")
                print(f"Archivos en professional_system/:")
                
                if os.path.exists("professional_system"):
                    files = os.listdir("professional_system")
                    for file in files[:10]:  # Mostrar primeros 10
                        print(f"    {file}")
                    if len(files) > 10:
                        print(f"   ... y {len(files)-10} más")
                else:
                    print("    Directorio no existe")
                
                input("\nPresiona Enter para continuar...")
            
            elif choice == "5":
                print("\n EJECUTANDO BOT EXTREMO...")
                print("-"*40)
                
                if os.path.exists("extreme_optimization/extreme_bot_simple.py"):
                    print("Iniciando bot extremo...")
                    os.system("python extreme_optimization/extreme_bot_simple.py")
                else:
                    print(" Bot extremo no encontrado")
                    print(" Ejecuta: python quick_start.py")
                
                input("\nPresiona Enter para continuar...")
            
            elif choice == "6":
                print("\n Saliendo del sistema profesional...")
                print("Gracias por usar Poker Coach Pro! ")
                break
            
            else:
                print("\n Opción no válida. Por favor selecciona 1-6.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n Operación cancelada por el usuario")
            break
        except Exception as e:
            print(f"\n Error: {e}")
            input("Presiona Enter para continuar...")

def quick_start():
    """Inicio rápido para nuevos usuarios"""
    
    print("\n INICIO RÁPIDO - POKER BOT PROFESIONAL")
    print("="*60)
    
    print("\n Este sistema te permite:")
    print("   1. Monitorear la calidad de tus decisiones")
    print("   2. Entrenar con contenido profesional")
    print("   3. Verificar que todo funciona correctamente")
    print("   4. Ejecutar el bot en modo automático")
    
    print("\n Primeros pasos:")
    
    # Verificar OpenCV (el problema más común)
    try:
        import cv2
        print("    OpenCV está instalado")
    except ImportError:
        print("     OpenCV NO está instalado")
        print("    Ejecuta: python -m pip install opencv-contrib-python")
        return False
    
    # Verificar otros paquetes esenciales
    essentials = ["numpy", "pandas", "pyautogui"]
    for package in essentials:
        try:
            __import__(package)
            print(f"    {package} está instalado")
        except ImportError:
            print(f"     {package} NO está instalado")
    
    print("\n Para comenzar:")
    print("   1. Usa el menú principal (opción 1 para monitoreo)")
    print("   2. Prueba el modo de entrenamiento (opción 2)")
    print("   3. Ejecuta el bot automático (opción 5)")
    
    input("\n Presiona Enter para continuar al menú principal...")
    return True

if __name__ == "__main__":
    try:
        # Mostrar inicio rápido para nuevos usuarios
        if len(sys.argv) == 1:
            quick_start()
        
        # Ejecutar menú principal
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n Error crítico: {e}")
        print("\n Solución:")
        print("   1. Verifica que todas las dependencias estén instaladas")
        print("   2. Asegúrate de estar en el directorio correcto")
        print("   3. Ejecuta: python -m pip install opencv-contrib-python numpy pandas pyautogui")
        
        input("\nPresiona Enter para salir...")
