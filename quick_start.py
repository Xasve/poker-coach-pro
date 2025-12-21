#  CONFIGURACIÓN RÁPIDA PARA EJECUCIÓN INMEDIATA

import os
import sys

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def quick_start():
    """Inicio rápido del sistema"""
    
    print(" INICIO RÁPIDO - SISTEMA DE APRENDIZAJE DE PÓKER")
    print("=" * 50)
    
    print("\n OPCIONES DISPONIBLES:")
    print("1. Optimización completa (recomendado)")
    print("2. Solo calibración de color")
    print("3. Solo entrenamiento rápido")
    print("4. Ver estado actual")
    
    choice = input("\nSeleccione opción (1-4): ").strip()
    
    from complete_poker_learning_system import PokerCoachProCompleteSystem
    
    system = PokerCoachProCompleteSystem()
    
    if choice == "1":
        # Optimización completa
        print("\n EJECUTANDO OPTIMIZACIÓN COMPLETA...")
        system.run_complete_optimization()
        
    elif choice == "2":
        # Solo calibración
        print("\n EJECUTANDO CALIBRACIÓN DE COLOR...")
        system.color_calibrator.run_calibration()
        
    elif choice == "3":
        # Solo entrenamiento
        print("\n EJECUTANDO ENTRENAMIENTO RÁPIDO...")
        hours = float(input("Horas de entrenamiento (ej: 0.5, 1, 2): ").strip() or "0.5")
        intensity = input("Intensidad (low/medium/high): ").strip() or "medium"
        system.learning_system.rapid_training_session(hours, intensity)
        
    elif choice == "4":
        # Ver estado
        print("\n ESTADO DEL SISTEMA:")
        system.display_final_summary()
        
    else:
        print(" Opción no válida")

if __name__ == "__main__":
    quick_start()
