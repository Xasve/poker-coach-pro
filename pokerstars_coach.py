#!/usr/bin/env python3
"""
Poker Coach Pro - Script final para PokerStars
"""
import os
import sys
import time
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_requirements():
    """Verificar requisitos del sistema"""
    print(" Verificando sistema...")
    
    try:
        import cv2
        print(" OpenCV instalado")
    except ImportError:
        print(" OpenCV no instalado")
        return False
    
    try:
        import numpy as np
        print(" NumPy instalado")
    except ImportError:
        print(" NumPy no instalado")
        return False
    
    try:
        import PIL
        print(" Pillow instalado")
    except ImportError:
        print(" Pillow no instalado")
        return False
    
    return True

def print_welcome():
    """Mostrar mensaje de bienvenida"""
    print("\n" + "=" * 60)
    print(" POKER COACH PRO - POKERSTARS EDITION")
    print("=" * 60)
    print("\n CARACTERÍSTICAS:")
    print(" Análisis en tiempo real de mesas PokerStars")
    print(" Recomendaciones GTO basadas en situación")
    print(" Modo demo integrado para práctica")
    print(" Historial completo de manos")
    print(" Sistema stealth anti-detección")
    print("\n  CONTROLES:")
    print(" Ctrl+C: Pausar/Continuar")
    print(" Ctrl+Q: Salir del programa")
    print("=" * 60)

def main():
    """Función principal"""
    print_welcome()
    
    # Verificar requisitos
    if not check_requirements():
        print("\n Faltan dependencias")
        print(" Ejecuta: python install_pokerstars.py")
        return
    
    print("\n Iniciando Poker Coach Pro...")
    time.sleep(1)
    
    try:
        # Importar coach de PokerStars
        from src.integration.pokerstars_coach import PokerStarsCoach
        
        # Crear y ejecutar coach
        coach = PokerStarsCoach()
        
        if coach.initialize():
            print("\n" + "=" * 60)
            print(" SISTEMA INICIALIZADO CORRECTAMENTE")
            print("=" * 60)
            
            try:
                coach.run()
            except KeyboardInterrupt:
                print("\n Programa terminado por usuario")
            finally:
                coach.stop()
        else:
            print("\n Error al inicializar el sistema")
            
    except ImportError as e:
        print(f"\n Error de importación: {e}")
        print("\n Ejecuta primero: python install_pokerstars.py")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
