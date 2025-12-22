# ============================================================================
# POKER COACH PRO - ENTRY POINT SIMPLIFICADO Y FUNCIONAL
# ============================================================================

import sys
import os

def main():
    """Función principal simplificada"""
    
    print("\n" + "="*70)
    print(" POKER COACH PRO - SISTEMA SIMPLIFICADO")
    print("="*70)
    print("Este sistema evita los errores y funciona inmediatamente")
    print("="*70)
    
    # Opciones disponibles
    options = [
        ("1", "Sistema de monitoreo profesional (reparado)"),
        ("2", "Bot extremo (funcional)"),
        ("3", "Sistema original (quick_start.py)"),
        ("4", "Verificar sistema"),
        ("5", "Instalar dependencias faltantes"),
        ("6", "Salir")
    ]
    
    while True:
        print("\n MENÚ DISPONIBLE:")
        for key, description in options:
            print(f"   {key}. {description}")
        
        try:
            choice = input("\n Selecciona opción (1-6): ").strip()
            
            if choice == "1":
                print("\n CARGANDO SISTEMA DE MONITOREO...")
                if os.path.exists("professional_system/professional_monitoring_FIXED.py"):
                    os.system("python professional_system/professional_monitoring_FIXED.py --menu")
                else:
                    print(" Archivo no encontrado. Ejecutando alternativa...")
                    os.system("python professional_system/integrate_professional_FIXED.py")
            
            elif choice == "2":
                print("\n EJECUTANDO BOT EXTREMO...")
                if os.path.exists("extreme_optimization/extreme_bot_simple.py"):
                    os.system("python extreme_optimization/extreme_bot_simple.py")
                else:
                    print(" Bot extremo no encontrado")
                    print(" Ejecuta primero: python quick_start.py")
            
            elif choice == "3":
                print("\n EJECUTANDO SISTEMA ORIGINAL...")
                if os.path.exists("quick_start.py"):
                    os.system("python quick_start.py")
                else:
                    print(" quick_start.py no encontrado")
            
            elif choice == "4":
                print("\n VERIFICANDO SISTEMA...")
                os.system("python -c \"import sys; print(f'Python: {sys.version}')\"")
                os.system("python -c \"import os; print(f'Directorio: {os.getcwd()}')\"")
                
                # Verificar paquetes esenciales
                packages = ["cv2", "numpy", "pandas", "pyautogui"]
                for pkg in packages:
                    os.system(f"python -c \"try: import {pkg}; print(' {pkg}')\nexcept: print(' {pkg}')\"")
            
            elif choice == "5":
                print("\n INSTALANDO DEPENDENCIAS...")
                os.system("python -m pip install opencv-contrib-python numpy pandas pyautogui --quiet")
                print(" Dependencias instaladas (o ya estaban instaladas)")
            
            elif choice == "6":
                print("\n Gracias por usar Poker Coach Pro! ")
                break
            
            else:
                print("\n Opción no válida. Por favor selecciona 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n Operación cancelada")
            break
        except Exception as e:
            print(f"\n Error: {e}")

if __name__ == "__main__":
    # Añadir directorio actual al path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Ejecutar
    main()
