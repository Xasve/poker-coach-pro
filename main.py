#!/usr/bin/env python3
"""
POKER COACH PRO - Punto de entrada principal
Sistema de asistencia para poker en tiempo real.
"""

import sys
import os
from pathlib import Path

# Añadir src/ al path para imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def setup_environment():
    """Configura el entorno y verifica dependencias."""
    print("=" * 60)
    print("POKER COACH PRO - Sistema de Asistencia GTO")
    print("=" * 60)
    
    # Verificar que estamos en el entorno correcto
    try:
        import cv2
        import numpy as np
        import pyautogui
        print("✅ Dependencias básicas cargadas correctamente")
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\nPor favor, instala las dependencias:")
        print("  pip install -r requirements.txt")
        return False
    
    # Verificar estructura de carpetas
    required_dirs = ["data/card_templates", "config", "logs"]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"⚠️  Creando directorio: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    return True

def display_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 60)
    print("MENÚ PRINCIPAL - POKER COACH PRO")
    print("=" * 60)
    print("1. 🎯 Iniciar Asistente en Tiempo Real")
    print("2. ⚙️  Calibrar Detección de Pantalla")
    print("3. 🃏 Probar Reconocimiento de Cartas")
    print("4. 📊 Analizar Rango GTO para Situación")
    print("5. 🧪 Modo Práctica (Sin PokerStars)")
    print("6. ❓ Ayuda y Configuración")
    print("0. 🚪 Salir")
    print("=" * 60)
    
    try:
        choice = input("\nSelecciona una opción (0-6): ").strip()
        return choice
    except (KeyboardInterrupt, EOFError):
        return "0"

def run_realtime_assistant():
    """Función principal del asistente en tiempo real."""
    print("\n[🎯] Iniciando asistente en tiempo real...")
    print("  Presiona Ctrl+C para detener.")
    
    try:
        # TODO: Importar e iniciar el sistema principal
        from core.game_state import GameStateManager
        from core.gto_advisor import GTOAdvisor
        from integration.pokerstars_handler import PokerStarsCapture
        
        print("  ✅ Módulos cargados correctamente")
        print("  🔍 Buscando mesa de PokerStars...")
        
        # Aquí iría la lógica principal
        # Por ahora solo un placeholder
        import time
        for i in range(3, 0, -1):
            print(f"  Iniciando en {i}... (modo simulación)")
            time.sleep(1)
        
        print("\n  ⚠️  Funcionalidad en desarrollo.")
        print("  Los módulos principales están listos para implementar.")
        
    except ImportError as e:
        print(f"  ❌ Error: {e}")
        print("  ℹ️  Ejecuta la refactorización primero.")
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")

def calibrate_system():
    """Calibra la detección de pantalla."""
    print("\n[⚙️] Iniciando calibración...")
    print("  Esta herramienta te ayudará a configurar las coordenadas")
    print("  de la mesa de poker en tu pantalla.")
    
    # TODO: Implementar calibración
    print("  ⚠️  Herramienta de calibración en desarrollo.")

def test_card_recognition():
    """Prueba el reconocimiento de cartas."""
    print("\n[🃏] Probando reconocimiento de cartas...")
    
    try:
        # Intentar importar el módulo de reconocimiento
        from core.card_recognizer import CardRecognizer
        
        recognizer = CardRecognizer()
        print("  ✅ Reconocedor de cartas cargado")
        
        # Probar con imagen de ejemplo si existe
        test_image = "data/card_templates/test_table.png"
        if os.path.exists(test_image):
            print(f"  🔍 Analizando {test_image}...")
            # cards = recognizer.recognize_from_file(test_image)
            # print(f"  📋 Cartas detectadas: {cards}")
            print("  ⚠️  Lógica de reconocimiento pendiente de implementar.")
        else:
            print("  ℹ️  Crea una captura de prueba en data/card_templates/test_table.png")
            
    except ImportError:
        print("  ❌ Módulo card_recognizer no encontrado.")
        print("  ℹ️  Ejecuta la refactorización del código.")

def main():
    """Función principal."""
    if not setup_environment():
        print("\n❌ No se pudo configurar el entorno. Saliendo...")
        return
    
    print("\n✅ Entorno configurado correctamente")
    print("ℹ️  Sistema listo para la refactorización del código")
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            run_realtime_assistant()
        elif choice == "2":
            calibrate_system()
        elif choice == "3":
            test_card_recognition()
        elif choice == "4":
            print("\n[📊] Análisis GTO - En desarrollo")
            print("  Esta función analizará situaciones específicas")
            print("  usando tablas de rangos GTO precalculadas.")
        elif choice == "5":
            print("\n[🧪] Modo Práctica - En desarrollo")
            print("  Practica decisiones sin conexión a PokerStars.")
        elif choice == "6":
            print("\n[❓] Ayuda y Configuración")
            print("\n  Estructura del proyecto:")
            print("  • src/core/        - Lógica principal (GTO, detección)")
            print("  • src/integration/ - Captura de pantalla, PokerStars")
            print("  • src/utils/       - Utilidades, helpers")
            print("  • data/            - Plantillas y configuraciones")
            print("  • config/          - Archivos de configuración")
            print("\n  Siguientes pasos:")
            print("  1. Ejecutar la refactorización del código existente")
            print("  2. Implementar los módulos core con tu lógica")
            print("  3. Probar el sistema completo")
        elif choice == "0":
            print("\n🚪 Saliendo de Poker Coach Pro. ¡Buena suerte en las mesas!")
            break
        else:
            print("\n❌ Opción inválida. Por favor, selecciona 0-6.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()