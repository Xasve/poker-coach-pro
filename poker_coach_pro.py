#!/usr/bin/env python3
"""
 POKER_COACH_PRO.py - Sistema Original de Poker Coach Pro
Versión reparada y funcional
"""

import sys
import os
import time

def main():
    """Función principal del sistema original"""
    print(" POKER COACH PRO - SISTEMA ORIGINAL")
    print("=" * 50)
    print()
    print("Este es el sistema original de Poker Coach Pro.")
    print("Para la versión mejorada con menú interactivo,")
    print("ejecute: python quick_start.py")
    print()
    print("=" * 50)
    print()
    
    print("Opciones del sistema original:")
    print("1. Sistema de captura básico")
    print("2. Motor GTO simple")
    print("3. Sistema de aprendizaje básico")
    print("4. Salir")
    print()
    
    try:
        choice = input("Seleccione opción (1-4): ").strip()
        
        if choice == "1":
            print("\n SISTEMA DE CAPTURA BÁSICO")
            print("=" * 30)
            print("Esta función requiere OpenCV instalado.")
            print("Instale con: pip install opencv-python")
            print()
            print(" Para sistema completo use quick_start.py")
            
        elif choice == "2":
            print("\n🧠 MOTOR GTO SIMPLE")
            print("=" * 30)
            print("Motor GTO básico en desarrollo.")
            print("Decisiones preflop básicas:")
            print("- AA, KK, QQ: RAISE")
            print("- AK, AQ: RAISE/CALL")
            print("- Manos pequeñas: FOLD")
            
        elif choice == "3":
            print("\n SISTEMA DE APRENDIZAJE BÁSICO")
            print("=" * 30)
            print("Modo aprendizaje básico:")
            print("1. Rangos preflop")
            print("2. Cálculo de odds")
            print("3. Decisiones básicas")
            print("\n Para cursos completos use quick_start.py")
            
        elif choice == "4":
            print("\n Saliendo...")
            return
            
        else:
            print(" Opción no válida")
            
    except KeyboardInterrupt:
        print("\n\n  Operación cancelada")
    except Exception as e:
        print(f"\n Error: {e}")
    
    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f" Error crítico: {e}")
        print(" Ejecute quick_start.py para sistema completo")
        input("Presione Enter para salir...")
