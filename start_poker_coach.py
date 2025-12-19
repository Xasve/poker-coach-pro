# start_poker_coach.py - Inicio rápido del sistema
import os
import sys

def quick_start():
    """Inicio rápido del sistema"""
    print(" POKER COACH PRO - INICIO RÁPIDO")
    print("=" * 60)
    
    print("\n OPCIONES DE INICIO RÁPIDO:")
    print("1. Sistema principal completo (Recomendado)")
    print("2. Solo captura de dataset")
    print("3. Solo verificación y análisis")
    print("4. Solo gestión de sesiones")
    print("5. Dashboard del sistema")
    
    try:
        choice = input("\n Selecciona opción (1-5): ").strip()
        
        if choice == "1":
            print("\n Iniciando sistema principal...")
            os.system("python main_integrated.py")
            
        elif choice == "2":
            print("\n Iniciando captura balanceada...")
            os.system("python smart_capture_fixed.py")
            
        elif choice == "3":
            print("\n Verificando y analizando...")
            if os.path.exists("verify_balance.py"):
                os.system("python verify_balance.py")
            if os.path.exists("start_auto_simple.py"):
                os.system("python start_auto_simple.py")
                
        elif choice == "4":
            print("\n📁 Gestionando sesiones...")
            os.system("python session_manager.py")
            
        elif choice == "5":
            print("\n📊 Mostrando dashboard...")
            if os.path.exists("main_integrated.py"):
                # Importar y ejecutar función del dashboard
                import main_integrated
                main_integrated.show_dashboard()
            else:
                print(" main_integrated.py no disponible")
                
        else:
            print(" Opción no válida")
            print(" Ejecuta directamente: python main_integrated.py")
            
    except KeyboardInterrupt:
        print("\n\n Inicio interrumpido")
    except Exception as e:
        print(f" Error: {e}")

def check_requirements():
    """Verificar requisitos del sistema"""
    print("\n VERIFICANDO REQUISITOS...")
    
    requirements = [
        ("OpenCV (cv2)", "cv2"),
        ("NumPy", "numpy"),
        ("Pillow (PIL)", "PIL"),
        ("JSON", "json"),
        ("OS", "os"),
        ("Sys", "sys")
    ]
    
    all_ok = True
    for name, module in requirements:
        try:
            __import__(module)
            print(f" {name}")
        except ImportError:
            print(f" {name}")
            all_ok = False
    
    return all_ok

def main():
    """Función principal"""
    print(" POKER COACH PRO - INICIADOR")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("data/card_templates"):
        print(" Error: No estás en el directorio correcto")
        print(" Navega a: cd poker-coach-pro")
        return
    
    # Verificar requisitos
    if check_requirements():
        print("\n✅ Todos los requisitos cumplidos")
        
        # Mostrar opciones de inicio
        quick_start()
    else:
        print("\n❌ Faltan algunas dependencias")
        print(" Instala las dependencias con:")
        print("   pip install opencv-python numpy pillow")
        
        # Preguntar si quiere instalar automáticamente
        install = input("\nInstalar dependencias automáticamente? (s/n): ").strip().lower()
        if install == 's':
            print("\n Instalando dependencias...")
            os.system("pip install opencv-python numpy pillow")
            print("\n Dependencias instaladas")
            quick_start()

if __name__ == "__main__":
    main()
