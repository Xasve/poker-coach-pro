import os
import time
import cv2
import numpy as np
from datetime import datetime

print("📸 CAPTURA DE TEMPLATES DE CARTAS")
print("=" * 60)
print("Este script te ayudará a capturar cartas reales de PokerStars")
print("=" * 60)

def create_folders():
    """Crear estructura de carpetas para templates"""
    folders = ["hearts", "diamonds", "clubs", "spades", "uncategorized"]
    
    for folder in folders:
        path = f"data/card_templates/pokerstars_real/{folder}"
        os.makedirs(path, exist_ok=True)
        print(f"   📁 {path}")
    
    print("\n✅ Estructura de carpetas creada")

def show_instructions():
    """Mostrar instrucciones de captura"""
    print("\n�� INSTRUCCIONES DE CAPTURA:")
    print("   1. Abre PokerStars en una mesa")
    print("   2. Juega algunas manos normalmente")
    print("   3. Las cartas se guardarán automáticamente")
    print("   4. Luego clasifícalas manualmente en las carpetas")
    print("\n   💡 CONSEJOS:")
    print("   • Juega en mesas de poker gratuito para más manos")
    print("   • Usa diferentes decks para variedad")
    print("   • Captura cartas en diferentes posiciones")

def manual_capture_guide():
    """Guía para captura manual con PrintScreen"""
    print("\n🖼️  CAPTURA MANUAL (PrintScreen):")
    print("   1. Presiona PrintScreen cuando veas cartas")
    print("   2. Abre Paint y pega (Ctrl+V)")
    print("   3. Recorta cada carta (70x95 píxeles aprox)")
    print("   4. Guarda como: As_hearts.png, Kd_diamonds.png, etc.")
    print("   5. Mueve a la carpeta correspondiente")

def auto_capture_setup():
    """Configurar captura automática"""
    print("\n🤖 CAPTURA AUTOMÁTICA (Próxima versión):")
    print("   Esta funcionalidad está en desarrollo")
    print("   Por ahora usa la captura manual")
    print("\n   Para desarrollo avanzado, necesitarás:")
    print("   • Mejor detección de cartas")
    print("   • Reconocimiento de palos y valores")
    print("   • Sistema de clasificación automática")

if __name__ == "__main__":
    create_folders()
    show_instructions()
    manual_capture_guide()
    auto_capture_setup()
    
    print("\n" + "=" * 60)
    print("🎴 POKER COACH PRO - CAPTURA DE TEMPLATES")
    print("\n🚀 Comienza capturando cartas manualmente:")
    print("   1. data/card_templates/pokerstars_real/uncategorized/")
    print("   2. Luego clasifícalas en subcarpetas")
    print("\n📞 Para ayuda, consulta la documentación")
