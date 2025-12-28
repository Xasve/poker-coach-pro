"""
MAIN INTEGRATOR - Poker Coach Pro
Conecta todos los módulos restaurados del sistema.
Este archivo se genera automáticamente.
"""

import sys
import os

# Añadir ruta para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# === IMPORTS DE MÓDULOS RESTAURADOS ===
from core.card_recognizer import CardOCRSystem
from integration.pokerstars_calibrator import PokerStarsCalibrator
from integration.pokerstars_assistant import PokerStarsAssistant
from core.learning_system import PokerLearningSystem
from utils.auto_fixer import AutoFixer
from utils.system_checker import SystemChecker

__all__ = ['CardOCRSystem', 'PokerStarsCalibrator', 'PokerStarsAssistant', 'PokerLearningSystem', 'AutoFixer', 'SystemChecker']

# === VERIFICACIÓN DE MÓDULOS ===
def verify_modules():
    """Verifica que todos los módulos se importen correctamente."""
    print("🔍 VERIFICANDO MÓDULOS RESTAURADOS...")
    print("-" * 50)
    
    modules_status = []

    # Verificar CardOCRSystem
    try:
        from core.card_recognizer import CardOCRSystem
        modules_status.append(("✅", "CardOCRSystem", "CARD_OCR_SYSTEM.py"))
    except ImportError as e:
        modules_status.append(("❌", "CardOCRSystem", f"Error: {e}"))

    # Verificar PokerStarsCalibrator
    try:
        from integration.pokerstars_calibrator import PokerStarsCalibrator
        modules_status.append(("✅", "PokerStarsCalibrator", "POKERSTARS_CALIBRATOR.py"))
    except ImportError as e:
        modules_status.append(("❌", "PokerStarsCalibrator", f"Error: {e}"))

    # Verificar PokerStarsAssistant
    try:
        from integration.pokerstars_assistant import PokerStarsAssistant
        modules_status.append(("✅", "PokerStarsAssistant", "pokerstars_assistant.py"))
    except ImportError as e:
        modules_status.append(("❌", "PokerStarsAssistant", f"Error: {e}"))

    # Verificar PokerLearningSystem
    try:
        from core.learning_system import PokerLearningSystem
        modules_status.append(("✅", "PokerLearningSystem", "complete_poker_learning_system.py"))
    except ImportError as e:
        modules_status.append(("❌", "PokerLearningSystem", f"Error: {e}"))

    # Verificar AutoFixer
    try:
        from utils.auto_fixer import AutoFixer
        modules_status.append(("✅", "AutoFixer", "auto_fix.py"))
    except ImportError as e:
        modules_status.append(("❌", "AutoFixer", f"Error: {e}"))

    # Verificar SystemChecker
    try:
        from utils.system_checker import SystemChecker
        modules_status.append(("✅", "SystemChecker", "check_system.py"))
    except ImportError as e:
        modules_status.append(("❌", "SystemChecker", f"Error: {e}"))

    # Mostrar resultados
    for status, module, info in modules_status:
        print(f"{status} {module:20} | {info}")
    
    print("-" * 50)
    success = all(status == "✅" for status, _, _ in modules_status)
    
    if success:
        print("🎉 TODOS los módulos se importan correctamente!")
        return True
    else:
        print("⚠️  Algunos módulos tienen problemas de importación.")
        print("   Revisa los imports en los archivos individuales.")
        return False

if __name__ == "__main__":
    verify_modules()
